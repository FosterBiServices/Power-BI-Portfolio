from __future__ import annotations


def is_auto_date_table(name: str) -> bool:
  normalized = name.strip().casefold()
  return normalized.startswith("localdatetable_") or normalized.startswith("datetabletemplate_")


def is_dedicated_measures_table(table) -> bool:
  """Identify dedicated measure containers without excluding mixed data tables."""
  name = table.name.strip().casefold()
  if name in {"_measures", "measures", "measure table", "measure tables"}:
    return True

  # A table containing measures but no business columns is also a measure container.
  # This supports custom names while avoiding removal of tables that contain data columns.
  visible_columns = [column for column in table.columns if not getattr(column, "is_hidden", False)]
  return bool(table.measures) and not visible_columns


def _escape(value) -> str:
  import html
  return html.escape(str(value or ""))


def diagram_v21(
  project,
  show_auto_date_tables: bool = False,
  include_measures_tables: bool = True,
) -> str:
  """Create a two-sided SVG ERD with visible endpoints and optional technical-table filtering."""
  visible_names = [
    name
    for name in sorted(project.tables, key=str.casefold)
    if (show_auto_date_tables or not is_auto_date_table(name))
    and (include_measures_tables or not is_dedicated_measures_table(project.tables[name]))
  ]
  visible = set(visible_names)
  relationships = [
    item
    for item in project.relationships
    if item.from_table in visible and item.to_table in visible
  ]
  if not visible_names:
    return '<p>No tables are available for the selected diagram options.</p>'

  degree = {name: 0 for name in visible_names}
  many_side = {name: 0 for name in visible_names}
  one_side = {name: 0 for name in visible_names}
  for item in relationships:
    degree[item.from_table] += 1
    degree[item.to_table] += 1
    if item.from_cardinality.casefold() == "many":
      many_side[item.from_table] += 1
    if item.to_cardinality.casefold() == "many":
      many_side[item.to_table] += 1
    if item.from_cardinality.casefold() == "one":
      one_side[item.from_table] += 1
    if item.to_cardinality.casefold() == "one":
      one_side[item.to_table] += 1

  connected = [name for name in visible_names if degree[name] > 0]
  disconnected = [name for name in visible_names if degree[name] == 0]
  left = sorted(
    [name for name in connected if many_side[name] >= one_side[name]],
    key=lambda name: (-degree[name], name.casefold()),
  )
  right = sorted(
    [name for name in connected if name not in left],
    key=lambda name: (-degree[name], name.casefold()),
  )
  if not left and right:
    split = max(1, len(right) // 2)
    left, right = right[:split], right[split:]
  if not right and len(left) > 1:
    split = (len(left) + 1) // 2
    left, right = left[:split], left[split:]

  card_width = 250
  card_height = 64
  left_x = 55
  right_x = 795
  top = 70
  row_gap = 100
  row_count = max(len(left), len(right), 1)
  disconnected_rows = (len(disconnected) + 2) // 3
  disconnected_top = top + row_count * row_gap + 60
  height = max(360, disconnected_top + disconnected_rows * 90 + 70)
  width = 1100

  positions = {}
  for index, name in enumerate(left):
    positions[name] = (left_x, top + index * row_gap)
  for index, name in enumerate(right):
    positions[name] = (right_x, top + index * row_gap)
  for index, name in enumerate(disconnected):
    positions[name] = (
      55 + (index % 3) * 345,
      disconnected_top + (index // 3) * 90,
    )

  def endpoint(name: str, side: str):
    x, y = positions[name]
    if side == "right":
      return x + card_width, y + card_height / 2
    return x, y + card_height / 2

  edge_parts = []
  parallel_counts = {}
  for item in relationships:
    from_x = positions[item.from_table][0]
    to_x = positions[item.to_table][0]
    if from_x <= to_x:
      start = endpoint(item.from_table, "right")
      finish = endpoint(item.to_table, "left")
    else:
      start = endpoint(item.from_table, "left")
      finish = endpoint(item.to_table, "right")

    key = tuple(sorted((item.from_table, item.to_table)))
    parallel_index = parallel_counts.get(key, 0)
    parallel_counts[key] = parallel_index + 1
    offset = (parallel_index - 1) * 12
    sx, sy = start
    tx, ty = finish
    curve = max(90, abs(tx - sx) * 0.38)
    color = "#1a3a5c" if item.is_active else "#c62828"
    dash = "" if item.is_active else ' stroke-dasharray="7,5"'
    marker_start = (
      ' marker-start="url(#arrow-start)"'
      if "both" in item.cross_filtering.casefold()
      else ""
    )
    tooltip = _escape(
      f"{item.from_table}[{item.from_column}] -> "
      f"{item.to_table}[{item.to_column}] | "
      f"{item.from_cardinality}:{item.to_cardinality} | "
      f"{item.cross_filtering} | "
      f"{'Active' if item.is_active else 'Inactive'}"
    )
    start_label = "*" if item.from_cardinality.casefold() == "many" else "1"
    finish_label = "*" if item.to_cardinality.casefold() == "many" else "1"
    edge_parts.append(
      f'<g class="relationship-edge"><title>{tooltip}</title>'
      f'<path d="M {sx} {sy} C {sx + curve} {sy + offset}, '
      f'{tx - curve} {ty + offset}, {tx} {ty}" fill="none" '
      f'stroke="{color}" stroke-width="2"{dash} '
      f'marker-end="url(#arrow-end)"{marker_start}/>'
      f'<text x="{sx + (16 if tx >= sx else -16)}" y="{sy - 8}" '
      f'text-anchor="middle" class="cardinality">{start_label}</text>'
      f'<text x="{tx + (-16 if tx >= sx else 16)}" y="{ty - 8}" '
      f'text-anchor="middle" class="cardinality">{finish_label}</text>'
      f'</g>'
    )

  node_parts = []
  for name in visible_names:
    x, y = positions[name]
    table = project.tables[name]
    if many_side[name] > one_side[name]:
      role, header = "Fact / many-side", "#1f4e79"
    elif one_side[name] > many_side[name]:
      role, header = "Dimension / one-side", "#2f855a"
    else:
      role, header = "Bridge / standalone", "#6b7280"
    node_parts.append(
      f'<g class="table-node"><title>{_escape(name)} | {_escape(role)}</title>'
      f'<rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" '
      f'rx="7" fill="#fff" stroke="#d0ccc4" stroke-width="1.5"/>'
      f'<rect x="{x}" y="{y}" width="{card_width}" height="32" '
      f'rx="7" fill="{header}"/>'
      f'<rect x="{x}" y="{y + 22}" width="{card_width}" height="10" '
      f'fill="{header}"/>'
      f'<text x="{x + card_width / 2}" y="{y + 21}" text-anchor="middle" '
      f'fill="#fff" class="node-title">{_escape(name[:34])}</text>'
      f'<text x="{x + 10}" y="{y + 51}" class="node-meta">'
      f'{len(table.columns)} columns · {len(table.measures)} measures</text>'
      f'</g>'
    )

  standalone_label = ""
  if disconnected:
    standalone_label = (
      f'<text x="55" y="{disconnected_top - 18}" class="standalone">'
      f'Standalone tables ({len(disconnected)})</text>'
    )

  hidden_auto_count = 0
  if not show_auto_date_tables:
    hidden_auto_count = sum(
      1 for name in project.tables if is_auto_date_table(name)
    )
  hidden_measure_count = 0
  if not include_measures_tables:
    hidden_measure_count = sum(
      1 for table in project.tables.values() if is_dedicated_measures_table(table)
    )
  notes = []
  if hidden_auto_count:
    notes.append(f"{hidden_auto_count} auto date table(s) hidden")
  if hidden_measure_count:
    notes.append(f"{hidden_measure_count} measures table(s) hidden")
  hidden_note = ""
  if notes:
    hidden_note = (
      f'<text x="{width - 45}" y="30" text-anchor="end" '
      f'class="note-svg">{_escape(" · ".join(notes))}</text>'
    )

  return (
    f'<svg viewBox="0 0 {width} {height}" class="diagram" role="img" '
    f'aria-label="Semantic model relationship diagram">'
    '<defs><marker id="arrow-end" markerWidth="8" markerHeight="8" '
    'refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" '
    'fill="#1a3a5c"/></marker><marker id="arrow-start" markerWidth="8" '
    'markerHeight="8" refX="1" refY="4" orient="auto-start-reverse">'
    '<path d="M8,0 L0,4 L8,8 z" fill="#1a3a5c"/></marker></defs>'
    '<style>.node-title{font:600 12px Segoe UI}.node-meta{font:11px Segoe UI;'
    'fill:#666}.cardinality{font:700 12px Segoe UI;fill:#1a3a5c;'
    'paint-order:stroke;stroke:#fff;stroke-width:3px}.standalone{font:600 13px '
    'Segoe UI;fill:#666}.note-svg{font:11px Segoe UI;fill:#666}</style>'
    f'{hidden_note}{"".join(edge_parts)}{standalone_label}{"".join(node_parts)}'
    f'<g transform="translate(55,{height - 44})"><line x1="0" y1="0" '
    'x2="30" y2="0" stroke="#1a3a5c" stroke-width="2"/><text x="38" '
    'y="4" class="node-meta">Active</text><line x1="100" y1="0" x2="130" '
    'y2="0" stroke="#c62828" stroke-width="2" stroke-dasharray="7,5"/>'
    '<text x="138" y="4" class="node-meta">Inactive</text><text x="230" '
    'y="4" class="node-meta">1 = one · * = many · arrows = filter direction</text>'
    '</g></svg>'
  )
