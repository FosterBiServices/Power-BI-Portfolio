"""Semantic model validation."""

from dataclasses import dataclass, field

from .domain import SemanticModel


@dataclass(slots=True)
class ValidationResult:
  errors: list[str] = field(default_factory=list)
  warnings: list[str] = field(default_factory=list)

  @property
  def is_valid(self) -> bool:
    return not self.errors


def validate_model(model: SemanticModel) -> ValidationResult:
  result = ValidationResult()
  table_names: set[str] = set()
  columns_by_table: dict[str, set[str]] = {}

  for table in model.tables:
    normalized_table = table.name.casefold()
    if normalized_table in table_names:
      result.errors.append(f"Duplicate table name: {table.name}")
    table_names.add(normalized_table)

    column_names: set[str] = set()
    for column in table.columns:
      normalized_column = column.name.casefold()
      if normalized_column in column_names:
        result.errors.append(f"Duplicate column name: {table.name}[{column.name}]")
      column_names.add(normalized_column)
    columns_by_table[normalized_table] = column_names

  for relationship in model.relationships:
    endpoints = (
      (relationship.from_table, relationship.from_column),
      (relationship.to_table, relationship.to_column),
    )
    for table_name, column_name in endpoints:
      normalized_table = table_name.casefold()
      if normalized_table not in columns_by_table:
        result.errors.append(f"Relationship references missing table: {table_name}")
      elif column_name.casefold() not in columns_by_table[normalized_table]:
        result.errors.append(f"Relationship references missing column: {table_name}[{column_name}]")

  if not model.tables:
    result.warnings.append("The parsed model does not contain any tables.")
  return result
