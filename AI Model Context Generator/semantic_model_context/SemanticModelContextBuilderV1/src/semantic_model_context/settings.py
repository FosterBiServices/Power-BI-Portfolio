"""Local application settings."""

import json
from pathlib import Path


APP_FOLDER = Path.home() / "AppData" / "Roaming" / "SemanticModelContextBuilder"
SETTINGS_PATH = APP_FOLDER / "settings.json"


def load_settings() -> dict[str, object]:
  if not SETTINGS_PATH.is_file():
    return {}
  try:
    value = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError):
    return {}
  return value if isinstance(value, dict) else {}


def save_settings(settings: dict[str, object]) -> None:
  APP_FOLDER.mkdir(parents=True, exist_ok=True)
  temporary_path = SETTINGS_PATH.with_suffix(".tmp")
  temporary_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
  temporary_path.replace(SETTINGS_PATH)
