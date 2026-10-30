# Worked example: Total Sales by Product (datagoblins report)

Source: diff of `pbip/start/datagoblins_start.*` -> `pbip/end/datagoblins_end.*`. The end
state adds one new clustered bar chart visual to page `dab238165c5348774fb4` and four
supporting measures to the `_Measures` table.

## Token substitutions used

| Token | Value |
|---|---|
| `<MEASURES_TABLE>` | `_Measures` |
| `<VALUE_MEASURE>` | `Total Sales` |
| `<CATEGORY_TABLE>` | `dimProdusts` |
| `<CATEGORY_COLUMN>` | `ProductName` |
| `<SPACER_MEASURE_NAME>` | `Clustered Chart Spacing` |
| `<SPACER_FORMAT_STRING>` | `0` |
| `<CATEGORY_LABEL_MEASURE_NAME>` | `Selected Product` |
| `<PERCENT_MEASURE_NAME>` | `% of Total Sales` |
| `<PERCENT_FORMAT_STRING>` | `0.0%` |
| `<SUBTITLE_MEASURE_NAME>` | `Total Sales Subtitle` |
| `<SUBTITLE_VALUE_MEASURE>` | `Total Sales` |
| `<SUBTITLE_PREFIX_TEXT>` | `Total Sales: ` |
| `<SUBTITLE_VALUE_FORMAT>` | `$#,#` |
| `<PAGE_ID>` | `dab238165c5348774fb4` |
| `<VISUAL_ID>` | `3467fd7dcb8644c49092` |
| `<VISUAL_TYPE>` | `clusteredBarChart` |
| `<POS_X>` / `<POS_Y>` / `<POS_Z>` | `646.25` / `212.5` / `0` |
| `<POS_HEIGHT>` / `<POS_WIDTH>` | `473.75` / `651.25` |
| `<TAB_ORDER>` | `0` |
| `<TITLE_TEXT>` | `Total Sales` |
| `<TITLE_FONT_COLOR_THEME_ID>` | `3` |
| `<CLUSTERED_GAP_SIZE>` | `25D` |
| `<CATEGORY_INNER_PADDING>` | `25L` |
| `<LABEL_DISPLAY_UNITS>` | `1D` |
| `<LABEL_COLOR_THEME_ID>` / `<LABEL_COLOR_PERCENT>` | `0` / `-0.5` |
| `<LABEL_BACKGROUND_THEME_ID>` / `<LABEL_BACKGROUND_PERCENT>` | `0` / `0` |
| `<LABEL_BACKGROUND_TRANSPARENCY>` | `0D` |
| `<FILTER_ID_CATEGORY>` | `18550cd9f3b8bdf1cbc8` |
| `<FILTER_ID_SPACER>` | `3600743584b413cca813` |
| `<FILTER_ID_VALUE>` | `220a77cacbba9f21fd25` |

## 1. Append to `definition/tables/_Measures.tmdl`

```tmdl
	measure 'Clustered Chart Spacing' = If ( ISBLANK([Total Sales]), BLANK(), 0 )
		formatString: 0

	measure 'Selected Product' = SELECTEDVALUE(dimProdusts[ProductName])

	measure '% of Total Sales' = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALLSELECTED ( dimProdusts[ProductName] ) ) )
		formatString: 0.0%

	measure 'Total Sales Subtitle' = ```

			var _value = [Total Sales]
			var _Header = "Total Sales: "
			RETURN
			_Header & FORMAT(_value,"$#,#")
			```
```

Power BI Desktop assigns each measure a `lineageTag` automatically the next time the model
is saved from the TMDL view, so none is hand-authored here.

