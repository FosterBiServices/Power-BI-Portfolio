# DAX Pattern Templates

A Git-friendly library of reusable, commented DAX patterns for Power BI semantic models. Each pattern is stored in its own `.dax` file so changes are easy to review, test, and merge.

## Included pattern categories

- Period to Date
- Moving Periods
- Previous Periods
- Growth
- Dynamic Calculations
- Modeling
- Security
- Icons and Indicators
- Filter Display
- Field Parameters
- Navigation
- Conditional Formatting
- Formatting

## Placeholder contract

- `[#VALUE_MEASURE#]`: Existing measure evaluated by the pattern.
- `[#DETAIL_MEASURE#]`: Supporting detail measure used by formatting patterns.
- `<#MEASURE_NAME#>`: Published measure name.
- `<#TABLE_NAME#>`: Published calculated table name.
- `<#PARAMETER_NAME#>`: Published field parameter name.
- `<DATE_TABLE>`: Marked date table.
- `[&DATE_FIELD&]`: Continuous date column.
- `<CATEGORY_TABLE>`: Table containing the comparison category.
- `[&CATEGORY_FIELD&]`: Category field used by the visual.
- `<PARAMETER_TABLE>`: Field parameter table.
- `[&PARAMETER_FIELD&]`: Display field from the parameter table.
- `<MEASURE_TABLE>`: Table containing referenced measures.

Example replacement:

```text
<#MEASURE_NAME#>            -> Revenue YTD
[#VALUE_MEASURE#]          -> [Revenue]
<DATE_TABLE>[&DATE_FIELD&] -> 'dimDates'[DateValue]
<CATEGORY_TABLE>           -> 'dimProvider'
[&CATEGORY_FIELD&]         -> [Provider Name]
```

## Repository Workflow

1. Create a branch named `feature/<pattern-or-change>`.
2. Edit one pattern per file whenever practical.
3. Update documentation when behavior changes.
4. Validate the DAX against the checklist in `docs/testing.md`.
5. Open a pull request and include the tested model, date range, and expected result.

## Design Decisions

- Reusable placeholders are preferred over hard-coded model references.
- Time-intelligence templates assume a properly configured marked date table.
- Percentage calculations should use `DIVIDE` for safe zero-denominator handling.
- Formatting and icon patterns return text and should not be used in numeric calculations.
- Conditional formatting patterns return values intended for field-value conditional formatting.
- Security patterns are intended as display-layer controls and do not replace Row-Level Security.
- Field-parameter templates are stored separately from standard measure templates.
- Calculated-table patterns clearly identify themselves in metadata and comments.

## Folder Structure

```text
patterns/
├── period-to-date/
├── moving/
├── previous-period/
├── growth/
├── dynamic/
├── modeling/
├── security/
├── icons/
├── filter-display/
├── field-parameters/
├── navigation/
├── conditional-formatting/
└── formatting/

docs/
```

## Validation Checklist

Before publishing a pattern:

- Replace all placeholders.
- Confirm referenced measures exist.
- Verify date table configuration.
- Test row-level values.
- Test subtotals.
- Test grand totals.
- Test slicer interactions.
- Validate blank handling.
- Validate zero-denominator handling.
- Confirm expected formatting.
- Confirm the pattern returns the documented data type.

## Status

This repository is provided as an internal template library. 
