---
contextType: Power BI Semantic Model
schemaVersion: 1.0
generator: Semantic Model Context Builder
modelName: Inclement-Weather-Sample
generatedUtc: 2026-09-24T01:48:36+00:00
---

# Semantic Model Instructions

Treat this file as the authoritative structural reference for this model.
Do not invent tables, columns, measures, or relationships that are not listed.
Use exact object names when proposing DAX.

# Model Summary

- Model: Inclement-Weather-Sample
- Storage mode: Unknown
- Tables: 13
- Measure-Only Tables Remaining: 1
- Columns: 124
- Measures: 71
- Relationships: 9

## Model Profile

### Measure Dependencies Found

- Total Dependencies: 120

### Data Type Distribution

- string: 73
- dateTime: 19
- int64: 19
- Unknown: 13

### Most Connected Tables

1. dimDate (5 relationships)
2. MPR (5 relationships)
3. Activations (2 relationships)
4. Clients (2 relationships)
5. HMIS (2 relationships)
6. Community (1 relationships)
7. Intake (1 relationships)
8. _Measures (0 relationships)
9. Capacity Measure Selection (0 relationships)
10. MPR Dimension Selection (0 relationships)

# Tables

## _Measures

No description provided.

### Statistics

- Columns: 0
- Measures: 71
- Relationships: 0
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|

### Measures

#### Activations

#### Enrollments
```dax
COUNTROWS( 'MPR' )
```

#### Children

##### Dependencies

**Referenced Columns**
- MPR[NUMBER OF CHILDREN]

```dax
SUM( 'MPR'[NUMBER OF CHILDREN] )
```

#### Adults

##### Dependencies

**Referenced Columns**
- MPR[NUMBER OF ADULTS]

```dax
SUM( 'MPR'[NUMBER OF ADULTS] )
```

#### Household

##### Dependencies

**Referenced Columns**
- MPR[HOUSEHOLD]
- MPR[UID_SOURCE]

```dax
CALCULATE(
     SUM( 'MPR'[HOUSEHOLD] ),
     'MPR'[UID_SOURCE] = "MPR"
)
```

#### Intake - Pets

##### Dependencies

**Referenced Columns**
- Intake[# OF PETS]

```dax
SUM( 'Intake'[# OF PETS] )
```

#### Gender - female

##### Dependencies

**Referenced Columns**
- MPR[GENDER]
- MPR[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          'MPR'[UNIQUE IDENTIFIER NUMBER]
     ),
     'MPR'[GENDER] = "female"
)
```

#### Gender - Male

##### Dependencies

**Referenced Columns**
- MPR[GENDER]
- MPR[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          'MPR'[UNIQUE IDENTIFIER NUMBER]
     ),
     'MPR'[GENDER] = "male"
)
```

#### Gender - Non-Binary

##### Dependencies

**Referenced Columns**
- MPR[GENDER]
- MPR[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          'MPR'[UNIQUE IDENTIFIER NUMBER]
     ),
     'MPR'[GENDER] = "non-binary"
)
```

#### Gender - Different Identity

##### Dependencies

**Referenced Columns**
- MPR[GENDER]
- MPR[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          'MPR'[UNIQUE IDENTIFIER NUMBER]
     ),
     'MPR'[GENDER] = "different identity"
)
```

#### Gender - Prefers Not to Answer

##### Dependencies

**Referenced Columns**
- MPR[GENDER]
- MPR[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          'MPR'[UNIQUE IDENTIFIER NUMBER]
     ),
     'MPR'[GENDER] = "prefers not to answer"
)
```

#### Age - 18 to 24

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[CLIENT AGE]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[CLIENT AGE] >= 18
          && 'MPR'[CLIENT AGE] < 25
)
```

#### Age - 55 to 64

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[CLIENT AGE]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[CLIENT AGE] >= 55
          && 'MPR'[CLIENT AGE] < 65
)
```

#### Age - 65 and Over

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[CLIENT AGE]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[CLIENT AGE] >= 65
)
```

#### Veteran - Yes

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[VETERAN]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[VETERAN] = "yes"
)
```

#### Veteran - No

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[VETERAN]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[VETERAN] = "no"
)
```

#### Disability - Yes

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[DISABILITY]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[DISABILITY] = "yes"
)
```

#### Disability - No

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[DISABILITY]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[DISABILITY] = "no"
)
```

#### Avg Intakes Per Day

##### Dependencies

**Referenced Measures**
- Days Worked (Intake)
- Intake Count

```dax
DIVIDE(
     [Intake Count],
     [Days Worked (Intake)]
)
```

