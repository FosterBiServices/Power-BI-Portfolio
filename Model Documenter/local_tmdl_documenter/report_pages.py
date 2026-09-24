from __future__ import annotations

from collections import defaultdict
import html


def _escape(value) -> str:
  return html.escape(str(value or ""))


def _field_kinds(project) -> dict[str, str]:
  kinds = {}
  for table in project.tables.values():
    for column in table.columns:
      kinds[f"{table.name}[{column.name}]".casefold()] = "Column"
    for measure in table.measures:
      kinds[f"{table.name}[{measure.name}]".casefold()] = "Measure"
  return kinds


def _field_kind(field: str, kinds: dict[str, str]) -> str:
  if "].[" in field:
    return "Hierarchy level"
  return kinds.get(field.casefold(), "Not in model")


def _page_canvas(page) -> str:
  """Scaled wireframe of the page: one box per visual, labelled with its ID."""
  width = max(page.width, 1)
  height = max(page.height, 1)
  boxes = []
  for visual in page.visuals:
    classes = ["vbox"]
    if visual.is_group:
      classes.append("group")
    if visual.is_hidden:
      classes.append("hidden")
    tooltip = "\n".join(filter(None, [
      f"ID: {visual.name}", f"Type: {visual.visual_type}",
      f"Title: {visual.title}" if visual.title else "",
      f"Fields: {', '.join(visual.fields)}" if visual.fields else "",
      "Hidden" if visual.is_hidden else "",
    ]))
    boxes.append(
      f'<div class="{" ".join(classes)}" title="{_escape(tooltip)}" style="'
      f'left:{visual.x / width * 100:.3f}%;top:{visual.y / height * 100:.3f}%;'
      f'width:{max(visual.width, 1) / width * 100:.3f}%;height:{max(visual.height, 1) / height * 100:.3f}%">'
      f'<b>{_escape(visual.visual_type)}</b><code>{_escape(visual.name)}</code></div>'
    )
  return (
    f'<div class="page" style="aspect-ratio:{width:g}/{height:g}">'
    + "".join(boxes) + '</div>'
  )


def _page_visual_table(page) -> str:
  rows = "".join(
    '<tr>'
    f'<td><code>{_escape(visual.name)}</code></td>'
    f'<td>{_escape(visual.visual_type)}{" (hidden)" if visual.is_hidden else ""}</td>'
    f'<td>{_escape(visual.title)}</td>'
    f'<td>{visual.x:.0f}, {visual.y:.0f} · {visual.width:.0f} × {visual.height:.0f}</td>'
    f'<td>{_escape(", ".join(visual.fields)) or "—"}</td>'
    '</tr>'
    for visual in sorted(page.visuals, key=lambda item: (item.y, item.x))
  )
  groups = sum(visual.is_group for visual in page.visuals)
  count = f"{len(page.visuals) - groups} visuals" + (f", {groups} groups" if groups else "")
  return (
    f'<details><summary>Visual details ({count})</summary><div class="inside table-scroll">'
    '<table><thead><tr><th>Visual ID</th><th>Type</th><th>Title</th>'
    '<th>Position (x, y · w × h)</th><th>Fields</th></tr></thead>'
    f'<tbody>{rows}</tbody></table></div></details>'
  )


def build_report_pages_html(project) -> str:
  pages = project.pages
  visuals = [visual for page in pages for visual in page.visuals if not visual.is_group]
  groups = sum(visual.is_group for page in pages for visual in page.visuals)
  hidden_pages = sum(page.is_hidden for page in pages)
  cards = (
    '<div class="grid">'
    f'<div class="stat"><b>{len(pages)}</b><span>Pages</span></div>'
    f'<div class="stat"><b>{hidden_pages}</b><span>Hidden pages</span></div>'
    f'<div class="stat"><b>{len(visuals)}</b><span>Visuals</span></div>'
    f'<div class="stat"><b>{groups}</b><span>Visual groups</span></div>'
    '</div>'
  )
  page_html = []
  for number, page in enumerate(pages, 1):
    page_visuals = [visual for visual in page.visuals if not visual.is_group]
    badge = ' <span class="badge">Hidden</span>' if page.is_hidden else ""
    page_html.append(
      f'<h3>{number}. {_escape(page.display_name)}{badge}</h3>'
      f'<p class="muted">{len(page_visuals)} visuals · {page.width:g} × {page.height:g} · '
      f'page ID <code>{_escape(page.name)}</code></p>'
      + _page_canvas(page) + _page_visual_table(page)
    )
  return (
    '<h2 id="pages">Report Pages</h2>'
    '<p>Each box is a visual, labelled with its type and visual ID. Dashed outlines '
    'are groups; faded boxes are hidden visuals. Hover a box for its title and fields.</p>'
    + cards + "".join(page_html)
  )


def build_visual_usage_html(project) -> str:
  kinds = _field_kinds(project)
  usage: dict[str, list] = defaultdict(list)
  for page in project.pages:
    for visual in page.visuals:
      for field in visual.fields:
        usage[field].append((page, visual))
  if not usage:
    return '<h2 id="usage">Visual Usage</h2><p>No field references were found in report visuals.</p>'
  rows = []
  for field in sorted(usage, key=str.casefold):
    uses = usage[field]
    used_in = "<br>".join(
      f'{_escape(page.display_name)} › {_escape(visual.title or visual.visual_type)} '
      f'<code>{_escape(visual.name)}</code>'
      for page, visual in sorted(uses, key=lambda item: (item[0].display_name.casefold(), item[1].name))
    )
    rows.append(
      f'<tr><td>{_escape(field)}</td><td>{_field_kind(field, kinds)}</td>'
      f'<td>{len(uses)}</td><td>{len({page.name for page, _ in uses})}</td><td>{used_in}</td></tr>'
    )
  return (
    '<h2 id="usage">Visual Usage</h2>'
    f'<p>{len(usage)} fields are referenced by report visuals, including filters and '
    'conditional formatting.</p>'
    '<input id="usage-filter" class="matrix-filter" type="search" '
    'placeholder="Filter fields, pages, or visual IDs" oninput="filterUsage()">'
    '<div class="table-scroll"><table id="usage-table" class="top"><thead><tr><th>Field</th><th>Kind</th>'
    '<th>Visuals</th><th>Pages</th><th>Used In</th></tr></thead><tbody>'
    + "".join(rows) + '</tbody></table></div>'
    '<script>function filterUsage(){const q=document.getElementById("usage-filter")'
    '.value.toLowerCase();document.querySelectorAll("#usage-table tbody tr").forEach(row=>'
    '{row.style.display=row.innerText.toLowerCase().includes(q)?"":"none";});}</script>'
  )
