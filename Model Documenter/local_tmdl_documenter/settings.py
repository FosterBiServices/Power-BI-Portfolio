from __future__ import annotations

import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

_DEFAULTS = {
  "Profile": "Business Documentation",
  "IncludeReport": False,
  "IncludeHidden": False,
  "IncludeDax": False,
  "IncludePowerQuery": False,
  "IncludeSources": False,
  "ShowAutoDateTables": False,
  "IncludeMeasuresTable": False,
  "WindowWidth": 1250,
  "WindowHeight": 800,
  "RecentProjects": [],
  "LastProject": "",
  "OpenLastProject": False,
}


def settings_folder() -> Path:
  app_data = os.environ.get("APPDATA")
  base = Path(app_data) if app_data else Path.home() / "AppData" / "Roaming"
  return base / "LocalTmdlDocumenter"


def settings_path() -> Path:
  folder = settings_folder()
  folder.mkdir(parents=True, exist_ok=True)
  return folder / "settings.json"


def default_settings() -> dict:
  return deepcopy(_DEFAULTS)


def _validated(settings: dict) -> dict:
  output = default_settings()
  if not isinstance(settings, dict):
    return output
  if settings.get("Profile") in {
    "Business Documentation", "Developer Documentation", "Custom"
  }:
    output["Profile"] = settings["Profile"]
  for key in (
    "IncludeReport", "IncludeHidden", "IncludeDax", "IncludePowerQuery",
    "IncludeSources", "ShowAutoDateTables", "IncludeMeasuresTable",
    "OpenLastProject",
  ):
    if isinstance(settings.get(key), bool):
      output[key] = settings[key]
  for key, minimum, maximum in (
    ("WindowWidth", 800, 5000), ("WindowHeight", 600, 3000),
  ):
    value = settings.get(key)
    if isinstance(value, int):
      output[key] = min(max(value, minimum), maximum)
  recent = settings.get("RecentProjects", [])
  if isinstance(recent, list):
    output["RecentProjects"] = [
      str(Path(value)) for value in recent
      if isinstance(value, str) and value.strip()
    ][:10]
  last = settings.get("LastProject", "")
  if isinstance(last, str):
    output["LastProject"] = last
  return output


def load_settings() -> dict:
  path = settings_path()
  if not path.exists():
    return default_settings()
  try:
    return _validated(json.loads(path.read_text(encoding="utf-8")))
  except (OSError, json.JSONDecodeError, TypeError, ValueError):
    return default_settings()


def save_settings(settings: dict) -> None:
  path = settings_path()
  temporary = path.with_suffix(".json.tmp")
  temporary.write_text(
    json.dumps(_validated(settings), indent=2, ensure_ascii=False),
    encoding="utf-8",
  )
  temporary.replace(path)


def add_recent_project(settings: dict, project_path: str | Path) -> None:
  resolved = str(Path(project_path).expanduser().resolve())
  recent = [
    value for value in settings.get("RecentProjects", [])
    if value.casefold() != resolved.casefold()
  ]
  settings["RecentProjects"] = [resolved, *recent][:10]
  settings["LastProject"] = resolved


def reset_settings() -> None:
  path = settings_path()
  if path.exists():
    path.unlink()


def open_settings_folder() -> None:
  folder = settings_folder()
  folder.mkdir(parents=True, exist_ok=True)
  if os.name == "nt":
    os.startfile(folder)  # type: ignore[attr-defined]
  elif sys.platform == "darwin":
    subprocess.Popen(["open", str(folder)])
  else:
    subprocess.Popen(["xdg-open", str(folder)])
