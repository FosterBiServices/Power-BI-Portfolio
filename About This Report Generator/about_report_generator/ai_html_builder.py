from html import escape
from .config import GeneratorConfig, KPI_COLORS, SOURCE_COLORS

def _Title(Text): return f'<b style="color:#003B5C;">{escape(Text)}</b>'
def _ListSection(Title,Items):
  if not Items: return ""
  Rows="".join(f'<li style="margin:0 0 6px 0;">{escape(Item)}</li>' for Item in Items)
  return '<div style="height:20px;"></div>'+_Title(Title)+f'<ul style="margin:8px 0 0 20px;padding:0;">{Rows}</ul>'

def BuildAiHtml(Result,FontSize=18,Config=None):
  Config=Config or GeneratorConfig(FontSize=FontSize)
  Sources=[]
  for Index,Name in enumerate(Result.Sources):
    Background,Foreground=SOURCE_COLORS[Index%len(SOURCE_COLORS)]
    Sources.append(f'<span style="background:{Background};color:{Foreground};padding:4px 10px;border-radius:12px;">{escape(Name)}</span>')
  SourceHtml="".join(Sources) or '<span style="background:#E5E7EB;color:#374151;padding:4px 10px;border-radius:12px;">No classified sources supplied</span>'
  KpiHtml = "".join(f'''<span style="background:{KPI_COLORS[Index % len(KPI_COLORS)]};padding:4px 10px;border-radius:12px;display:inline-block;white-space:nowrap;">{escape(Kpi.Name)}</span>'''for Index, Kpi in enumerate(Result.Kpis))
  Audience=f'<div style="margin:8px 0 14px;color:#4B5563;"><b>Intended Audience:</b> {escape(Result.Audience)}</div>' if Config.ShowAudience and Result.Audience else ""
  Value=f'<div style="height:20px;"></div><div style="background:#FDF0D5;border-left:4px solid #E9B949;border-radius:10px;padding:12px;margin-top:8px;"><b>Business Value:</b> {escape(Result.BusinessValue)}</div>' if Result.BusinessValue else ""
  Extra=""
  if Config.ShowBusinessObjectives: Extra+=_ListSection("Business Objectives",Result.BusinessObjectives)
  if Config.ShowKeyDecisions: Extra+=_ListSection("Key Decisions Supported",Result.KeyDecisionsSupported)
  return f'''<div style="font-family:Segoe UI;font-size:{Config.FontSize}px;line-height:1.3;overflow:hidden;box-sizing:border-box;">
{_Title("Report Summary")}{Audience}<p>{escape(Result.ReportSummary)}</p>
{_Title("Data Sources")}<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{SourceHtml}</div>
{Value}<div style="height:20px;"></div>{_Title("Top KPIs")}
<div style="display:flex;flex-wrap:wrap;align-items:flex-start;gap:6px;margin-top:6px;">{KpiHtml}</div>'''