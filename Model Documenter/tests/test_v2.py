from pathlib import Path
from local_tmdl_documenter.parser import load_project
from local_tmdl_documenter.documentation import DocumentationOptions, generate_html

def test_model_and_html(tmp_path: Path):
  definition=tmp_path/'Demo.SemanticModel'/'definition'/'tables'; definition.mkdir(parents=True)
  (definition/'Sales.tmdl').write_text("table Sales\n  column Key\n    dataType: int64\n  measure Total = SUM(Sales[Key])\n    formatString: 0\n",encoding='utf-8')
  root=definition.parent
  (root/'relationships.tmdl').write_text("relationship rel\n  fromColumn: Sales.Key\n  toColumn: Sales.Key\n",encoding='utf-8')
  project=load_project(tmp_path)
  assert len(project.tables)==1 and len(project.relationships)==1
  report=generate_html(project,DocumentationOptions(include_dax=True))
  assert 'Measure Catalog' in report and 'SUM(Sales[Key])' in report
