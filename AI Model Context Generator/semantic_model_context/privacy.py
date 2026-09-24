"""Privacy options and metadata minimization."""

import re
from dataclasses import dataclass, replace

from .domain import Column, DataSource, Measure, SemanticModel, Table


@dataclass(frozen=True, slots=True)
class PrivacyOptions:
  include_hidden_objects: bool = False
  include_dax: bool = True
  include_power_query: bool = False
  include_data_source_locations: bool = False
  include_role_expressions: bool = False
  include_local_paths: bool = False
  include_measure_only_tables: bool = True


def apply_privacy(model: SemanticModel, options: PrivacyOptions) -> SemanticModel:
  tables: list[Table] = []
  for table in model.tables:

    is_measure_only_table = (
        len(table.columns) == 0
        and len(table.measures) > 0
    )

    if (
        is_measure_only_table
        and not options.include_measure_only_tables
    ):
        continue
    
    if table.is_hidden and not options.include_hidden_objects:
      continue
    columns = [
      replace(column, expression=column.expression if options.include_dax else "")
      for column in table.columns
      if options.include_hidden_objects or not column.is_hidden
    ]
    measures = [
      replace(measure, expression=measure.expression if options.include_dax else "")
      for measure in table.measures
      if options.include_hidden_objects or not measure.is_hidden
    ]
    tables.append(replace(table, columns=columns, measures=measures))

  included_tables = {table.name for table in tables}
  sources = [
    replace(
      source,
      server=_location(source.server, options.include_data_source_locations),
      database=_location(source.database, options.include_data_source_locations),
      path=_location(
        source.path,
        options.include_local_paths if _is_local_path(source.path)
        else options.include_data_source_locations,
      ),
    )
    for source in model.data_sources
    if not source.table or source.table in included_tables
  ]
  relationships = [
    relationship for relationship in model.relationships
    if relationship.from_table in included_tables and relationship.to_table in included_tables
  ]
  return replace(model, tables=tables, relationships=relationships, data_sources=sources)


def _is_local_path(value: str) -> bool:
  """Drive-letter or UNC paths; URLs and server names are data-source locations."""
  return bool(re.match(r"^(?:[A-Za-z]:[\\/]|\\\\)", value or ""))


def _location(value: str, include: bool) -> str:
  if not value:
    return ""
  return value if include else "[Redacted]"
