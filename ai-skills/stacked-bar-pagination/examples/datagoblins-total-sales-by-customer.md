# Worked example: Total Sales by Customer, paginated (datagoblins report)

Source: diff of `pbip/start/datagoblins_start.*` -> `pbip/end/datagoblins_end.*`. The end
state adds a paginated stacked bar chart of customers, ranked by `Total Sales`, 5 per page,
to page `dab238165c5348774fb4`.

## Token substitutions used

| Token | Value |
|---|---|
| `<MEASURES_TABLE>` / `<VALUE_MEASURE>` | `_Measures` / `Total Sales` |
| `<FACT_TABLE>` / `<FACT_KEY_COLUMN>` | `factOrders` / `CustomerKey` |
| `<RANK_TABLE>` / `<RANK_COLUMN>` / `<RANK_KEY_COLUMN>` / `<RANK_RELATIONSHIP_KEY_COLUMN>` | `dimCustomers` / `CustomerName` / `CustomerKey` / `CustKey` |
| `<RELATIONSHIP_ID>` | `9be4ca76-6075-7b88-41b6-e9cf6ae0fec7` |
| `<ALPHA_RANK_MEASURE>` / `<RANK_MEASURE>` / `<RANK_LABEL_MEASURE>` | `Alphabetical Rank` / `Customer Rank` / `Customer Rank #` |
| `<SPACER_MEASURE>` | `Stacked Chart Spacing by Customer` |
| `<SUBTITLE_MEASURE>` | `Total Sales by Customer Subtitle` |
| `<AXIS_MAX_MEASURE>` / `<AXIS_MAX_HEADROOM>` | `Pagination Max Bar Width` / `1.15` |
| `<AXIS_MIN_MEASURE>` / `<AXIS_MIN_HEADROOM>` | `Pagination Min Bar Width` / `-1.1` |
| `<SUBTITLE_SHOWN_LABEL>` / `<SUBTITLE_ALL_LABEL>` | `Total Sales (displayed customers): ` / `Total Sales (all customers): ` |
| `<ITEMS_TABLE>` / `<ITEMS_COLUMN>` / `<ITEMS_VALUE_MEASURE>` / `<ITEM_FILTER_MEASURE>` / `<ITEMS_DEFAULT>` / `<ITEMS_SERIES_MAX>` | `# of items` / `# of items` / `# of items Value` / `Item Filter` / `5` / `20` |
| `<PAGES_TABLE>` / `<PAGES_COLUMN>` / `<PAGES_VALUE_MEASURE>` / `<PAGE_FILTER_MEASURE>` / `<PAGES_DEFAULT>` / `<PAGES_SERIES_MAX>` / `<PAGES_DEFAULT_SELECTED>` | `# of Pages` / `# of Pages` / `# of Pages Value` / `Page Filter` / `10` / `20` / `1` |
| `<PAGE_ID>` | `dab238165c5348774fb4` |
| `<PAGINATION_GROUP_ID>` / `<PAGINATION_GROUP_TITLE>` | `996b2bb7710dff6a6136` / `Pagination` |
| `<ITEMS_GROUP_ID>` / `<ITEMS_GROUP_TITLE>` | `ecb5bdc6d80ef0dc906e` / `Items` |
| `<CHART_VISUAL_ID>` / `<PAGES_SLICER_ID>` / `<ITEMS_SLICER_ID>` / `<ITEMS_LABEL_ID>` | `8aaab693b25d07f24bb6` / `79bf90b41b53dc873f27` / `e0e6fbb4b70be6775325` / `592225dae72130b04349` |
| `<TITLE_TEXT>` / `<TITLE_FONT_COLOR_HEX>` | `Total Sales by Customer` / `#242424` |
| `<RANK_BADGE_FILL_HEX>` | `#ffffff` |
| `<RANK_LABEL_COLOR_THEME_ID>` / `<RANK_LABEL_COLOR_PERCENT>` | `0` / `-0.5` |
| `<VALUE_LABEL_FONT_COLOR_HEX>` | `#ffffff` |
| `<VALUE_BADGE_COLOR_THEME_ID>` / `<VALUE_BADGE_COLOR_PERCENT>` / `<VALUE_BADGE_FONT_SIZE>` | `3` / `0` / `8D` |
| `<LABEL_DISPLAY_UNITS>` / `<LABEL_PRECISION>` | `1D` / `0L` |
| `<ITEMS_LABEL_TEXT_LINE1>` / `<ITEMS_LABEL_TEXT_LINE2>` | `Items per` / `page:` |
| `<ITEMS_LABEL_FONT_SIZE>` / `<ITEMS_LABEL_SPACER_COLOR_HEX>` | `8pt` / `#e6e6e6` |
| `<LABEL_BACKGROUND_COLOR_THEME_ID>` / `<LABEL_BACKGROUND_COLOR_PERCENT>` | `0` / `-0.1` |
| `<ITEMS_SLICER_TITLE>` / `<PAGES_SLICER_TITLE>` | `# of items` / `Pages` |
| `<ITEMS_SLICER_TEXT_SIZE>` / `<PAGES_SLICER_TEXT_SIZE>` | `8D` / `8D` |
| `<ITEMS_SLICER_SLIDER_COLOR_THEME_ID>` | `4` |
| `<ITEMS_SLICER_INPUT_FONT_COLOR_THEME_ID>` | `3` |
| `<ITEMS_SLICER_INPUT_BG_COLOR_THEME_ID>` / `<ITEMS_SLICER_INPUT_BG_COLOR_PERCENT>` | `0` / `-0.1` |
| `<FILTER_ID_ITEMS_COLUMN>` | `cd83fec03a2eab4e3ab2` |
| `<FILTER_ID_PAGE_FILTER>` | `ea14ac157313aa0df13b` |
| `<FILTER_ID_CATEGORY>` / `<FILTER_ID_VALUE>` / `<FILTER_ID_SPACER>` / `<FILTER_ID_ITEM_FILTER>` | `97f09df944ae85d87948` / `bb035f172f073d4aa633` / `233e7752301cba72a907` / `8b4b99d485543c4d5148` |
| `<PAGINATION_GROUP_POS_*>` (`GROUP_POS_X/Y/Z/HEIGHT/WIDTH`, `GROUP_TAB_ORDER`) | `481.27272727272725` / `232` / `2501` / `484` / `677.26887142221562` / `2000` |
| `<ITEMS_GROUP_POS_*>` (`ITEMS_GROUP_POS_X/Y/Z/HEIGHT/WIDTH`, `ITEMS_GROUP_TAB_ORDER`) | `464.56087794750113` / `0` / `2000` / `41.25` / `212.70799347471453` / `2000` |
| `<CHART_POS_*>` (`CHART_POS_X/Y/Z/HEIGHT/WIDTH`, `CHART_TAB_ORDER`) | `0` / `26` / `2500` / `416` / `656` / `0` |
| `<PAGES_SLICER_POS_*>` | `482.74061990212078` / `673.01794453507353` / `9000` / `56.378466557911914` / `650.11419249592177` / `9000` |
| `<ITEMS_SLICER_POS_*>` | `106.45799347471453` / `0` / `0` / `41.25` / `106.25` / `0` |
| `<LABEL_POS_*>` (textbox) | `0` / `5.25` / `1000` / `22` / `99` / `1000` |

