"""Local rotating-file logging configuration."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging() -> Path:
  log_folder = Path.home() / "AppData" / "Roaming" / "SemanticModelContextBuilder" / "logs"
  log_folder.mkdir(parents=True, exist_ok=True)
  log_path = log_folder / "application.log"
  handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
  handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
  root = logging.getLogger()
  root.setLevel(logging.INFO)
  if not root.handlers:
    root.addHandler(handler)
  return log_path
