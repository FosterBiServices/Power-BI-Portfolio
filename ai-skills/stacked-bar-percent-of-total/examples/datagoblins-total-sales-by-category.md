# Worked example: Total Sales by Product Category (datagoblins report)

Source: diff of `pbip/start/datagoblins_start.*` -> `pbip/end/datagoblins_end.*`. The end
state adds one new stacked bar chart visual to page `dab238165c5348774fb4` and two
supporting measures to the `_Measures` table.

## Token substitutions used

| Token | Value |
|---|---|
| `<MEASURES_TABLE>` | `_Measures` |
| `<VALUE_MEASURE>` | `Total Sales` |
| `<CATEGORY_TABLE>` | `dimProducts` |
| `<CATEGORY_COLUMN>` | `ProductCategory` |
| `<SPACER_MEASURE_NAME>` | `Stacked Chart Spacing` |
| `<SPACER_RATIO>` | `.10` |
| `<PERCENT_MEASURE_NAME>` | `% of Total Sales by Product Category` |
| `<PERCENT_FORMAT_STRING>` | `0.00%;-0.00%;0.00%` |
| `<PAGE_ID>` | `dab238165c5348774fb4` |
| `<VISUAL_ID>` | `5e6a3a0a2d634dc3513c` |
| `<VISUAL_TYPE>` | `barChart` |
| `<POS_X>` / `<POS_Y>` / `<POS_Z>` | `517.97716150081567` / `327.699836867863` / `0` |
| `<POS_HEIGHT>` / `<POS_WIDTH>` | `607.83034257748784` / `794.584013050571` |
| `<TAB_ORDER>` | `0` |
| `<TITLE_TEXT>` | `Total Sales by Product Category` |
| `<TITLE_FONT_COLOR_THEME_ID>` / `<TITLE_FONT_COLOR_PERCENT>` | `0` / `-0.6` |
| `<LABEL_DISPLAY_UNITS>` | `1D` |
| `<LABEL_PRECISION>` | `0L` |
| `<BAR_COLOR_THEME_ID>` / `<BAR_COLOR_PERCENT>` | `0` / `0` |
| `<SPACER_LABEL_COLOR_THEME_ID>` / `<SPACER_LABEL_COLOR_PERCENT>` | `0` / `-0.6` |
| `<SPACER_LABEL_FONT_SIZE>` | `10D` |
| `<FILTER_ID_CATEGORY>` | `a514f8f7fb2ae0353838` |
| `<FILTER_ID_SPACER>` | `d3506b9eeaa68a392739` |
| `<FILTER_ID_VALUE>` | `cee35892e484c41eb974` |

## 1. Append to `definition/tables/_Measures.tmdl`

	measure 'Stacked Chart Spacing' = ```

			var __Spacing =
			CALCULATE(
			    MAXX ( dimProducts, [Total Sales] )
			    , ALLSELECTED( dimProducts[ProductCategory] )
			)
			RETURN
			IF ( ISBLANK([Total Sales]), BLANK(),
			__Spacing * .10
			)
			```
		annotation PBI_FormatHint = {"isGeneralNumber":true}

	measure '% of Total Sales by Product Category' = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALLSELECTED ( dimProducts[ProductCategory] ) ) )
		formatString: 0.00%;-0.00%;0.00%

Power BI Desktop assigns each measure a `lineageTag` automatically the next time the model
is saved from the TMDL view, so none is hand-authored here.

