"""Privacy options and metadata minimization."""

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


def apply_privacy(model: SemanticModel, options: PrivacyOptions) -> SemanticModel:
  tables: list[Table] = []
  for table in model.tables:
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

  sources = [
    DataSource(
      source_type=source.source_type,
      server=source.server if options.include_data_source_locations else "[Redacted]",
      database=source.database if options.include_data_source_locations else "[Redacted]",
      path=source.path if options.include_local_paths else "[Redacted]",
    )
    for source in model.data_sources
  ]
  return replace(model, tables=tables, data_sources=sources)
