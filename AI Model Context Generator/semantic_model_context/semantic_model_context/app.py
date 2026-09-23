"""PySide6 desktop interface."""

import logging
import sys
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
  QApplication,
  QCheckBox,
  QFileDialog,
  QFormLayout,
  QHBoxLayout,
  QLabel,
  QLineEdit,
  QMainWindow,
  QMessageBox,
  QPushButton,
  QVBoxLayout,
  QWidget,
)

from .logging_config import configure_logging
from .privacy import PrivacyOptions
from .service import ContextService

LOGGER = logging.getLogger(__name__)


class BuildWorker(QThread):
  completed = Signal(str)
  failed = Signal(str)

  def __init__(self, pbip_path: Path, output_path: Path, options: PrivacyOptions) -> None:
    super().__init__()
    self._pbip_path = pbip_path
    self._output_path = output_path
    self._options = options

  def run(self) -> None:
    try:
      output = ContextService().build(self._pbip_path, self._output_path, self._options)
    except Exception as error:  # GUI boundary logs unexpected failures before presenting them.
      LOGGER.exception("Context generation failed")
      self.failed.emit(str(error))
      return
    self.completed.emit(str(output))


class MainWindow(QMainWindow):
  def __init__(self) -> None:
    super().__init__()
    self._worker: BuildWorker | None = None
    self.setWindowTitle("Semantic Model Context Builder 1.0")
    self.resize(760, 360)

    self.pbip_edit = QLineEdit()
    self.output_edit = QLineEdit()
    self.hidden_check = QCheckBox("Include hidden objects")
    self.dax_check = QCheckBox("Include DAX expressions")
    self.dax_check.setChecked(True)
    self.measure_only_tables_check = QCheckBox("Include Measure-Only Tables")
    self.measure_only_tables_check.setChecked(True)
    self.sources_check = QCheckBox("Include data-source locations")
    self.status_label = QLabel("Select a PBIP file to begin.")
    self.build_button = QPushButton("Build Context File")

    pbip_button = QPushButton("Browse")
    pbip_button.clicked.connect(self._select_pbip)
    output_button = QPushButton("Browse")
    output_button.clicked.connect(self._select_output)
    self.build_button.clicked.connect(self._build)

    pbip_row = QHBoxLayout()
    pbip_row.addWidget(self.pbip_edit)
    pbip_row.addWidget(pbip_button)
    output_row = QHBoxLayout()
    output_row.addWidget(self.output_edit)
    output_row.addWidget(output_button)

    form = QFormLayout()
    form.addRow("PBIP file", pbip_row)
    form.addRow("Output file", output_row)

    layout = QVBoxLayout()
    layout.addLayout(form)
    layout.addWidget(self.hidden_check)
    layout.addWidget(self.dax_check)
    layout.addWidget(self.measure_only_tables_check)
    layout.addWidget(self.sources_check)
    layout.addStretch()
    layout.addWidget(self.build_button)
    layout.addWidget(self.status_label)

    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)

  def _select_pbip(self) -> None:
    selected, _ = QFileDialog.getOpenFileName(self, "Select PBIP", "", "Power BI Project (*.pbip)")
    if selected:
      self.pbip_edit.setText(selected)
      self.output_edit.setText(str(Path(selected).with_suffix(".semantic-context.md")))

  def _select_output(self) -> None:
    selected, _ = QFileDialog.getSaveFileName(
      self,
      "Save Context File",
      self.output_edit.text(),
      "Markdown (*.md)",
    )
    if selected:
      self.output_edit.setText(selected)

  def _build(self) -> None:
    pbip_path = Path(self.pbip_edit.text().strip())
    output_path = Path(self.output_edit.text().strip())
    if not self.pbip_edit.text().strip() or not self.output_edit.text().strip():
      QMessageBox.warning(self, "Missing Selection", "Select a PBIP file and output file.")
      return

    options = PrivacyOptions(
        include_hidden_objects=self.hidden_check.isChecked(),
        include_dax=self.dax_check.isChecked(),
        include_data_source_locations=self.sources_check.isChecked(),
        include_measure_only_tables=(
            self.measure_only_tables_check.isChecked()
        ),
    )
    self.build_button.setEnabled(False)
    self.status_label.setText("Building context file...")
    self._worker = BuildWorker(pbip_path, output_path, options)
    self._worker.completed.connect(self._build_completed)
    self._worker.failed.connect(self._build_failed)
    self._worker.start()

  def _build_completed(self, output: str) -> None:
    self.build_button.setEnabled(True)
    self.status_label.setText(f"Created: {output}")
    QMessageBox.information(self, "Complete", f"Context file created:\n{output}")

  def _build_failed(self, message: str) -> None:
    self.build_button.setEnabled(True)
    self.status_label.setText("Generation failed. See the local log for details.")
    QMessageBox.critical(self, "Unable to Build Context", message)


def main() -> int:
  configure_logging()
  application = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  return application.exec()


if __name__ == "__main__":
  raise SystemExit(main())