#### Days Worked (Intake)

##### Dependencies

**Referenced Columns**
- Intake[CHECK IN DATE]

```dax
DISTINCTCOUNT( 'Intake'[CHECK IN DATE] )
```

#### Distinct Communities

##### Dependencies

**Referenced Columns**
- MPR[COMMUNITY]

```dax
DISTINCTCOUNT( 'MPR'[COMMUNITY] )
```

#### First Intake Date

##### Dependencies

**Referenced Columns**
- Intake[CHECK IN DATE]

```dax
MIN( 'Intake'[CHECK IN DATE] )
```

#### Intake Count
```dax
COUNTROWS( 'Intake' )
```

#### Last Intake Date

##### Dependencies

**Referenced Columns**
- Intake[CHECK IN DATE]

```dax
MAX( 'Intake'[CHECK IN DATE] )
```

#### Staff Count

##### Dependencies

**Referenced Columns**
- Intake[STAFF NAME]

```dax
DISTINCTCOUNT( 'Intake'[STAFF NAME] )
```

#### Intake - Activations

##### Dependencies

**Referenced Columns**
- Intake[CONFIRMATION #]

```dax
DISTINCTCOUNTNOBLANK(
     'Intake'[CONFIRMATION #]
)
```

#### Clients

##### Dependencies

**Referenced Columns**
- Clients[UNIQUE IDENTIFIER NUMBER]

```dax
DISTINCTCOUNT(
     'Clients'[UNIQUE IDENTIFIER NUMBER]
)
```

#### Average Age

##### Dependencies

**Referenced Columns**
- Clients[AGE]

```dax
AVERAGE( 'Clients'[AGE] )
```

#### Nights

##### Dependencies

**Referenced Columns**
- MPR[NUMBER OF HOTEL NIGHTS]

```dax
SUM( 'MPR'[NUMBER OF HOTEL NIGHTS] )
```

#### Rooms

##### Dependencies

**Referenced Columns**
- MPR[NUMBER OF HOTEL ROOMS RENTED]

```dax
SUM(
     'MPR'[NUMBER OF HOTEL ROOMS RENTED]
)
```

#### Average Length of Stay

##### Dependencies

**Referenced Columns**
- MPR[NUMBER OF HOTEL NIGHTS]

```dax
AVERAGE( 'MPR'[NUMBER OF HOTEL NIGHTS] )
```

#### Activations

##### Dependencies

**Referenced Columns**
- MPR[ACTIVATION ID]

```dax
DISTINCTCOUNT( 'MPR'[ACTIVATION ID] )
```

#### HMIS Only UIDs

##### Dependencies

**Referenced Columns**
- DataIntegrity[HMIS Flag]
- DataIntegrity[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          DataIntegrity[UNIQUE IDENTIFIER NUMBER]
     ),
     DataIntegrity[HMIS Flag] = "HMIS"
)
```

#### UID

##### Dependencies

**Referenced Columns**
- MPR[UNIQUE IDENTIFIER NUMBER]

```dax
DISTINCTCOUNT(
     'MPR'[UNIQUE IDENTIFIER NUMBER]
)
```

#### Veteran Percentage

##### Dependencies

**Referenced Measures**
- Veteran - No
- Veteran - Yes

```dax
DIVIDE(
     [Veteran - Yes],
     [Veteran - Yes] + [Veteran - No]
)
```

#### Disability Percentage

##### Dependencies

**Referenced Measures**
- Disability - No
- Disability - Yes

```dax
DIVIDE(
     [Disability - Yes],
     [Disability - Yes] + [Disability - No]
)
```

#### People Measure Selection Title

##### Dependencies

**Referenced Columns**
- People Measure Selection[Measure]
- People Measure Selection[Name]

```dax
VAR _Selection =
     SELECTCOLUMNS(
          SUMMARIZE(
               'People Measure Selection',
               'People Measure Selection'[Name],
               'People Measure Selection'[Measure]
          ),
          "SelectedName", 'People Measure Selection'[Name]
     )
VAR Choice =
     IF(
          COUNTROWS( _Selection ) = 1,
          _Selection
     )
RETURN
     Choice & " by month"
```

#### Multiple Check-ins

##### Dependencies

**Referenced Measures**
- CheckInCount

**Referenced Columns**
- MPR[UNIQUE IDENTIFIER NUMBER]
- People Measure Selection[Measure]
- People Measure Selection[Name]
- dimDate[Month Year]

```dax
// Only applying this as tooltip -- Duplicate if needed elsewhere
VAR _Selection =
     SELECTCOLUMNS(
          SUMMARIZE(
               'People Measure Selection',
               'People Measure Selection'[Name],
               'People Measure Selection'[Measure]
          ),
          "SelectedName", 'People Measure Selection'[Name]
     )
