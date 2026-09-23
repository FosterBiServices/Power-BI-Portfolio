from pathlib import Path

from semantic_model_context.parser import TmdlParser
from semantic_model_context.pbip_resolver import ResolvedProject


def test_parser_maps_documenter_objects(tmp_path: Path) -> None:
  semantic_root = tmp_path / "Sales.SemanticModel"
  definition = semantic_root / "definition"
  tables = definition / "tables"
  tables.mkdir(parents=True)
  (semantic_root / "definition.pbism").write_text("{}", encoding="utf-8")
  (definition / "model.tmdl").write_text(
    "model Model\n  culture: en-US\n  defaultMode: import\n",
    encoding="utf-8",
  )
  (tables / "Sales.tmdl").write_text(
    """table Sales
  description: Sales facts
  column 'Sale ID'
    dataType: int64
    isKey: true
  column Amount
    dataType: decimal
  measure 'Total Sales' = SUM ( Sales[Amount] )
    formatString: $#,0.00
  partition Sales = m
    mode: import
    source = Sql.Database(\"ServerA\", \"Warehouse\")
""",
    encoding="utf-8",
  )
  (definition / "relationships.tmdl").write_text(
    """relationship Relationship1
  fromColumn: Sales.'Sale ID'
  toColumn: Customer.'Customer ID'
  fromCardinality: many
  toCardinality: one
  crossFilteringBehavior: oneDirection
""",
    encoding="utf-8",
  )
  (tables / "Customer.tmdl").write_text(
    """table Customer
  column 'Customer ID'
    dataType: int64
""",
    encoding="utf-8",
  )
  pbip = tmp_path / "Sales.pbip"
  pbip.write_text("{}", encoding="utf-8")
  resolved = ResolvedProject(pbip, tmp_path / "Sales.Report", semantic_root, definition)

  model = TmdlParser().parse(resolved)

  assert model.name == "Sales"
  assert model.storage_mode == "import"
  assert [table.name for table in model.tables] == ["Customer", "Sales"]
  sales = next(table for table in model.tables if table.name == "Sales")
  assert [column.name for column in sales.columns] == ["Sale ID", "Amount"]
  assert sales.columns[0].is_key
  assert sales.measures[0].name == "Total Sales"
  assert "SUM" in sales.measures[0].expression
  assert model.relationships[0].cardinality == "many to one"
  assert model.relationships[0].from_table == "Sales"
  assert model.data_sources[0].source_type == "SQL Server"
