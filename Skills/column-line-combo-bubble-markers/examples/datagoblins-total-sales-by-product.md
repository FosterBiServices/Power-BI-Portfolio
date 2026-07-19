# Worked example: Total Sales by Product (datagoblins report)

Source: diff of `pbip/start/datagoblins_start.*` -> `pbip/end/datagoblins_end.*`. The end
state adds one new column+line combo chart visual to page `dab238165c5348774fb4` and five
supporting measures to the `_Measures` table.

## Token substitutions used

| Token | Value |
|---|---|
| `<MEASURES_TABLE>` | `_Measures` |
| `<VALUE_MEASURE>` | `Total Sales` |
| `<CATEGORY_TABLE>` | `dimProducts` |
| `<CATEGORY_KEY_COLUMN>` | `ProdKey` |
| `<CATEGORY_COLUMN>` | `ProductName` |
| `<PERCENT_MEASURE_NAME>` | `Total Sales Percent of Total` |
| `<PERCENT_FORMAT_STRING>` | `0.00%;-0.00%;0.00%` |
| `<LABEL_MEASURE_NAME>` | `Detail Label` |
| `<LABEL_HEIGHT_MULTIPLIER>` | `1.6` |
| `<MARKER_MEASURE_NAME>` | `Detail Position` |
| `<MARKER_HEIGHT_MULTIPLIER>` | `1.7` |
| `<AXIS_MAX_MEASURE_NAME>` | `Y Axis Max Position` |
| `<AXIS_HEADROOM_MULTIPLIER>` | `2.2` |
| `<SUBTITLE_MEASURE_NAME>` | `Total Sales by Products Subtitle` |
| `<SUBTITLE_PREFIX_TEXT>` | `Total Sales (all products): ` |
| `<SUBTITLE_VALUE_FORMAT>` | `$#,#` |
| `<PAGE_ID>` | `dab238165c5348774fb4` |
| `<VISUAL_ID>` | `0eeb8cfbd559d778eeb5` |
| `<POS_X>` / `<POS_Y>` / `<POS_Z>` | `333.75` / `295` / `0` |
| `<POS_HEIGHT>` / `<POS_WIDTH>` | `460` / `970` |
| `<TAB_ORDER>` | `0` |
| `<TITLE_TEXT>` | `Total Sales` |
| `<BAR_COLOR_THEME_ID>` / `<BAR_COLOR_PERCENT>` | `0` / `-0.2` |
| `<MARKER_COLOR_THEME_ID>` / `<MARKER_COLOR_PERCENT>` | `0` / `-0.1` |
| `<VALUE_LABEL_FONT_THEME_ID>` / `<VALUE_LABEL_FONT_PERCENT>` | `2` / `0` |
| `<VALUE_LABEL_BACKGROUND_THEME_ID>` / `<VALUE_LABEL_BACKGROUND_PERCENT>` | `0` / `0` |
| `<LABEL_DISPLAY_UNITS>` | `1D` |
| `<LABEL_PRECISION>` | `1L` |
| `<LABEL_FONT_SIZE>` | `9D` |
| `<MARKER_SIZE>` | `30` |

