from __future__ import annotations

import json
import os
import platform
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from .reliability import application_folder, logs_folder
from .settings import load_settings, settings_path

APPLICATION_NAME = "Local TMDL Documenter"
APPLICATION_VERSION = "2.9.1"


def diagnostics_folder() -> Path:
  folder = application_folder() / "Diagnostics"
  folder.mkdir(parents=True, exist_ok=True)
  return folder


def _safe_settings() -> dict:
  """Return useful settings while excluding recent and last project paths."""
  settings = load_settings()
  return {
    key: value
    for key, value in settings.items()
    if key not in {"RecentProjects", "LastProject"}
  }


def _latest_log() -> Path | None:
  candidates = [path for path in logs_folder().glob("*.log") if path.is_file()]
  return max(candidates, key=lambda path: path.stat().st_mtime) if candidates else None


def export_diagnostics() -> Path:
  """Create a local diagnostics ZIP without PBIP/TMDL source content."""
  generated = datetime.now()
  output = diagnostics_folder() / f"Diagnostics_{generated:%Y%m%d_%H%M%S}.zip"

  application = {
    "Application": APPLICATION_NAME,
    "Version": APPLICATION_VERSION,
    "Generated": generated.isoformat(timespec="seconds"),
  }
  environment = {
    "PythonVersion": platform.python_version(),
    "Platform": platform.platform(),
    "System": platform.system(),
    "Release": platform.release(),
    "Machine": platform.machine(),
    "ExecutableName": Path(sys.executable).name,
    "PackagedExecutable": bool(getattr(sys, "frozen", False)),
  }
  recent = load_settings()
  project_history = {
    "LastProject": recent.get("LastProject", ""),
    "RecentProjects": recent.get("RecentProjects", []),
    "Note": "Local paths may be organization-specific. Review before sharing.",
  }

  with tempfile.TemporaryDirectory(prefix="LocalTmdlDiagnostics_") as folder:
    root = Path(folder)
    (root / "application.json").write_text(
      json.dumps(application, indent=2), encoding="utf-8"
    )
    (root / "environment.json").write_text(
      json.dumps(environment, indent=2), encoding="utf-8"
    )
    (root / "settings.json").write_text(
      json.dumps(_safe_settings(), indent=2), encoding="utf-8"
    )
    (root / "recent-projects.json").write_text(
      json.dumps(project_history, indent=2), encoding="utf-8"
    )
    latest_log = _latest_log()
    if latest_log is not None:
      (root / "latest.log").write_text(
        latest_log.read_text(encoding="utf-8", errors="replace"),
        encoding="utf-8",
      )
    else:
      (root / "latest.log").write_text(
        "No application log was available when diagnostics were exported.\n",
        encoding="utf-8",
      )

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
      for path in sorted(root.iterdir(), key=lambda value: value.name.casefold()):
        archive.write(path, arcname=path.name)

  return output


def open_diagnostics_folder() -> None:
  folder = diagnostics_folder()
  if os.name == "nt":
    os.startfile(folder)  # type: ignore[attr-defined]
  elif sys.platform == "darwin":
    import subprocess
    subprocess.Popen(["open", str(folder)])
  else:
    import subprocess
    subprocess.Popen(["xdg-open", str(folder)])
