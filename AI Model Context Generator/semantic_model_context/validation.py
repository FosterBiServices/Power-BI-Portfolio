"""Semantic model validation."""

from dataclasses import dataclass, field

from .dax_checks import check_measure
from .domain import SemanticModel


@dataclass(slots=True)
class ValidationResult:
  errors: list[str] = field(default_factory=list)
  warnings: list[str] = field(default_factory=list)

  @property
  def is_valid(self) -> bool:
    return not self.errors


def validate_model(model: SemanticModel, source_model: SemanticModel | None = None) -> ValidationResult:
  """Validate the exported model.

  `source_model` is the unfiltered model. Structure and DAX are checked against
  it so hidden or excluded objects don't look missing, but DAX errors are only
  reported for measures present in `model`.
  """
  result = ValidationResult()
  source = source_model or model
  table_names: set[str] = set()
  columns_by_table: dict[str, set[str]] = {}

  for table in source.tables:
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

  for relationship in source.relationships:
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

  measure_names: dict[str, str] = {}
  for table in source.tables:
    for measure in table.measures:
      key = measure.name.casefold()
      if key in measure_names:
        result.errors.append(
          f"Duplicate measure name: [{measure.name}] in {measure_names[key]} and {table.name}"
        )
      measure_names.setdefault(key, table.name)

  exported = {(table.name, measure.name) for table in model.tables for measure in table.measures}
  for table in source.tables:
    for measure in table.measures:
      if (table.name, measure.name) not in exported:
        continue
      for message in check_measure(measure.name, measure.expression, source.tables):
        result.errors.append(f"DAX error in {table.name}[{measure.name}]: {message}")

  if not model.tables:
    result.warnings.append("The parsed model does not contain any tables.")
  return result
