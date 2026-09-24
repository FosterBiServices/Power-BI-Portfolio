from html import escape

def BuildHtml(Model, Config):
  Sources = "\n".join(f'<span style="background:{Item.Background};color:{Item.Foreground};padding:4px 10px;border-radius:12px;">{escape(Item.Name)}</span>' for Item in Model.Sources) or '<span style="background:#E5E7EB;color:#374151;padding:4px 10px;border-radius:12px;">Evidence Gap: No classified sources detected</span>'
  Kpis = "\n".join(f'<span style="background:{Item.Color};padding:4px 10px;border-radius:12px;">{escape(Item.Name)}</span>' for Item in Model.Kpis) or '<span style="background:#E5E7EB;padding:4px 10px;border-radius:12px;">Evidence Gap: No qualifying KPIs detected</span>'
  return f"""<div style="display:flex;gap:12px;font-family:Segoe UI;font-size:{Config.FontSize}px;line-height:1.3;overflow:hidden;box-sizing:border-box;">
  <div style="width:50%;min-width:0;">
    <b style="color:#003B5C;">Report Summary</b>
    <p>{escape(Model.ReportSummary)}</p>
    <b style="color:#003B5C;">Data Sources</b>
    <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{Sources}</div>
    <div style="height:20px;"></div>
    <div style="background:#FDF0D5;border-left:4px solid #E9B949;border-radius:10px;padding:12px;margin-top:8px;"><b>Business Value:</b> {escape(Model.BusinessValue)}</div>
    <div style="height:20px;"></div>
    <b style="color:#003B5C;">Top KPIs</b>
    <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{Kpis}</div>
  </div>
  <div style="width:50%;min-width:0;">
    <b style="color:#003B5C;">Technical Model Details</b>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px;">
      <div style="background:#F8F9FA;color:#4B5563;border-radius:8px;padding:8px;text-align:center;"><b>{Model.TableCount}</b><br>Tables</div>
      <div style="background:#F8F9FA;color:#4B5563;border-radius:8px;padding:8px;text-align:center;"><b>{Model.ColumnCount}</b><br>Columns</div>
      <div style="background:#F8F9FA;color:#4B5563;border-radius:8px;padding:8px;text-align:center;"><b>{Model.MeasureCount}</b><br>Measures</div>
      <div style="background:#F8F9FA;color:#4B5563;border-radius:8px;padding:8px;text-align:center;"><b>{Model.RelationshipCount}</b><br>Relationships</div>
    </div>
    <div style="margin-top:20px;"><b style="color:#4B5563;">Relationship Strategy</b><div style="margin-top:8px;background:#F8F9FA;color:#4B5563;border-radius:10px;padding:12px;">{escape(Model.RelationshipStrategy)}</div></div>
  </div>
</div>"""
