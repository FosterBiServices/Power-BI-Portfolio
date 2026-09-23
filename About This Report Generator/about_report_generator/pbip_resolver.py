import json
from dataclasses import dataclass
from pathlib import Path

class ProjectError(ValueError): pass

@dataclass(frozen=True)
class ProjectPaths:
  PbipPath: Path
  ReportRoot: Path
  SemanticRoot: Path
  DefinitionRoot: Path

def _read_json(PathValue):
  try: return json.loads(PathValue.read_text(encoding="utf-8-sig"))
  except (OSError, json.JSONDecodeError) as Error: raise ProjectError(f"Cannot read JSON file: {PathValue}\n{Error}") from Error

def ResolvePbip(PbipPath: Path):
  PbipPath = PbipPath.resolve()
  if not PbipPath.exists() or PbipPath.suffix.casefold() != ".pbip": raise ProjectError("Select a valid .pbip file.")
  Data = _read_json(PbipPath)
  RelativeReport = next((Item.get("report", {}).get("path") for Item in Data.get("artifacts", []) if Item.get("report", {}).get("path")), None)
  if not RelativeReport: raise ProjectError("PBIP does not contain a report artifact path.")
  ReportRoot = (PbipPath.parent / RelativeReport).resolve()
  if not ReportRoot.exists(): raise ProjectError(f"Report folder was not found: {ReportRoot}")
  Candidates = (ReportRoot / "definition.pbir", ReportRoot / "definition" / "definition.pbir")
  DefinitionPbir = next((Item for Item in Candidates if Item.exists()), None)
  if not DefinitionPbir: raise ProjectError(f"definition.pbir was not found under: {ReportRoot}")
  Pbir = _read_json(DefinitionPbir)
  RelativeSemantic = Pbir.get("datasetReference", {}).get("byPath", {}).get("path")
  if not RelativeSemantic: raise ProjectError("definition.pbir does not contain datasetReference.byPath.path.")
  SemanticRoot = (DefinitionPbir.parent / RelativeSemantic).resolve()
  if not SemanticRoot.exists():
    SemanticRoot = (ReportRoot / RelativeSemantic).resolve()
  if not SemanticRoot.exists(): raise ProjectError(f"Semantic model folder was not found: {SemanticRoot}")
  DefinitionRoot = SemanticRoot / "definition"
  if not DefinitionRoot.exists(): raise ProjectError(f"Semantic model definition folder was not found: {DefinitionRoot}")
  return ProjectPaths(PbipPath, ReportRoot, SemanticRoot, DefinitionRoot)
