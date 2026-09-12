---
name: stacked-bar-percent-of-total
description: Add a stacked bar/column chart where each bar reads as a single solid-color segment carrying a "% of total" label in blended headroom, using a same-color spacer measure stacked alongside the real value instead of a second visible series.
---

# Stacked bar chart with a percent-of-total label

## Goal
Add a stacked bar or column chart to an existing PBIP report page where each bar shows
its real value with a normal label, plus a second label — the category's `% of total`
share — that appears to float in extra headroom above/beside the bar rather than as a
second visible stack segment. The trick: stack a second "spacer" measure (sized to a
fixed fraction of the largest category value) on top of the real measure, then recolor
that spacer segment to exactly match the real segment's color so the two blend into what
looks like one bar, and attach the `% of total` label to the spacer segment instead of a
value.

## Prerequisites
- An existing PBIP report with a semantic model open in TMDL view (Power BI Desktop or
  Tabular Editor) and a report page already created.
- A base fact/measure table with a working numeric measure to chart (`<VALUE_MEASURE>`).
- A dimension table with the category column to chart by (`<CATEGORY_TABLE>`,
  `<CATEGORY_COLUMN>`).
- No relationship or date-table setup is required by this pattern itself.

## Tokens

| Token | Description | Example |
|---|---|---|
| `<MEASURES_TABLE>` | Table holding the model's measures | `_Measures` |
| `<VALUE_MEASURE>` | Existing measure being charted | `Total Sales` |
| `<CATEGORY_TABLE>` | Dimension table for the category axis | `dimProducts` |
| `<CATEGORY_COLUMN>` | Category column on that table | `ProductCategory` |
| `<SPACER_MEASURE_NAME>` | New measure that pads each bar with blended-color headroom | `Stacked Chart Spacing` |
| `<SPACER_RATIO>` | Fraction of the largest category value used as headroom, DAX literal | `.10` |
| `<PERCENT_MEASURE_NAME>` | New % of category-total measure shown in the headroom label | `% of Total Sales by Product Category` |
| `<PERCENT_FORMAT_STRING>` | Format string for the percent measure | `0.00%;-0.00%;0.00%` |
| `<PAGE_ID>` | Folder name of the target report page | `dab238165c5348774fb4` |
| `<VISUAL_ID>` | New visual's folder name and `name` field (unique id) | `5e6a3a0a2d634dc3513c` |
| `<VISUAL_TYPE>` | `barChart` (horizontal stacked) or `columnChart` (vertical stacked) | `barChart` |
| `<POS_X>` `<POS_Y>` `<POS_Z>` | Visual canvas position | `517.98` `327.70` `0` |
| `<POS_HEIGHT>` `<POS_WIDTH>` | Visual size | `607.83` `794.58` |
| `<TAB_ORDER>` | Visual tab order on the page | `0` |
| `<TITLE_TEXT>` | Visual title text | `Total Sales by Product Category` |
| `<TITLE_FONT_COLOR_THEME_ID>` `<TITLE_FONT_COLOR_PERCENT>` | Theme color + shade for the title font | `0` `-0.6` |
| `<LABEL_DISPLAY_UNITS>` | Display units applied to value labels, DAX literal | `1D` |
| `<LABEL_PRECISION>` | Decimal precision applied to value labels, DAX literal | `0L` |
| `<BAR_COLOR_THEME_ID>` `<BAR_COLOR_PERCENT>` | Theme color + shade for the spacer segment — must match the real segment's default color so it blends in | `0` `0` |
| `<SPACER_LABEL_COLOR_THEME_ID>` `<SPACER_LABEL_COLOR_PERCENT>` | Theme color + shade for the `% of total` label text | `0` `-0.6` |
| `<SPACER_LABEL_FONT_SIZE>` | Font size for the `% of total` label, DAX literal | `10D` |
| `<FILTER_ID_CATEGORY>` `<FILTER_ID_SPACER>` `<FILTER_ID_VALUE>` | Unique hidden-filter-card ids (any new 20-char hex string) | `a514f8f7fb2ae0353838` |

## File map (apply in order)
1. Append the block in
   [templates/stacked-chart-support-measures.tmdl](templates/stacked-chart-support-measures.tmdl)
   to the end of `<MEASURES_TABLE>`'s existing `.tmdl` file (e.g.
   `definition/tables/_Measures.tmdl`), substituting all tokens.
2. Create a new file from
   [templates/stacked-chart-visual.json](templates/stacked-chart-visual.json) at
   `definition/pages/<PAGE_ID>/visuals/<VISUAL_ID>/visual.json`, substituting all tokens.
   No other page or report file needs to change — visuals are discovered from this folder.

See [examples/datagoblins-total-sales-by-category.md](examples/datagoblins-total-sales-by-category.md)
for a fully substituted instance of both files.

## Validation
- Open the model in TMDL view (or reload it) and confirm the two new measures compile
  with no syntax errors; Desktop assigns each a `lineageTag` on save.
- Reload the report page in Power BI Desktop and confirm the new visual renders as a
  `<VISUAL_TYPE>` sorted descending by `<VALUE_MEASURE>`.
- Confirm each bar reads as a single solid-color segment with no visible seam or second
  color, the real value's label showing on the main segment, and a smaller `% of total`
  label rendered in the headroom above/beside it.
- Confirm no stack-total summary label appears above the bar (totals are hidden), and the
  three hidden filter cards in the filter pane show no error state.