VAR Choice =
     IF(
          COUNTROWS( _Selection ) = 1,
          _Selection
     )
VAR _GroupedTable =
     SUMMARIZE(
          'MPR',
          'MPR'[UNIQUE IDENTIFIER NUMBER],
          'dimDate'[Month Year],
          "CheckInCount", COUNTROWS( 'MPR' )
     )
RETURN
     IF(
          Choice = "Enrollments",
          COUNTROWS(
               SUMMARIZE(
                    FILTER(
                         _GroupedTable,
                         [CheckInCount] > 1
                    ),
                    'MPR'[UNIQUE IDENTIFIER NUMBER]
               )
          )
     )
```

#### Hotel Activation Rank

##### Dependencies

**Referenced Measures**
- Activations
- Enrollments
- People Measure Selection Value

**Referenced Columns**
- MPR[HOTEL NAME]

```dax
VAR m = [People Measure Selection Value]
RETURN
     IF(
          m = "Activations",
          RANKX(
               ALLSELECTED( 'MPR'[HOTEL NAME] ),
               [Activations],
               ,
               DESC,
               DENSE
          ),
          RANKX(
               ALLSELECTED( 'MPR'[HOTEL NAME] ),
               [Enrollments],
               ,
               DESC,
               DENSE
          )
     )
```

#### Community Activation Rank

##### Dependencies

**Referenced Measures**
- Activations
- Enrollments
- People Measure Selection Value

**Referenced Columns**
- MPR[COMMUNITY]

```dax
VAR m = [People Measure Selection Value]
RETURN
     IF(
          m = "Activations",
          RANKX(
               ALLSELECTED( 'MPR'[COMMUNITY] ),
               [Activations],
               ,
               DESC,
               DENSE
          ),
          RANKX(
               ALLSELECTED( 'MPR'[COMMUNITY] ),
               [Enrollments],
               ,
               DESC,
               DENSE
          )
     )
```

#### Hotel Show Top X

##### Dependencies

**Referenced Measures**
- Hotel Activation Rank

**Referenced Columns**
- Top X[Top X]

```dax
VAR _TopN =
     SELECTEDVALUE( 'Top X'[Top X], 5 )
RETURN
     IF(
          [Hotel Activation Rank] <= _TopN,
          1,
          0
     )
```

#### Community Show Top X

##### Dependencies

**Referenced Measures**
- Community Activation Rank

**Referenced Columns**
- Top X[Top X]

```dax
VAR _TopN =
     SELECTEDVALUE( 'Top X'[Top X], 5 )
RETURN
     IF(
          [Community Activation Rank] <= _TopN,
          1,
          0
     )
```

#### Top X Title

##### Dependencies

**Referenced Measures**
- MPR Dimension Selection Value
- People Measure Selection Value

**Referenced Columns**
- Top X[Top X]

```dax
VAR _TopN =
     SELECTEDVALUE( 'Top X'[Top X], 5 )
VAR _Value =
     [People Measure Selection Value]
VAR _Dimension =
     [MPR Dimension Selection Value]
RETURN
     "Top " & _TopN & " " & _Value & " by "
          & _Dimension
```

#### Gender - Other

##### Dependencies

**Referenced Measures**
- Gender - Different Identity
- Gender - Non-Binary
- Gender - Prefers Not to Answer

```dax
[Gender - Non-Binary]
     + [Gender - Prefers Not to Answer]
     + [Gender - Different Identity]
```

#### People Measure Selection Value

##### Dependencies

**Referenced Columns**
- People Measure Selection[Measure]
- People Measure Selection[Name]

```dax
VAR _Selection =
     SELECTCOLUMNS(
          SUMMARIZE(
               'People Measure Selection',
               'People Measure Selection'[Name],
               'People Measure Selection'[Measure]
          ),
          "SelectedName", 'People Measure Selection'[Name]
     )
RETURN
     IF(
          COUNTROWS( _Selection ) = 1,
          _Selection
     )
```

#### MPR Dimension Selection Value

##### Dependencies

**Referenced Columns**
- MPR Dimension Selection[Dimension]
- MPR Dimension Selection[Fields]

```dax
VAR _Selection =
     SELECTCOLUMNS(
          SUMMARIZE(
               'MPR Dimension Selection',
               'MPR Dimension Selection'[Dimension],
               'MPR Dimension Selection'[Fields]
          ),
          "SelectedName", 'MPR Dimension Selection'[Dimension]
     )
