from dataclasses import dataclass, field
from .domain import SemanticModel
@dataclass(slots=True)
class ValidationResult:
  errors: list[str] = field(default_factory=list)
  warnings: list[str] = field(default_factory=list)
  @property
  def is_valid(self) -> bool: return not self.errors

def validate_model(model: SemanticModel) -> ValidationResult:
  result = ValidationResult(); tables = {}; seen_tables = set()
  for table in model.tables:
    key = table.name.casefold()
    if key in seen_tables: result.errors.append(f"Duplicate table name: {table.name}")
    seen_tables.add(key); columns = set()
    for column in table.columns:
      ckey = column.name.casefold()
      if ckey in columns: result.errors.append(f"Duplicate column name: {table.name}[{column.name}]")
      columns.add(ckey)
    tables[key] = columns
  for relationship in model.relationships:
    for table_name, column_name in ((relationship.from_table, relationship.from_column),(relationship.to_table, relationship.to_column)):
      key = table_name.casefold()
      if key not in tables: result.errors.append(f"Relationship references missing table: {table_name}")
      elif column_name.casefold() not in tables[key]: result.errors.append(f"Relationship references missing column: {table_name}[{column_name}]")
  return result
