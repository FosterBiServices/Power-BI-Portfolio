---
name: column-line-combo-bubble-markers
description: Add a column+line combo chart where a line series floats fixed-height "bubble" markers above every column, each carrying a custom dynamic label (e.g. % of total), connected to its bar top by an error-bar stem.
---

# Column and line combo chart with bubble marker labels

## Goal
Add a `lineClusteredColumnComboChart` visual where columns show the real measure
(sorted descending, `OutsideEnd` value label) and a line series on the secondary
(`Y2`) axis contributes two invisible-stroke series that render as floating bubble
markers sitting at a fixed height above the tallest column: one visible marker
carrying no text, one hidden marker carrying an `Above`-positioned custom label
(e.g. percent of total). An error-bar "stem" is drawn from each column's top up to
the marker so the bubble reads as attached to its bar. The secondary axis is hidden
and its range is padded so nothing clips.

## Prerequisites
- An existing PBIP report with a semantic model open in TMDL view (Power BI Desktop
  or Tabular Editor) and a report page already created.
- A base fact/measure table with a working numeric measure to chart
  (`<VALUE_MEASURE>`).
- A dimension table with a surrogate key column and a display column
  (`<CATEGORY_TABLE>`, `<CATEGORY_KEY_COLUMN>`, `<CATEGORY_COLUMN>`).
- The report's `report.json` must register a custom theme file under
  `StaticResources/RegisteredResources/*.json` (see its `resourcePackages` >
  `RegisteredResources` entry). Power BI's default `lineClusteredColumnComboChart`
  marker size renders too small to read as a "bubble" — the theme must set it
  explicitly above 20.

## Tokens

| Token | Description | Example |
|---|---|---|
| `<MEASURES_TABLE>` | Table holding the model's measures | `_Measures` |
| `<VALUE_MEASURE>` | Existing measure charted as columns | `Total Sales` |
| `<CATEGORY_TABLE>` | Dimension table for the category axis | `dimProducts` |
| `<CATEGORY_KEY_COLUMN>` | Surrogate key column on that table | `ProdKey` |
| `<CATEGORY_COLUMN>` | Display column on that table | `ProductName` |
| `<PERCENT_MEASURE_NAME>` | New % of total measure shown in the floating label | `% of Total Sales` |
| `<PERCENT_FORMAT_STRING>` | Format string for the percent measure | `0.00%;-0.00%;0.00%` |
| `<LABEL_MEASURE_NAME>` | New hidden-marker measure carrying the label (shorter shelf) | `Detail Label` |
| `<LABEL_HEIGHT_MULTIPLIER>` | Multiplier on the max value for the label shelf height | `1.6` |
| `<MARKER_MEASURE_NAME>` | New visible-marker measure (taller shelf) | `Detail Position` |
| `<MARKER_HEIGHT_MULTIPLIER>` | Multiplier on the max value for the marker shelf height | `1.7` |
| `<AXIS_MAX_MEASURE_NAME>` | New measure fixing the value-axis end so markers fit | `Y Axis Max Position` |
| `<AXIS_HEADROOM_MULTIPLIER>` | Multiplier on the max value for the axis end | `2.2` |
| `<SUBTITLE_MEASURE_NAME>` | New measure producing the visual's subtitle text | `Total Sales Subtitle` |
| `<SUBTITLE_PREFIX_TEXT>` | Literal text prefixed to the subtitle value | `Total Sales (all products): ` |
| `<SUBTITLE_VALUE_FORMAT>` | `FORMAT()` format string for the subtitle value | `$#,#` |
| `<PAGE_ID>` | Folder name of the target report page | `dab238165c5348774fb4` |
| `<VISUAL_ID>` | New visual's folder name and `name` field (unique id) | `0eeb8cfbd559d778eeb5` |
| `<POS_X>` `<POS_Y>` `<POS_Z>` | Visual canvas position | `333.75` `295` `0` |
| `<POS_HEIGHT>` `<POS_WIDTH>` | Visual size | `460` `970` |
| `<TAB_ORDER>` | Visual tab order on the page | `0` |
| `<TITLE_TEXT>` | Visual title text | `Total Sales` |
| `<BAR_COLOR_THEME_ID>` `<BAR_COLOR_PERCENT>` | Theme color + shade for the error-bar stem | `0` `-0.2` |
| `<MARKER_COLOR_THEME_ID>` `<MARKER_COLOR_PERCENT>` | Theme color + shade for both bubble marker series | `0` `-0.1` |
| `<VALUE_LABEL_FONT_THEME_ID>` `<VALUE_LABEL_FONT_PERCENT>` | Theme color + shade for the column value label font | `2` `0` |
| `<VALUE_LABEL_BACKGROUND_THEME_ID>` `<VALUE_LABEL_BACKGROUND_PERCENT>` | Theme color + shade for the column value label pill background | `0` `0` |
| `<LABEL_DISPLAY_UNITS>` | Display units, DAX literal | `1D` |
| `<LABEL_PRECISION>` | Bubble label decimal precision, DAX literal | `1L` |
| `<LABEL_FONT_SIZE>` | Bubble label font size, DAX literal | `9D` |
| `<MARKER_SIZE>` | Theme-level bubble marker diameter; must be > 20 or bubbles read as dots | `30` |

## File map (apply in order)
1. Append the block in
   [templates/combo-chart-support-measures.tmdl](templates/combo-chart-support-measures.tmdl)
   to the end of `<MEASURES_TABLE>`'s existing `.tmdl` file (e.g.
   `definition/tables/_Measures.tmdl`), substituting all tokens.
2. Create a new file from
   [templates/combo-chart-visual.json](templates/combo-chart-visual.json) at
   `definition/pages/<PAGE_ID>/visuals/<VISUAL_ID>/visual.json`, substituting all
   tokens.
3. Merge the block in
   [templates/combo-chart-theme-marker-style.json](templates/combo-chart-theme-marker-style.json),
   substituting `<MARKER_SIZE>`, into the `visualStyles` object of the report's
   registered custom theme file. Add `lineClusteredColumnComboChart` as a new sibling
   key next to the existing `*`/`page` keys; if that key already exists, merge only
   the `lineStyles` array into it rather than overwriting other properties. No other
   page or report file needs to change.

See [examples/datagoblins-total-sales-by-product.md](examples/datagoblins-total-sales-by-product.md)
for a fully substituted instance of both files.

## Validation
- Open the model in TMDL view (or reload it) and confirm the five new measures
  compile with no syntax errors; Desktop assigns each a `lineageTag` on save.
- Reload the report page in Power BI Desktop and confirm the new visual renders as a
  `lineClusteredColumnComboChart` sorted descending by `<VALUE_MEASURE>`.
- Confirm each column shows its own `OutsideEnd` value label, a thin stem rises from
  the column top, and a bubble marker floats at a fixed height with a percent label
  above it — with no visible line stroke connecting bubbles across categories.
- Confirm the value axis is hidden and no marker or label is clipped at the top of
  the plot area.
- Confirm the bubble markers render as visible circles (per `<MARKER_SIZE>`), not
  small dots, and that no other visual's marker-based chart type was affected by the
  theme edit (the key is scoped to `lineClusteredColumnComboChart` only).
