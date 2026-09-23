"""Write one AI-readable Markdown context file."""

from datetime import UTC, datetime
from pathlib import Path

from .domain import SemanticModel
from .validation import ValidationResult


def _safe_cell(value: object) -> str:
  return str(value).replace("|", "\\|").replace("\n", " ").strip()


def write_context(
  model: SemanticModel,
  validation: ValidationResult,
  output_path: Path,
) -> Path:
  generated_utc = datetime.now(UTC).isoformat(timespec="seconds")
  measure_count = sum(len(table.measures) for table in model.tables)
  column_count = sum(len(table.columns) for table in model.tables)
  lines = [
    "---",
    "contextType: Power BI Semantic Model",
    "schemaVersion: 1.0",
    "generator: Semantic Model Context Builder",
    f"modelName: {_safe_cell(model.name)}",
    f"generatedUtc: {generated_utc}",
    "---",
    "",
    "# Semantic Model Instructions",
    "",
    "Treat this file as the authoritative structural reference for this model.",
    "Do not invent tables, columns, measures, or relationships that are not listed.",
    "Use exact object names when proposing DAX.",
    "",
    "# Model Summary",
    "",
    f"- Model: {model.name}",
    f"- Storage mode: {model.storage_mode}",
    f"- Tables: {len(model.tables)}",
    f"- Columns: {column_count}",
    f"- Measures: {measure_count}",
    f"- Relationships: {len(model.relationships)}",
    "",
    "# Tables",
  ]

  for table in model.tables:
    lines.extend(["", f"## {table.name}", "", table.description or "No description provided."])
    lines.extend(["", "### Columns", "", "| Column | Data Type | Hidden | Key | Sort By |", "|---|---|---:|---:|---|"])
    for column in table.columns:
      lines.append(
        f"| {_safe_cell(column.name)} | {_safe_cell(column.data_type)} | "
        f"{'Yes' if column.is_hidden else 'No'} | {'Yes' if column.is_key else 'No'} | "
        f"{_safe_cell(column.sort_by_column)} |"
      )
    if table.measures:
      lines.extend(["", "### Measures"])
      for measure in table.measures:
        lines.extend(["", f"#### {measure.name}", "", "```dax", measure.expression, "```"])

  lines.extend(["", "# Relationships", "", "| From | To | Cardinality | Direction | Active |", "|---|---|---|---|---:|"])
  for relationship in model.relationships:
    lines.append(
      f"| {relationship.from_table}[{relationship.from_column}] | "
      f"{relationship.to_table}[{relationship.to_column}] | "
      f"{_safe_cell(relationship.cardinality)} | "
      f"{_safe_cell(relationship.cross_filter_direction)} | "
      f"{'Yes' if relationship.is_active else 'No'} |"
    )

  lines.extend(["", "# Validation", "", f"- Model parsed successfully: {'Yes' if validation.is_valid else 'No'}"])
  lines.append(f"- Errors: {len(validation.errors)}")
  lines.append(f"- Warnings: {len(validation.warnings)}")
  for error in validation.errors:
    lines.append(f"  - Error: {error}")
  for warning in validation.warnings:
    lines.append(f"  - Warning: {warning}")

  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
  return output_path
