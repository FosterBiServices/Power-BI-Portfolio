from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import html

from .dax_checks import check_measure
from .diagram_v21 import is_auto_date_table
from .v26_lineage import build_measure_lineage


@dataclass(frozen=True)
class ValidationFinding:
  severity: str
  category: str
  object_name: str
  message: str
  recommendation: str


def _escape(value) -> str:
  return html.escape(str(value or ""))


def _relationship_label(relationship) -> str:
  return (
    f"{relationship.from_table}[{relationship.from_column}] -> "
    f"{relationship.to_table}[{relationship.to_column}]"
  )


def _relationship_detail(relationship) -> str:
  direction = "both directions" if "both" in relationship.cross_filtering.casefold() else "single direction"
  state = "active" if relationship.is_active else "inactive"
  return (
    f" From {relationship.from_table}[{relationship.from_column}] "
    f"({relationship.from_cardinality}) to {relationship.to_table}[{relationship.to_column}] "
    f"({relationship.to_cardinality}); {direction}, {state}."
  )


def analyze_model(project, tables) -> list[ValidationFinding]:
  """Run conservative, evidence-based model quality checks.

  Findings identify review candidates. They do not modify the model and do not
  claim that an object is definitively wrong or safe to delete.
  """
  findings: list[ValidationFinding] = []
  included_names = {table.name for table in tables}

  # DAX errors. References resolve against the whole model, not just the
  # selected scope, so hidden or excluded tables do not cause false errors.
  model_tables = list(project.tables.values())
  for table in tables:
    for measure in table.measures:
      for message in check_measure(measure.name, measure.expression, model_tables):
        findings.append(ValidationFinding(
          "Error", "DAX Errors", f"{table.name}[{measure.name}]", message,
          "Fix the measure expression; visuals using this measure will fail to render.",
        ))

  # Table connectivity within selected scope.
  connected = set()
  for relationship in project.relationships:
    if relationship.from_table in included_names and relationship.to_table in included_names:
      connected.update((relationship.from_table, relationship.to_table))
  for table in tables:
    if table.name not in connected:
      outside = [
        _relationship_label(relationship) for relationship in project.relationships
        if table.name in (relationship.from_table, relationship.to_table)
      ]
      message = "Table is disconnected in the selected documentation scope."
      if outside:
        message += " Relationships to tables outside the scope: " + "; ".join(outside) + "."
      findings.append(ValidationFinding(
        "Warning", "Relationships", table.name,
        message,
        "Confirm that the table is intentionally standalone or used through measures only.",
      ))

  # Relationship review candidates.
  endpoint_counter = Counter()
  endpoint_labels = {}
  for relationship in project.relationships:
    if relationship.from_table not in included_names or relationship.to_table not in included_names:
      continue
    endpoint_key = (
      relationship.from_table.casefold(), relationship.from_column.casefold(),
      relationship.to_table.casefold(), relationship.to_column.casefold(),
    )
    endpoint_counter[endpoint_key] += 1
    endpoint_labels.setdefault(endpoint_key, _relationship_label(relationship))
    relationship_name = _relationship_label(relationship)
    detail = _relationship_detail(relationship)
    if not relationship.is_active:
      findings.append(ValidationFinding(
        "Info", "Relationships", relationship_name,
        "Relationship is inactive." + detail,
        "Confirm that DAX intentionally activates this relationship when needed.",
      ))
    if "both" in relationship.cross_filtering.casefold():
      findings.append(ValidationFinding(
        "Warning", "Relationships", relationship_name,
        "Relationship uses bidirectional filtering." + detail,
        "Review filter propagation and ambiguity risk; retain only when intentional.",
      ))
    if (
      relationship.from_cardinality.casefold() == "many"
      and relationship.to_cardinality.casefold() == "many"
    ):
      findings.append(ValidationFinding(
        "Warning", "Relationships", relationship_name,
        "Relationship is many-to-many." + detail,
        "Validate the grain and confirm that many-to-many behavior is required.",
      ))
  for endpoint_key, count in endpoint_counter.items():
    if count > 1:
      findings.append(ValidationFinding(
        "Warning", "Relationships", endpoint_labels[endpoint_key],
        f"{count} relationship definitions use the same endpoints.",
        "Review whether each duplicate-endpoint relationship is necessary.",
      ))

  # Technical table review.
  for table in tables:
    if is_auto_date_table(table.name):
      findings.append(ValidationFinding(
        "Info", "Technical Tables", table.name,
        "Auto date table detected.",
        "Consider an explicit date dimension for governed enterprise models.",
      ))

  # Storage mode and source-family review.
  modes = Counter()
  source_kinds = Counter()
  for table in tables:
    for partition in table.partitions:
      modes[(partition.mode or "Not specified").casefold()] += 1
      source_kinds[partition.source_kind or "Other / not detected"] += 1
  meaningful_modes = {mode for mode in modes if mode not in {"", "not specified"}}
  if len(meaningful_modes) > 1:
    findings.append(ValidationFinding(
      "Info", "Storage", "Semantic model",
      "Multiple partition storage modes were detected: " + ", ".join(sorted(meaningful_modes)) + ".",
      "Confirm that mixed storage modes are intentional and tested for expected behavior.",
    ))
  if source_kinds.get("Other / not detected", 0):
    count = source_kinds["Other / not detected"]
    findings.append(ValidationFinding(
      "Info", "Sources", "Source Inventory",
      f"{count} partition source(s) could not be classified by the current connector rules.",
      "Review the Power Query section and extend connector detection when needed.",
    ))

  # Measure lineage review. This reuses the conservative V2.6 analyzer.
  nodes, cycles = build_measure_lineage(project, tables)
  cycle_members = {key for cycle in cycles for key in cycle}
  for cycle in cycles:
    findings.append(ValidationFinding(
      "Error", "DAX Errors", " -> ".join(cycle),
      "Circular measure dependency detected.",
      "Resolve the dependency cycle before model processing or deployment.",
    ))
  for node in nodes.values():
    if node.key not in cycle_members and not node.used_by and not node.visuals:
      findings.append(ValidationFinding(
        "Warning", "Measures", node.key,
        "Measure is potentially unused by parsed measures and visuals.",
        "Review external usage before deprecating or deleting the measure.",
      ))

  return sorted(
    findings,
    key=lambda item: (
      {"Error": 0, "Warning": 1, "Info": 2}.get(item.severity, 3),
      item.category.casefold(), item.object_name.casefold(), item.message.casefold(),
    ),
  )


