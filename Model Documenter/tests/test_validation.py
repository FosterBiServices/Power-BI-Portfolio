from pathlib import Path

from local_tmdl_documenter.dax_checks import check_measure
from local_tmdl_documenter.domain import Column, Measure, Project, Table
from local_tmdl_documenter.parser import parse_partitions, parse_tmdl
from local_tmdl_documenter.partition_support import detect_source_kind
from local_tmdl_documenter.v27_validation import analyze_model


def _write_model(tmp_path: Path) -> Project:
  definition = tmp_path / "definition"
  (definition / "tables").mkdir(parents=True)
  (definition / "cultures").mkdir()
  (definition / "expressions.tmdl").write_text(
    'expression stage_Sales =\n\t\tlet\n\t\t  Source = Sql.Database("srv", "db")\n\t\tin\n\t\t  Source\n'
    "\tlineageTag: x\n",
    encoding="utf-8",
  )
  (definition / "tables" / "Sales.tmdl").write_text(
    "table Sales\n"
    "\tcolumn Qty\n\t\tdataType: int64\n"
    "\tmeasure Total = SUM(Sales[Qty])\n"
    "\tmeasure Broken = SUM(Sales[Amount])\n"
    "\tpartition Sales = m\n\t\tmode: import\n\t\tsource =\n"
    "\t\t\t\tlet\n\t\t\t\t  Source = stage_Sales\n\t\t\t\tin\n\t\t\t\t  Source\n\n"
    "\tannotation PBI_Id = abc\n",
    encoding="utf-8",
  )
  (definition / "tables" / "Top N.tmdl").write_text(
    "table 'Top N'\n\tcolumn Value\n"
    "\tpartition 'Top N' = calculated\n\t\tmode: import\n\t\tsource = GENERATESERIES(1, 10, 1)\n\n"
    "\tannotation PBI_Id = def\n",
    encoding="utf-8",
  )
  (definition / "relationships.tmdl").write_text(
    "relationship 5f1c\n\tcrossFilteringBehavior: bothDirections\n"
    "\tfromColumn: Sales.Qty\n\ttoColumn: 'Top N'.Value\n",
    encoding="utf-8",
  )
  (definition / "cultures" / "en-US.tmdl").write_text(
    "cultureInfo en-US\n\ttranslations\n\t\tmodel Model\n\t\t\ttable Sales\n\t\t\t\tmeasure Total\n",
    encoding="utf-8",
  )
  project = Project(definition, definition, None)
  parse_tmdl(project)
  parse_partitions(project)
  return project


def test_partitions_follow_references_and_classify_dax(tmp_path: Path):
  project = _write_model(tmp_path)
  sales = project.tables["Sales"].partitions[0]
  top_n = project.tables["Top N"].partitions[0]
  assert sales.source_kind == "SQL Server"
  assert "annotation" not in sales.expression
  assert top_n.source_kind == "Parameter Series (DAX)"
  assert top_n.expression == "GENERATESERIES(1, 10, 1)"


def test_culture_files_do_not_create_measures(tmp_path: Path):
  project = _write_model(tmp_path)
  assert [m.name for m in project.tables["Sales"].measures] == ["Total", "Broken"]


def test_validation_findings(tmp_path: Path):
  project = _write_model(tmp_path)
  findings = analyze_model(project, list(project.tables.values()))
  assert not any("description" in f.message.casefold() for f in findings)
  errors = [f for f in findings if f.severity == "Error"]
  assert [f.object_name for f in errors] == ["Sales[Broken]"]
  bidirectional = next(f for f in findings if "bidirectional" in f.message)
  assert bidirectional.object_name == "Sales[Qty] -> Top N[Value]"


def test_entered_data_is_not_reported_as_json():
  expression = 'let Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("x"))))\nin Source'
  assert detect_source_kind(expression, "m") == "Entered Data (Power Query)"


def test_dax_checks():
  tables = [Table("Sales", [Column("Qty")], [Measure("Total")])]
  assert check_measure("M", 'VAR x = [Total] RETURN x + Sales[Qty] // [Gone]', tables) == []
  assert check_measure("M", "MAXX(GENERATESERIES(1, 5), [Value])", tables) == []
  assert check_measure("M", "CALCULATE([Total]", tables) == ["DAX syntax error: 1 unclosed '('."]
  assert check_measure("M", "[Totl]", tables) == ["References unknown measure(s)/column(s): [Totl]."]
  assert check_measure("M", "SUM(Returns[Qty])", tables) == ["References table(s) not in the model: Returns."]
