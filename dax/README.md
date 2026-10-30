# DAX

Reusable DAX I use across models, organised from the most general to the most specialised.

| Folder | What's inside |
|---|---|
| [`udf-library/`](udf-library/) | A versioned library of **DAX user-defined functions** for time intelligence: one `.dax` file per function, plus ready-to-paste `functions.tmdl` and query-view distributions. |
| [`time-intelligence/`](time-intelligence/) | The same calculations as classic measure templates, for models without UDFs. |
| [`patterns/`](patterns/) | Formatting, navigation, security and SVG visual patterns. |

## Time-intelligence templates

| Group | Measures |
|---|---|
| [dynamic](time-intelligence/dynamic/) | POP, PP |
| [growth](time-intelligence/growth/) | MATG, MOM, MOMTD, MTDOPM, QOQ, QOQTD, QTDOPQ, YOY, YOYTD, YTDOPY |
| [moving](time-intelligence/moving/) | MAT, PYMAT |
| [period-to-date](time-intelligence/period-to-date/) | MTD, PMTD, PQTD, PYTD, QTD, YTD |
| [previous-period](time-intelligence/previous-period/) | PM, PMC, PQ, PQC, PY, PYC |

## Patterns

Each file starts with a header listing its purpose and the placeholders to replace (`<#MEASURE_NAME#>`, `[#VALUE_MEASURE#]`, `<DATE_TABLE>[&DATE_FIELD&]`).

| Category | File | Purpose |
|---|---|---|
| Conditional Formatting | [`divergent_color.dax`](patterns/conditional-formatting/divergent_color.dax) | Returns a color based on the selected-range position of the current measure value. |
| Date Tables | [`dim-date-calendar.dax`](patterns/date-tables/dim-date-calendar.dax) | Date dimension built with CALENDAR over an explicit range. |
| Date Tables | [`dim-date-calendarauto.dax`](patterns/date-tables/dim-date-calendarauto.dax) | Date dimension built with CALENDARAUTO. |
| Field Parameters | [`measure_selection.dax`](patterns/field-parameters/measure_selection.dax) | Field parameter for switching between published measures. |
| Filter Display | [`month_filter_card.dax`](patterns/filter-display/month_filter_card.dax) | Displays selected months in a card visual. |
| Formatting | [`custom_spacing.dax`](patterns/formatting/custom_spacing.dax) | Aligns two formatted measure values by inserting invisible spacing characters. |
| Modeling | [`add_synthetic_row.dax`](patterns/modeling/add_synthetic_row.dax) | Adds a synthetic row to an existing table. |
| Navigation | [`drill_through_daily_text.dax`](patterns/navigation/drill_through_daily_text.dax) | Returns daily drill-through text when a parameter is selected. |
| Navigation | [`drill_through_monthly_text.dax`](patterns/navigation/drill_through_monthly_text.dax) | Returns monthly drill-through text when a parameter is selected. |
| Security | [`sensitive_data.dax`](patterns/security/sensitive_data.dax) | Returns data only when the required permission exists. |
| Svg Icons | [`calendar_details_svg.dax`](patterns/svg-icons/calendar_details_svg.dax) | Returns an SVG calendar grid with completed, qualifying, and remaining-day details. |
| Svg Icons | [`card_columns_no_target.dax`](patterns/svg-icons/card_columns_no_target.dax) | Returns an SVG card with a slicer-aware callout and a trailing-month column chart. |
| Svg Icons | [`card_columns_target.dax`](patterns/svg-icons/card_columns_target.dax) | Returns an SVG KPI card with columns, a target line, period labels, and summary text. |
| Svg Icons | [`card_text_only.dax`](patterns/svg-icons/card_text_only.dax) | Returns an SVG KPI card containing primary, secondary, and target-summary text. |
| Svg Icons | [`donut_target_progress_svg.dax`](patterns/svg-icons/donut_target_progress_svg.dax) | Returns an SVG donut showing target, current value, and the amount over or under target. |
| Svg Icons | [`notification_icon.dax`](patterns/svg-icons/notification_icon.dax) | Returns an SVG notification bell with a badge showing the number of actionable groups. |
| Svg Icons | [`period_change_icon.dax`](patterns/svg-icons/period_change_icon.dax) | Compares current MTD to prior month and returns an icon. |
| Svg Icons | [`star_rating_svg.dax`](patterns/svg-icons/star_rating_svg.dax) | Returns an SVG rating made from full, half, and empty stars. |
