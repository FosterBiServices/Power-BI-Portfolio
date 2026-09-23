from dataclasses import dataclass, field
from pathlib import Path

@dataclass(frozen=True, slots=True)
class Column:
  name: str
  data_type: str = "Unknown"
  description: str = ""
  format_string: str = ""
  is_hidden: bool = False
  is_key: bool = False
  sort_by_column: str = ""
  summarize_by: str = ""
  expression: str = ""

@dataclass(frozen=True, slots=True)
class Measure:
  name: str
  expression: str = ""
  description: str = ""
  format_string: str = ""
  display_folder: str = ""
  is_hidden: bool = False

@dataclass(slots=True)
class Table:
  name: str
  description: str = ""
  is_hidden: bool = False
  table_type: str = "Regular"
  columns: list[Column] = field(default_factory=list)
  measures: list[Measure] = field(default_factory=list)

@dataclass(frozen=True, slots=True)
class Relationship:
  name: str
  from_table: str
  from_column: str
  to_table: str
  to_column: str
  cardinality: str = ""
  cross_filter_direction: str = ""
  is_active: bool = True
  rely_on_referential_integrity: bool = False
  security_filtering_behavior: str = ""

@dataclass(frozen=True, slots=True)
class DataSource:
  source_type: str
  server: str = ""
  database: str = ""
  path: str = ""

@dataclass(slots=True)
class SemanticModel:
  name: str
  pbip_path: Path
  semantic_model_path: Path
  storage_mode: str = "Unknown"
  tables: list[Table] = field(default_factory=list)
  relationships: list[Relationship] = field(default_factory=list)
  data_sources: list[DataSource] = field(default_factory=list)
