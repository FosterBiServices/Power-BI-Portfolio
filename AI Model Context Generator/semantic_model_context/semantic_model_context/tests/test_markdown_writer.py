from pathlib import Path

from semantic_model_context.domain import Column, SemanticModel, Table
from semantic_model_context.markdown_writer import write_context
from semantic_model_context.validation import ValidationResult


def test_writer_creates_single_markdown_file(tmp_path: Path) -> None:
  model = SemanticModel(
    name="Test",
    pbip_path=Path("Test.pbip"),
    semantic_model_path=Path("Test.SemanticModel"),
    tables=[Table(name="Employees", columns=[Column("Employee ID", "Int64")])],
  )
  output = tmp_path / "Test.semantic-context.md"

  write_context(model, ValidationResult(), output)

  content = output.read_text(encoding="utf-8")
  assert "# Semantic Model Instructions" in content
  assert "Employees" in content
  assert "Employee ID" in content