## 2. New file `definition/pages/dab238165c5348774fb4/visuals/5e6a3a0a2d634dc3513c/visual.json`

	{
	  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
	  "name": "5e6a3a0a2d634dc3513c",
	  "position": { "x": 517.97716150081567, "y": 327.699836867863, "z": 0, "height": 607.83034257748784, "width": 794.584013050571, "tabOrder": 0 },
	  "visual": {
	    "visualType": "barChart",
	    "query": {
	      "queryState": {
	        "Category": { "projections": [ { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "dimProducts" } }, "Property": "ProductCategory" } }, "queryRef": "dimProducts.ProductCategory", "nativeQueryRef": "ProductCategory", "active": true } ] },
	        "Y": { "projections": [
	          { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Stacked Chart Spacing" } }, "queryRef": "_Measures.Stacked Chart Spacing", "nativeQueryRef": "Stacked Chart Spacing" },
	          { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "queryRef": "_Measures.Total Sales", "nativeQueryRef": "Total Sales" }
	        ] }
	      },
	      "sortDefinition": { "sort": [ { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "direction": "Descending" } ] }
	    },
	    "objects": {
	      "categoryAxis": [ { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } }, "showAxisTitle": { "expr": { "Literal": { "Value": "false" } } } } } ],
	      "valueAxis": [ { "properties": { "showAxisTitle": { "expr": { "Literal": { "Value": "false" } } }, "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
	      "legend": [ { "properties": { "showGradientLegend": { "expr": { "Literal": { "Value": "false" } } }, "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
	      "totals": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } }, "enableBackground": { "expr": { "Literal": { "Value": "false" } } } } } ],
	      "dataPoint": [ { "properties": { "fill": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } } }, "selector": { "metadata": "_Measures.Stacked Chart Spacing" } } ],
	      "labels": [
	        { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } }, "labelDisplayUnits": { "expr": { "Literal": { "Value": "1D" } } }, "labelPrecision": { "expr": { "Literal": { "Value": "0L" } } } } },
	        { "properties": { "dynamicLabelValue": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "% of Total Sales by Product Category" } } } }, "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ], "metadata": "_Measures.Stacked Chart Spacing", "highlightMatching": 1 } },
	        { "properties": { "showSeries": { "expr": { "Literal": { "Value": "true" } } }, "labelPosition": { "expr": { "Literal": { "Value": "'Auto'" } } }, "enableTitleDataLabel": { "expr": { "Literal": { "Value": "false" } } }, "enableDetailDataLabel": { "expr": { "Literal": { "Value": "false" } } }, "enableBackground": { "expr": { "Literal": { "Value": "false" } } }, "backgroundTransparency": { "expr": { "Literal": { "Value": "0D" } } }, "color": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": -0.6 } } } } }, "fontSize": { "expr": { "Literal": { "Value": "10D" } } } }, "selector": { "metadata": "_Measures.Stacked Chart Spacing" } }
	      ]
	    },
	    "visualContainerObjects": {
	      "title": [ { "properties": { "text": { "expr": { "Literal": { "Value": "'Total Sales by Product Category'" } } }, "background": { "solid": { "color": { "expr": { "Literal": { "Value": "null" } } } } }, "fontColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": -0.6 } } } } } } } ]
	    },
	    "drillFilterOtherVisuals": true
	  },
	  "filterConfig": {
	    "filters": [
	      { "name": "a514f8f7fb2ae0353838", "field": { "Column": { "Expression": { "SourceRef": { "Entity": "dimProducts" } }, "Property": "ProductCategory" } }, "type": "Categorical", "isHiddenInViewMode": true },
	      { "name": "d3506b9eeaa68a392739", "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Stacked Chart Spacing" } }, "type": "Advanced", "isHiddenInViewMode": true },
	      { "name": "cee35892e484c41eb974", "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "type": "Advanced", "isHiddenInViewMode": true }
	    ]
	  }
	}

## Result

A vertical/horizontal stacked bar chart ranked descending by `Total Sales`, one bar per
`ProductCategory`. The `Stacked Chart Spacing` segment is colored identically to the
`Total Sales` segment (`ColorId 0, Percent 0` on both), so the two stack into what reads
as a single solid bar — the spacer only adds ~10% headroom. The real segment keeps its
normal value label; the spacer segment's label is overridden via `dynamicLabelValue` to
show `% of Total Sales by Product Category` instead, so the extra headroom carries the
percent-of-total callout without a visible second color or a stack-total label (totals
are hidden).

## Not part of this pattern

The source `end/` folder also adds a `dimDate` table, two relationships
(`factOrders`->`dimProducts`, `factOrders`->`dimCustomers`), a `Total Sales YTD` measure,
a `Total Sales Subtitle` measure, a `Selected Proudcut`/`% of Total Sales` measure pair
used by a separate clustered-bar visual on the same page, and `summarizeBy` changes on
several columns plus a `dimProdusts` -> `dimProducts` table rename. Those came from the
same authoring session but are unrelated to the stacked-spacer technique and are
intentionally excluded here.
