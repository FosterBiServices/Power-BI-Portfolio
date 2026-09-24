from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import html
import re

_MEASURE_TOKEN = re.compile(r"(?<![\w'])\[([^\]]+)\]")
_QUALIFIED_COLUMN = re.compile(
  r"(?:'(?P<quoted>(?:''|[^'])+)'|(?P<plain>[A-Za-z_][\w ]*))\s*\[(?P<column>[^\]]+)\]"
)


@dataclass
class MeasureNode:
  key: str
  table: str
  name: str
  expression: str
  direct_dependencies: set[str] = field(default_factory=set)
  column_dependencies: set[str] = field(default_factory=set)
  used_by: set[str] = field(default_factory=set)
  visuals: set[str] = field(default_factory=set)
  unresolved_references: set[str] = field(default_factory=set)


def _escape(value) -> str:
  return html.escape(str(value or ""))


def _measure_key(table: str, measure: str) -> str:
  return f"{table}[{measure}]"


def build_measure_lineage(project, tables):
  """Build dependency and impact indexes for measures in the selected scope.

  Measure references are resolved by exact measure name. If the same measure name
  exists in multiple tables, an unqualified [Measure] reference is left unresolved
  rather than assigned to an arbitrary table.
  """
  nodes: dict[str, MeasureNode] = {}
  name_index: dict[str, list[str]] = defaultdict(list)

  for table in tables:
    for measure in table.measures:
      key = _measure_key(table.name, measure.name)
      node = MeasureNode(key, table.name, measure.name, measure.expression or "")
      nodes[key] = node
      name_index[measure.name.casefold()].append(key)

  for node in nodes.values():
    qualified_columns = set()
    column_names = set()
    for match in _QUALIFIED_COLUMN.finditer(node.expression):
      table_name = (match.group("quoted") or match.group("plain") or "").replace("''", "'").strip()
      column_name = match.group("column").strip()
      qualified_columns.add(f"{table_name}[{column_name}]")
      column_names.add(column_name.casefold())
    node.column_dependencies = qualified_columns

    for token in _MEASURE_TOKEN.findall(node.expression):
      candidate_name = token.strip()
      if candidate_name.casefold() in column_names:
        continue
      matches = name_index.get(candidate_name.casefold(), [])
      if len(matches) == 1 and matches[0] != node.key:
        node.direct_dependencies.add(matches[0])
      elif len(matches) != 1:
        node.unresolved_references.add(candidate_name)

  for node in nodes.values():
    for dependency in node.direct_dependencies:
      if dependency in nodes:
        nodes[dependency].used_by.add(node.key)

  # PBIR field references are stored as Table[Field]. Match only exact measures.
  for page in project.pages:
    for visual in page.visuals:
      visual_label = f"{page.display_name}: {visual.name} ({visual.visual_type})"
      for field_reference in visual.fields:
        if field_reference in nodes:
          nodes[field_reference].visuals.add(visual_label)

  cycles = _find_cycles(nodes)
  return nodes, cycles


def _find_cycles(nodes: dict[str, MeasureNode]) -> list[list[str]]:
  """Find unique measure dependency cycles using depth-first traversal."""
  state: dict[str, int] = {}
  stack: list[str] = []
  cycles: set[tuple[str, ...]] = set()

  def canonical(cycle: list[str]) -> tuple[str, ...]:
    body = cycle[:-1]
    rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
    normalized = min(rotations)
    return normalized + (normalized[0],)

  def visit(key: str):
    state[key] = 1
    stack.append(key)
    for dependency in nodes[key].direct_dependencies:
      if dependency not in nodes:
        continue
      if state.get(dependency, 0) == 0:
        visit(dependency)
      elif state.get(dependency) == 1 and dependency in stack:
        start = stack.index(dependency)
        cycles.add(canonical(stack[start:] + [dependency]))
    stack.pop()
    state[key] = 2

  for key in sorted(nodes, key=str.casefold):
    if state.get(key, 0) == 0:
      visit(key)
  return [list(cycle) for cycle in sorted(cycles)]


def _transitive_dependencies(start: str, nodes: dict[str, MeasureNode]) -> list[str]:
  seen = set()
  pending = list(nodes[start].direct_dependencies)
  while pending:
    key = pending.pop()
    if key in seen or key not in nodes:
      continue
    seen.add(key)
    pending.extend(nodes[key].direct_dependencies)
  return sorted(seen, key=str.casefold)


