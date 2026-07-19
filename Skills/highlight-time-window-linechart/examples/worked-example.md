# Worked Example: `target_range` report

Substitution values used, taken from the `pbip/start` → `pbip/end` diff (a Sales-by-month line chart with a Between date-range slicer):

| Token | Value |
|---|---|
| `<SLICER_TABLE_NAME>` | `dimDate Slicer` |
| `<SOURCE_DATE_TABLE>` | `dimDate` |
| `<DATE_COLUMN_NAME>` | `Date` |
| `<SLICER_DATE_FORMAT>` | `Short Date` |
| `<SLICER_TABLE_LINEAGE_TAG>` | `4043821c-b0f7-4c37-8bc5-b40d2aadee9a` |
| `<SLICER_COLUMN_LINEAGE_TAG>` | `0a04fbc5-36e8-4e1b-8e16-0174dfd1bdbe` |
| `<SLICER_TABLE_PBI_ID>` | `1ce96267a7de4a62afe0bcb32964a8f9` |
| `<MEASURES_TABLE_NAME>` | `_Measures` |
| `<WINDOW_START_MEASURE_NAME>` | `Window Start Date` |
| `<WINDOW_END_MEASURE_NAME>` | `Window End Date` |
| `<MEASURE_DATE_FORMAT>` | `General Date` |
| `<WINDOW_START_LINEAGE_TAG>` | `78e9a5f8-ead6-4eac-9465-dbf4a20b1323` |
| `<WINDOW_END_LINEAGE_TAG>` | `15a27af7-0669-4a4d-95ed-97e2d18a50ab` |
| `<CATEGORY_TABLE_NAME>` | `dimDate` |
| `<CATEGORY_COLUMN_NAME>` | `EOmonth` |
| `<BASE_MEASURE_NAME>` | `Sales` |
| `<WINDOWED_CALC_NAME>` | `Data Labels Window` |
| `<SLICER_VISUAL_ID>` | `b3734404e96bdca0e3d2` |
| `<CHART_VISUAL_ID>` | `c1c97d02ce9912d08174` |
| `<SLICER_POS_X/Y/Z>`, height, width, tabOrder | `1277.78`, `240`, `1`, `87.78`, `261.11`, `1` |
| `<CHART_POS_X/Y/Z>`, height, width, tabOrder | `878.89`, `218.89`, `0`, `430`, `712.22`, `0` |
| `<DEFAULT_WINDOW_START_LITERAL>` | `datetime'2025-08-30T01:00:00'` |
| `<DEFAULT_WINDOW_END_LITERAL>` | `datetime'2026-06-27T01:00:00'` |
| `<FILTER_WINDOW_START_LITERAL>` | `datetime'2025-08-30T00:00:00'` |
| `<FILTER_WINDOW_END_EXCLUSIVE_LITERAL>` | `datetime'2026-06-28T00:00:00'` |
| `<SLICER_DATE_TEXT_SIZE>` | `9D` |
| `<SLICER_FILTER_ID>` | `98ddb8015097c5696056` |
| `<REF_LINE_END_LABEL>` | `'window end'` |
| `<REF_LINE_START_LABEL>` | `'window start'` |
| `<SHADE_TRANSPARENCY_END>` | `85D` |
| `<SHADE_TRANSPARENCY_START>` | `0D` |
| `<SHADE_COLOR_THEME_ID>` | `0` |
| `<REF_LINE_END_SELECTOR_ID>` | `1` |
| `<REF_LINE_START_SELECTOR_ID>` | `2` |
| `<REF_LINE_WIDTH>` | `1D` |
| `<WINDOWED_MARKER_SIZE>` | `4D` |
| `<DEFAULT_MARKER_SIZE>` | `3D` |
| `<ACCENT_COLOR_THEME_ID>` | `2` |
| `<ACCENT_COLOR_PERCENT>` | `0.2` |
| `<LABEL_FONT_SIZE>` | `8D` |
| `<CATEGORY_AXIS_FONT_SIZE>` | `10D` |
| `<CHART_TITLE>` | `'Sales'` |

## How the shading actually works

Two `xAxisReferenceLine` entries both shade `'before'` themselves, and the two washes stack:

- The **window end** line sits at `MAX('dimDate Slicer'[Date])` and shades everything to its left at 85% transparency (`Function: 4` = MAX, `<SHADE_TRANSPARENCY_END>` = `85D`) — a faint wash from the chart's start up to the end of the selected window.
- The **window start** line sits at `MIN('dimDate Slicer'[Date])` and shades everything to its left at 0% transparency with an explicit theme color (`Function: 3` = MIN, `<SHADE_TRANSPARENCY_START>` = `0D`) — a fully solid wash from the chart's start up to the start of the selected window.

Because the solid wash (before window start) fully overpaints the faint wash in that same region, the net visible effect is: solid shade before the window, faint shade *inside* the window, and no shade after it — reading as a highlighted band between the two slicer handles.

## 1. `<SemanticModel>/definition/tables/dimDate Slicer.tmdl` (new file)

Rendered from `templates/disconnected-date-slicer-table.tmdl`:

	table 'dimDate Slicer'
		lineageTag: 4043821c-b0f7-4c37-8bc5-b40d2aadee9a

		column Date
			formatString: Short Date
			lineageTag: 0a04fbc5-36e8-4e1b-8e16-0174dfd1bdbe
			summarizeBy: none
			isNameInferred
			sourceColumn: dimDate[Date]

			annotation SummarizationSetBy = Automatic

		partition 'dimDate Slicer' = calculated
			mode: import
			source = ```

					VALUES( dimDate[Date] )

					```

		annotation PBI_Id = 1ce96267a7de4a62afe0bcb32964a8f9

## 2. `<SemanticModel>/definition/model.tmdl` (append one line)

Rendered from `templates/model-tmdl-table-ref.snippet.tmdl`, added next to the other `ref table` lines:

	ref table 'dimDate Slicer'

## 3. `<SemanticModel>/definition/tables/_Measures.tmdl` (insert above `partition`)

Rendered from `templates/window-boundary-measures.snippet.tmdl`:

	measure 'Window Start Date' = MIN('dimDate Slicer'[Date])
		formatString: General Date
		lineageTag: 78e9a5f8-ead6-4eac-9465-dbf4a20b1323

	measure 'Window End Date' = MAX( 'dimDate Slicer'[Date])
		formatString: General Date
		lineageTag: 15a27af7-0669-4a4d-95ed-97e2d18a50ab

## 4. Slicer visual and 5. Line chart visual

The fully rendered `visual.json` output for both visuals is exactly the content already captured in this repo at:

- `pbip/end/target_range_end.Report/definition/pages/2904eb2c583866b57ec8/visuals/b3734404e96bdca0e3d2/visual.json` (the Between slicer, rendered from `templates/between-date-slicer-visual.json`)
- `pbip/end/target_range_end.Report/definition/pages/2904eb2c583866b57ec8/visuals/c1c97d02ce9912d08174/visual.json` (the windowed line chart, rendered from `templates/windowed-line-chart-visual.json`)

Diffing either against its template with the token table above substituted in reproduces the file byte-for-byte (aside from whitespace).

## Result

Moving the slicer's Between handles moves both reference lines on the chart. Everything left of the window-start handle reads as dimmed, everything from window-start to window-end reads as a lightly-washed highlighted band, and only the months inside that band carry the `Data Labels Window` markers/labels — because `Data Labels Window` is `BLANK()` outside `[Window Start Date]..[Window End Date]` and Power BI never draws a marker or label for a blank point.
