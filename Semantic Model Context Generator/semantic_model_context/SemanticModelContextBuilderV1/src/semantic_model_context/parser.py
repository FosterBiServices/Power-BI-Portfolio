"""TMDL parser boundary.

Version 1.0 intentionally keeps parsing behind one class so the proven parser from
Local TMDL Documenter can be moved here without changing the GUI, CLI, or writer.
"""

from pathlib import Path

from .domain import SemanticModel
from .exceptions import ModelParseError
from .pbip_resolver import ResolvedProject


class TmdlParser:
  """Parse a resolved TMDL semantic model into domain objects."""

  def parse(self, project: ResolvedProject) -> SemanticModel:
    table_files = sorted((project.definition_path / "tables").glob("*.tmdl"))
    if not table_files:
      raise ModelParseError(
        "No table TMDL files were found. Replace TmdlParser.parse with the parser "
        "from Local TMDL Documenter before production use."
      )

    # Safe scaffold behavior: create the model shell but do not guess at TMDL grammar.
    # The existing Model Documenter parser should be extracted into this boundary.
    return SemanticModel(
      name=project.semantic_model_path.name.removesuffix(".SemanticModel"),
      pbip_path=project.pbip_path,
      semantic_model_path=project.semantic_model_path,
    )