RETURN
     IF(
          COUNTROWS( _Selection ) = 1,
          _Selection
     )
```

#### Top X Filter

##### Dependencies

**Referenced Measures**
- Community Show Top X
- Hotel Show Top X
- MPR Dimension Selection Value

```dax
VAR _Dimension =
     [MPR Dimension Selection Value]
RETURN
     IF(
          _Dimension = "Hotel",
          [Hotel Show Top X],
          [Community Show Top X]
     )
```

#### Capacity Measure Selection Title

##### Dependencies

**Referenced Columns**
- Capacity Measure Selection[Selection Fields]
- Capacity Measure Selection[Selection]

```dax
VAR _Selection =
     SELECTCOLUMNS(
          SUMMARIZE(
               'Capacity Measure Selection',
               'Capacity Measure Selection'[Selection],
               'Capacity Measure Selection'[Selection Fields]
          ),
          "SelectedName", 'Capacity Measure Selection'[Selection]
     )
VAR Choice =
     IF(
          COUNTROWS( _Selection ) = 1,
          _Selection
     )
RETURN
     Choice & " by month"
```

#### Adults Variance

##### Dependencies

**Referenced Columns**
- DataIntegrity[ADULTS VARIANCE]

```dax
CALCULATE(
     SUM( DataIntegrity[ADULTS VARIANCE] ),
     'Clients'
)
```

#### Children Variance

##### Dependencies

**Referenced Columns**
- DataIntegrity[CHILDREN VARIANCE]

```dax
CALCULATE(
     SUM( DataIntegrity[CHILDREN VARIANCE] ),
     'Clients'
)
```

#### Household Variance

##### Dependencies

**Referenced Columns**
- DataIntegrity[HOUSEHOLD VARIANCE]

```dax
CALCULATE(
     SUM( DataIntegrity[HOUSEHOLD VARIANCE] ),
     'Clients'
)
```

#### Clients with Census Variance

##### Dependencies

**Referenced Measures**
- Records Scanned

**Referenced Columns**
- DataIntegrity[Has_Variance]

```dax
CALCULATE(
     [Records Scanned],
     DataIntegrity[Has_Variance] = TRUE( )
)
```

#### Clients with Multiple Locations

##### Dependencies

**Referenced Measures**
- Records Scanned

**Referenced Columns**
- DataIntegrity[Multiple_Locations]

```dax
CALCULATE(
     [Records Scanned],
     DataIntegrity[Multiple_Locations]
          = TRUE( )
)
```

#### Records Scanned
```dax
COUNTROWS( DataIntegrity )
```

#### Records with Concerns

##### Dependencies

**Referenced Measures**
- Records Scanned

**Referenced Columns**
- DataIntegrity[Has_Concerns]

```dax
CALCULATE(
     [Records Scanned],
     DataIntegrity[Has_Concerns] = TRUE( )
)
```

#### MPR Only UIDs

##### Dependencies

**Referenced Columns**
- DataIntegrity[MPR Only]
- DataIntegrity[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          DataIntegrity[UNIQUE IDENTIFIER NUMBER]
     ),
     DataIntegrity[MPR Only] = TRUE( )
)
```

#### Age - 25 to 54

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[CLIENT AGE]

```dax
CALCULATE(
     [Enrollments],
     'MPR'[CLIENT AGE] >= 25
          && 'MPR'[CLIENT AGE] < 55
)
```

#### Name Mismatch

##### Dependencies

**Referenced Columns**
- DataIntegrity[NameMismatchFlag]
- DataIntegrity[UNIQUE IDENTIFIER NUMBER]

```dax
CALCULATE(
     DISTINCTCOUNT(
          DataIntegrity[UNIQUE IDENTIFIER NUMBER]
     ),
     DataIntegrity[NameMismatchFlag]
          = "Mismatch"
)
```

#### Enrollments (all ethnicity)

##### Dependencies

**Referenced Measures**
- Enrollments

**Referenced Columns**
- MPR[RACE_ETHNICITY]

```dax
CALCULATE(
     [Enrollments],
     ALLSELECTED( 'MPR'[RACE_ETHNICITY] )
)
```

#### Enrollments (Ethnicity Percent to total)

##### Dependencies

**Referenced Measures**
- Enrollments
- Enrollments (all ethnicity)

```dax
VAR result =
     DIVIDE(
          [Enrollments],
          [Enrollments (all ethnicity)]
     )
RETURN
     "( " & FORMAT( result, "#,0%" ) & " ) "
```

