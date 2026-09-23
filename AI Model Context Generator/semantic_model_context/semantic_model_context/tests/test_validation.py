from pathlib import Path

from semantic_model_context.domain import Column, SemanticModel, Table
from semantic_model_context.validation import validate_model


def test_duplicate_column_is_error() -> None:
  model = SemanticModel(
    name="Test",
    pbip_path=Path("Test.pbip"),
    semantic_model_path=Path("Test.SemanticModel"),
    tables=[Table(name="Employees", columns=[Column("Id"), Column("ID")])],
  )

  result = validate_model(model)

  assert not result.is_valid
  assert "Duplicate column name: Employees[ID]" in result.errors
