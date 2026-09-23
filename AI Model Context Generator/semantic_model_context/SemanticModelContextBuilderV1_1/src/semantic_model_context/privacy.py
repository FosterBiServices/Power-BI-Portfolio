from dataclasses import dataclass, replace
from .domain import DataSource, SemanticModel, Table
@dataclass(frozen=True, slots=True)
class PrivacyOptions:
  include_hidden_objects: bool = False
  include_dax: bool = True
  include_data_source_locations: bool = False
  include_local_paths: bool = False

def apply_privacy(model: SemanticModel, options: PrivacyOptions) -> SemanticModel:
  tables=[]
  for table in model.tables:
    if table.is_hidden and not options.include_hidden_objects: continue
    columns=[replace(c, expression=c.expression if options.include_dax else "") for c in table.columns if options.include_hidden_objects or not c.is_hidden]
    measures=[replace(m, expression=m.expression if options.include_dax else "") for m in table.measures if options.include_hidden_objects or not m.is_hidden]
    tables.append(replace(table, columns=columns, measures=measures))
  sources=[DataSource(s.source_type, s.server if options.include_data_source_locations else "[Redacted]", s.database if options.include_data_source_locations else "[Redacted]", s.path if options.include_local_paths else "[Redacted]") for s in model.data_sources]
  return replace(model, tables=tables, data_sources=sources)
