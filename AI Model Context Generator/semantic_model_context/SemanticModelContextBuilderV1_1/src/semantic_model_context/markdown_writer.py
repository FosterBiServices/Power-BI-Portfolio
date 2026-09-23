from datetime import UTC, datetime
from pathlib import Path
from .domain import SemanticModel
from .validation import ValidationResult

def write_context(model: SemanticModel, validation: ValidationResult, output_path: Path) -> Path:
  columns=sum(len(t.columns) for t in model.tables); measures=sum(len(t.measures) for t in model.tables)
  lines=["---","contextType: Power BI Semantic Model","schemaVersion: 1.0",f"modelName: {model.name}",f"generatedUtc: {datetime.now(UTC).isoformat(timespec='seconds')}","---","","# Semantic Model Instructions","","Treat this file as the authoritative structural reference for this model.","Do not invent objects that are not listed.","","# Model Summary","",f"- Model: {model.name}",f"- Storage mode: {model.storage_mode}",f"- Tables: {len(model.tables)}",f"- Columns: {columns}",f"- Measures: {measures}",f"- Relationships: {len(model.relationships)}","","# Tables"]
  for table in model.tables:
    lines += ["",f"## {table.name}","",table.description or "No description provided.","","### Columns","","| Column | Data Type | Hidden | Key | Sort By |","|---|---|---:|---:|---|"]
    for c in table.columns: lines.append(f"| {c.name} | {c.data_type} | {'Yes' if c.is_hidden else 'No'} | {'Yes' if c.is_key else 'No'} | {c.sort_by_column} |")
    if table.measures:
      lines += ["","### Measures"]
      for m in table.measures: lines += ["",f"#### {m.name}","","```dax",m.expression,"```"]
  lines += ["","# Relationships","","| From | To | Cardinality | Direction | Active |","|---|---|---|---|---:|"]
  for r in model.relationships: lines.append(f"| {r.from_table}[{r.from_column}] | {r.to_table}[{r.to_column}] | {r.cardinality} | {r.cross_filter_direction} | {'Yes' if r.is_active else 'No'} |")
  lines += ["","# Validation","",f"- Model parsed successfully: {'Yes' if validation.is_valid else 'No'}",f"- Errors: {len(validation.errors)}",f"- Warnings: {len(validation.warnings)}"]
  output_path.parent.mkdir(parents=True, exist_ok=True); output_path.write_text("\n".join(lines)+"\n",encoding="utf-8"); return output_path
