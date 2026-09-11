# Balanced Scorecard DAX Generator

## Overview

This utility generates Power BI DAX code for Operational Excellence scorecard reporting from a metadata-driven Excel file.

Instead of manually creating DAX variables, threshold logic, status calculations, layout tables, and HTML row definitions for every metric, this script generates the code automatically from a spreadsheet.

The output is a ready-to-use DAX block that can be pasted into a Power BI measure or model.

---

## Features

- Generates metric layout DATATABLE definitions
- Generates monthly metric variables
- Generates YTD calculations
- Generates target calculations
- Generates Year-over-Year calculations
- Generates Red / Amber / Green status logic
- Generates dynamic HTML table rows
- Validates metadata before code generation
- Detects duplicate metric keys
- Detects duplicate sort orders
- Supports clipboard copy
- Exports generated DAX to a text file

---

## Requirements

### Python Version

Python 3.10+

### Packages

Install required packages:

```bash
pip install pandas openpyxl pyperclip
```

---

## Input File

The script reads an Excel file containing metric definitions.

Example:

```python
InputFilePath = Path(
    r"ARG Operational Excellence Metric Thresholds.xlsx"
)
```

The input file location is configurable and can be changed to any valid Excel workbook.

### Required Columns

| Column | Description |
|----------|----------|
| SortOrder | Display order |
| MetricName | Display name |
| MetricKey | Unique metric identifier |
| FormatString | DAX formatting string |
| ThresholdFlag | Yes / No |
| RedOperator | Threshold comparison |
| RedThreshold | Red threshold value |
| AmberOperator | Threshold comparison |
| AmberThreshold | Amber threshold value |
| YTDFlag | Yes / No |
| YoYFlag | Yes / No |
| YTDTargetFlag | Yes / No |
| MonthTargetFlag | Yes / No |
| Measure | Power BI measure name |
| Target | Target measure name |

---

## Example Metadata

| MetricName | MetricKey | Measure | Target |
|-------------|-------------|----------|----------|
| Applications Processed | ApplicationsProcessed | Applications Processed | Applications Target |
| Placement Rate | PlacementRate | Placement Rate | Placement Rate Target |

---

## Output

The script generates:

### Layout Table

```dax
ARG Operational Metric Layout =
DATATABLE(...)
```

### Operational Variables

```dax
VAR _placementRateMonth1
VAR _placementRateYtd
VAR _placementRateStatus
```

### Dynamic HTML

```dax
VAR _operationalRows
```

### Output File

```text
ARG_Operational_Metric_DAX.txt
```

---

## Configuration

The following values can be modified without changing the script logic.

```python
LayoutTableName
OutputFileName
CopyToClipboard
GenerateLayoutTable
BlankStatusWhenValueIsBlank
BaseIndent
```

### Example

```python
LayoutTableName = "Financial Metrics Layout"

OutputFileName = "Financial_Metrics_DAX.txt"
```

---

## Validation Rules

The script validates:

- Required columns exist
- Metric names are populated
- Metric keys are unique
- Sort order values are unique
- Format strings are populated
- Threshold operators are valid
- Numeric thresholds contain valid numbers
- Target measures exist when target flags are enabled

Generation stops if validation fails.

---

## Reusing the Generator

This utility is metadata driven.

To generate DAX for a different scorecard:

1. Create a new metric definition workbook.
2. Update:

```python
InputFilePath
```

3. Update:

```python
LayoutTableName
```

4. Update:

```python
OutputFileName
```

5. Run the script.

No additional code changes should be required.

---

## Design Philosophy

This generator follows three principles:

### Metadata Driven

Business users maintain metric definitions in Excel rather than modifying Python code.

### Validation First

All metadata is validated before DAX generation begins.

### Reusable

The same generator can support:

- Balanced Scorecards
- Executive Dashboards
- Operational Metrics
- Financial Metrics
- KPI Reporting Solutions

---

## Author

Steven Foster

Data & Insights