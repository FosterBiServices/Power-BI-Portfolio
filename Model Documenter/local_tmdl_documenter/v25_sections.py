from __future__ import annotations

from collections import Counter


def _escape(value) -> str:
  import html
  return html.escape(str(value or ""))


def build_source_inventory(project, tables) -> str:
  """Build a source inventory from table partition metadata."""
  rows = []
  source_counts = Counter()
  mode_counts = Counter()

  for table in sorted(tables, key=lambda item: item.name.casefold()):
    for partition in table.partitions:
      source_kind = partition.source_kind or "Other / not detected"
      mode = partition.mode or "Not specified"
      source_type = partition.source_type or "Not specified"
      source_counts[source_kind] += 1
      mode_counts[mode] += 1
      rows.append(
        "<tr>"
        f"<td>{_escape(table.name)}</td>"
        f"<td>{_escape(partition.name)}</td>"
        f"<td>{_escape(mode)}</td>"
        f"<td>{_escape(source_type)}</td>"
        f"<td>{_escape(source_kind)}</td>"
        "</tr>"
      )

  if not rows:
    return (
      '<h2 id="source-inventory">Source Inventory</h2>'
      '<p>No table partitions were detected for the selected documentation scope.</p>'
    )

  source_cards = "".join(
    f'<div class="stat"><b>{count}</b><span>{_escape(source)}</span></div>'
    for source, count in sorted(source_counts.items(), key=lambda item: item[0].casefold())
  )
  mode_summary = ", ".join(
    f"{mode}: {count}" for mode, count in sorted(mode_counts.items())
  )
  return (
    '<h2 id="source-inventory">Source Inventory</h2>'
    f'<div class="grid">{source_cards}</div>'
    f'<p><b>Partition modes:</b> {_escape(mode_summary)}</p>'
    '<table><thead><tr>'
    '<th>Table</th><th>Partition</th><th>Mode</th>'
    '<th>Partition Type</th><th>Detected Source</th>'
    '</tr></thead><tbody>'
    + "".join(rows)
    + '</tbody></table>'
  )


def build_relationship_matrix(project, included_table_names: set[str]) -> str:
  """Build a searchable relationship matrix for the selected table scope."""
  relationships = [
    item
    for item in project.relationships
    if item.from_table in included_table_names
    and item.to_table in included_table_names
  ]

  if not relationships:
    return (
      '<h2 id="relationship-matrix">Relationship Matrix</h2>'
      '<p>No relationships were found for the selected documentation scope.</p>'
    )

  rows = []
  for index, item in enumerate(
    sorted(
      relationships,
      key=lambda value: (
        value.from_table.casefold(),
        value.to_table.casefold(),
        value.name.casefold(),
      ),
    ),
    start=1,
  ):
    status = "Active" if item.is_active else "Inactive"
    cardinality = f"{item.from_cardinality} : {item.to_cardinality}"
    rows.append(
      '<tr class="relationship-row">'
      f'<td>{index}</td>'
      f'<td>{_escape(item.name)}</td>'
      f'<td>{_escape(item.from_table)}</td>'
      f'<td>{_escape(item.from_column)}</td>'
      f'<td>{_escape(item.to_table)}</td>'
      f'<td>{_escape(item.to_column)}</td>'
      f'<td>{_escape(cardinality)}</td>'
      f'<td>{_escape(item.cross_filtering)}</td>'
      f'<td>{status}</td>'
      '</tr>'
    )

  return (
    '<h2 id="relationship-matrix">Relationship Matrix</h2>'
    '<p>Use the field below to filter by table, column, relationship, '
    'cardinality, direction, or status.</p>'
    '<input id="relationship-filter" class="matrix-filter" '
    'type="search" placeholder="Filter relationships" '
    'oninput="filterRelationshipMatrix()">'
    '<div class="table-scroll"><table id="relationship-matrix-table">'
    '<thead><tr><th>#</th><th>Relationship</th><th>From Table</th>'
    '<th>From Column</th><th>To Table</th><th>To Column</th>'
    '<th>Cardinality</th><th>Filter Direction</th><th>Status</th>'
    '</tr></thead><tbody>'
    + "".join(rows)
    + '</tbody></table></div>'
    '<script>'
    'function filterRelationshipMatrix(){'
    'const q=document.getElementById("relationship-filter").value.toLowerCase();'
    'document.querySelectorAll("#relationship-matrix-table tbody tr").forEach('
    'row=>{row.style.display=row.innerText.toLowerCase().includes(q)?"":"none";});'
    '}'
    '</script>'
  )
