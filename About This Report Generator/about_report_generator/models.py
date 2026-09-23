from dataclasses import dataclass, field

@dataclass(frozen=True)
class SourceInfo:
  Name: str
  TableCount: int
  Background: str = ""
  Foreground: str = ""

@dataclass(frozen=True)
class MeasureInfo:
  Name: str
  TableName: str
  DisplayFolder: str
  Expression: str
  DependsOn: tuple[str, ...] = ()
  UsedBy: tuple[str, ...] = ()
  VisualCount: int = 0
  IsCompound: bool = False
  Score: int = 0
  Color: str = ""

@dataclass(frozen=True)
class RelationshipInfo:
  FromTable: str
  FromColumn: str
  ToTable: str
  ToColumn: str
  Cardinality: str
  Direction: str
  IsActive: bool

@dataclass(frozen=True)
class ModelInventory:
  ReportName: str
  TableCount: int
  ColumnCount: int
  MeasureCount: int
  RelationshipCount: int
  Sources: tuple[SourceInfo, ...] = ()
  Measures: tuple[MeasureInfo, ...] = ()
  Relationships: tuple[RelationshipInfo, ...] = ()

@dataclass(frozen=True)
class AboutReportModel:
  ReportName: str
  ReportSummary: str
  BusinessValue: str
  Sources: tuple[SourceInfo, ...]
  Kpis: tuple[MeasureInfo, ...]
  TableCount: int
  ColumnCount: int
  MeasureCount: int
  RelationshipCount: int
  RelationshipStrategy: str
  EvidenceGaps: tuple[str, ...] = field(default_factory=tuple)