## 1. Append to `definition/tables/_Measures.tmdl`

	measure 'Total Sales Percent of Total' = ```

			var _Numerator = [Total Sales]
			var _Denominator = CALCULATE([Total Sales], REMOVEFILTERS(dimProducts[ProductName]))
			RETURN
			    DIVIDE(
			        _Numerator,
			        _Denominator
			    )
			```
		formatString: 0.00%;-0.00%;0.00%

	measure 'Detail Label' = ```

			var _MaxValue =
			MAXX(
			    ALLSELECTED( dimProducts[ProdKey], dimProducts[ProductName]),
			        [Total Sales]
			    )
			RETURN
			    IF ( [Total Sales],
			        _MaxValue * 1.6
			    )
			```

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	measure 'Detail Position' = ```

			var _MaxValue =
			MAXX(
			    ALLSELECTED( dimProducts[ProdKey], dimProducts[ProductName]),
			        [Total Sales]
			    )
			RETURN
			    IF ( [Total Sales],
			        _MaxValue * 1.7
			    )
			```

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	measure 'Y Axis Max Position' = ```

			var _MaxValue =
			MAXX(
			    ALLSELECTED( dimProducts[ProdKey], dimProducts[ProductName]),
			        [Total Sales]
			    )
			RETURN
			        _MaxValue * 2.2
			```

		annotation PBI_FormatHint = {"isGeneralNumber":true}

	measure 'Total Sales by Products Subtitle' = ```

			var _value = CALCULATE([Total Sales], REMOVEFILTERS(dimProducts[ProdKey], dimProducts[ProductName]))
			var _Header = "Total Sales (all products): "
			RETURN
			_Header & FORMAT(_value,"$#,#")
			```

Power BI Desktop assigns each measure a `lineageTag` automatically the next time the model
is saved from the TMDL view, so none is hand-authored here.