#### Hours

##### Dependencies

**Referenced Columns**
- StaffTime[DURATION]

```dax
SUM( StaffTime[DURATION] )
```

#### Staff Measure Selection Title

##### Dependencies

**Referenced Columns**
- Staff Measure Selection[Staff Measure Selection Fields]
- Staff Measure Selection[Staff Measure Selection]

```dax
VAR _Selection =
     SELECTCOLUMNS(
          SUMMARIZE(
               'Staff Measure Selection',
               'Staff Measure Selection'[Staff Measure Selection],
               'Staff Measure Selection'[Staff Measure Selection Fields]
          ),
          "SelectedName", 'Staff Measure Selection'[Staff Measure Selection]
     )
VAR Choice =
     IF(
          COUNTROWS( _Selection ) = 1,
          _Selection
     )
RETURN
     IF(
          Choice = "Activations",
          "Activations (from Intake form)",
          "Hours (from Staff Time Sheet)"
     )
```

#### Hours needing Research

##### Dependencies

**Referenced Columns**
- StaffTime[REVIEW]

```dax
CALCULATE(
     COUNTROWS( StaffTime ),
     StaffTime[REVIEW] = "Review"
)
```

#### Budget

##### Dependencies

**Referenced Columns**
- Financials[BUDGET]

```dax
SUM( Financials[BUDGET] )
```

#### Invested

##### Dependencies

**Referenced Columns**
- Financials[INVESTED]

```dax
SUM( Financials[INVESTED] )
```

#### Obligated

##### Dependencies

**Referenced Columns**
- Financials[OBLIGATED]

```dax
SUM( Financials[OBLIGATED] )
```

#### Actual

##### Dependencies

**Referenced Measures**
- Invested
- Obligated

```dax
[Invested] + [Obligated]
```

#### Actual v Budget

##### Dependencies

**Referenced Measures**
- Actual
- Budget

**Referenced Columns**
- dimDate[Month Sort]
- dimDate[Month Year]

