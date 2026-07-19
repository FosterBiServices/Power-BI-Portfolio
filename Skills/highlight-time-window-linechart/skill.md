---
name: highlight-time-window-linechart
description: Add a "Between" date-range slicer that shades a highlighted time window on a Power BI line chart, using a disconnected calculated date table, MIN/MAX boundary measures, and reference-line shading, with data labels shown only for points inside the window. Use for PBIP (TMDL + PBIR) reports when highlighting/shading a date range on a line chart, adding a between-dates slicer, or showing conditional data labels within a selected window.
---

# Highlight Time Window in Line Chart

## Goal
Add a "Between" date-range slicer that shades a highlighted window on a line chart and shows data labels only for points inside that window, using a disconnected calculated date table, two MIN/MAX boundary measures, and reference-line shading — without filtering the chart's own date axis.

## Prerequisites
- A PBIP-format Power BI project (Report in PBIR, model in TMDL).
- An existing date dimension table with a Date column (e.g. `dimDate[Date]`).
- An existing line chart visual on a report page, with a category field on the date axis and one base measure on Y.
- A hidden measures table to hold the two new boundary measures.
- Power BI Desktop to reload and validate after edits (TMDL/PBIR are not live-validated by hand).

## Token Table
| Token | Meaning | Example |
|---|---|---|
| `<SLICER_TABLE_NAME>` | Disconnected calculated table name, plain (no quotes — TMDL templates add required `'...'` quoting themselves) | `dimDate Slicer` |
| `<SOURCE_DATE_TABLE>` | Existing date dimension table the slicer table pulls `VALUES()` from | `dimDate` |
| `<DATE_COLUMN_NAME>` | Date column name, shared by source and slicer table | `Date` |
| `<SLICER_DATE_FORMAT>` | Format string on the slicer table's Date column | `Short Date` |
| `<SLICER_TABLE_LINEAGE_TAG>`, `<SLICER_COLUMN_LINEAGE_TAG>`, `<SLICER_TABLE_PBI_ID>` | Fresh GUIDs for the new table/column/partition | new GUID each |
| `<MEASURES_TABLE_NAME>` | Existing hidden measures table | `_Measures` |
| `<WINDOW_START_MEASURE_NAME>`, `<WINDOW_END_MEASURE_NAME>` | New MIN/MAX boundary measure names, plain (TMDL template adds quoting) | `Window Start Date`, `Window End Date` |
| `<MEASURE_DATE_FORMAT>` | Format string on both boundary measures | `General Date` |
| `<WINDOW_START_LINEAGE_TAG>`, `<WINDOW_END_LINEAGE_TAG>` | Fresh GUIDs for the two measures | new GUID each |
| `<CATEGORY_TABLE_NAME>`, `<CATEGORY_COLUMN_NAME>` | Table/column already on the chart's date axis | `dimDate`, `EOmonth` |
| `<BASE_MEASURE_NAME>` | Existing measure already on the chart's Y axis | `Sales` |
| `<WINDOWED_CALC_NAME>` | Name of the new native visual calculation series | `Data Labels Window` |
| `<SLICER_VISUAL_ID>`, `<CHART_VISUAL_ID>` | 20-char hex visual container ids (chart id must match the visual you're editing) | `b3734404e96bdca0e3d2` |
| `<SLICER_POS_X/Y/Z>`, `<SLICER_HEIGHT>`, `<SLICER_WIDTH>`, `<SLICER_TAB_ORDER>` | Slicer container position/size on the page grid | numeric |
| `<CHART_POS_X/Y/Z>`, `<CHART_HEIGHT>`, `<CHART_WIDTH>`, `<CHART_TAB_ORDER>` | Must match the existing chart's current position/size (do not move it) | numeric |
| `<DEFAULT_WINDOW_START_LITERAL>`, `<DEFAULT_WINDOW_END_LITERAL>` | Initial slicer handle positions, e.g. `datetime'2025-08-30T01:00:00'` | datetime literal |
| `<FILTER_WINDOW_START_LITERAL>`, `<FILTER_WINDOW_END_EXCLUSIVE_LITERAL>` | Matching default-filter bounds (end is midnight of the day *after* the last included date) | datetime literal |
| `<SLICER_DATE_TEXT_SIZE>` | Font size on the slicer's date labels | `9D` |
| `<SLICER_FILTER_ID>` | 20-char hex filter id in the slicer's `filterConfig` | random hex |
| `<REF_LINE_END_LABEL>`, `<REF_LINE_START_LABEL>` | Reference-line display names, quoted | `'window end'`, `'window start'` |
| `<SHADE_TRANSPARENCY_END>` | Transparency of the light wash covering everything up to window end | `85D` |
| `<SHADE_TRANSPARENCY_START>` | Transparency of the solid shade covering everything before window start | `0D` |
| `<SHADE_COLOR_THEME_ID>` | Theme color id used for the window-start shade | `0` |
| `<REF_LINE_END_SELECTOR_ID>`, `<REF_LINE_START_SELECTOR_ID>` | Selector ids distinguishing the two reference lines | `1`, `2` |
| `<REF_LINE_WIDTH>` | Reference line stroke width | `1D` |
| `<WINDOWED_MARKER_SIZE>`, `<DEFAULT_MARKER_SIZE>` | Marker size inside vs. outside the window | `4D`, `3D` |
| `<ACCENT_COLOR_THEME_ID>`, `<ACCENT_COLOR_PERCENT>` | Theme color for windowed markers and data labels | `2`, `0.2` |
| `<LABEL_FONT_SIZE>`, `<CATEGORY_AXIS_FONT_SIZE>` | Data label and category axis font sizes | `8D`, `10D` |
| `<CHART_TITLE>` | Chart title text, quoted | `'Sales'` |

## File Map (apply in order)
1. `templates/disconnected-date-slicer-table.tmdl` → write as new file `<SemanticModel>/definition/tables/<SLICER_TABLE_NAME>.tmdl`.
2. `templates/model-tmdl-table-ref.snippet.tmdl` → append its one line into the existing `<SemanticModel>/definition/model.tmdl`, alongside the other `ref table` lines.
3. `templates/window-boundary-measures.snippet.tmdl` → insert into the existing measures table file (`<MEASURES_TABLE_NAME>.tmdl`), directly above its `partition` line.
4. `templates/between-date-slicer-visual.json` → write as new file `<Report>/definition/pages/<page-id>/visuals/<SLICER_VISUAL_ID>/visual.json`.
5. `templates/windowed-line-chart-visual.json` → merge into the existing line chart's `visual.json`: add the `Tooltips` block and second `Y` projection to `query.queryState`, add `xAxisReferenceLine`, `lineStyles`, `labels`, `legend`, and `valueAxis` under `objects`. Keep the chart's own existing `Category`/base `Y` projection, position, filters, and any other `visualContainerObjects` untouched.

Do not add a relationship between `<SLICER_TABLE_NAME>` and the model — it must stay disconnected; the boundary measures read it via `MIN`/`MAX` regardless of the chart's own filter context.

## Validation
- Reload the .pbip in Power BI Desktop; confirm no load errors.
- In Model view, confirm `<SLICER_TABLE_NAME>` has zero relationship lines to any other table.
- On the report page, confirm the slicer renders as a single "Between" date-range control with no header.
- Drag either slicer handle; confirm the shaded band on the line chart moves and only points inside the window keep data labels/markers.
- Add a temporary card visual with `<WINDOW_START_MEASURE_NAME>` and `<WINDOW_END_MEASURE_NAME>`; confirm they match the slicer's current handles, then remove the card.