## 2. New file `definition/pages/dab238165c5348774fb4/visuals/3467fd7dcb8644c49092/visual.json`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
  "name": "3467fd7dcb8644c49092",
  "position": { "x": 646.25, "y": 212.5, "z": 0, "height": 473.75, "width": 651.25, "tabOrder": 0 },
  "visual": {
    "visualType": "clusteredBarChart",
    "query": {
      "queryState": {
        "Category": { "projections": [ { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "dimProdusts" } }, "Property": "ProductName" } }, "queryRef": "dimProdusts.ProductName", "nativeQueryRef": "ProductName", "active": true } ] },
        "Y": { "projections": [
          { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Clustered Chart Spacing" } }, "queryRef": "_Measures.Clustered Chart Spacing", "nativeQueryRef": "Clustered Chart Spacing" },
          { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "queryRef": "_Measures.Total Sales", "nativeQueryRef": "Total Sales" }
        ] }
      },
      "sortDefinition": { "sort": [ { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "direction": "Descending" } ] }
    },
    "objects": {
      "labels": [
        { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } }, "enableDetailDataLabel": { "expr": { "Literal": { "Value": "true" } } }, "detailContentType": { "expr": { "Literal": { "Value": "'Custom'" } } } } },
        { "properties": { "dynamicLabelValue": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Selected Product" } } }, "dynamicLabelDetail": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "% of Total Sales" } } } }, "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ], "metadata": "_Measures.Clustered Chart Spacing", "highlightMatching": 1 } },
        { "properties": { "detailLabelDisplayUnits": { "expr": { "Literal": { "Value": "1D" } } } }, "selector": { "metadata": "_Measures.Clustered Chart Spacing" } },
        { "properties": { "labelDisplayUnits": { "expr": { "Literal": { "Value": "1D" } } }, "italic": { "expr": { "Literal": { "Value": "true" } } }, "labelPosition": { "expr": { "Literal": { "Value": "'OutsideEnd'" } } }, "color": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": -0.5 } } } } }, "enableBackground": { "expr": { "Literal": { "Value": "true" } } }, "backgroundColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } }, "backgroundTransparency": { "expr": { "Literal": { "Value": "0D" } } } }, "selector": { "metadata": "_Measures.Total Sales" } }
      ],
      "categoryAxis": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } }, "showAxisTitle": { "expr": { "Literal": { "Value": "false" } } }, "innerPadding": { "expr": { "Literal": { "Value": "25L" } } } } } ],
      "valueAxis": [ { "properties": { "showAxisTitle": { "expr": { "Literal": { "Value": "false" } } }, "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
      "legend": [ { "properties": { "showGradientLegend": { "expr": { "Literal": { "Value": "false" } } }, "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
      "layout": [ { "properties": { "clusteredGapSize": { "expr": { "Literal": { "Value": "25D" } } } } } ]
    },
    "visualContainerObjects": {
      "title": [ { "properties": { "text": { "expr": { "Literal": { "Value": "'Total Sales'" } } }, "background": { "solid": { "color": { "expr": { "Literal": { "Value": "null" } } } } }, "fontColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 3, "Percent": 0 } } } } } } } ],
      "subTitle": [ { "properties": { "text": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales Subtitle" } } } } } ]
    },
    "drillFilterOtherVisuals": true
  },
  "filterConfig": {
    "filters": [
      { "name": "18550cd9f3b8bdf1cbc8", "field": { "Column": { "Expression": { "SourceRef": { "Entity": "dimProdusts" } }, "Property": "ProductName" } }, "type": "Categorical", "isHiddenInViewMode": true },
      { "name": "3600743584b413cca813", "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Clustered Chart Spacing" } }, "type": "Advanced", "isHiddenInViewMode": true },
      { "name": "220a77cacbba9f21fd25", "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "type": "Advanced", "isHiddenInViewMode": true }
    ]
  }
}
```

## Result

A horizontal clustered bar chart ranked descending by `Total Sales`. Each bar's real value
gets a highlighted "pill" label at `OutsideEnd` (from the `Total Sales` selector); the
zero-valued `Clustered Chart Spacing` series contributes no visible second bar but carries
its own custom label showing the product name and its `% of Total Sales`, which renders
above the real bar. Title reads "Total Sales"; subtitle reads "Total Sales: $1,234".

## Not part of this pattern

The source `end/` folder also adds a `dimDate` table, two relationships
(`factOrders`->`dimProdusts`, `factOrders`->`dimCustomers`), a `Total Sales YTD` measure,
and `summarizeBy` changes on several columns. Those came from the same authoring session
but are unrelated to the label-above-bar technique and are intentionally excluded here.