## 1. `relationships.tmdl` (new file — none existed before)

	relationship 9be4ca76-6075-7b88-41b6-e9cf6ae0fec7
		fromColumn: factOrders.CustomerKey
		toColumn: dimCustomers.CustKey

## 2. Append to `definition/tables/_Measures.tmdl`

	measure 'Alphabetical Rank' = ```

			var _current = SELECTEDVALUE( 'dimCustomers'[CustomerName] )
			var __Result =
			    COUNTROWS(
			        FILTER(
			            ALL ( 'dimCustomers'[CustomerName] )
			            , 'dimCustomers'[CustomerName] <= _current
			        )
			    )
			RETURN
			    __Result
			```
		formatString: 0

	measure 'Customer Rank' = ```

			var __Result = [Total Sales]
			RETURN
			IF ( ISBLANK( __Result ), BLANK(),
			  RANKX( ALL ( 'dimCustomers'[CustomerKey], 'dimCustomers'[CustomerName]), [Total Sales] ) ) - DIVIDE( [Alphabetical Rank], 1000000)
			```
		formatString: 0

	measure 'Customer Rank #' = ```

			var __Result = [Total Sales]
			RETURN
			IF ( ISBLANK( __Result ), BLANK(),
			"#" & FORMAT(
			  (RANKX( ALL ( 'dimCustomers'[CustomerKey], 'dimCustomers'[CustomerName]), [Total Sales] ) )
			    - DIVIDE( [Alphabetical Rank], 1000000),"#,#0"))
			```

	measure 'Stacked Chart Spacing by Customer' = ```

			var __Spacing =
			CALCULATE ( MINX ( 'dimCustomers', [Total Sales] ), ALLSELECTED ( 'dimCustomers'[CustomerKey], 'dimCustomers'[CustomerName] ) )
			RETURN
			IF ( ISBLANK([Total Sales]), BLANK(),
			__Spacing * -1
			)
			```
		annotation PBI_FormatHint = {"isGeneralNumber":true}

	measure 'Total Sales by Customer Subtitle' = ```

			var _value = CALCULATE([Total Sales], REMOVEFILTERS('dimCustomers'[CustomerKey], 'dimCustomers'[CustomerName]))
			var _Header = "Total Sales (all customers): "
			var _shown = [Total Sales]
			RETURN
			"Total Sales (displayed customers): " & FORMAT(_shown,"$#,#") & " | " & _Header & FORMAT(_value,"$#,#")
			```

	measure 'Pagination Max Bar Width' = ```

			CALCULATE ( MAXX ( 'dimCustomers', [Total Sales] ), REMOVEFILTERS ( 'dimCustomers' ) ) * 1.15
			```
		formatString: 0

	measure 'Pagination Min Bar Width' = ```

			CALCULATE ( MINX ( 'dimCustomers', [Total Sales] ), REMOVEFILTERS ( 'dimCustomers' ) ) * -1.1
			```
		formatString: 0

