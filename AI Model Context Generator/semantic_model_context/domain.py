"""Domain objects shared by the parser, service, and writer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Column:
  name: str
  data_type: str = ""
  format_string: str = ""
  description: str = ""
  summarize_by: str = ""
  sort_by: str = ""
  source_column: str = ""
  is_hidden: bool = False
  is_key: bool = False
  expression: str = ""

  @property
  def sort_by_column(self) -> str:
    """Compatibility property used by the Markdown writer."""
    return self.sort_by


@dataclass
class Measure:
  name: str
  expression: str = ""
  format_string: str = ""
  display_folder: str = ""
  description: str = ""
  is_hidden: bool = False
  column_refs: list[str] = field(default_factory=list)
  measure_refs: list[str] = field(default_factory=list)


@dataclass
class Partition:
  name: str
  mode: str = ""
  source_type: str = ""
  expression: str = ""
  source_kind: str = "Other / not detected"
  source_arguments: list[str] = field(default_factory=list)


@dataclass
class Table:
  name: str
  columns: list[Column] = field(default_factory=list)
  measures: list[Measure] = field(default_factory=list)
  partitions: list[Partition] = field(default_factory=list)
  description: str = ""
  is_hidden: bool = False
  table_type: str = "Regular"


@dataclass
class Relationship:
  name: str
  from_table: str
  from_column: str
  to_table: str
  to_column: str
  from_cardinality: str = "many"
  to_cardinality: str = "one"
  cross_filtering: str = "oneDirection"
  is_active: bool = True
  rely_on_referential_integrity: bool = False
  security_filtering_behavior: str = ""

  @property
  def cardinality(self) -> str:
    """Combined cardinality used by the Markdown writer."""
    return (
      f"{self.from_cardinality} "
      f"to "
      f"{self.to_cardinality}"
    )

  @property
  def cross_filter_direction(self) -> str:
    """Compatibility property used by the Markdown writer."""
    return self.cross_filtering


@dataclass
class Expression:
  name: str
  expression: str


@dataclass
class Visual:
  page: str
  name: str
  visual_type: str
  x: float = 0
  y: float = 0
  width: float = 0
  height: float = 0
  fields: list[str] = field(default_factory=list)


@dataclass
class ReportPage:
  name: str
  display_name: str
  width: float = 1280
  height: float = 720
  visuals: list[Visual] = field(default_factory=list)


@dataclass
class Project:
  selected_root: Path
  semantic_root: Path
  report_root: Path | None = None
  name: str = "Model"
  compatibility_level: str = ""
  culture: str = ""
  tables: dict[str, Table] = field(default_factory=dict)
  relationships: list[Relationship] = field(default_factory=list)
  expressions: list[Expression] = field(default_factory=list)
  pages: list[ReportPage] = field(default_factory=list)
  warnings: list[str] = field(default_factory=list)


@dataclass
class DataSource:
  source_type: str
  server: str = ""
  database: str = ""
  path: str = ""
  table: str = ""
  mode: str = ""


@dataclass
class SemanticModel:
  name: str
  pbip_path: Path
  semantic_model_path: Path
  storage_mode: str = "Unknown"
  tables: list[Table] = field(default_factory=list)
  relationships: list[Relationship] = field(default_factory=list)
  data_sources: list[DataSource] = field(default_factory=list)