```dax
VAR _monthYearSort =
     IF(
          HASONEVALUE( 'dimDate'[Month Year] )
               && ISBLANK( CALCULATE( [Actual] ) ),
          MAXX(
               FILTER(
                    ALL( 'dimDate' ),
                    NOT ISBLANK( CALCULATE( [Actual] ) )
                         || NOT ISBLANK( CALCULATE( [Budget] ) )
               ),
               'dimDate'[Month Sort]
          ),
          IF(
               HASONEVALUE( 'dimDate'[Month Year] ),
               SELECTEDVALUE( 'dimDate'[Month Sort] ),
               IF(
                    NOT ISFILTERED( 'dimDate'[Month Year] ),
                    MAXX(
                         FILTER(
                              ALL( 'dimDate' ),
                              NOT ISBLANK( CALCULATE( [Actual] ) )
                                   || NOT ISBLANK( CALCULATE( [Budget] ) )
                         ),
                         'dimDate'[Month Sort]
                    )
               )
          )
     )
VAR _monthYear =
     CALCULATE(
          MAX( 'dimDate'[Month Year] ),
          ALL( 'dimDate' ),
          'dimDate'[Month Sort] = _monthYearSort
     )
VAR _actual =
     CALCULATE(
          [Actual],
          ALL( 'dimDate' ),
          'dimDate'[Month Sort] = _monthYearSort
     )
VAR _budget =
     CALCULATE(
          [Budget],
          ALL( 'dimDate' ),
          'dimDate'[Month Sort] = _monthYearSort
     )
VAR _percent =
     DIVIDE( _actual, _budget, 0 )
VAR _actualPM =
     CALCULATE(
          [Actual],
          ALL( 'dimDate' ),
          'dimDate'[Month Sort]
               = _monthYearSort - 1
     )
VAR _actualPM2 =
     CALCULATE(
          [Actual],
          ALL( 'dimDate' ),
          'dimDate'[Month Sort]
               = _monthYearSort - 2
     )

-- Current month increase
VAR _currentIncrease =
     IF(
          ISBLANK( _actualPM )
               || ISBLANK( _actual ),
          BLANK( ),
          _actual - _actualPM
     )

-- Current month increase percent
VAR _increasePercent =
     DIVIDE( _currentIncrease, _actualPM )

-- Previous month increase
VAR _priorIncrease =
     IF(
          ISBLANK( _actualPM2 ),
          BLANK( ),
          _actualPM - _actualPM2
     )

-- Difference between increases
VAR _momChange =
     IF(
          ISBLANK( _priorIncrease ),
          BLANK( ),
          _currentIncrease - _priorIncrease
     )
VAR _momPercent =
     DIVIDE( _momChange, _priorIncrease )
VAR _actualText =
     "Actual: " & FORMAT( _actual, "$#,##0" )
VAR _budgetText =
     "Budget: " & FORMAT( _budget, "$#,##0" )
VAR _percentText = FORMAT( _percent, "0%" )
VAR _momArrow =
     SWITCH(
          TRUE( ),
          ISBLANK( _momChange ), "",
          _momChange > 0, "↗ ",
          _momChange < 0, "↘ ",
          "• "
     )
VAR _momText =
     "Trend: " & _momArrow
          & FORMAT( ABS( _momChange ), "$#,##0" )
          & " "
          & FORMAT( _momPercent, "0.0%; (0.0%)" )

-- Bar
VAR _percentClamped =
     MIN( MAX( _percent, 0 ), 1 )
VAR _barWidth =
     INT( 360 * _percentClamped )

-- Colors
VAR _bgColor = "#C6C6C6"
VAR _barColor = "#63C17A"
VAR _momColor =
     IF(
          _momChange >= 0,
          "#57B26C",
          "#9C0006"
     )
RETURN
     IF(
          ISBLANK( _actual ),
          BLANK( ),
          "data:image/svg+xml;utf8,"
               & "<svg width='590' height='100' viewBox='0 0 590 100' xmlns='http://www.w3.org/2000/svg'>"
               & "<!-- Title -->"
               & "<text x='50' y='14' font-size='18' fill='#615E9B' font-weight='bold'>"
               & _monthYear
               & "</text>"
               & "<!-- Actual -->"
               & "<text x='50' y='34' font-size='13' font-weight='bold'>"
               & "<tspan fill='#333'>"
               & _actualText
               & "</tspan>"
               & "<tspan fill='#57B26C'>"
               & " ( ▲ "
               & FORMAT( _currentIncrease, "$#,##0" )
               & "</tspan>"
               & "<tspan fill='#808080'>"
               & " | "
               & "</tspan>"
               & "<tspan fill='#57B26C'>"
               & "+"
               & FORMAT( _increasePercent, "#,#.0%" )
               & " )"
               & "</tspan>"
               & "</text>"
               & "<!-- Budget -->"
               & "<text x='540' y='34' font-size='13' fill='#333' font-weight='bold' text-anchor='end'>"
               & _budgetText
               & "</text>"
               & "<!-- Growth Trend -->"
               & "<text x='50' y='54' font-size='12' fill='"
               & _momColor
               & "' font-weight='bold'>"
               & _momText
               & "</text>"
               & "<!-- Background Bar -->"
               & "<rect x='50' y='68' width='360' height='16' rx='8' fill='"
               & _bgColor
               & "' />"
               & "<!-- Progress Bar -->"
               & "<rect x='50' y='68' width='"
               & INT( _barWidth )
               & "' height='14' rx='7' fill='"
               & _barColor
               & "' />"
               & "<!-- Percent -->"
               & "<text x='540' y='82' font-size='14' text-anchor='end' fill='#615E9B' font-weight='bold'>"
               & _percentText
               & " of budget"
               & "</text>"
               & "</svg>"
     )
```

#### Percent Actual

##### Dependencies

**Referenced Measures**
- Actual
- Budget

```dax
DIVIDE( [Actual], [Budget], 0 )
```

#### Blank
```dax
""
```

#### Monthly Actual

##### Dependencies

**Referenced Measures**
- Actual

**Referenced Columns**
- dimDate[Month Sort]

```dax
VAR _monthYearSort =
     SELECTEDVALUE( 'dimDate'[Month Sort] )
VAR _actual =
     CALCULATE(
          [Actual],
          ALL( 'dimDate' ),
          'dimDate'[Month Sort] = _monthYearSort
     )
VAR _actualPM =
     CALCULATE(
          [Actual],
          ALL( 'dimDate' ),
          'dimDate'[Month Sort]
               = _monthYearSort - 1
     )

-- Current month increase
VAR _currentIncrease =
     IF(
          ISBLANK( _actual )
               || ISBLANK( _actualPM ),
          BLANK( ),
          _actual - _actualPM
     )
RETURN
     _currentIncrease
```

## Activations

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 2
- Date Columns: 1
- Numeric Columns: 0

### Related Tables

- MPR
- dimDate

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| ACTIVATION INDICATOR | string | No | No |  |
| ACTIVATION ID | string | No | No |  |
| ACTIVATION DATE | dateTime | No | No |  |

