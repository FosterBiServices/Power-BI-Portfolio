import json,sys
from pathlib import Path
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication,QFileDialog,QMainWindow,QMessageBox,QPlainTextEdit,QTabWidget,QToolBar,QWidget,QVBoxLayout
from .ai_html_builder import BuildAiHtml
from .config import GeneratorConfig
from .context_builder import BuildContext,ContextToJson
from .dax_builder import BuildDaxMeasure
from .parser import ParseProject
from .prompt_builder import BuildPrompt
from .response_validator import ParseAiResponse

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__();self.setWindowTitle("About This Report AI Context Generator V1.3");self.resize(1200,800);self.ProjectPath=None;self.Inventory=None
    self.Tabs=QTabWidget();self.Context=QPlainTextEdit();self.Prompt=QPlainTextEdit();self.Response=QPlainTextEdit();self.Dax=QPlainTextEdit()
    for Label,Editor in (("Context JSON",self.Context),("AI Prompt",self.Prompt),("AI Response JSON",self.Response),("HTML DAX Measure",self.Dax)): self.Tabs.addTab(Editor,Label)
    self.setCentralWidget(self.Tabs);Bar=QToolBar("Main",self);self.addToolBar(Bar)
    for Text,Handler in (("Open PBIP",self.open_pbip),("Copy Prompt",lambda:self.copy(self.Prompt)),("Load AI Response",self.load_response),("Build DAX",self.build_dax),("Copy DAX",lambda:self.copy(self.Dax)),("Save DAX",self.save_dax)):
      Action=QAction(Text,self);Action.triggered.connect(Handler);Bar.addAction(Action)
  def copy(self,Editor): QApplication.clipboard().setText(Editor.toPlainText())
  def open_pbip(self):
    Value,_=QFileDialog.getOpenFileName(self,"Open Power BI Project","","Power BI Project (*.pbip)")
    if not Value:return
    try:
      self.ProjectPath=Path(Value);self.Inventory=ParseProject(self.ProjectPath);Context=BuildContext(self.Inventory)
      self.Context.setPlainText(ContextToJson(Context));self.Prompt.setPlainText(BuildPrompt(Context));self.Response.clear();self.Dax.clear();self.Tabs.setCurrentWidget(self.Prompt)
    except Exception as Error: QMessageBox.critical(self,"Analysis Failed",str(Error))
  def load_response(self):
    Value,_=QFileDialog.getOpenFileName(self,"Load AI Response","","JSON (*.json);;Text (*.txt)")
    if Value:
      try:self.Response.setPlainText(Path(Value).read_text(encoding="utf-8-sig"));self.Tabs.setCurrentWidget(self.Response)
      except OSError as Error:QMessageBox.critical(self,"Load Failed",str(Error))
  def build_dax(self):
    if not self.Inventory: QMessageBox.information(self,"No Project","Open a PBIP file first.");return
    try:
      KnownSources=[Item.Name for Item in self.Inventory.Sources if Item.Name not in {"Other / not detected","JSON"}];KnownMeasures=[Item.Name for Item in self.Inventory.Measures]
      Result=ParseAiResponse(self.Response.toPlainText(),KnownSources,KnownMeasures,5);Html=BuildAiHtml(Result,18);self.Dax.setPlainText(BuildDaxMeasure(Html,GeneratorConfig()));self.Tabs.setCurrentWidget(self.Dax)
    except Exception as Error: QMessageBox.critical(self,"Build Failed",str(Error))
  def save_dax(self):
    if not self.Dax.toPlainText().strip():return
    Value,_=QFileDialog.getSaveFileName(self,"Save DAX","About This Report.dax","DAX (*.dax);;Text (*.txt)")
    if Value:
      try:Path(Value).write_text(self.Dax.toPlainText(),encoding="utf-8")
      except OSError as Error:QMessageBox.critical(self,"Save Failed",str(Error))

def main():
  App=QApplication(sys.argv);Window=MainWindow();Window.show();return App.exec()
