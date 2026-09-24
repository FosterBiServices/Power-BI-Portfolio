from about_report_generator.config import GeneratorConfig
from about_report_generator.dax_builder import BuildDaxMeasure
from about_report_generator.kpis import SelectKpis
from about_report_generator.models import MeasureInfo

def test_dax_escape():
  assert 'style=""color:red;""' in BuildDaxMeasure('<div style="color:red;">x</div>',GeneratorConfig())
def test_compound_excluded():
  Items=(MeasureInfo("Base","_Measures","KPIs","COUNTROWS(Fact)",UsedBy=("Rate",)),MeasureInfo("Rate","_Measures","KPIs","DIVIDE([Base],[Other])"))
  assert [Item.Name for Item in SelectKpis(Items,5)]==["Base"]