## Capacity Measure Selection

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 0
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Selection |  | No | No | 'Capacity Measure Selection Order' |
| Selection Fields |  | No | No | 'Capacity Measure Selection Order' |
| Capacity Measure Selection Order |  | No | No |  |

## Clients

No description provided.

### Statistics

- Columns: 12
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 10
- Date Columns: 1
- Numeric Columns: 1

### Related Tables

- HMIS
- MPR

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| SOURCE | string | No | No |  |
| AGE | int64 | No | No |  |
| Census UID | string | No | No |  |
| Demographics UID | string | No | No |  |
| Community UID | string | No | No |  |
| CLIENT | string | No | No |  |
| FIRST NAME | string | No | No |  |
| LAST NAME | string | No | No |  |
| BIRTH DATE | dateTime | No | No |  |
| First_Cleaned | string | No | No |  |
| Last_Cleaned | string | No | No |  |
| UNIQUE IDENTIFIER NUMBER | string | No | No |  |

## Community

No description provided.

### Statistics

- Columns: 2
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 2
- Date Columns: 0
- Numeric Columns: 0

### Related Tables

- MPR

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| COMMUNITY | string | No | No |  |
| ZIPCODE | string | No | No |  |

## dimDate

No description provided.

### Statistics

- Columns: 10
- Measures: 0
- Relationships: 5
- Hidden Columns: 0

### Summary

- String Columns: 3
- Date Columns: 3
- Numeric Columns: 4

### Related Tables

- Activations
- HMIS
- Intake
- MPR

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Date | dateTime | No | No |  |
| Month Name | string | No | No |  |
| Month Number | int64 | No | No |  |
| Quarter | string | No | No |  |
| Month Sort | int64 | No | No |  |
| Month Year | dateTime | No | No |  |
| Year | int64 | No | No |  |
| Week Ending | dateTime | No | No |  |
| Weekday | string | No | No |  |
| Weekday number | int64 | No | No |  |

## HMIS

No description provided.

### Statistics

- Columns: 20
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 12
- Date Columns: 5
- Numeric Columns: 3

### Related Tables

- Clients
- dimDate

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| PROGRAM NAME | string | No | No |  |
| CLIENT | string | No | No |  |
| BIRTH DATE | dateTime | No | No |  |
| AGE AT ENTRY | int64 | No | No |  |
| CURRENT AGE | int64 | No | No |  |
| ENROLL DATE | dateTime | No | No |  |
| EXIT DATE | dateTime | No | No |  |
| LOS | int64 | No | No |  |
| HOUSING MOVE-IN | string | No | No |  |
| SERVICES | string | No | No |  |
| CASE NOTES | string | No | No |  |
| UNIT ASSIGNMENT | string | No | No |  |
| BED ASSIGNMENT | string | No | No |  |
| OCCUPANCY START DATE | dateTime | No | No |  |
| OCCUPANCY END DATE | dateTime | No | No |  |
| CHECK IN ID | string | No | No |  |
| ID | string | No | No |  |
| UNIQUE IDENTIFIER NUMBER | string | No | No |  |
| ASSIGNED STAFF | string | No | No |  |
| ASSESSMENTS | string | No | No |  |

## Intake

No description provided.

### Statistics

- Columns: 27
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 20
- Date Columns: 3
- Numeric Columns: 4

### Related Tables

- dimDate

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| STAFF NAME | string | No | No |  |
| HMIS UNIQUE IDENTIFIER | string | No | No |  |
| CONFIRMATION # | string | No | No |  |
| CHECK IN DATE | dateTime | No | No |  |
| # OF PETS | int64 | No | No |  |
| FIRST NAME | string | No | No |  |
| LAST NAME | string | No | No |  |
| DOB | dateTime | No | No |  |
| SSN | string | No | No |  |
| VALID ID | string | No | No |  |
| COMMUNITY | string | No | No |  |
| ZIPCODE | string | No | No |  |
| BLACK LIST | string | No | No |  |
| PHONE NUMBER | string | No | No |  |
| ALLOW TEXT | string | No | No |  |
| GENDER | string | No | No |  |
| RACE_ETHNICITY | string | No | No |  |
| VETERAN STATUS | string | No | No |  |
| DISABILITY | string | No | No |  |
| # OF ADULTS | int64 | No | No |  |
| # OF CHILDREN | int64 | No | No |  |
| # OF ROOMS NEEDED | int64 | No | No |  |
| TYPE OF PET | string | No | No |  |
| HOTEL PREFERRED | string | No | No |  |
| ADA ROOM | string | No | No |  |
| CHECK OUT DATE | dateTime | No | No |  |
| ID | string | No | No |  |