## 2. New file `definition/pages/dab238165c5348774fb4/visuals/0eeb8cfbd559d778eeb5/visual.json`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
  "name": "0eeb8cfbd559d778eeb5",
  "position": { "x": 333.75, "y": 295, "z": 0, "height": 460, "width": 970, "tabOrder": 0 },
  "visual": {
    "visualType": "lineClusteredColumnComboChart",
    "query": {
      "queryState": {
        "Category": { "projections": [ { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "dimProducts" } }, "Property": "ProductName" } }, "queryRef": "dimProducts.ProductName", "nativeQueryRef": "ProductName", "active": true } ] },
        "Y": { "projections": [ { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "queryRef": "_Measures.Total Sales", "nativeQueryRef": "Total Sales" } ] },
        "Y2": { "projections": [
          { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Detail Position" } }, "queryRef": "_Measures.Detail Position", "nativeQueryRef": "Detail Position" },
          { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Detail Label" } }, "queryRef": "_Measures.Detail Label", "nativeQueryRef": "Detail Label" }
        ] }
      },
      "sortDefinition": { "sort": [ { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales" } }, "direction": "Descending" } ] }
    },
    "objects": {
      "error": [
        { "properties": { "enabled": { "expr": { "Literal": { "Value": "true" } } }, "barColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": -0.2 } } } } }, "tooltipShow": { "expr": { "Literal": { "Value": "false" } } } }, "selector": { "metadata": "_Measures.Total Sales" } },
        { "properties": { "errorRange": { "kind": "ErrorRange", "explicit": { "isRelative": { "expr": { "Literal": { "Value": "false" } } }, "upperBound": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Detail Position" } } } } } }, "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 0 } } ], "metadata": "_Measures.Total Sales", "highlightMatching": 1 } }
      ],
      "lineStyles": [
        { "properties": { "showMarker": { "expr": { "Literal": { "Value": "true" } } }, "strokeShow": { "expr": { "Literal": { "Value": "false" } } } } },
        { "properties": { "showMarker": { "expr": { "Literal": { "Value": "false" } } }, "markerColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": -0.1 } } } } } }, "selector": { "metadata": "_Measures.Detail Label" } },
        { "properties": { "showMarker": { "expr": { "Literal": { "Value": "true" } } }, "markerColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": -0.1 } } } } } }, "selector": { "metadata": "_Measures.Detail Position" } }
      ],
      "valueAxis": [
        { "properties": { "end": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Y Axis Max Position" } } }, "show": { "expr": { "Literal": { "Value": "false" } } }, "secRoundRange": { "expr": { "Literal": { "Value": "false" } } }, "secShow": { "expr": { "Literal": { "Value": "false" } } } } }
      ],
      "legend": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
      "labels": [
        { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } },
        { "properties": { "labelPosition": { "expr": { "Literal": { "Value": "'OutsideEnd'" } } }, "color": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 2, "Percent": 0 } } } } }, "backgroundColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } }, "labelDisplayUnits": { "expr": { "Literal": { "Value": "1D" } } } }, "selector": { "metadata": "_Measures.Total Sales" } },
        { "properties": { "showSeries": { "expr": { "Literal": { "Value": "false" } } }, "enableValueDataLabel": { "expr": { "Literal": { "Value": "true" } } }, "enableBackground": { "expr": { "Literal": { "Value": "false" } } }, "labelDisplayUnits": { "expr": { "Literal": { "Value": "1D" } } } }, "selector": { "metadata": "_Measures.Detail Position" } },
        { "properties": { "enableBackground": { "expr": { "Literal": { "Value": "false" } } }, "enableDetailDataLabel": { "expr": { "Literal": { "Value": "false" } } }, "labelDisplayUnits": { "expr": { "Literal": { "Value": "1D" } } }, "labelPosition": { "expr": { "Literal": { "Value": "'Above'" } } }, "showSeries": { "expr": { "Literal": { "Value": "true" } } }, "labelPrecision": { "expr": { "Literal": { "Value": "1L" } } }, "fontSize": { "expr": { "Literal": { "Value": "9D" } } } }, "selector": { "metadata": "_Measures.Detail Label" } },
        { "properties": { "dynamicLabelValue": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales Percent of Total" } } } }, "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ], "metadata": "_Measures.Detail Label", "highlightMatching": 1 } },
        { "properties": { "dynamicLabelValue": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales Percent of Total" } } } }, "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ], "metadata": "_Measures.Detail Position", "highlightMatching": 1 } }
      ],
      "categoryAxis": [ { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } } ]
    },
    "visualContainerObjects": {
      "title": [ { "properties": { "text": { "expr": { "Literal": { "Value": "'Total Sales'" } } } } } ],
      "subTitle": [ { "properties": { "text": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Measures" } }, "Property": "Total Sales by Products Subtitle" } } } } } ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

## 3. Merge into the report's registered custom theme file (e.g. `StaticResources/RegisteredResources/Equus_Collab36706858771014383.json`)

Add `lineClusteredColumnComboChart` as a new sibling key inside the existing
`visualStyles` object, alongside the theme's existing `*` and `page` keys:

```json
    "lineClusteredColumnComboChart": {
      "*": {
        "lineStyles": [
          {
            "markerSize": 30
          }
        ]
      }
    }
```

Without this, Power BI's default marker size renders the bubbles as small dots
rather than clearly visible circles.

## Result

A column+line combo chart ranked descending by `Total Sales`. Each column gets a
highlighted `OutsideEnd` value label. The `Detail Position` line series is invisible
(no stroke) but its marker shows as a bubble sitting at a fixed shelf 1.7x the tallest
column's value, with its own value label suppressed and replaced by `Total Sales
Percent of Total` (dynamic label). The `Detail Label` series sits at a 1.6x shelf,
has its marker hidden entirely, and shows an `Above`-positioned dynamic label with the
same percent value at 9pt font. An error-bar stem (dark theme color, tooltip off) rises
from each column's top to the `Detail Position` height, visually anchoring the bubble to
its bar. The value axis is hidden and its range is fixed to 2.2x the max value so nothing
clips. Title reads "Total Sales"; subtitle reads "Total Sales (all products): $1,234".

## Not part of this pattern

The source `end/` folder also renames/replaces several dimension and fact tables
(`dimCustomers`, `factOrders Slicer`, `factOrders Delivery Slicer` -> `dimDate` plus a
new `relationships.tmdl`), removes older window/delivery-speed measures, and applies a
custom report theme (`customTheme`, `outspacePane`, `queryLimitOption` in `report.json`).
Those came from the same shared sample file being reused across other tutorials and are
unrelated to the combo-chart-with-bubble-markers technique, so they are intentionally
excluded here.