def build_measure_lineage_html(project, tables) -> str:
  nodes, cycles = build_measure_lineage(project, tables)
  if not nodes:
    return (
      '<h2 id="measure-lineage">Measure Lineage</h2>'
      '<p>No measures were found in the selected documentation scope.</p>'
    )

  orphaned = [
    node for node in nodes.values()
    if not node.used_by and not node.visuals
  ]
  unresolved_count = sum(len(node.unresolved_references) for node in nodes.values())
  cards = (
    '<div class="grid">'
    f'<div class="stat"><b>{len(nodes)}</b><span>Measures analyzed</span></div>'
    f'<div class="stat"><b>{sum(len(node.direct_dependencies) for node in nodes.values())}</b><span>Measure dependencies</span></div>'
    f'<div class="stat"><b>{len(orphaned)}</b><span>Potentially unused</span></div>'
    f'<div class="stat"><b>{len(cycles)}</b><span>Dependency cycles</span></div>'
    f'<div class="stat"><b>{unresolved_count}</b><span>Unresolved references</span></div>'
    '</div>'
  )

  rows = []
  details = []
  for node in sorted(nodes.values(), key=lambda item: (item.table.casefold(), item.name.casefold())):
    dependencies = sorted(node.direct_dependencies, key=str.casefold)
    impacts = sorted(node.used_by, key=str.casefold)
    visuals = sorted(node.visuals, key=str.casefold)
    transitive = _transitive_dependencies(node.key, nodes)
    status = "Potentially unused" if not impacts and not visuals else "Used"
    rows.append(
      '<tr class="lineage-row">'
      f'<td>{_escape(node.table)}</td><td>{_escape(node.name)}</td>'
      f'<td>{_escape(", ".join(dependencies) or "None")}</td>'
      f'<td>{_escape(", ".join(impacts) or "None")}</td>'
      f'<td>{len(visuals)}</td><td>{status}</td></tr>'
    )
    details.append(
      f'<details><summary>{_escape(node.key)}</summary><div class="inside">'
      f'<p><b>Direct measure dependencies:</b> {_escape(", ".join(dependencies) or "None")}</p>'
      f'<p><b>All downstream dependencies:</b> {_escape(", ".join(transitive) or "None")}</p>'
      f'<p><b>Column dependencies:</b> {_escape(", ".join(sorted(node.column_dependencies)) or "None detected")}</p>'
      f'<p><b>Used by measures:</b> {_escape(", ".join(impacts) or "None")}</p>'
      f'<p><b>Used by visuals:</b> {_escape("; ".join(visuals) or "None detected")}</p>'
      f'<p><b>Unresolved bracket references:</b> {_escape(", ".join(sorted(node.unresolved_references)) or "None")}</p>'
      '</div></details>'
    )

  cycle_html = ''
  if cycles:
    cycle_html = '<h3>Dependency Cycles</h3><ul>' + ''.join(
      f'<li>{_escape(" -> ".join(cycle))}</li>' for cycle in cycles
    ) + '</ul>'

  unused_html = '<h3>Potentially Unused Measures</h3>'
  if orphaned:
    unused_html += '<ul>' + ''.join(
      f'<li>{_escape(node.key)}</li>' for node in sorted(orphaned, key=lambda item: item.key.casefold())
    ) + '</ul>'
  else:
    unused_html += '<p>No potentially unused measures were detected.</p>'

  return (
    '<h2 id="measure-lineage">Measure Lineage and Impact Analysis</h2>'
    '<p>Lineage is derived from exact bracket references in parsed DAX and exact '
    'Table[Field] references in parsed report visuals. Review unresolved references '
    'before using the results for deletion decisions.</p>'
    + cards
    + '<input id="lineage-filter" class="matrix-filter" type="search" '
      'placeholder="Filter measures or dependencies" oninput="filterLineage()">'
      '<div class="table-scroll"><table id="measure-lineage-table"><thead><tr>'
      '<th>Table</th><th>Measure</th><th>Depends On</th><th>Used By</th>'
      '<th>Visuals</th><th>Status</th></tr></thead><tbody>'
    + ''.join(rows)
    + '</tbody></table></div>'
    + cycle_html
    + unused_html
    + '<h3>Measure Details</h3>'
    + ''.join(details)
    + '<script>function filterLineage(){const q=document.getElementById('
      '"lineage-filter").value.toLowerCase();document.querySelectorAll('
      '"#measure-lineage-table tbody tr").forEach(row=>{row.style.display='
      'row.innerText.toLowerCase().includes(q)?"":"none";});}</script>'
  )
