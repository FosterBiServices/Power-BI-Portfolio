from html import escape
from .config import SOURCE_COLORS,KPI_COLORS

def BuildAiHtml(Result,FontSize=18):
  SourceChips=[]
  for Index,Name in enumerate(Result["data_sources"]):
    Background,Foreground=SOURCE_COLORS[Index%len(SOURCE_COLORS)]
    SourceChips.append(f'<span style="background:{Background};color:{Foreground};padding:4px 10px;border-radius:12px;">{escape(Name)}</span>')
  KpiChips=[f'<span style="background:{KPI_COLORS[Index%len(KPI_COLORS)]};padding:4px 10px;border-radius:12px;">{escape(Name)}</span>' for Index,Name in enumerate(Result["top_kpis"])]
  Sources="\n".join(SourceChips) or '<span style="background:#E5E7EB;color:#374151;padding:4px 10px;border-radius:12px;">No classified sources supplied</span>'
  Kpis="\n".join(KpiChips) or '<span style="background:#E5E7EB;padding:4px 10px;border-radius:12px;">No qualifying KPIs supplied</span>'
  return f"""<div style="font-family:Segoe UI;font-size:{FontSize}px;line-height:1.3;overflow:hidden;box-sizing:border-box;">
  <b style="color:#003B5C;">Report Summary</b>
  <p>{escape(Result['report_summary'])}</p>
  <b style="color:#003B5C;">Data Sources</b>
  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{Sources}</div>
  <div style="height:20px;"></div>
  <div style="background:#FDF0D5;border-left:4px solid #E9B949;border-radius:10px;padding:12px;margin-top:8px;"><b>Business Value:</b> {escape(Result['business_value'])}</div>
  <div style="height:20px;"></div>
  <b style="color:#003B5C;">Top KPIs</b>
  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{Kpis}</div>
</div>"""