Power BI Desktop assigns lineage tags to all new objects the next time the model is saved
from TMDL view, so none is hand-authored here.

**Why `Stacked Chart Spacing by Customer` uses `MINX * -1` and not the original
`MAXX * .10`:** the first version made the spacer a small *positive* segment (10% of the
page's own tallest bar) stacked before the real value — a proportional badge zone. It
looked fine on page 1 but caused the actual bug this example now avoids: nothing kept the
*value axis itself* fixed across pages, so each page auto-scaled to its own max and every
page's tallest bar stretched edge-to-edge regardless of its real magnitude. The fix has two
parts: (1) two new measures below give the chart a fixed, dataset-wide value-axis range via
`REMOVEFILTERS`, and (2) the spacer became a small *negative*, page-local-width segment
(`-1 * MINX`, no ratio) that sits to the left of a zero baseline purely to host the "#N"
label — its magnitude no longer needs to track the axis scale at all, since the real value
segment (right of zero) is what the fixed axis now governs.

## 3. New file `definition/tables/# of items.tmdl`

	table '# of items'

		measure '# of items Value' = SELECTEDVALUE('# of items'[# of items], 5)
			formatString: 0

		measure 'Item Filter' = ```

				var __Result = [Total Sales]
				var __Pages = [# of Pages Value]
				var __Items = [# of items Value]
				VAR __ItemRank = [Customer Rank]
				VAR __FilteredItems = FILTER( ALLSELECTED( 'dimCustomers'[CustomerName] ), __ItemRank > (__Pages - 1) * __Items && __ItemRank <= (__Pages) * __Items )
				VAR __ItemsShow = IF ( ISBLANK(__Result), 0, IF ( SELECTEDVALUE( 'dimCustomers'[CustomerName] ) IN __FilteredItems, 1, 0 ) )
				RETURN
				__ItemsShow
				```
			formatString: 0

		column '# of items'
			formatString: 0
			summarizeBy: none
			sourceColumn: [Value]

			annotation SummarizationSetBy = User

		partition '# of items' = calculated
			mode: import
			source = GENERATESERIES(1, 20, 1)

## 4. New file `definition/tables/# of Pages.tmdl`

	table '# of Pages'

		measure '# of Pages Value' = SELECTEDVALUE('# of Pages'[# of Pages], 10)
			formatString: 0

		measure 'Page Filter' = ```

				VAR __FilteredItems = FILTER( ALLSELECTED( 'dimCustomers'[CustomerName] ), [Total Sales] > 0 )
				var __ItemTotal =
				    CALCULATE(
				        DISTINCTCOUNT( 'dimCustomers'[CustomerName] )
				        , __FilteredItems
				    )
				var __ShowItems = [# of items Value]
				var __Pages = ROUNDUP ( DIVIDE( __ItemTotal, __ShowItems ) , 0)
				var __PageFilter = IF ( SELECTEDVALUE( '# of Pages'[# of Pages] ) <= __Pages, 1, 0 )
				RETURN
				__PageFilter
				```
			formatString: 0

		column '# of Pages'
			formatString: 0
			summarizeBy: none
			sourceColumn: [Value]

			annotation SummarizationSetBy = User

		partition '# of Pages' = calculated
			mode: import
			source = GENERATESERIES(1, 20, 1)

## 5. `model.tmdl` — add to the `ref table` list

	ref table '# of items'
	ref table '# of Pages'

## 6-11. New visual.json files under `definition/pages/dab238165c5348774fb4/visuals/`

Six sibling files, each substituting the tokens above into the matching template:

- `996b2bb7710dff6a6136/visual.json` — [pagination-group.json](../templates/pagination-group.json), the outer "Pagination" group (top-level, no `parentGroupName`).
- `ecb5bdc6d80ef0dc906e/visual.json` — [items-group.json](../templates/items-group.json), the "Items" group, `parentGroupName: 996b2bb7710dff6a6136`.
- `8aaab693b25d07f24bb6/visual.json` — [paginated-stacked-bar-visual.json](../templates/paginated-stacked-bar-visual.json), the chart, `parentGroupName: 996b2bb7710dff6a6136`. Its `valueAxis` object's `start`/`end` are bound to `Pagination Min Bar Width` / `Pagination Max Bar Width` (see "Axis scaling" in the skill for why `REMOVEFILTERS`, not `ALLSELECTED`, is required here).
- `79bf90b41b53dc873f27/visual.json` — [page-number-slicer-visual.json](../templates/page-number-slicer-visual.json), top-level, no `parentGroupName` (verified against source: this slicer sits outside the Pagination group despite being part of the pattern).
- `e0e6fbb4b70be6775325/visual.json` — [items-per-page-slicer-visual.json](../templates/items-per-page-slicer-visual.json), `parentGroupName: ecb5bdc6d80ef0dc906e`.
- `592225dae72130b04349/visual.json` — [items-per-page-label-textbox.json](../templates/items-per-page-label-textbox.json), `parentGroupName: ecb5bdc6d80ef0dc906e`.

No page.json or pages.json change is needed — visuals are discovered from their folders.

## Result

A bar chart of `dimCustomers` ranked descending by `Total Sales`, showing only 5 customers
at a time. Each bar is two stacked segments straddling a zero baseline: a small white,
negative `Stacked Chart Spacing by Customer` "badge" segment carrying the `Customer Rank #`
label (`#1`, `#2`, ...), and the real positive `Total Sales` segment carrying its own value
as a white-on-color pill pinned to the end of the bar. The `Item Filter` measure (home table
`# of items`) is applied as a hidden row-level filter on the chart, comparing each
customer's `Customer Rank` against the current `# of Pages Value` / `# of items Value`
window; the `Page Filter` measure (home table `# of Pages`) is applied as a hidden filter on
the page slicer itself so only pages that actually contain data are selectable. Changing the
"# of items" numeric slicer changes the page size and therefore the page count; changing the
"Pages" list slicer changes which window of ranked customers is shown.

The chart's value axis is hidden but its `start`/`end` are bound to `Pagination Min Bar
Width` / `Pagination Max Bar Width`, both computed with `REMOVEFILTERS('dimCustomers')`
against the whole (unfiltered) customer table. This keeps the axis range — and therefore
bar length — identical no matter which page is showing, so a page 4 bar that's genuinely
smaller than a page 1 bar renders visibly shorter instead of both auto-stretching to fill
the chart.

## Not part of this pattern

The source `end/` folder also adds a `dimDate` calculated table, a `dimProducts`→`dimCustomers`/`dimProducts`
rename and `summarizeBy: none` cleanup on several columns, and report-level session settings
(`outspacePane`, `queryLimitOption`, `customMemoryLimit`, `customTimeoutLimit`). Those came
from the same authoring session but are unrelated to the pagination technique and are
intentionally excluded here. The `factOrders`→`dimProducts` relationship and the
`Stacked Chart Spacing` / `% of Total Sales` measure pair used by a separate clustered/stacked
bar visual on the same page belong to the `clustered-chart-labels-above-bar` and
`stacked-bar-percent-of-total` skills, not this one.

The raw chart `visual.json` also carries several `dataPoint`/`labels` selector entries copied
from that other visual (referencing a nonexistent `__Measures` table and a `Stacked Chart
Spacing`/`SubCategory Rank #` measure pair that isn't part of this model). Power BI ignores
selectors that don't match a field in the query, so they're harmless but inert; the template
omits them and keeps only the four selectors that actually drive this pattern's badges.
