import json
from pathlib import Path

from local_tmdl_documenter.documentation import DocumentationOptions, documentation_title, generate_html
from local_tmdl_documenter.domain import Project
from local_tmdl_documenter.parser import parse_pbir
from local_tmdl_documenter.partition_support import detect_source_kind


def _write_json(path: Path, data):
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(data), encoding="utf-8")


def _field(entity, prop, kind="Column"):
  return {kind: {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def _report(tmp_path: Path) -> Project:
  report = tmp_path / "Demo.Report"
  pages = report / "definition" / "pages"
  (report / ".pbi").mkdir(parents=True)
  (report / "StaticResources").mkdir()
  _write_json(pages / "pages.json", {"pageOrder": ["p2", "p1"]})
  _write_json(pages / "p1" / "page.json", {"name": "p1", "displayName": "Overview", "width": 1280, "height": 720})
  _write_json(pages / "p2" / "page.json", {"name": "p2", "displayName": "Tooltip", "width": 320, "height": 240,
                                             "visibility": "HiddenInViewMode"})
  _write_json(pages / "p1" / "visuals" / "g1" / "visual.json", {
    "name": "g1", "position": {"x": 100, "y": 200, "width": 400, "height": 300}, "visualGroup": {"displayName": "Cards"}})
  _write_json(pages / "p1" / "visuals" / "v1" / "visual.json", {
    "name": "v1", "parentGroupName": "g1", "position": {"x": 10, "y": 0, "width": 50, "height": 50},
    "visual": {"visualType": "card", "query": {"queryState": {"Values": {"projections": [
      {"field": _field("Sales", "Total", "Measure")}]}}}}})
  _write_json(pages / "p1" / "visuals" / "v2" / "visual.json", {
    "name": "v2", "position": {"x": 0, "y": 0, "width": 50, "height": 50},
    "visual": {"visualType": "slicer", "query": {"queryState": {"Values": {"projections": [
      {"field": _field("Date", "Year")}]}}}},
    "filterConfig": {"filters": [{"filter": {"From": [{"Name": "s", "Entity": "Region"}], "Where": [
      {"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "s"}}, "Property": "Name"}}]}}}]}}]}})
  project = Project(tmp_path / "Demo.pbip", tmp_path, report, "Demo")
  parse_pbir(project)
  return project


def test_pages_come_from_definition_in_page_order(tmp_path: Path):
  project = _report(tmp_path)
  assert [(page.display_name, page.is_hidden) for page in project.pages] == [("Tooltip", True), ("Overview", False)]


def test_group_children_use_absolute_positions_and_fields_are_exact(tmp_path: Path):
  visuals = {visual.name: visual for visual in _report(tmp_path).pages[1].visuals}
  assert (visuals["v1"].x, visuals["v1"].y) == (110, 200)
  assert visuals["g1"].is_group and visuals["g1"].title == "Cards"
  assert visuals["v1"].fields == ["Sales[Total]"]
  assert visuals["v2"].fields == ["Date[Year]", "Region[Name]"]


def test_report_sections_and_title(tmp_path: Path):
  project = _report(tmp_path)
  options = DocumentationOptions(profile="Developer Documentation")
  assert documentation_title(options)[0] == "Developer Model & Report Documentation"
  html = generate_html(project, options)
  assert "Full Report" not in html
  assert "<code>v1</code>" in html and "Region[Name]" in html
  assert documentation_title(DocumentationOptions())[0] == "Business Semantic Model Documentation"


def test_quickbase_connector():
  assert detect_source_kind('let Source = Quickbased("https://rci.quickbase.com/db/abc") in Source', "m") == "Quickbase"
  assert detect_source_kind('let S = Json.Document(Web.Contents("https://api.quickbase.com/v1")) in S', "m") == "Quickbase"