## MPR Dimension Selection

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 0
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Dimension |  | No | No | Order |
| Fields |  | No | No | Order |
| Order |  | No | No |  |

## MPR

No description provided.

### Statistics

- Columns: 37
- Measures: 0
- Relationships: 5
- Hidden Columns: 0

### Summary

- String Columns: 24
- Date Columns: 6
- Numeric Columns: 7

### Related Tables

- Activations
- Clients
- Community
- dimDate

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| RECORD ID | string | No | No |  |
| UNIQUE IDENTIFIER NUMBER | string | No | No |  |
| FIRST NAME | string | No | No |  |
| LAST NAME | string | No | No |  |
| HOTEL CHECK IN | dateTime | No | No |  |
| EXIT DATE | dateTime | No | No |  |
| NUMBER OF ADULTS | int64 | No | No |  |
| DATE OF BIRTH | dateTime | No | No |  |
| CLIENT AGE | int64 | No | No |  |
| GENDER | string | No | No |  |
| RACE_ETHNICITY | string | No | No |  |
| VETERAN | string | No | No |  |
| DISABILITY | string | No | No |  |
| COMMUNITY | string | No | No |  |
| ENROLLMENT DATE | dateTime | No | No |  |
| HOTEL NAME | string | No | No |  |
| NUMBER OF HOTEL ROOMS RENTED | int64 | No | No |  |
| NUMBER OF HOTEL NIGHTS | int64 | No | No |  |
| HOUSEHOLD | int64 | No | No |  |
| NUMBER OF CHILDREN | int64 | No | No |  |
| UID_SOURCE | string | No | No |  |
| LOS | string | No | No |  |
| TURNDOWNS | string | No | No |  |
| ACTIVATION ID | string | No | No |  |
| ACTIVATION INDICATOR | string | No | No |  |
| ACTIVATION DATE | dateTime | No | No |  |
| REFERRAL DATE | dateTime | No | No |  |
| ENROLLMENT WITHIN 30 MIN | string | No | No |  |
| TOTAL NIGHTS | int64 | No | No |  |
| TRANSPORTED SINCE REFERRAL WITHIN 6 HRS | string | No | No |  |
| TRANSPORTATION PROVIDED | string | No | No |  |
| ENROLLED THIS MONTH | string | No | No |  |
| ENROLLED THIS FY | string | No | No |  |
| CHECK IN ID | string | No | No |  |
| ID | string | No | No |  |
| ZIPCODE | string | No | No |  |
| DATE OF BIRTH - STRING | string | No | No |  |

## People Measure Selection

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 0
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Name |  | No | No | 'Sort Order' |
| Measure |  | No | No | 'Sort Order' |
| Sort Order |  | No | No |  |

## Staff Measure Selection

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 0
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Staff Measure Selection |  | No | No | 'Staff Measure Selection Order' |
| Staff Measure Selection Fields |  | No | No | 'Staff Measure Selection Order' |
| Staff Measure Selection Order |  | No | No |  |

## Top X

No description provided.

### Statistics

- Columns: 1
- Measures: 0
- Relationships: 0
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Top X |  | No | No |  |

# Relationships

| From | To | Cardinality | Direction | Active |
|---|---|---|---|---:|
| MPR[ACTIVATION ID] | Activations[ACTIVATION ID] | many to one | oneDirection | Yes |
| MPR[COMMUNITY] | Community[COMMUNITY] | many to one | oneDirection | Yes |
| HMIS[UNIQUE IDENTIFIER NUMBER] | Clients[UNIQUE IDENTIFIER NUMBER] | many to one | oneDirection | Yes |
| MPR[UNIQUE IDENTIFIER NUMBER] | Clients[UNIQUE IDENTIFIER NUMBER] | many to one | oneDirection | Yes |
| dimDate[Date] | Activations[ACTIVATION DATE] | one to one | bothDirections | Yes |
| HMIS[ENROLL DATE] | dimDate[Date] | many to one | oneDirection | Yes |
| Intake[CHECK IN DATE] | dimDate[Date] | many to one | oneDirection | Yes |
| MPR[HOTEL CHECK IN] | dimDate[Date] | many to one | oneDirection | No |
| MPR[ENROLLMENT DATE] | dimDate[Date] | many to one | oneDirection | No |

# Validation

- Model parsed successfully: Yes
- Errors: 0
- Warnings: 0
