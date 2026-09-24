import re
from pathlib import Path
from .models import ModelInventory, MeasureInfo, RelationshipInfo, SourceInfo
from .pbip_resolver import ResolvePbip, ProjectError

_QUOTED = r"(?:'((?:''|[^'])+)'|([^\s]+))"
def _name(Match): return (Match.group(1) or Match.group(2) or "").replace("''", "'").strip()
def _blocks(Text, Keyword):
  Pattern = re.compile(rf"(?ms)^\s*{Keyword}\s+{_QUOTED}.*?(?=^\s*(?:table|measure|partition|relationship|column|hierarchy|annotation)\s+|\Z)")
  return [(Name, Block) for M in Pattern.finditer(Text) for Name, Block in [(_name(M), M.group(0))]]
def _read_all(Root, Suffix):
  return [(P, P.read_text(encoding="utf-8-sig", errors="replace")) for P in Root.rglob(f"*{Suffix}")]
def _source_kind(Expression):
  Rules=(("QuickBase.Contents","QuickBase"),("PowerPlatform.Dataflows","Power Platform Dataflow"),("Sql.Database","SQL Server"),("SharePoint.","SharePoint"),("Excel.Workbook","Excel"),("Snowflake.Databases","Snowflake"),("Databricks.","Databricks"),("Web.Contents","Web/API"),("OData.Feed","OData"),("Folder.Files","Folder"),("Csv.Document","CSV"),("Json.Document","JSON"))
  return next((Label for Token,Label in Rules if Token.casefold() in Expression.casefold()), "Other / not detected")
def _measure_refs(Expression): return tuple(dict.fromkeys(re.findall(r"(?<![A-Za-z0-9_])\[([^\]]+)\]", Expression)))
def _visual_counts(ReportRoot, Names):
  Counts={Name:0 for Name in Names}
  for PathValue in ReportRoot.rglob("*.json"):
    Text=PathValue.read_text(encoding="utf-8-sig",errors="replace").casefold()
    for Name in Names: Counts[Name]+=Text.count(Name.casefold())
  return Counts

def ParseProject(PbipPath: Path):
  Paths=ResolvePbip(PbipPath); Files=_read_all(Paths.DefinitionRoot,".tmdl")
  Text="\n".join(Value for _,Value in Files)
  TableMatches=list(re.finditer(rf"(?m)^\s*table\s+{_QUOTED}",Text)); TableNames=[_name(M) for M in TableMatches]
  ColumnCount=len(re.findall(r"(?m)^\s*column\s+",Text))
  RawMeasures=[]
  for PathValue,Value in Files:
    CurrentTable=PathValue.stem
    TableMatch=re.search(rf"(?m)^\s*table\s+{_QUOTED}",Value)
    if TableMatch: CurrentTable=_name(TableMatch)
    for Name,Block in _blocks(Value,"measure"):
      ExpressionMatch=re.search(r"(?ms)^\s*measure\s+.+?=\s*(.*?)(?=^\s*(?:formatString|displayFolder|description|annotation)\s*:|\Z)",Block)
      FolderMatch=re.search(r"(?m)^\s*displayFolder\s*:\s*(.+)$",Block)
      Expression=(ExpressionMatch.group(1).strip() if ExpressionMatch else "")
      Folder=(FolderMatch.group(1).strip().strip('"') if FolderMatch else "")
      RawMeasures.append((Name,CurrentTable,Folder,Expression))
  Names=[Item[0] for Item in RawMeasures]; VisualCounts=_visual_counts(Paths.ReportRoot,Names)
  UsedBy={Name:[] for Name in Names}
  for Name,_,_,Expression in RawMeasures:
    for Ref in _measure_refs(Expression):
      if Ref in UsedBy and Ref != Name: UsedBy[Ref].append(Name)
  Measures=tuple(MeasureInfo(Name,Table,Folder,Expression,_measure_refs(Expression),tuple(dict.fromkeys(UsedBy[Name])),VisualCounts[Name]) for Name,Table,Folder,Expression in RawMeasures)
  Sources={}
  for Name,Block in _blocks(Text,"partition"):
    Kind=_source_kind(Block); Sources.setdefault(Kind,set()).add(Name)
  SourceItems=tuple(SourceInfo(Name,len(Items)) for Name,Items in sorted(Sources.items(),key=lambda Item:(-len(Item[1]),Item[0].casefold())))
  Relationships=[]
  for Name,Block in _blocks(Text,"relationship"):
    From=re.search(r"(?m)^\s*fromColumn\s*:\s*([^\[]+)\[([^\]]+)\]",Block); To=re.search(r"(?m)^\s*toColumn\s*:\s*([^\[]+)\[([^\]]+)\]",Block)
    if not From or not To: continue
    Active=not bool(re.search(r"(?mi)^\s*isActive\s*:\s*false",Block)); Direction="bothDirections" if re.search(r"(?mi)^\s*crossFilteringBehavior\s*:\s*bothDirections",Block) else "oneDirection"
    Relationships.append(RelationshipInfo(From.group(1).strip().strip("'"),From.group(2),To.group(1).strip().strip("'"),To.group(2),"many : one",Direction,Active))
  return ModelInventory(PbipPath.stem,len(set(TableNames)),ColumnCount,len(Measures),len(Relationships),SourceItems,Measures,tuple(Relationships))
