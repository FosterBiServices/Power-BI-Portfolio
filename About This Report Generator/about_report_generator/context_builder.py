import json
from dataclasses import asdict

def BuildContext(Inventory):
  return {
    "schema_version":"1.0",
    "report_name":Inventory.ReportName,
    "model_counts":{"tables":Inventory.TableCount,"columns":Inventory.ColumnCount,"measures":Inventory.MeasureCount,"relationships":Inventory.RelationshipCount},
    "data_sources":[{"name":Item.Name,"table_count":Item.TableCount} for Item in Inventory.Sources if Item.Name not in {"Other / not detected","JSON"}],
    "measures":[{
      "name":Item.Name,"table":Item.TableName,"display_folder":Item.DisplayFolder,
      "expression":Item.Expression,"depends_on":list(Item.DependsOn),"used_by":list(Item.UsedBy),
      "visual_reference_count":Item.VisualCount
    } for Item in Inventory.Measures],
    "relationships":[{
      "from_table":Item.FromTable,"from_column":Item.FromColumn,"to_table":Item.ToTable,"to_column":Item.ToColumn,
      "cardinality":Item.Cardinality,"filter_direction":Item.Direction,"active":Item.IsActive
    } for Item in Inventory.Relationships],
    "instructions":{"kpi_limit":5,"exclude_compound_measures":True,"exclude_technical_content_from_output":True}
  }

def ContextToJson(Context): return json.dumps(Context,indent=2,ensure_ascii=False)
