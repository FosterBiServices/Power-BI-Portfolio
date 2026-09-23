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

def _json(path: Path) -> dict[str, object]:
  try:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
  except (OSError, json.JSONDecodeError) as error:
    raise PbipResolutionError(f"Cannot read JSON file: {path}") from error
  if not isinstance(value, dict):
    raise PbipResolutionError(f"Expected a JSON object in: {path}")
  return value

def resolve_pbip(pbip_path: Path) -> ResolvedProject:
  selected = pbip_path.expanduser().resolve()
  if selected.suffix.lower() != ".pbip" or not selected.is_file():
    raise PbipResolutionError("Select an existing .pbip file.")
  data = _json(selected)
  artifacts = data.get("artifacts")
  if not isinstance(artifacts, list):
    raise PbipResolutionError("The PBIP file does not contain an artifacts list.")
  report_value = next((a.get("report", {}).get("path") for a in artifacts if isinstance(a, dict) and isinstance(a.get("report"), dict)), None)
  if not isinstance(report_value, str) or not report_value:
    raise PbipResolutionError("The PBIP file does not reference a report artifact.")
  report_path = (selected.parent / report_value).resolve()
  report_definition = report_path / "definition.pbir"
  if not report_definition.is_file():
    report_definition = report_path / "definition" / "definition.pbir"
  if not report_definition.is_file():
    raise PbipResolutionError(f"Report definition not found under: {report_path}")
  report_data = _json(report_definition)
  reference = report_data.get("datasetReference")
  by_path = reference.get("byPath") if isinstance(reference, dict) else None
  relative = by_path.get("path") if isinstance(by_path, dict) else None
  if not isinstance(relative, str) or not relative:
    raise PbipResolutionError("Only datasetReference.byPath is supported in Version 1.0.")
  semantic_path = (report_path / relative).resolve()
  project_root = selected.parent.resolve()
  if semantic_path != project_root and project_root not in semantic_path.parents:
    raise PbipResolutionError("Semantic model reference escapes the PBIP project folder.")
  definition = semantic_path / "definition"
  if not (semantic_path / "definition.pbism").is_file() or not definition.is_dir():
    raise PbipResolutionError(f"Semantic model TMDL definition not found: {semantic_path}")
  return ResolvedProject(selected, report_path, semantic_path, definition)
