import json
from pathlib import Path

from semantic_model_context.privacy import PrivacyOptions
from semantic_model_context.service import ContextService


def _write(path: Path, text: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(text, encoding="utf-8")


def _project(tmp_path: Path) -> Path:
  _write(tmp_path / "Demo.pbip", json.dumps({"artifacts": [{"report": {"path": "Demo.Report"}}]}))
  _write(tmp_path / "Demo.Report" / "definition.pbir",
         json.dumps({"datasetReference": {"byPath": {"path": "../Demo.SemanticModel"}}}))
  model = tmp_path / "Demo.SemanticModel"
  _write(model / "definition.pbism", "{}")
  definition = model / "definition"
  _write(definition / "expressions.tmdl",
         'expression stage_Sales =\n\t\tlet\n\t\t  Source = Quickbased("https://rci.quickbase.com/db/abc")\n'
         "\t\tin\n\t\t  Source\n\tlineageTag: x\n")
  _write(definition / "tables" / "Sales.tmdl",
         "/// Sales transactions from Quickbase.\n"
         "table Sales\n"
         "\t/// Units sold.\n\tcolumn Qty\n\t\tdataType: int64\n\t\tsummarizeBy: sum\n\n"
         "\tcolumn Secret\n\t\tdataType: string\n\t\tisHidden\n\n"
         "\t/// Total units.\n\tmeasure Total = SUM(Sales[Qty])\n\t\tformatString: 0\n\n"
         "\t/// Broken on purpose.\n\tmeasure Broken =\n\t\t\tVAR x = [Total]\n\t\t\tRETURN\n\t\t\t\tSUM(Sales[Amount])\n\t\tisHidden\n\n"
         "\tmeasure Visible Broken = [Totl]\n\n"
         "\tpartition Sales = m\n\t\tmode: import\n\t\tsource =\n"
         "\t\t\t\tlet\n\t\t\t\t  Source = stage_Sales\n\t\t\t\tin\n\t\t\t\t  Source\n\n"
         "\tannotation PBI_Id = abc\n")
  _write(definition / "tables" / "LocalDateTable_1.tmdl",
         "table LocalDateTable_1\n\tisHidden\n\n\tcolumn Date\n\t\tdataType: dateTime\n\t\tisHidden\n\n"
         "\tpartition LocalDateTable_1 = calculated\n\t\tmode: import\n\t\tsource = Calendar(Date(2015,1,1), Date(2015,1,1))\n")
  _write(definition / "cultures" / "en-US.tmdl",
         "cultureInfo en-US\n\ttranslations\n\t\tmodel Model\n\t\t\ttable Sales\n\t\t\t\tmeasure Total\n")
  return tmp_path / "Demo.pbip"


def _build(tmp_path: Path, **options) -> str:
  output = ContextService().build(_project(tmp_path), tmp_path / "out.md", PrivacyOptions(**options))
  return output.read_text(encoding="utf-8")


def test_sources_descriptions_and_hidden_objects(tmp_path: Path):
  text = _build(tmp_path)
  assert "- Storage mode: import" in text
  assert "| Sales | Quickbase | import | [Redacted] |" in text
  assert "LocalDateTable_1" not in text  # hidden table (bare isHidden flag)
  assert "Secret" not in text  # hidden column
  assert "#### Broken" not in text  # hidden measure
  assert "Sales transactions from Quickbase." in text
  assert "| Units sold. |" in text and "Total units." in text
  assert text.count("#### Total") == 1  # culture file does not add a phantom measure


def test_source_locations_are_opt_in(tmp_path: Path):
  text = _build(tmp_path, include_data_source_locations=True)
  assert "| Sales | Quickbase | import | https://rci.quickbase.com/db/abc |" in text


def test_dax_errors_are_reported_for_exported_measures_only(tmp_path: Path):
  text = _build(tmp_path, include_dax=False)
  assert "- Validation passed: No" in text
  assert "DAX error in Sales[Visible Broken]: References unknown measure(s)/column(s): [Totl]." in text
  assert "Sales[Broken]" not in text  # hidden, so not exported or reported


def test_dependencies_ignore_keywords_and_variables(tmp_path: Path):
  text = _build(tmp_path, include_hidden_objects=True)
  broken = text.split("\n#### Broken\n")[1].split("\n#### ")[0]
  assert "- Sales[Amount]" in broken and "- Total" in broken
  assert "RETURN" not in broken.split("```dax")[0]
  assert "isHidden" not in broken
