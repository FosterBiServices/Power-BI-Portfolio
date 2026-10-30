---
name: stacked-bar-pagination
description: Add a "top N per page" stacked bar chart with Next/page-number pagination, using rank measures, two disconnected parameter tables (# of items, # of Pages), a negative rank-badge spacer segment, and a fixed (REMOVEFILTERS-based) value-axis scale instead of a scrollable/paged native visual.
---

# Stacked bar chart with pagination

## Goal
Add a stacked bar chart to a PBIP report page that shows only a fixed-size "page" of
ranked categories at a time (e.g. top 5 customers on page 1, next 5 on page 2), with a
numeric slicer choosing items-per-page and a list slicer choosing the page number.
Ranking and paging are computed entirely in DAX (RANKX plus two disconnected
GENERATESERIES parameter tables) and applied as row-level visual filters — no native
Power BI paging feature is used. Each bar has two stacked segments straddling a zero
baseline: a small negative "spacer" segment (a fixed fraction of the axis max, the same
width on every bar regardless of that row's own value) that carries the "#N" rank badge,
and the real positive value segment that carries a colored value badge. The value axis's
min/max are themselves bound to two measures (`REMOVEFILTERS`-based, not `ALLSELECTED`)
so bar length stays comparable across pages instead of auto-rescaling to whatever the
current page's tallest bar is — see "Axis scaling" below for why this matters.

## Prerequisites
- An existing PBIP report with the semantic model open in TMDL view and a report page
  already created.
- A working numeric measure to rank and chart (`<VALUE_MEASURE>`).
- A dimension table holding the entities to paginate, with a display column and a key
  column (`<RANK_TABLE>`, `<RANK_COLUMN>`, `<RANK_KEY_COLUMN>`), related to the fact table
  the value measure sums from. If that relationship doesn't exist yet, step 1 adds it.

## Tokens
| Token | Description |
|---|---|
| `<MEASURES_TABLE>` `<VALUE_MEASURE>` | Existing measures table and the measure being ranked/charted |
| `<FACT_TABLE>` `<FACT_KEY_COLUMN>` | Fact table and its FK column, for the relationship |
| `<RANK_TABLE>` `<RANK_COLUMN>` `<RANK_KEY_COLUMN>` `<RANK_RELATIONSHIP_KEY_COLUMN>` | Dimension paginated by; display column, RANKX/ALL key column, relationship PK column |
| `<RELATIONSHIP_ID>` | New relationship GUID (skip step 1 if the relationship already exists) |
| `<ALPHA_RANK_MEASURE>` `<RANK_MEASURE>` `<RANK_LABEL_MEASURE>` | Tie-break rank, numeric rank, "#N"-formatted rank label |
| `<SPACER_MEASURE>` `<SPACER_FRACTION>` | Negative rank-badge spacer segment: `-1 * <SPACER_FRACTION> * [<AXIS_MAX_MEASURE>]` — a constant width on every bar (e.g. `0.15`, i.e. 15% of the axis max), sized for the "#N" text rather than tied to any row's own value |
| `<SUBTITLE_MEASURE>` `<SUBTITLE_SHOWN_LABEL>` `<SUBTITLE_ALL_LABEL>` | Chart subtitle measure and its two literal text prefixes |
| `<AXIS_MAX_MEASURE>` `<AXIS_MAX_HEADROOM>` | Value-axis max measure (`REMOVEFILTERS`-based global `MAXX` times this positive multiplier, e.g. `1.15`) |
| `<AXIS_MIN_MEASURE>` `<AXIS_MIN_FRACTION>` | Value-axis min measure: `-1 * <AXIS_MIN_FRACTION> * [<AXIS_MAX_MEASURE>]` — must be a larger fraction than `<SPACER_FRACTION>` (e.g. `0.2` vs `0.15`) so the badge segment never clips against the axis edge |
| `<ITEMS_TABLE>` `<ITEMS_COLUMN>` `<ITEMS_VALUE_MEASURE>` `<ITEM_FILTER_MEASURE>` `<ITEMS_DEFAULT>` `<ITEMS_SERIES_MAX>` | Items-per-page parameter table |
| `<PAGES_TABLE>` `<PAGES_COLUMN>` `<PAGES_VALUE_MEASURE>` `<PAGE_FILTER_MEASURE>` `<PAGES_DEFAULT>` `<PAGES_SERIES_MAX>` `<PAGES_DEFAULT_SELECTED>` | Page-number parameter table and its default selected page |
| `<PAGE_ID>` | Target report page folder |
| `<PAGINATION_GROUP_ID>` `<PAGINATION_GROUP_TITLE>` `<ITEMS_GROUP_ID>` `<ITEMS_GROUP_TITLE>` | Visual-group container ids/titles — chart nests in Pagination; items slicer + label nest in Items, itself inside Pagination; the page-number slicer stays top-level (ungrouped) |
| `<CHART_VISUAL_ID>` `<PAGES_SLICER_ID>` `<ITEMS_SLICER_ID>` `<ITEMS_LABEL_ID>` | New visual ids |
| `*_POS_X/Y/Z/HEIGHT/WIDTH` `*_TAB_ORDER` | Per-visual canvas geometry, one set per template file — concrete values are in the example |
| `<TITLE_TEXT>` `<TITLE_FONT_COLOR_HEX>` | Chart title text and font color |
| `<RANK_BADGE_FILL_HEX>` `<RANK_LABEL_COLOR_THEME_ID>` `<RANK_LABEL_COLOR_PERCENT>` | Rank-badge segment fill and its "#N" label color |
| `<VALUE_LABEL_FONT_COLOR_HEX>` `<VALUE_BADGE_COLOR_THEME_ID>` `<VALUE_BADGE_COLOR_PERCENT>` `<VALUE_BADGE_FONT_SIZE>` | Value badge label style on the real segment |
| `<LABEL_DISPLAY_UNITS>` `<LABEL_PRECISION>` | Value label formatting |
| `<ITEMS_LABEL_TEXT_LINE1>` `<ITEMS_LABEL_TEXT_LINE2>` `<ITEMS_LABEL_FONT_SIZE>` `<ITEMS_LABEL_SPACER_COLOR_HEX>` `<LABEL_BACKGROUND_COLOR_THEME_ID>` `<LABEL_BACKGROUND_COLOR_PERCENT>` | "Items per page:" caption textbox |
| `<ITEMS_SLICER_TITLE>` `<PAGES_SLICER_TITLE>` `<ITEMS_SLICER_TEXT_SIZE>` `<PAGES_SLICER_TEXT_SIZE>` `<ITEMS_SLICER_SLIDER_COLOR_THEME_ID>` `<ITEMS_SLICER_INPUT_FONT_COLOR_THEME_ID>` `<ITEMS_SLICER_INPUT_BG_COLOR_THEME_ID>` `<ITEMS_SLICER_INPUT_BG_COLOR_PERCENT>` | Slicer titles and styling |
| `<FILTER_ID_*>` | Unique hidden-filter-card ids (any new 20-char hex string), one per filter listed in each template — the page-number slicer has exactly one (`<FILTER_ID_PAGE_FILTER>`) |

## File map (apply in order)
1. If `<RANK_TABLE>` isn't already related to `<FACT_TABLE>`, append [templates/fact-to-rank-relationship.tmdl](templates/fact-to-rank-relationship.tmdl) to `relationships.tmdl`.
2. Append [templates/rank-and-pagination-measures.tmdl](templates/rank-and-pagination-measures.tmdl) to `<MEASURES_TABLE>`'s `.tmdl` file.
3. Create `definition/tables/<ITEMS_TABLE>.tmdl` from [templates/items-per-page-table.tmdl](templates/items-per-page-table.tmdl).
4. Create `definition/tables/<PAGES_TABLE>.tmdl` from [templates/page-number-table.tmdl](templates/page-number-table.tmdl).
5. Add `ref table '<ITEMS_TABLE>'` and `ref table '<PAGES_TABLE>'` to `model.tmdl`'s ref table list.
6. Create `definition/pages/<PAGE_ID>/visuals/<PAGINATION_GROUP_ID>/visual.json` from [templates/pagination-group.json](templates/pagination-group.json).
7. Create `definition/pages/<PAGE_ID>/visuals/<ITEMS_GROUP_ID>/visual.json` from [templates/items-group.json](templates/items-group.json).
8. Create `definition/pages/<PAGE_ID>/visuals/<CHART_VISUAL_ID>/visual.json` from [templates/paginated-stacked-bar-visual.json](templates/paginated-stacked-bar-visual.json).
9. Create `definition/pages/<PAGE_ID>/visuals/<PAGES_SLICER_ID>/visual.json` from [templates/page-number-slicer-visual.json](templates/page-number-slicer-visual.json).
10. Create `definition/pages/<PAGE_ID>/visuals/<ITEMS_SLICER_ID>/visual.json` from [templates/items-per-page-slicer-visual.json](templates/items-per-page-slicer-visual.json).
11. Create `definition/pages/<PAGE_ID>/visuals/<ITEMS_LABEL_ID>/visual.json` from [templates/items-per-page-label-textbox.json](templates/items-per-page-label-textbox.json).

See [examples/datagoblins-total-sales-by-customer.md](examples/datagoblins-total-sales-by-customer.md)
for a fully substituted instance of every file.

## Axis scaling — use `REMOVEFILTERS`, not `ALLSELECTED`, for the axis min/max measures
`<AXIS_MAX_MEASURE>` / `<AXIS_MIN_MEASURE>` are bound directly to the chart's value axis
`start`/`end` properties (a scalar "format by field value" binding evaluated once for the
whole visual), not projected as a data field. `ALLSELECTED` on the rank table's key/display
columns does **not** reliably escape the pagination row filter (the `Item Filter` advanced
filter from `<ITEM_FILTER_MEASURE>`) in that whole-visual scalar context — it still sees
only the current page's rows, so the "max" ends up being the current page's own max every
time. The symptom is bars that always stretch to fill the visual regardless of which page
is shown, because the axis rescales to match whatever's currently visible instead of
staying fixed to the true dataset-wide range.

`REMOVEFILTERS('<RANK_TABLE>')` sidesteps this entirely — it clears every filter on the
table regardless of which query level applied it, giving a genuinely page-independent
constant. Verify this with a DAX query (via the modeling MCP's `dax_query_operations`, or
DAX query view in Desktop) before trusting the axis to render correctly — wrap a
`SUMMARIZECOLUMNS` in `CALCULATETABLE` with the `# of Pages`/`# of items` selections and the
`FILTER(ALLSELECTED(...), [<ITEM_FILTER_MEASURE>] = 1)` filter applied, the same way the
chart's own filterConfig applies it, and confirm the axis measure returns the identical
value for at least two different simulated pages.

### Spacer sizing — a fixed fraction of the axis max, not `MINX` of the data
An earlier version of this pattern sized `<SPACER_MEASURE>` off `MINX` of the rank
table's value (scoped with `ALLSELECTED`), on the theory that the badge only needed to be
"small." In practice this made the badge's width depend on whatever the smallest value on
the current page happened to be — on a page whose smallest bar was tiny, the spacer shrank
along with it and the "#N" text had almost no room, and (per the same DAX-query
verification used for the axis measures) `ALLSELECTED` doesn't reliably escape the
pagination filter here either, so the width was also inconsistent page to page.

The fix is to size the spacer off `<AXIS_MAX_MEASURE>` instead — a fixed, dataset-wide
constant — rather than off any row's own value:
`<SPACER_MEASURE> = -1 * <SPACER_FRACTION> * [<AXIS_MAX_MEASURE>]`. Every bar on every
page then gets the exact same badge width, sized for the "#N" text rather than for
whatever value that row happens to hold. Pick `<SPACER_FRACTION>` and `<AXIS_MIN_FRACTION>`
together (e.g. `0.15` and `0.2`) so `<AXIS_MIN_FRACTION>` is comfortably larger — that gap
is what guarantees the badge segment never clips against the axis edge, on any page, for
any dimension this pattern is applied to.

## Validation
- Open the model in TMDL view (or reload it) and confirm all new measures compile with no
  syntax errors; Desktop assigns lineage tags to new objects on save.
- Reload the report page and confirm the chart shows only `<ITEMS_DEFAULT>` bars, ranked
  descending by `<VALUE_MEASURE>`, each with a rank badge segment and a colored value
  badge.
- Change the items-per-page slicer value and confirm the bar count and page count both
  update; change the page slicer and confirm a different slice of ranked rows appears.
- Confirm the page slicer only offers selectable pages up to the computed max (no blank
  trailing pages), and that none of the six visuals show a filter/field error.
- In the Format pane, confirm the chart's X-axis Values Minimum/Maximum show the
  conditional-formatting (fx) binding to `<AXIS_MIN_MEASURE>` / `<AXIS_MAX_MEASURE>`, not
  "Auto".
- Navigate to the last page and confirm bar lengths are visibly shorter than page 1's (a
  lower-ranked page's tallest bar should not stretch edge-to-edge) — this is the actual
  proof the axis fix works, since a bound-but-still-page-local axis measure looks identical
  to "Auto" in the Format pane. See "Axis scaling" above if it doesn't hold.
- Confirm the "#N" rank badge is legibly sized (not clipped or overlapping the value
  segment) on both the page with the largest values and the page with the smallest —
  since the spacer is now a fixed fraction of the axis max, it should look identical on
  every page. If it clips, increase the gap between `<SPACER_FRACTION>` and
  `<AXIS_MIN_FRACTION>`.
