---
name: clustered-chart-labels-above-bar
description: Add a clustered column/bar chart whose data labels sit above (outside) the bar, using a zero-value spacer measure to carry a custom category+percent label independent of the real value's own highlighted label.
---

# Clustered chart with labels above the bar

## Goal
Add a clustered column or bar chart to an existing PBIP report page where each bar shows
two labels: a highlighted "pill" label with the real value on the bar itself, and a
second custom label (category name + % of total) rendered `OutsideEnd`, appearing to
float above/outside the bar. The trick: plot a second, zero/blank-valued "spacer" measure
alongside the real measure and attach the custom dynamic label to the spacer series.

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
| `<CATEGORY_TABLE>` | Dimension table for the category axis | `dimProdusts` |
| `<CATEGORY_COLUMN>` | Category column on that table | `ProductName` |
| `<SPACER_MEASURE_NAME>` | New zero/blank spacer measure name | `Clustered Chart Spacing` |
| `<SPACER_FORMAT_STRING>` | Format string for the spacer measure | `0` |
| `<CATEGORY_LABEL_MEASURE_NAME>` | New `SELECTEDVALUE` measure carrying the label's category text | `Selected Product` |
| `<PERCENT_MEASURE_NAME>` | New % of total measure for the label's detail line | `% of Total Sales` |
| `<PERCENT_FORMAT_STRING>` | Format string for the percent measure | `0.0%` |
| `<SUBTITLE_MEASURE_NAME>` | New measure producing the visual's subtitle text | `Total Sales Subtitle` |
| `<SUBTITLE_VALUE_MEASURE>` | Existing measure whose value appears in the subtitle | `Total Sales` |
| `<SUBTITLE_PREFIX_TEXT>` | Literal text prefixed to the subtitle value | `Total Sales: ` |
| `<SUBTITLE_VALUE_FORMAT>` | `FORMAT()` format string for the subtitle value | `$#,#` |
| `<PAGE_ID>` | Folder name of the target report page | `dab238165c5348774fb4` |
| `<VISUAL_ID>` | New visual's folder name and `name` field (unique id) | `3467fd7dcb8644c49092` |
| `<VISUAL_TYPE>` | `clusteredColumnChart` or `clusteredBarChart` | `clusteredBarChart` |
| `<POS_X>` `<POS_Y>` `<POS_Z>` | Visual canvas position | `646.25` `212.5` `0` |
| `<POS_HEIGHT>` `<POS_WIDTH>` | Visual size | `473.75` `651.25` |
| `<TAB_ORDER>` | Visual tab order on the page | `0` |
| `<TITLE_TEXT>` | Visual title text | `Total Sales` |
| `<TITLE_FONT_COLOR_THEME_ID>` | Theme color index for the title font | `3` |
| `<CLUSTERED_GAP_SIZE>` | Gap size between clustered bars, DAX literal | `25D` |
| `<CATEGORY_INNER_PADDING>` | Category axis inner padding, DAX literal | `25L` |
| `<LABEL_DISPLAY_UNITS>` | Display units for both label series, DAX literal | `1D` |
| `<LABEL_COLOR_THEME_ID>` `<LABEL_COLOR_PERCENT>` | Theme color + shade for the value label's font | `0` `-0.5` |
| `<LABEL_BACKGROUND_THEME_ID>` `<LABEL_BACKGROUND_PERCENT>` | Theme color + shade for the value label's pill background | `0` `0` |
| `<LABEL_BACKGROUND_TRANSPARENCY>` | Value label background transparency, DAX literal | `0D` |
| `<FILTER_ID_CATEGORY>` `<FILTER_ID_SPACER>` `<FILTER_ID_VALUE>` | Unique hidden-filter-card ids (any new 20-char hex string) | `18550cd9f3b8bdf1cbc8` |

## File map (apply in order)
1. Append the block in
   [templates/clustered-chart-support-measures.tmdl](templates/clustered-chart-support-measures.tmdl)
   to the end of `<MEASURES_TABLE>`'s existing `.tmdl` file (e.g.
   `definition/tables/_Measures.tmdl`), substituting all tokens.
2. Create a new file from
   [templates/clustered-chart-visual.json](templates/clustered-chart-visual.json) at
   `definition/pages/<PAGE_ID>/visuals/<VISUAL_ID>/visual.json`, substituting all tokens.
   No other page or report file needs to change — visuals are discovered from this folder.

See [examples/datagoblins-total-sales-by-product.md](examples/datagoblins-total-sales-by-product.md)
for a fully substituted instance of both files.

## Validation
- Open the model in TMDL view (or reload it) and confirm the four new measures compile
  with no syntax errors; Desktop assigns each a `lineageTag` on save.
- Reload the report page in Power BI Desktop and confirm the new visual renders as a
  `<VISUAL_TYPE>` sorted descending by `<VALUE_MEASURE>`.
- Confirm each bar shows a highlighted value label on the bar itself, and a second
  category+percent label positioned above/outside the bar with no visible second series.
- Confirm the visual's title and subtitle render, and that the three hidden filter cards
  in the filter pane show no error state.
