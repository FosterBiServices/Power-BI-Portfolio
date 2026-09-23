"""Resolve report and semantic model folders from PBIP file contents."""

import json
from dataclasses import dataclass
from pathlib import Path

from .exceptions import PbipResolutionError


@dataclass(frozen=True, slots=True)
class ResolvedProject:
  pbip_path: Path
  report_path: Path
  semantic_model_path: Path
  definition_path: Path


def _load_json(path: Path) -> dict[str, object]:
  try:
    with path.open("r", encoding="utf-8-sig") as file_handle:
      value = json.load(file_handle)
  except (OSError, json.JSONDecodeError) as error:
    raise PbipResolutionError(f"Cannot read JSON file: {path}") from error
  if not isinstance(value, dict):
    raise PbipResolutionError(f"Expected a JSON object in: {path}")
  return value


def _safe_resolve(base_path: Path, relative_value: str) -> Path:
  candidate = (base_path / relative_value).resolve()
  base = base_path.resolve()
  if candidate != base and base not in candidate.parents:
    raise PbipResolutionError(f"Referenced path escapes the PBIP folder: {relative_value}")
  return candidate


def resolve_pbip(pbip_path: Path) -> ResolvedProject:
  selected = pbip_path.expanduser().resolve()
  if selected.suffix.lower() != ".pbip" or not selected.is_file():
    raise PbipResolutionError("Select an existing .pbip file.")

  pbip_data = _load_json(selected)
  artifacts = pbip_data.get("artifacts")
  if not isinstance(artifacts, list):
    raise PbipResolutionError("The PBIP file does not contain an artifacts list.")

  report_value = ""
  for artifact in artifacts:
    if not isinstance(artifact, dict):
      continue
    report = artifact.get("report")
    if isinstance(report, dict) and isinstance(report.get("path"), str):
      report_value = report["path"]
      break
  if not report_value:
    raise PbipResolutionError("The PBIP file does not reference a report artifact.")

  report_path = _safe_resolve(selected.parent, report_value)
  report_properties = report_path / "definition.pbir"
  if not report_properties.is_file():
    raise PbipResolutionError(f"Report definition not found: {report_properties}")

  report_data = _load_json(report_properties)
  dataset_reference = report_data.get("datasetReference")
  if not isinstance(dataset_reference, dict):
    raise PbipResolutionError("The report does not contain a datasetReference.")
  by_path = dataset_reference.get("byPath")
  if not isinstance(by_path, dict) or not isinstance(by_path.get("path"), str):
    raise PbipResolutionError("Only datasetReference.byPath is supported in Version 1.0.")

  semantic_model_path = (report_path / by_path["path"]).resolve()
  definition_pbism = semantic_model_path / "definition.pbism"
  definition_path = semantic_model_path / "definition"
  if not definition_pbism.is_file():
    raise PbipResolutionError(f"Semantic model definition not found: {definition_pbism}")
  if not definition_path.is_dir():
    raise PbipResolutionError(f"TMDL definition folder not found: {definition_path}")

  return ResolvedProject(selected, report_path, semantic_model_path, definition_path)