def build_validation_html(project, tables) -> str:
  findings = analyze_model(project, tables)
  severity_counts = Counter(item.severity for item in findings)
  category_counts = Counter(item.category for item in findings)

  cards = (
    '<div class="grid">'
    f'<div class="stat"><b>{severity_counts.get("Error", 0)}</b><span>Errors</span></div>'
    f'<div class="stat"><b>{severity_counts.get("Warning", 0)}</b><span>Warnings</span></div>'
    f'<div class="stat"><b>{severity_counts.get("Info", 0)}</b><span>Informational</span></div>'
    f'<div class="stat"><b>{len(findings)}</b><span>Total findings</span></div>'
    '</div>'
  )
  category_summary = ', '.join(
    f'{category}: {count}' for category, count in sorted(category_counts.items())
  ) or 'No findings'

  rows = ''.join(
    '<tr class="validation-row">'
    f'<td><span class="severity {item.severity.casefold()}">{_escape(item.severity)}</span></td>'
    f'<td>{_escape(item.category)}</td><td>{_escape(item.object_name)}</td>'
    f'<td>{_escape(item.message)}</td><td>{_escape(item.recommendation)}</td></tr>'
    for item in findings
  )
  if not rows:
    rows = '<tr><td colspan="5">No validation findings for the selected scope.</td></tr>'

  return (
    '<h2 id="model-validation">Model Validation</h2>'
    '<p>Validation findings are review candidates generated from the selected '
    'documentation scope. Informational and warning findings do not prove that '
    'the model is incorrect.</p>'
    + cards
    + f'<p><b>Findings by category:</b> {_escape(category_summary)}</p>'
    + '<h3>Validation Findings</h3>'
      '<div class="validation-controls"><input id="validation-filter" '
      'class="matrix-filter" type="search" placeholder="Filter validation findings" '
      'oninput="filterValidation()"><select id="validation-severity" '
      'onchange="filterValidation()"><option value="">All severities</option>'
      '<option>Error</option><option>Warning</option><option>Info</option></select></div>'
      '<div class="table-scroll"><table id="validation-table"><thead><tr>'
      '<th>Severity</th><th>Category</th><th>Object</th><th>Finding</th>'
      '<th>Recommendation</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
    + '<script>function filterValidation(){'
      'const q=document.getElementById("validation-filter").value.toLowerCase();'
      'const s=document.getElementById("validation-severity").value.toLowerCase();'
      'document.querySelectorAll("#validation-table tbody tr").forEach(row=>{'
      'const text=row.innerText.toLowerCase();const severity=row.cells[0]?'
      'row.cells[0].innerText.toLowerCase():"";row.style.display='
      '(text.includes(q)&&(!s||severity.includes(s)))?"":"none";});}</script>'
  )
