from about_report_generator.context_builder import BuildContext
from about_report_generator.response_validator import ParseAiResponse,AiResponseError
from about_report_generator.models import ModelInventory,MeasureInfo,SourceInfo

def test_context_contains_evidence():
  Inventory=ModelInventory("Test",1,2,1,0,(SourceInfo("SQL Server",1),),(MeasureInfo("Revenue","Measures","KPIs","SUM(Fact[Revenue])"),),())
  Data=BuildContext(Inventory);assert Data["report_name"]=="Test" and Data["measures"][0]["name"]=="Revenue"
def test_response_rejects_unknown_kpi():
  Text='{"report_summary":"x","business_value":"y","data_sources":["SQL Server"],"top_kpis":["Made Up"],"evidence_gaps":[]}'
  try:ParseAiResponse(Text,["SQL Server"],["Revenue"]);assert False
  except AiResponseError:assert True
