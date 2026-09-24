from __future__ import annotations

import logging
import os
import platform
import sys
import traceback
from datetime import datetime
from pathlib import Path


def application_folder() -> Path:
  app_data = os.environ.get("APPDATA")
  base = Path(app_data) if app_data else Path.home() / "AppData" / "Roaming"
  folder = base / "LocalTmdlDocumenter"
  folder.mkdir(parents=True, exist_ok=True)
  return folder


def logs_folder() -> Path:
  folder = application_folder() / "logs"
  folder.mkdir(parents=True, exist_ok=True)
  return folder


def configure_logging() -> Path:
  log_path = logs_folder() / f"{datetime.now():%Y-%m-%d}.log"
  logger = logging.getLogger("LocalTmdlDocumenter")
  logger.setLevel(logging.INFO)
  if not any(
    isinstance(handler, logging.FileHandler)
    and Path(handler.baseFilename) == log_path
    for handler in logger.handlers
  ):
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter(
      "%(asctime)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(handler)
  logger.info(
    "Application started | Python=%s | Platform=%s",
    sys.version.split()[0],
    platform.platform(),
  )
  return log_path


def log_info(message: str, *args) -> None:
  logging.getLogger("LocalTmdlDocumenter").info(message, *args)


def log_exception(context: str, error: BaseException) -> Path:
  log_path = configure_logging()
  logging.getLogger("LocalTmdlDocumenter").error(
    "%s | %s\n%s",
    context,
    error,
    "".join(traceback.format_exception(type(error), error, error.__traceback__)),
  )
  return log_path


def open_logs_folder() -> None:
  folder = logs_folder()
  if os.name == "nt":
    os.startfile(folder)  # type: ignore[attr-defined]
  elif sys.platform == "darwin":
    import subprocess
    subprocess.Popen(["open", str(folder)])
  else:
    import subprocess
    subprocess.Popen(["xdg-open", str(folder)])
