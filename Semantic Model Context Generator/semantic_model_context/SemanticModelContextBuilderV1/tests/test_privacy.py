from pathlib import Path

from semantic_model_context.domain import DataSource, SemanticModel
from semantic_model_context.privacy import PrivacyOptions, apply_privacy


def test_source_locations_are_redacted_by_default() -> None:
  model = SemanticModel(
    name="Test",
    pbip_path=Path("Test.pbip"),
    semantic_model_path=Path("Test.SemanticModel"),
    data_sources=[DataSource("SQL", server="ServerA", database="Finance")],
  )

  safe_model = apply_privacy(model, PrivacyOptions())

  assert safe_model.data_sources[0].server == "[Redacted]"
  assert safe_model.data_sources[0].database == "[Redacted]"
