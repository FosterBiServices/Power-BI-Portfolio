---
contextType: Power BI Semantic Model
schemaVersion: 1.0
generator: Semantic Model Context Builder
modelName: Terminations Examples
generatedUtc: 2026-09-24T02:35:36+00:00
---

# Semantic Model Instructions

Treat this file as the authoritative structural reference for this model.
Do not invent tables, columns, measures, or relationships that are not listed.
Use exact object names when proposing DAX.

# Model Summary

- Model: Terminations Examples
- Storage mode: Unknown
- Tables: 11
- Measure-Only Tables Remaining: 1
- Columns: 123
- Measures: 25
- Relationships: 8

## Model Profile

### Measure Dependencies Found

- Total Dependencies: 110

### Data Type Distribution

- string: 89
- int64: 18
- dateTime: 9
- Unknown: 5
- double: 2

### Most Connected Tables

1. dimLocationHierarchy (3 relationships)
2. Projects (3 relationships)
3. dimdate (2 relationships)
4. dimLocationCrosswalk (2 relationships)
5. Headcount (2 relationships)
6. Terms for TO details (2 relationships)
7. Companies (1 relationships)
8. ProjectsContractPeriod (1 relationships)
9. _Measures (0 relationships)
10. IncludeInactiveProject (0 relationships)

# Tables

## _Measures

No description provided.

### Statistics

- Columns: 0
- Measures: 25
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

#### Terms

##### Dependencies

**Referenced Columns**
- Terms for TO details[Employee ID]

```dax
COUNT(
     'Terms for TO details'[Employee ID]
)
```

#### Demographics header

##### Dependencies

**Referenced Columns**
- Termination Demographics[Demographic]

```dax
VAR _demographic =
     SELECTEDVALUE(
          'Termination Demographics'[Demographic],
          "Gender"
     )
VAR _title =
     SWITCH(
          _demographic,
          "Gender", "Gender (for Insurance Coverage)",
          "Race", "Race/Ethnicity",
          "Veteran", "Veteran Status",
          "Disability", "Disability Status",
          "Generation", "Generation",
          "Age", "Age (Bands)",
          "Gender"
     )
RETURN
     "Terminations by " & _title
```

#### Drillthrough Breadcrumb HTML

##### Dependencies

**Referenced Measures**
- Value

**Referenced Columns**
- Projects[Project Name]
- Projects[VP Name]
- Terms for TO details[Age Band]
- Terms for TO details[Disability Status]
- Terms for TO details[Gender for Insurance Coverage]
- Terms for TO details[Generation]
- Terms for TO details[Race/Ethnicity]
- Terms for TO details[Tenure Band]
- Terms for TO details[Termination Reason]
- Terms for TO details[Veteran Status]
- dimdate[Month Year]

```dax
VAR _ProjectValues =
     VALUES( 'Projects'[Project Name] )
VAR _ProjectCount =
     COUNTROWS( _ProjectValues )
VAR _Project =
     IF(
          ISFILTERED( 'Projects'[Project Name] ),
          "<span class='pill context'>Project: "
               & SWITCH(
                    TRUE( ),
                    _ProjectCount > 2, "Multiple Selections",
                    _ProjectCount = 2,
                         CONCATENATEX(
                              _ProjectValues,
                              'Projects'[Project Name],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Projects'[Project Name]
                    )
               )
               & "</span>"
     )
VAR _VPValues =
     VALUES( 'Projects'[VP Name] )
VAR _VPCount = COUNTROWS( _VPValues )
VAR _VP =
     IF(
          ISFILTERED( 'Projects'[VP Name] ),
          "<span class='pill context'>VP: "
               & SWITCH(
                    TRUE( ),
                    _VPCount > 2, "Multiple Selections",
                    _VPCount = 2,
                         CONCATENATEX(
                              _VPValues,
                              'Projects'[VP Name],
                              ", "
                         ),
                    SELECTEDVALUE( 'Projects'[VP Name] )
               )
               & "</span>"
     )
VAR _MonthYearValues =
     VALUES( 'dimdate'[Month Year] )
VAR _MonthYearCount =
     COUNTROWS( _MonthYearValues )
VAR _MonthYear =
     IF(
          ISFILTERED( 'dimdate'[Month Year] ),
          "<span class='pill context'>Month: "
               & SWITCH(
                    TRUE( ),
                    _MonthYearCount > 2, "Multiple Selections",
                    _MonthYearCount = 2,
                         CONCATENATEX(
                              _MonthYearValues,
                              'dimdate'[Month Year],
                              ", "
                         ),
                    SELECTEDVALUE( 'dimdate'[Month Year] )
               )
               & "</span>"
     )
VAR _ReasonValues =
     VALUES(
          'Terms for TO details'[Termination Reason]
     )
VAR _ReasonCount =
     COUNTROWS( _ReasonValues )
VAR _Reason =
     IF(
          ISFILTERED(
               'Terms for TO details'[Termination Reason]
          ),
          "<span class='pill termination'>Reason: "
               & SWITCH(
                    TRUE( ),
                    _ReasonCount > 2, "Multiple Selections",
                    _ReasonCount = 2,
                         CONCATENATEX(
                              _ReasonValues,
                              'Terms for TO details'[Termination Reason],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Termination Reason]
                    )
               )
               & "</span>"
     )
VAR _TenureValues =
     VALUES(
          'Terms for TO details'[Tenure Band]
     )
VAR _TenureCount =
     COUNTROWS( _TenureValues )
VAR _Tenure =
     IF(
          ISFILTERED(
               'Terms for TO details'[Tenure Band]
          ),
          "<span class='pill termination'>Tenure: "
               & SWITCH(
                    TRUE( ),
                    _TenureCount > 2, "Multiple Selections",
                    _TenureCount = 2,
                         CONCATENATEX(
                              _TenureValues,
                              'Terms for TO details'[Tenure Band],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Tenure Band]
                    )
               )
               & "</span>"
     )
VAR _GenderValues =
     VALUES(
          'Terms for TO details'[Gender for Insurance Coverage]
     )
VAR _GenderCount =
     COUNTROWS( _GenderValues )
VAR _Gender =
     IF(
          ISFILTERED(
               'Terms for TO details'[Gender for Insurance Coverage]
          ),
          "<span class='pill demographic'>Gender: "
               & SWITCH(
                    TRUE( ),
                    _GenderCount > 2, "Multiple Selections",
                    _GenderCount = 2,
                         CONCATENATEX(
                              _GenderValues,
                              'Terms for TO details'[Gender for Insurance Coverage],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Gender for Insurance Coverage]
                    )
               )
               & "</span>"
     )
VAR _RaceValues =
     VALUES(
          'Terms for TO details'[Race/Ethnicity]
     )
VAR _RaceCount = COUNTROWS( _RaceValues )
VAR _Race =
     IF(
          ISFILTERED(
               'Terms for TO details'[Race/Ethnicity]
          ),
          "<span class='pill demographic'>Race: "
               & SWITCH(
                    TRUE( ),
                    _RaceCount > 2, "Multiple Selections",
                    _RaceCount = 2,
                         CONCATENATEX(
                              _RaceValues,
                              'Terms for TO details'[Race/Ethnicity],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Race/Ethnicity]
                    )
               )
               & "</span>"
     )
VAR _VeteranValues =
     VALUES(
          'Terms for TO details'[Veteran Status]
     )
VAR _VeteranCount =
     COUNTROWS( _VeteranValues )
VAR _Veteran =
     IF(
          ISFILTERED(
               'Terms for TO details'[Veteran Status]
          ),
          "<span class='pill demographic'>Veteran: "
               & SWITCH(
                    TRUE( ),
                    _VeteranCount > 2, "Multiple Selections",
                    _VeteranCount = 2,
                         CONCATENATEX(
                              _VeteranValues,
                              'Terms for TO details'[Veteran Status],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Veteran Status]
                    )
               )
               & "</span>"
     )
VAR _DisabilityValues =
     VALUES(
          'Terms for TO details'[Disability Status]
     )
VAR _DisabilityCount =
     COUNTROWS( _DisabilityValues )
VAR _Disability =
     IF(
          ISFILTERED(
               'Terms for TO details'[Disability Status]
          ),
          "<span class='pill demographic'>Disability: "
               & SWITCH(
                    TRUE( ),
                    _DisabilityCount > 2, "Multiple Selections",
                    _DisabilityCount = 2,
                         CONCATENATEX(
                              _DisabilityValues,
                              'Terms for TO details'[Disability Status],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Disability Status]
                    )
               )
               & "</span>"
     )
VAR _GenerationValues =
     VALUES(
          'Terms for TO details'[Generation]
     )
VAR _GenerationCount =
     COUNTROWS( _GenerationValues )
VAR _Generation =
     IF(
          ISFILTERED(
               'Terms for TO details'[Generation]
          ),
          "<span class='pill demographic'>Generation: "
               & SWITCH(
                    TRUE( ),
                    _GenerationCount > 2, "Multiple Selections",
                    _GenerationCount = 2,
                         CONCATENATEX(
                              _GenerationValues,
                              'Terms for TO details'[Generation],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Generation]
                    )
               )
               & "</span>"
     )
VAR _AgeBandValues =
     VALUES(
          'Terms for TO details'[Age Band]
     )
VAR _AgeBandCount =
     COUNTROWS( _AgeBandValues )
VAR _AgeBand =
     IF(
          ISFILTERED(
               'Terms for TO details'[Age Band]
          ),
          "<span class='pill demographic'>Age: "
               & SWITCH(
                    TRUE( ),
                    _AgeBandCount > 2, "Multiple Selections",
                    _AgeBandCount = 2,
                         CONCATENATEX(
                              _AgeBandValues,
                              'Terms for TO details'[Age Band],
                              ", "
                         ),
                    SELECTEDVALUE(
                         'Terms for TO details'[Age Band]
                    )
               )
               & "</span>"
     )
VAR _Breadcrumbs =
     CONCATENATEX(
          FILTER(
               {
                    _Project,
                    _VP,
                    _MonthYear,
                    _Reason,
                    _Tenure,
                    _Gender,
                    _Race,
                    _Veteran,
                    _Disability,
                    _Generation,
                    _AgeBand
               },
               NOT ISBLANK( [Value] )
          ),
          [Value],
          " "
     )
RETURN
     "
<style>

.container{
    width:100%;
    font-family:'Segoe UI';
    line-height:1.3;
}

.pill{
    display:inline-block;
    padding:3px 8px;
    border-radius:999px;
    margin-right:6px;
    margin-bottom:4px;
    font-size:10px;
    font-weight:600;
    white-space:nowrap;
}

.context{
    background:#E5F1FB;
    border:1px solid #C7E0F4;
    color:#003366;
}

.termination{
    background:#FFF4CE;
    border:1px solid #FCE100;
    color:#8A6D00;
}

.demographic{
    background:#E6F4EA;
    border:1px solid #B7E1C1;
    color:#107C10;
}

</style>

<div class='container'>
"
          & _Breadcrumbs
          & "
</div>
"
```

#### First Year Terms

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Terms for TO details[Tenure Band]

```dax
CALCULATE(
     [Terms Project Level],
     'Terms for TO details'[Tenure Band]
          = "Under 1 Year"
)
```

#### First Year Terms Rate Project Level

##### Dependencies

**Referenced Measures**
- First Year Terms
- Headcount 12 Months Ago Project Level

```dax
DIVIDE(
     [First Year Terms],
     [Headcount 12 Months Ago Project Level]
)
```

#### First Year Terms Subtitle

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Terms for TO details[Tenure Band]

```dax
VAR _FirstYearTerms =
     CALCULATE(
          [Terms Project Level],
          KEEPFILTERS(
               'Terms for TO details'[Tenure Band]
                    = "Under 1 Years"
          )
     )
VAR _TotalTerms =
     CALCULATE(
          [Terms Project Level],
          REMOVEFILTERS(
               'Terms for TO details'[Tenure Band]
          )
     )
VAR _Percent =
     DIVIDE( _FirstYearTerms, _TotalTerms )
RETURN
     FORMAT( _Percent, "0.0%" )
          & " of terminations occurred within the first year."
```

#### FirstYearTerms HTML

##### Dependencies

**Referenced Measures**
- First Year Terms
- First Year Terms Rate Project Level
- Headcount 12 Months Ago Project Level

```dax
VAR _FirstYearTerms =
     FORMAT( [First Year Terms], "#,##0" )
VAR _Hires =
     FORMAT(
          [Headcount 12 Months Ago Project Level],
          "#,##0"
     )
VAR _Pct =
     FORMAT(
          [First Year Terms Rate Project Level],
          "0.0%"
     )
RETURN
     "
<div style='
    width:330px;
    height:82px;
    padding:5px 20px;
    box-sizing:border-box;
    font-family:Segoe UI;
    position:relative;
    background:transparent;
'>

    <div style='
        display:flex;
        justify-content:space-between;
        align-items:flex-start;
        flex:1;
    '>

        <div>
            <div style='
                font-size:42px;
                font-weight:700;
                color:#666666;
                line-height:36px;
            '>
                "
          & _FirstYearTerms
          & "
            </div>

            <div style='
                font-size:12px;
                font-weight:600;
                color:#003366;
                margin-top:2px;
            '>
                First Year Terms
            </div>
        </div>

        <div style='
            display:flex;
            flex-direction:column;
            align-items:flex-end;
            gap:3px;
        '>

            <div>
                <div style='
                    font-size:16px;
                    font-weight:700;
                    color:#666666;
                    text-align:right;
                    line-height:16px;
                '>
                    "
          & _Hires
          & "
                </div>

                <div style='
                    font-size:11px;
                    font-weight:600;
                    color:#003366;
                    text-align:right;
                '>
                    Avg. Headcount L12M
                </div>
            </div>

            <div style='
                display:flex;
                align-items:center;
                gap:6px;
            '>

                <span style='
                    font-size:11px;
                    font-weight:600;
                    color:#003366;
                '>
                    FY Terms %
                </span>

                <span style='
                    font-size:13px;
                    font-weight:700;
                    color:#9C0006;
                    background:#FFC7CE;
                    padding:1px 6px;
                    border-radius:3px;
                '>
                    "
          & _Pct
          & "
                </span>

            </div>

        </div>

            </div>
                <div style='
                    font-size:9px;
                    color:#999999;
                    text-align:center;
                    width:100%;
                    margin-top:auto;
                    padding-bottom:5px;
                '>
                    * Avg Headcount is affected only by Project and VP selections.
                </div>
    </div>
"
```

#### FT Terms Project Level

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Terms for TO details[Worker Category]

```dax
CALCULATE(
     [Terms Project Level],
     'Terms for TO details'[Worker Category]
          = "FT - Full Time"
)
```

#### Headcount 12 Months Ago Project Level

##### Dependencies

**Referenced Columns**
- Headcount[Headcount]
- dimdate[Date]

```dax
CALCULATE(
     AVERAGEX(
          VALUES( 'dimdate'[Date] ),
          CALCULATE(
               SUM( 'Headcount'[Headcount] ),
               'Headcount'[Headcount] <> 0
          )
     ),
     DATESINPERIOD(
          'dimdate'[Date],
          LASTDATE( 'dimdate'[Date] ),
          -12,
          MONTH
     )
)
```

#### OTHER Terms Project Level

##### Dependencies

**Referenced Measures**
- FT Terms Project Level
- PT Terms Project Level
- Terms Project Level

```dax
[Terms Project Level]
     - [PT Terms Project Level]
     - [FT Terms Project Level]
```

#### PT Terms Project Level

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Terms for TO details[Worker Category]

```dax
CALCULATE(
     [Terms Project Level],
     'Terms for TO details'[Worker Category]
          = "PT - Part Time"
)
```

#### Termination Narrative Summary HTML

##### Dependencies

**Referenced Measures**
- @Month
- @Project
- @ProjectTerms
- @Reason
- @ReasonTerms
- @ReasonTermsValue
- @Terms
- Terms Project Level

**Referenced Columns**
- Projects[Project Name]
- Terms for TO details[Age Band]
- Terms for TO details[Disability Status]
- Terms for TO details[Gender for Insurance Coverage]
- Terms for TO details[Generation]
- Terms for TO details[Race/Ethnicity]
- Terms for TO details[Termination Reason]
- Terms for TO details[Termination Type]
- Terms for TO details[Veteran Status]
- dimdate[Fiscal Period]
- dimdate[Month Sort]
- dimdate[Month Year]

```dax
VAR _voluntaryMonthReason =
     TOPN(
          1,
          FILTER(
               SUMMARIZECOLUMNS(
                    'dimdate'[Fiscal Period],
                    'dimdate'[Month Year],
                    'Terms for TO details'[Termination Reason],
                    'Terms for TO details'[Termination Type],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && 'Terms for TO details'[Termination Type]
                    = "Voluntary"
                    && NOT ISBLANK(
                         'Terms for TO details'[Termination Reason]
                    )
          ),
          [@Terms], DESC,
          'dimdate'[Month Year], ASC,
          'Terms for TO details'[Termination Reason], ASC
     )
VAR _voluntaryMonthReasonText =
     CONCATENATEX(
          _voluntaryMonthReason,
          "<li><strong>Voluntary:</strong> "
               & 'dimdate'[Fiscal Period]
               & " for <strong>"
               & 'Terms for TO details'[Termination Reason]
               & "</strong>: "
               & FORMAT( [@Terms], "#,0" )
               & " terms</li>",
          "",
          [@Terms], DESC,
          'dimdate'[Month Year], ASC
     )
VAR _involuntaryMonthReason =
     TOPN(
          1,
          FILTER(
               SUMMARIZECOLUMNS(
                    'dimdate'[Fiscal Period],
                    'dimdate'[Month Year],
                    'Terms for TO details'[Termination Reason],
                    'Terms for TO details'[Termination Type],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && 'Terms for TO details'[Termination Type]
                    = "Involuntary"
                    && NOT ISBLANK(
                         'Terms for TO details'[Termination Reason]
                    )
          ),
          [@Terms], DESC,
          'dimdate'[Month Year], ASC,
          'Terms for TO details'[Termination Reason], ASC
     )
VAR _involuntaryMonthReasonText =
     CONCATENATEX(
          _involuntaryMonthReason,
          "<li><strong>Involuntary:</strong> "
               & 'dimdate'[Fiscal Period]
               & " for <strong>"
               & 'Terms for TO details'[Termination Reason]
               & "</strong>: "
               & FORMAT( [@Terms], "#,0" )
               & " terms</li>",
          "",
          [@Terms], DESC,
          'dimdate'[Month Year], ASC
     )
VAR _monthTypeReasonText =
     _voluntaryMonthReasonText
          & _involuntaryMonthReasonText
VAR _voluntaryReason =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Termination Reason],
                    'Terms for TO details'[Termination Type],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && 'Terms for TO details'[Termination Type]
                    = "Voluntary"
                    && NOT ISBLANK(
                         'Terms for TO details'[Termination Reason]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Termination Reason], ASC
     )
VAR _voluntaryReasonText =
     CONCATENATEX(
          _voluntaryReason,
          "<li>"
               & 'Terms for TO details'[Termination Reason]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & " terms</li>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Termination Reason], ASC
     )
VAR _involuntaryReason =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Termination Reason],
                    'Terms for TO details'[Termination Type],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && 'Terms for TO details'[Termination Type]
                    = "Involuntary"
                    && NOT ISBLANK(
                         'Terms for TO details'[Termination Reason]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Termination Reason], ASC
     )
VAR _involuntaryReasonText =
     CONCATENATEX(
          _involuntaryReason,
          "<li>"
               & 'Terms for TO details'[Termination Reason]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & " terms</li>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Termination Reason], ASC
     )
VAR _last3Months =
     TOPN(
          3,
          VALUES( 'dimdate'[Month Sort] ),
          'dimdate'[Month Sort], DESC
     )
VAR _topProjectByMonth =
     ADDCOLUMNS(
          _last3Months,
          "@Project",
               VAR _monthSort = 'dimdate'[Month Sort]
               RETURN
                    MAXX(
                         TOPN(
                              1,
                              SUMMARIZE(
                                   FILTER(
                                        ALL( 'Projects'[Project Name] ),
                                        NOT ISBLANK( 'Projects'[Project Name] )
                                   ),
                                   'Projects'[Project Name],
                                   "@Terms",
                                        CALCULATE(
                                             [Terms Project Level],
                                             'dimdate'[Month Sort] = _monthSort
                                        )
                              ),
                              [@Terms], DESC,
                              'Projects'[Project Name], ASC
                         ),
                         'Projects'[Project Name]
                    ),
          "@Terms",
               VAR _monthSort = 'dimdate'[Month Sort]
               RETURN
                    MAXX(
                         TOPN(
                              1,
                              SUMMARIZE(
                                   FILTER(
                                        ALL( 'Projects'[Project Name] ),
                                        NOT ISBLANK( 'Projects'[Project Name] )
                                   ),
                                   'Projects'[Project Name],
                                   "@Terms",
                                        CALCULATE(
                                             [Terms Project Level],
                                             'dimdate'[Month Sort] = _monthSort
                                        )
                              ),
                              [@Terms], DESC,
                              'Projects'[Project Name], ASC
                         ),
                         [@Terms]
                    ),
          "@Month",
               CALCULATE(
                    MAX( 'dimdate'[Month Year] ),
                    'dimdate'[Month Sort]
                         = EARLIER( 'dimdate'[Month Sort] )
               )
     )
VAR _projectMonthText =
     CONCATENATEX(
          _topProjectByMonth,
          "<li><strong>" & [@Month]
               & "</strong>: <strong>"
               & [@Project]
               & "</strong>: "
               & FORMAT( [@Terms], "#,0" )
               & " terms</li>",
          "",
          'dimdate'[Month Sort], DESC
     )
VAR _gender =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Gender for Insurance Coverage],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && NOT ISBLANK(
                         'Terms for TO details'[Gender for Insurance Coverage]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Gender for Insurance Coverage], ASC
     )
VAR _genderText =
     CONCATENATEX(
          _gender,
          "<span class='tag'>"
               & 'Terms for TO details'[Gender for Insurance Coverage]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & "</span>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Gender for Insurance Coverage], ASC
     )
VAR _race =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Race/Ethnicity],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && NOT ISBLANK(
                         'Terms for TO details'[Race/Ethnicity]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Race/Ethnicity], ASC
     )
VAR _raceText =
     CONCATENATEX(
          _race,
          "<span class='tag'>"
               & 'Terms for TO details'[Race/Ethnicity]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & "</span>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Race/Ethnicity], ASC
     )
VAR _age =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Age Band],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && NOT ISBLANK(
                         'Terms for TO details'[Age Band]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Age Band], ASC
     )
VAR _ageText =
     CONCATENATEX(
          _age,
          "<span class='tag'>"
               & 'Terms for TO details'[Age Band]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & "</span>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Age Band], ASC
     )
VAR _veteran =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Veteran Status],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && NOT ISBLANK(
                         'Terms for TO details'[Veteran Status]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Veteran Status], ASC
     )
VAR _veteranText =
     CONCATENATEX(
          _veteran,
          "<span class='tag'>"
               & 'Terms for TO details'[Veteran Status]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & "</span>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Veteran Status], ASC
     )
VAR _disability =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Disability Status],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && NOT ISBLANK(
                         'Terms for TO details'[Disability Status]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Disability Status], ASC
     )
VAR _disabilityText =
     CONCATENATEX(
          _disability,
          "<span class='tag'>"
               & 'Terms for TO details'[Disability Status]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & "</span>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Disability Status], ASC
     )
VAR _generation =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Generation],
                    "@Terms", [Terms Project Level]
               ),
               NOT ISBLANK( [@Terms] ) && [@Terms] > 0
                    && NOT ISBLANK(
                         'Terms for TO details'[Generation]
                    )
          ),
          [@Terms], DESC,
          'Terms for TO details'[Generation], ASC
     )
VAR _generationText =
     CONCATENATEX(
          _generation,
          "<span class='tag'>"
               & 'Terms for TO details'[Generation]
               & ": "
               & FORMAT( [@Terms], "#,0" )
               & "</span>",
          "",
          [@Terms], DESC,
          'Terms for TO details'[Generation], ASC
     )

// Rank the top three projects by total voluntary termination volume.
VAR _voluntaryProject =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Projects'[Project Name],
                    'Terms for TO details'[Termination Type],
                    "@ProjectTerms", [Terms Project Level]
               ),
               NOT ISBLANK( [@ProjectTerms] )
                    && [@ProjectTerms] > 0
                    && 'Terms for TO details'[Termination Type]
                    = "Voluntary"
                    && NOT ISBLANK( 'Projects'[Project Name] )
          ),
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )

// Add the leading voluntary reason and its count for each ranked project.
VAR _voluntaryProjectReason =
     ADDCOLUMNS(
          _voluntaryProject,
          "@Reason",
               VAR _project = 'Projects'[Project Name]
               VAR _reasonTable =
                    TOPN(
                         1,
                         FILTER(
                              CALCULATETABLE(
                                   SUMMARIZECOLUMNS(
                                        'Terms for TO details'[Termination Reason],
                                        "@ReasonTerms", [Terms Project Level]
                                   ),
                                   'Projects'[Project Name] = _project,
                                   'Terms for TO details'[Termination Type]
                                        = "Voluntary"
                              ),
                              NOT ISBLANK(
                                   'Terms for TO details'[Termination Reason]
                              )
                                   && [@ReasonTerms] > 0
                         ),
                         [@ReasonTerms], DESC,
                         'Terms for TO details'[Termination Reason], ASC
                    )
               RETURN
                    MAXX(
                         _reasonTable,
                         'Terms for TO details'[Termination Reason]
                    ),
          "@ReasonTerms",
               VAR _project = 'Projects'[Project Name]
               VAR _reasonTable =
                    TOPN(
                         1,
                         FILTER(
                              CALCULATETABLE(
                                   SUMMARIZECOLUMNS(
                                        'Terms for TO details'[Termination Reason],
                                        "@ReasonTermsValue", [Terms Project Level]
                                   ),
                                   'Projects'[Project Name] = _project,
                                   'Terms for TO details'[Termination Type]
                                        = "Voluntary"
                              ),
                              NOT ISBLANK(
                                   'Terms for TO details'[Termination Reason]
                              )
                                   && [@ReasonTermsValue] > 0
                         ),
                         [@ReasonTermsValue], DESC,
                         'Terms for TO details'[Termination Reason], ASC
                    )
               RETURN
                    MAXX(
                         _reasonTable,
                         [@ReasonTermsValue]
                    )
     )
VAR _voluntaryProjectText =
     CONCATENATEX(
          _voluntaryProjectReason,
          "<li><strong>"
               & 'Projects'[Project Name]
               & "</strong> | "
               & [@Reason]
               & ": "
               & FORMAT( [@ReasonTerms], "#,0" )
               & " terms</li>",
          "",
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )

// Rank the top three projects by total involuntary termination volume.
VAR _involuntaryProject =
     TOPN(
          3,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Projects'[Project Name],
                    'Terms for TO details'[Termination Type],
                    "@ProjectTerms", [Terms Project Level]
               ),
               NOT ISBLANK( [@ProjectTerms] )
                    && [@ProjectTerms] > 0
                    && 'Terms for TO details'[Termination Type]
                    = "Involuntary"
                    && NOT ISBLANK( 'Projects'[Project Name] )
          ),
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )

// Add the leading involuntary reason and its count for each ranked project.
VAR _involuntaryProjectReason =
     ADDCOLUMNS(
          _involuntaryProject,
          "@Reason",
               VAR _project = 'Projects'[Project Name]
               VAR _reasonTable =
                    TOPN(
                         1,
                         FILTER(
                              CALCULATETABLE(
                                   SUMMARIZECOLUMNS(
                                        'Terms for TO details'[Termination Reason],
                                        "@ReasonTerms", [Terms Project Level]
                                   ),
                                   'Projects'[Project Name] = _project,
                                   'Terms for TO details'[Termination Type]
                                        = "Involuntary"
                              ),
                              NOT ISBLANK(
                                   'Terms for TO details'[Termination Reason]
                              )
                                   && [@ReasonTerms] > 0
                         ),
                         [@ReasonTerms], DESC,
                         'Terms for TO details'[Termination Reason], ASC
                    )
               RETURN
                    MAXX(
                         _reasonTable,
                         'Terms for TO details'[Termination Reason]
                    ),
          "@ReasonTerms",
               VAR _project = 'Projects'[Project Name]
               VAR _reasonTable =
                    TOPN(
                         1,
                         FILTER(
                              CALCULATETABLE(
                                   SUMMARIZECOLUMNS(
                                        'Terms for TO details'[Termination Reason],
                                        "@ReasonTermsValue", [Terms Project Level]
                                   ),
                                   'Projects'[Project Name] = _project,
                                   'Terms for TO details'[Termination Type]
                                        = "Involuntary"
                              ),
                              NOT ISBLANK(
                                   'Terms for TO details'[Termination Reason]
                              )
                                   && [@ReasonTermsValue] > 0
                         ),
                         [@ReasonTermsValue], DESC,
                         'Terms for TO details'[Termination Reason], ASC
                    )
               RETURN
                    MAXX(
                         _reasonTable,
                         [@ReasonTermsValue]
                    )
     )
VAR _involuntaryProjectText =
     CONCATENATEX(
          _involuntaryProjectReason,
          "<li><strong>"
               & 'Projects'[Project Name]
               & "</strong> | "
               & [@Reason]
               & ": "
               & FORMAT( [@ReasonTerms], "#,0" )
               & " terms</li>",
          "",
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )
RETURN
     "<div style='font-family: Segoe UI, Arial, sans-serif; color: #252423; line-height: 1.35; padding: 14px 16px; width: 100%; box-sizing: border-box;'>"
          & "<style>"
          & ".summary-title { font-size: 22px; font-weight: 700; color: #201f1e; margin-bottom: 4px; }"
          & ".summary-subtitle { font-size: 12px; color: #605e5c; margin-bottom: 14px; }"
          & ".summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; width: 100%; }"
          & ".summary-card { background-color: #F8F9FB; border-radius: 6px; padding: 12px 14px; min-height: 132px; box-sizing: border-box; }"
          & ".summary-card.context { border-left: 4px solid #C7E0F4; }"
          & ".summary-card.termination { border-left: 4px solid #FCE100; }"
          & ".summary-card.demographic { grid-column: 1 / span 2; border-left: 4px solid #B7E1C1; padding: 8px 10px; }"
          & ".section-title { font-size: 14px; font-weight: 700; color: #323130; margin: 0 0 6px 0; }"
          & ".section-subtitle { font-size: 11px; color: #605e5c; margin-bottom: 6px; }"
          & ".summary-list { margin: 4px 0 0 18px; padding: 0; font-size: 12px; }"
          & ".summary-list li { margin-bottom: 5px; }"
          & ".tag { display: inline-block; background-color: #EEF6FC; color: #201F1E; border: 1px solid #C7E0F4; border-radius: 12px; padding: 2px 6px; margin: 1px 2px 1px 0; font-size: 11px; }"
          & ".demo-label { font-size: 12px; font-weight: 700; color: #323130; margin-top: 2px; margin-bottom: 0; }"
          & ".demographic-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; width: 100%; }"
          & ".demographic-item { min-width: 0; }"
          & ".empty { color: #A4262C; font-size: 12px; }"
          & "</style>"
          & "<div class='summary-title'>Key Termination Drivers</div>"
          & "<div class='summary-subtitle'>Top termination activity based on the current report filters.</div>"
          & "<div class='summary-grid'>"
          & "<div class='summary-card context'>"
          & "<div class='section-title'>Highest Month By Type</div>"
          & "<div class='section-subtitle'>Highest monthly termination activity for voluntary and involuntary terms, including the leading reason.</div>"
          & IF(
               LEN( _monthTypeReasonText ) > 0,
               "<ul class='summary-list'>"
                    & _monthTypeReasonText
                    & "</ul>",
               "<div class='empty'>No voluntary or involuntary month activity is available for the current filters.</div>"
          )
          & "</div>"
          & "<div class='summary-card context'>"
          & "<div class='section-title'>Top Projects By Month</div>"
          & "<div class='section-subtitle'>Leading project by termination volume during the last three months.</div>"
          & IF(
               LEN( _projectMonthText ) > 0,
               "<ul class='summary-list'>"
                    & _projectMonthText
                    & "</ul>",
               "<div class='empty'>No project and month activity is available for the current filters.</div>"
          )
          & "</div>"
          & "<div class='summary-card termination'>"
          & "<div class='section-title'>Top Reasons By Type</div>"
          & "<div class='section-subtitle'>Top termination reasons within voluntary and involuntary categories.</div>"
          & "<div class='demo-label'>Voluntary</div>"
          & IF(
               LEN( _voluntaryReasonText ) > 0,
               "<ul class='summary-list'>"
                    & _voluntaryReasonText
                    & "</ul>",
               "<div class='empty'>No voluntary reason activity is available for the current filters.</div>"
          )
          & "<div class='demo-label'>Involuntary</div>"
          & IF(
               LEN( _involuntaryReasonText ) > 0,
               "<ul class='summary-list'>"
                    & _involuntaryReasonText
                    & "</ul>",
               "<div class='empty'>No involuntary reason activity is available for the current filters.</div>"
          )
          & "</div>"
          & "<div class='summary-card termination'>"
          & "<div class='section-title'>Top Projects By Type</div>"
          & "<div class='section-subtitle'>Top three projects within each termination type, including the leading termination reason.</div>"
          & "<div class='demo-label'>Voluntary</div>"
          & IF(
               LEN( _voluntaryProjectText ) > 0,
               "<ul class='summary-list'>"
                    & _voluntaryProjectText
                    & "</ul>",
               "<div class='empty'>No voluntary project activity is available for the current filters.</div>"
          )
          & "<div class='demo-label'>Involuntary</div>"
          & IF(
               LEN( _involuntaryProjectText ) > 0,
               "<ul class='summary-list'>"
                    & _involuntaryProjectText
                    & "</ul>",
               "<div class='empty'>No involuntary project activity is available for the current filters.</div>"
          )
          & "</div>"
          & "<div class='summary-card demographic'>"
          & "<div class='section-title'>Overall Demographics</div>"
          & "<div class='section-subtitle'>Largest termination groups by demographic category.</div>"
          & "<div class='demographic-grid'>"
          & "<div class='demographic-item'>"
          & "<div class='demo-label'>Gender</div>"
          & IF(
               LEN( _genderText ) > 0,
               _genderText,
               "<div class='empty'>No gender values are available.</div>"
          )
          & "</div>"
          & "<div class='demographic-item'>"
          & "<div class='demo-label'>Veteran Status</div>"
          & IF(
               LEN( _veteranText ) > 0,
               _veteranText,
               "<div class='empty'>No veteran status values are available.</div>"
          )
          & "</div>"
          & "<div class='demographic-item'>"
          & "<div class='demo-label'>Race/Ethnicity</div>"
          & IF(
               LEN( _raceText ) > 0,
               _raceText,
               "<div class='empty'>No race/ethnicity values are available.</div>"
          )
          & "</div>"
          & "<div class='demographic-item'>"
          & "<div class='demo-label'>Disability Status</div>"
          & IF(
               LEN( _disabilityText ) > 0,
               _disabilityText,
               "<div class='empty'>No disability status values are available.</div>"
          )
          & "</div>"
          & "<div class='demographic-item'>"
          & "<div class='demo-label'>Age Band</div>"
          & IF(
               LEN( _ageText ) > 0,
               _ageText,
               "<div class='empty'>No age band values are available.</div>"
          )
          & "</div>"
          & "<div class='demographic-item'>"
          & "<div class='demo-label'>Generation</div>"
          & IF(
               LEN( _generationText ) > 0,
               _generationText,
               "<div class='empty'>No generation values are available.</div>"
          )
          & "</div>"
          & "</div>"
          & "</div>"
          & "</div>"
          & "</div>"
```

#### Termination Reason Tooltip HTML

##### Dependencies

**Referenced Measures**
- @MonthTerms
- @ProjectTerms
- @TopProject
- @TopProjectTerms
- @VPTerms
- Terms Project Level

**Referenced Columns**
- Projects[Project Name]
- Projects[VP Name]
- Terms for TO details[Termination Reason]
- Terms for TO details[Termination Type]
- dimdate[Date]
- dimdate[Month Sort]
- dimdate[Month Year]

```dax
VAR _startDate =
     MINX(
          ALLSELECTED( 'dimdate'[Date] ),
          'dimdate'[Date]
     )
VAR _endDate =
     MAXX(
          ALLSELECTED( 'dimdate'[Date] ),
          'dimdate'[Date]
     )
VAR _dateRange =
     SWITCH(
          TRUE( ),
          ISBLANK( _startDate )
               || ISBLANK( _endDate ), "Date range unavailable",
          _startDate = _endDate,
               FORMAT( _startDate, "mmm d, yyyy" ),
          FORMAT( _startDate, "mmm d, yyyy" )
               & " - "
               & FORMAT( _endDate, "mmm d, yyyy" )
     )
VAR _terminationReason =
     SELECTEDVALUE(
          'Terms for TO details'[Termination Reason],
          "Selected Termination Reason"
     )
VAR _terminationType =
     SELECTEDVALUE(
          'Terms for TO details'[Termination Type]
     )
VAR _isVoluntary =
     _terminationType = "Voluntary"
VAR _isInvoluntary =
     _terminationType = "Involuntary"
VAR _typeLabel =
     SWITCH(
          TRUE( ),
          _isVoluntary, "Voluntary",
          _isInvoluntary, "Involuntary",
          "Termination Type"
     )
VAR _typeBackground =
     SWITCH(
          TRUE( ),
          _isVoluntary, "#DFF6DD",
          _isInvoluntary, "#FDE7E9",
          "#F3F2F1"
     )
VAR _accentColor =
     SWITCH(
          TRUE( ),
          _isVoluntary, "#107C10",
          _isInvoluntary, "#A4262C",
          "#666666"
     )

/*
  Terminations associated with the hovered
  Termination Reason.
*/
VAR _reasonTerms = [Terms Project Level]

/*
  Calculate the grand total across all Termination Reasons
  and both Termination Types.

  The current date, company, VP, project, and remaining
  report filters stay applied.
*/
VAR _grandTotalTerms =
     CALCULATE(
          [Terms Project Level],
          REMOVEFILTERS(
               'Terms for TO details'[Termination Reason]
          ),
          REMOVEFILTERS(
               'Terms for TO details'[Termination Type]
          )
     )
VAR _percentToGrandTotal =
     DIVIDE( _reasonTerms, _grandTotalTerms )

/*
  Display the count for the applicable Termination Type.

  The hovered Termination Reason should resolve to
  either Voluntary or Involuntary.
*/
VAR _typeTerms =
     SWITCH(
          TRUE( ),
          _isVoluntary,
               CALCULATE(
                    [Terms Project Level],
                    KEEPFILTERS(
                         'Terms for TO details'[Termination Type]
                              = "Voluntary"
                    )
               ),
          _isInvoluntary,
               CALCULATE(
                    [Terms Project Level],
                    KEEPFILTERS(
                         'Terms for TO details'[Termination Type]
                              = "Involuntary"
                    )
               ),
          [Terms Project Level]
     )

/*
  Determine whether the tooltip should display
  VP, project, or monthly details.
*/
VAR _vpCount =
     COUNTROWS(
          FILTER(
               ALLSELECTED( 'Projects'[VP Name] ),
               NOT ISBLANK( 'Projects'[VP Name] )
          )
     )
VAR _isSingleProject =
     HASONEVALUE( 'Projects'[Project Name] )
VAR _showByVP =
     NOT _isSingleProject && _vpCount > 1
VAR _selectedProject =
     SELECTEDVALUE(
          'Projects'[Project Name],
          "Selected Project"
     )

/*
  When one project is selected, return the five months
  with the highest termination counts for the hovered
  Termination Reason.

  Month Sort provides chronological tie-breaking.
*/
VAR _monthTable =
     TOPN(
          5,
          FILTER(
               SUMMARIZECOLUMNS(
                    'dimdate'[Month Sort],
                    'dimdate'[Month Year],
                    "@MonthTerms", [Terms Project Level]
               ),
               NOT ISBLANK( 'dimdate'[Month Sort] )
                    && NOT ISBLANK( 'dimdate'[Month Year] )
                    && NOT ISBLANK( [@MonthTerms] )
                    && [@MonthTerms] > 0
          ),
          [@MonthTerms], DESC,
          'dimdate'[Month Sort], DESC
     )
VAR _monthText =
     CONCATENATEX(
          _monthTable,
          "<li>" & "<strong>"
               & 'dimdate'[Month Year]
               & "</strong>: "
               & FORMAT( [@MonthTerms], "#,##0" )
               & " terms"
               & "</li>",
          "",
          [@MonthTerms], DESC,
          'dimdate'[Month Sort], DESC
     )

/*
  Return the top five VPs when multiple VPs
  are available in the current filter context.
*/
VAR _vpTable =
     TOPN(
          5,
          FILTER(
               ADDCOLUMNS(
                    FILTER(
                         ALLSELECTED( 'Projects'[VP Name] ),
                         NOT ISBLANK( 'Projects'[VP Name] )
                    ),
                    "@VPTerms",
                         CALCULATE( [Terms Project Level] )
               ),
               NOT ISBLANK( [@VPTerms] ) && [@VPTerms] > 0
          ),
          [@VPTerms], DESC,
          'Projects'[VP Name], ASC
     )

/*
  Identify the highest-termination project
  for each VP.
*/
VAR _vpTopProjectTable =
     GENERATE(
          _vpTable,
          VAR _currentVP = 'Projects'[VP Name]
          VAR _topProject =
               TOPN(
                    1,
                    FILTER(
                         CALCULATETABLE(
                              ADDCOLUMNS(
                                   VALUES( 'Projects'[Project Name] ),
                                   "@ProjectTerms",
                                        CALCULATE( [Terms Project Level] )
                              ),
                              KEEPFILTERS(
                                   'Projects'[VP Name] = _currentVP
                              )
                         ),
                         NOT ISBLANK( 'Projects'[Project Name] )
                              && NOT ISBLANK( [@ProjectTerms] )
                              && [@ProjectTerms] > 0
                    ),
                    [@ProjectTerms], DESC,
                    'Projects'[Project Name], ASC
               )
          RETURN
               SELECTCOLUMNS(
                    _topProject,
                    "@TopProject", 'Projects'[Project Name],
                    "@TopProjectTerms", [@ProjectTerms]
               )
     )
VAR _vpText =
     CONCATENATEX(
          _vpTopProjectTable,
          "<li>" & "<strong>"
               & 'Projects'[VP Name]
               & "</strong>: "
               & FORMAT( [@VPTerms], "#,##0" )
               & " terms"
               & "<div class='detail'>"
               & "Top project: <strong>"
               & [@TopProject]
               & "</strong> with "
               & FORMAT( [@TopProjectTerms], "#,##0" )
               & " terms"
               & "</div>"
               & "</li>",
          "",
          [@VPTerms], DESC,
          'Projects'[VP Name], ASC
     )

/*
  When one VP and multiple projects are available,
  return the top five projects for the hovered
  Termination Reason.
*/
VAR _projectTable =
     TOPN(
          5,
          FILTER(
               ADDCOLUMNS(
                    VALUES( 'Projects'[Project Name] ),
                    "@ProjectTerms",
                         CALCULATE( [Terms Project Level] )
               ),
               NOT ISBLANK( 'Projects'[Project Name] )
                    && NOT ISBLANK( [@ProjectTerms] )
                    && [@ProjectTerms] > 0
          ),
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )
VAR _projectText =
     CONCATENATEX(
          _projectTable,
          "<li>" & "<strong>"
               & 'Projects'[Project Name]
               & "</strong>: "
               & FORMAT( [@ProjectTerms], "#,##0" )
               & " terms"
               & "</li>",
          "",
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )
VAR _title =
     SWITCH(
          TRUE( ),
          _isSingleProject,
               _selectedProject
                    & " Termination Summary",
          _showByVP,
               "Top VPs for " & _terminationReason,
          "Top Projects for " & _terminationReason
     )
VAR _description =
     SWITCH(
          TRUE( ),
          _isSingleProject,
               "Top five months for "
                    & _terminationReason
                    & ".",
          _showByVP,
               "Highest termination activity by VP for "
                    & _terminationReason
                    & ".",
          "Highest termination activity by project for "
               & _terminationReason
               & "."
     )
VAR _detailContent =
     SWITCH(
          TRUE( ),
          _isSingleProject && LEN( _monthText ) > 0,
               "<ol class='list'>" & _monthText
                    & "</ol>",
          _showByVP && LEN( _vpText ) > 0,
               "<ol class='list'>" & _vpText & "</ol>",
          NOT _showByVP && LEN( _projectText ) > 0,
               "<ol class='list'>" & _projectText
                    & "</ol>",
          "<div class='empty'>"
               & "No termination activity found."
               & "</div>"
     )
RETURN
     "<div class='reportContainer'>"
          & "<style>"
          & ".reportContainer{"
          & "font-family:Segoe UI,Arial,sans-serif;"
          & "color:#252423;"
          & "width:100%;"
          & "height:100%;"
          & "box-sizing:border-box;"
          & "}"
          & ".card{"
          & "background-color:#F8F9FB;"
          & "border-left:4px solid "
          & _accentColor
          & ";"
          & "border-radius:15px;"
          & "padding:12px 14px;"
          & "box-sizing:border-box;"
          & "min-height:100%;"
          & "}"
          & ".title{"
          & "font-size:16px;"
          & "font-weight:700;"
          & "color:#323130;"
          & "margin-bottom:4px;"
          & "}"
          & ".dateRange{"
          & "font-size:11px;"
          & "font-weight:400;"
          & "color:#605E5C;"
          & "margin-bottom:8px;"
          & "}"
          & ".subtitle{"
          & "font-size:11px;"
          & "color:#605E5C;"
          & "margin-bottom:8px;"
          & "}"
          & ".summary{"
          & "display:flex;"
          & "gap:8px;"
          & "margin-bottom:10px;"
          & "}"
          & ".kpi{"
          & "flex:1;"
          & "min-width:0;"
          & "padding:6px 8px;"
          & "border-radius:6px;"
          & "text-align:center;"
          & "box-sizing:border-box;"
          & "display:flex;"
          & "flex-direction:column;"
          & "align-items:center;"
          & "justify-content:center;"
          & "}"
          & ".kpiValue{"
          & "font-size:16px;"
          & "font-weight:700;"
          & "line-height:16px;"
          & "color:#666666;"
          & "white-space:nowrap;"
          & "}"
          & ".kpiLabel{"
          & "font-size:10px;"
          & "font-weight:600;"
          & "color:#003366;"
          & "margin-top:3px;"
          & "white-space:nowrap;"
          & "}"
          & ".list{"
          & "margin:0;"
          & "padding-left:20px;"
          & "font-size:12px;"
          & "line-height:1.4;"
          & "}"
          & ".list li{"
          & "margin-bottom:6px;"
          & "}"
          & ".detail{"
          & "font-size:10px;"
          & "font-weight:400;"
          & "color:#605E5C;"
          & "margin-top:1px;"
          & "}"
          & ".empty{"
          & "font-size:12px;"
          & "color:#A4262C;"
          & "}"
          & "</style>"
          & "<div class='card'>"
          & "<div class='title'>"
          & _title
          & "</div>"
          & "<div class='dateRange'>"
          & _dateRange
          & "</div>"
          & "<div class='summary'>"

          /*
                    Left KPI: applicable Termination Type.
                  */
          & "<div class='kpi' style='background:"
          & _typeBackground
          & ";'>"
          & "<div class='kpiValue'>"
          & FORMAT(
               COALESCE( _typeTerms, 0 ),
               "#,##0"
          )
          & "</div>"
          & "<div class='kpiLabel'>"
          & _terminationReason // _typeLabel
          & "</div>"
          & "</div>"

          /*
                    Right KPI: hovered reason as a percentage
                    of the grand total.
                  */
          & "<div class='kpi' "
          & "style='background:#E5F1FB;'>"
          & "<div class='kpiValue'>"
          & IF(
               ISBLANK( _percentToGrandTotal ),
               "N/A",
               FORMAT( _percentToGrandTotal, "0.0%" )
          )
          & "</div>"
          & "<div class='kpiLabel'>"
          & "% to Grand Total"
          & "</div>"
          & "</div>"
          & "</div>"
          & "<div class='subtitle'>"
          & _description
          & "</div>"
          & _detailContent
          & "</div>"
          & "</div>"
```

#### Termination Type Background Color

##### Dependencies

**Referenced Columns**
- Terms for TO details[Termination Type]

```dax
VAR _terminationType =
     SELECTEDVALUE(
          'Terms for TO details'[Termination Type]
     )
RETURN
     SWITCH(
          _terminationType,
          "Involuntary", "#FDE7E9",
          "Voluntary", "#DFF6DD",
          "#FFFFFF"
     )
```

#### TerminationCard HTML

##### Dependencies

**Referenced Measures**
- FT Terms Project Level
- OTHER Terms Project Level
- PT Terms Project Level
- Terms Project Level

```dax
VAR _Terms =
     FORMAT( [Terms Project Level], "#,##0" )
VAR _FTTerms =
     FORMAT(
          [FT Terms Project Level],
          "#,##0"
     )
VAR _PTTerms =
     FORMAT(
          [PT Terms Project Level],
          "#,##0"
     )
VAR _OtherTerms =
     FORMAT(
          [OTHER Terms Project Level],
          "#,##0"
     )
RETURN
     "
<div style='
    width:330px;
    height:78px;
    padding:5px 20px;
    box-sizing:border-box;
    font-family:Segoe UI;
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:#E5F1FB;
    border-radius:15px;
'>

    <div>
        <div style='
            font-size:42px;
            font-weight:700;
            color:#666666;
            line-height:36px;
        '>
            "
          & _Terms
          & "
        </div>

        <div style='
            font-size:12px;
            font-weight:600;
            color:#003366;
            margin-top:2px;
        '>
            Terminations
        </div>
    </div>

    <div style='
        display:flex;
        flex-direction:column;
        justify-content:center;
        gap:2px;
        min-width:110px;
    '>

        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <span style='font-size:11px; font-weight:600; color:#003366;'>Full Time</span>
            <span style='font-size:14px; font-weight:700; color:#666666;'>"
          & _FTTerms
          & "</span>
        </div>

        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <span style='font-size:11px; font-weight:600; color:#003366;'>Part Time</span>
            <span style='font-size:14px; font-weight:700; color:#666666;'>"
          & _PTTerms
          & "</span>
        </div>

        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <span style='font-size:11px; font-weight:600; color:#003366;'>Other</span>
            <span style='font-size:14px; font-weight:700; color:#666666;'>"
          & _OtherTerms
          & "</span>
        </div>

    </div>

</div>
"
```

#### Terminations By Month Subtitle

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- dimdate[Month Sort]
- dimdate[Month Year]

```dax
VAR _avgTerms =
     AVERAGEX(
          VALUES( 'dimdate'[Month Sort] ),
          [Terms Project Level]
     )
VAR _cm =
     CALCULATE(
          MAX( 'dimdate'[Month Year] ),
          TOPN(
               1,
               VALUES( 'dimdate'[Month Sort] ),
               'dimdate'[Month Sort], DESC
          )
     )
VAR _currentMonth =
     CALCULATE(
          [Terms Project Level],
          TOPN(
               1,
               VALUES( 'dimdate'[Month Sort] ),
               'dimdate'[Month Sort], DESC
          )
     )
VAR _variance = _currentMonth - _avgTerms
VAR _varianceText =
     IF(
          _variance > 0,
          "+" & FORMAT( _variance, "#,##0" ),
          IF(
               _variance < 0,
               "-" & FORMAT( _variance, "#,##0" ),
               FORMAT( _variance, "#,##0" )
          )
     )
RETURN
     _cm & ": "
          & FORMAT( _currentMonth, "#,##0" )
          & " | 12-Month Avg: "
          & FORMAT( _avgTerms, "#,##0" )
          & " | "
          & _varianceText
```

#### Terminations Demographic Bar SVG

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Termination Demographics[Demographic]
- Terms for TO details[Age Band]
- Terms for TO details[Disability Status]
- Terms for TO details[Gender for Insurance Coverage]
- Terms for TO details[Generation]
- Terms for TO details[Race/Ethnicity]
- Terms for TO details[Veteran Status]

```dax
VAR _demographic =
     SELECTEDVALUE(
          'Termination Demographics'[Demographic],
          "Gender"
     )
VAR _isDetailRow =
     SWITCH(
          _demographic,
          "Gender",
               HASONEVALUE(
                    'Terms for TO details'[Gender for Insurance Coverage]
               ),
          "Race",
               HASONEVALUE(
                    'Terms for TO details'[Race/Ethnicity]
               ),
          "Veteran",
               HASONEVALUE(
                    'Terms for TO details'[Veteran Status]
               ),
          "Disability",
               HASONEVALUE(
                    'Terms for TO details'[Disability Status]
               ),
          "Generation",
               HASONEVALUE(
                    'Terms for TO details'[Generation]
               ),
          "Age",
               HASONEVALUE(
                    'Terms for TO details'[Age Band]
               ),
          FALSE
     )
VAR _terms = [Terms Project Level]
VAR _total =
     SWITCH(
          _demographic,
          "Gender",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Gender for Insurance Coverage]
                    )
               ),
          "Race",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Race/Ethnicity]
                    )
               ),
          "Veteran",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Veteran Status]
                    )
               ),
          "Disability",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Disability Status]
                    )
               ),
          "Generation",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Generation]
                    )
               ),
          "Age",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Age Band]
                    )
               )
     )
VAR _percent = DIVIDE( _terms, _total )
VAR _barWidth =
     MIN(
          100,
          MAX( 0, ROUND( _percent * 100, 1 ) )
     )
VAR _svg =
     "<svg xmlns='http://www.w3.org/2000/svg' width='100' height='25' viewBox='0 0 100 25'>"
          & "<rect x='0' y='7' width='100' height='11' rx='3' fill='%23f3f2f1'></rect>"
          & "<rect x='0' y='7' width='"
          & FORMAT( _barWidth, "0.0" )
          & "' height='11' rx='3' fill='%23003a70'></rect>"
          & "</svg>"
RETURN
     IF(
          NOT _isDetailRow || ISBLANK( _terms )
               || _terms <= 0,
          BLANK( ),
          "data:image/svg+xml;utf8," & _svg
     )
```

#### Terms by Tenure Band - Percent Of Total

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Terms for TO details[Tenure Band]

```dax
DIVIDE(
     [Terms Project Level],
     CALCULATE(
          [Terms Project Level],
          ALLSELECTED(
               'Terms for TO details'[Tenure Band]
          )
     )
)
```

#### Terms by Termination Reason - Percent Of Total

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Terms for TO details[Termination Reason]

```dax
DIVIDE(
     [Terms Project Level],
     CALCULATE(
          [Terms Project Level],
          ALLSELECTED(
               'Terms for TO details'[Termination Reason]
          )
     )
)
```

#### Terms Percent Of Total

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Termination Demographics[Demographic]
- Terms for TO details[Age Band]
- Terms for TO details[Disability Status]
- Terms for TO details[Gender for Insurance Coverage]
- Terms for TO details[Generation]
- Terms for TO details[Race/Ethnicity]
- Terms for TO details[Veteran Status]

```dax
VAR _Total =
     SWITCH(
          SELECTEDVALUE(
               'Termination Demographics'[Demographic]
          ),
          "Gender",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Gender for Insurance Coverage]
                    )
               ),
          "Race",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Race/Ethnicity]
                    )
               ),
          "Veteran",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Veteran Status]
                    )
               ),
          "Disability",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Disability Status]
                    )
               ),
          "Generation",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Generation]
                    )
               ),
          "Age",
               CALCULATE(
                    [Terms Project Level],
                    ALLSELECTED(
                         'Terms for TO details'[Age Band]
                    )
               )
     )
RETURN
     DIVIDE( [Terms Project Level], _Total )
```

#### Terms Project Level

##### Dependencies

**Referenced Measures**
- Terms

**Referenced Columns**
- IncludeInactiveProject[IncludeInactiveProject]
- Projects[Status]

```dax
IF(
     SELECTEDVALUE(
          'IncludeInactiveProject'[IncludeInactiveProject],
          "Yes"
     )
          = "No",
     CALCULATE(
          [Terms],
          ALL( 'Companies' ),
          FILTER(
               'Projects',
               'Projects'[Status] IN { "Active", "Start Up" }
          )
     ),
     CALCULATE( [Terms], ALL( 'Companies' ) )
)
```

#### Top 3 Reasons Subtitle

##### Dependencies

**Referenced Measures**
- Terms Project Level

**Referenced Columns**
- Terms for TO details[Termination Reason]

```dax
VAR _Top3Terminations =
     SUMX(
          TOPN(
               3,
               VALUES(
                    'Terms for TO details'[Termination Reason]
               ),
               [Terms Project Level], DESC,
               'Terms for TO details'[Termination Reason], ASC
          ),
          [Terms Project Level]
     )
VAR _TotalTerminations =
     CALCULATE(
          [Terms Project Level],
          REMOVEFILTERS(
               'Terms for TO details'[Termination Reason]
          )
     )
VAR _Percent =
     DIVIDE(
          _Top3Terminations,
          _TotalTerminations
     )
RETURN
     "Top 3 reasons account for "
          & FORMAT( _Percent, "0.0%" )
          & " of overall terminations."
```

#### Top Projects HTML

##### Dependencies

**Referenced Measures**
- @ProjectTerms
- @ReasonTerms
- @TopProject
- @TopProjectTerms
- @VPTerms
- Terms Project Level

**Referenced Columns**
- Projects[Project Name]
- Projects[VP Name]
- Terms for TO details[Termination Reason]
- Terms for TO details[Termination Type]
- dimdate[Month Year]

```dax

VAR _month =
     SELECTEDVALUE(
          'dimdate'[Month Year],
          "All Months"
     )
VAR _selectedTerminationType =
     SELECTEDVALUE(
          'Terms for TO details'[Termination Type]
     )
VAR _vpCount =
     COUNTROWS(
          FILTER(
               ALLSELECTED( 'Projects'[VP Name] ),
               NOT ISBLANK( 'Projects'[VP Name] )
          )
     )
VAR _isSingleProject =
     HASONEVALUE( 'Projects'[Project Name] )
VAR _showByVP =
     NOT _isSingleProject && _vpCount > 1
VAR _selectedProject =
     SELECTEDVALUE(
          'Projects'[Project Name],
          "Selected Project"
     )
VAR _totalTerms = [Terms Project Level]
VAR _voluntaryTerms =
     CALCULATE(
          [Terms Project Level],
          KEEPFILTERS(
               'Terms for TO details'[Termination Type]
                    = "Voluntary"
          )
     )
VAR _involuntaryTerms =
     CALCULATE(
          [Terms Project Level],
          KEEPFILTERS(
               'Terms for TO details'[Termination Type]
                    = "Involuntary"
          )
     )

/*
  Display "Filtered Out" instead of zero when the
  opposing termination type is selected.
*/
VAR _voluntaryIsFiltered =
     _selectedTerminationType = "Involuntary"
VAR _involuntaryIsFiltered =
     _selectedTerminationType = "Voluntary"
VAR _voluntaryDisplay =
     IF(
          _voluntaryIsFiltered,
          "Filtered Out",
          FORMAT(
               COALESCE( _voluntaryTerms, 0 ),
               "#,##0"
          )
     )
VAR _involuntaryDisplay =
     IF(
          _involuntaryIsFiltered,
          "Filtered Out",
          FORMAT(
               COALESCE( _involuntaryTerms, 0 ),
               "#,##0"
          )
     )
VAR _voluntaryBackground =
     IF(
          _voluntaryIsFiltered,
          "#F3F2F1",
          "#DFF6DD"
     )
VAR _involuntaryBackground =
     IF(
          _involuntaryIsFiltered,
          "#F3F2F1",
          "#FDE7E9"
     )
VAR _voluntaryValueClass =
     IF(
          _voluntaryIsFiltered,
          "kpiValue filteredValue",
          "kpiValue"
     )
VAR _involuntaryValueClass =
     IF(
          _involuntaryIsFiltered,
          "kpiValue filteredValue",
          "kpiValue"
     )

/*
  Top five termination reasons when exactly
  one project is selected.
*/
VAR _reasonTable =
     TOPN(
          5,
          FILTER(
               SUMMARIZECOLUMNS(
                    'Terms for TO details'[Termination Reason],
                    "@ReasonTerms", [Terms Project Level]
               ),
               NOT ISBLANK(
                    'Terms for TO details'[Termination Reason]
               )
                    && NOT ISBLANK( [@ReasonTerms] )
                    && [@ReasonTerms] > 0
          ),
          [@ReasonTerms], DESC,
          'Terms for TO details'[Termination Reason], ASC
     )
VAR _reasonText =
     CONCATENATEX(
          _reasonTable,
          "<li>" & "<strong>"
               & 'Terms for TO details'[Termination Reason]
               & "</strong>: "
               & FORMAT( [@ReasonTerms], "#,##0" )
               & " terms"
               & "</li>",
          "",
          [@ReasonTerms], DESC,
          'Terms for TO details'[Termination Reason], ASC
     )

/*
  Top ten projects based on termination count
  when one VP is selected.
  
  Termination Type and Termination Reason remain
  available as report filters, but neither field
  is included as a grouping level in this table.
*/
VAR _projectTable =
     TOPN(
          10,
          FILTER(
               ADDCOLUMNS(
                    VALUES( 'Projects'[Project Name] ),
                    "@ProjectTerms",
                         CALCULATE( [Terms Project Level] )
               ),
               NOT ISBLANK( 'Projects'[Project Name] )
                    && NOT ISBLANK( [@ProjectTerms] )
                    && [@ProjectTerms] > 0
          ),
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )
VAR _projectText =
     CONCATENATEX(
          _projectTable,
          "<li>" & "<strong>"
               & 'Projects'[Project Name]
               & "</strong>: "
               & FORMAT( [@ProjectTerms], "#,##0" )
               & " terms"
               & "</li>",
          "",
          [@ProjectTerms], DESC,
          'Projects'[Project Name], ASC
     )


/*
  Top ten VPs based on termination count.
*/
VAR _vpTable =
     TOPN(
          10,
          FILTER(
               ADDCOLUMNS(
                    FILTER(
                         ALLSELECTED( 'Projects'[VP Name] ),
                         NOT ISBLANK( 'Projects'[VP Name] )
                    ),
                    "@VPTerms",
                         CALCULATE( [Terms Project Level] )
               ),
               NOT ISBLANK( [@VPTerms] ) && [@VPTerms] > 0
          ),
          [@VPTerms], DESC,
          'Projects'[VP Name], ASC
     )

/*
  Identify the highest-termination project
  for each VP.
*/
VAR _vpTopProjectTable =
     GENERATE(
          _vpTable,
          VAR _currentVP = 'Projects'[VP Name]
          VAR _topProject =
               TOPN(
                    1,
                    FILTER(
                         CALCULATETABLE(
                              ADDCOLUMNS(
                                   VALUES( 'Projects'[Project Name] ),
                                   "@ProjectTerms",
                                        CALCULATE( [Terms Project Level] )
                              ),
                              KEEPFILTERS(
                                   'Projects'[VP Name] = _currentVP
                              )
                         ),
                         NOT ISBLANK( 'Projects'[Project Name] )
                              && NOT ISBLANK( [@ProjectTerms] )
                              && [@ProjectTerms] > 0
                    ),
                    [@ProjectTerms], DESC,
                    'Projects'[Project Name], ASC
               )
          RETURN
               SELECTCOLUMNS(
                    _topProject,
                    "@TopProject", 'Projects'[Project Name],
                    "@TopProjectTerms", [@ProjectTerms]
               )
     )
VAR _vpText =
     CONCATENATEX(
          _vpTopProjectTable,
          "<li>" & "<strong>"
               & 'Projects'[VP Name]
               & "</strong>: "
               & FORMAT( [@VPTerms], "#,##0" )
               & " terms"
               & "<div class='detail'>"
               & "Top project: <strong>"
               & [@TopProject]
               & "</strong> with "
               & FORMAT( [@TopProjectTerms], "#,##0" )
               & " terms"
               & "</div>"
               & "</li>",
          "",
          [@VPTerms], DESC,
          'Projects'[VP Name], ASC
     )
VAR _title =
     SWITCH(
          TRUE( ),
          _isSingleProject,
               _selectedProject
                    & " Termination Summary",
          _showByVP, "Top VPs by Terminations",
          "Top Projects by Terminations"
     )
VAR _filterDescription =
     SWITCH(
          TRUE( ),
          _selectedTerminationType = "Voluntary", "Filtered to voluntary terminations.",
          _selectedTerminationType = "Involuntary", "Filtered to involuntary terminations.",
          ""
     )
VAR _description =
     SWITCH(
          TRUE( ),
          _isSingleProject, "Top five termination reasons for the selected project.",
          _showByVP, "VP termination totals with each VP's highest-termination project.",
          "Projects with the highest termination totals based on current filters."
     )
VAR _detailContent =
     SWITCH(
          TRUE( ),
          _isSingleProject
               && LEN( _reasonText ) > 0,
               "<ol class='list'>" & _reasonText
                    & "</ol>",
          _showByVP && LEN( _vpText ) > 0,
               "<ol class='list'>" & _vpText & "</ol>",
          NOT _showByVP && LEN( _projectText ) > 0,
               "<ol class='list'>" & _projectText
                    & "</ol>",
          "<div class='empty'>"
               & "No termination activity found."
               & "</div>"
     )
RETURN
     "<div class='reportContainer'>"
          & "<style>"
          & ".reportContainer{"
          & "font-family:Segoe UI,Arial,sans-serif;"
          & "color:#252423;"
          & "width:100%;"
          & "height:100%;"
          & "box-sizing:border-box;"
          & "}"
          & ".card{"
          & "background-color:#F8F9FB;"
          & "border-left:4px solid #107C10;"
          & "border-radius:15px;"
          & "padding:12px 14px;"
          & "box-sizing:border-box;"
          & "min-height:100%;"
          & "}"
          & ".title{"
          & "font-size:16px;"
          & "font-weight:700;"
          & "color:#323130;"
          & "margin-bottom:4px;"
          & "}"
          & ".subtitle{"
          & "font-size:11px;"
          & "color:#605E5C;"
          & "margin-bottom:8px;"
          & "}"
          & ".filterDescription{"
          & "font-size:10px;"
          & "font-style:italic;"
          & "color:#605E5C;"
          & "margin-top:-4px;"
          & "margin-bottom:8px;"
          & "}"
          & ".summary{"
          & "display:flex;"
          & "gap:8px;"
          & "margin-bottom:10px;"
          & "}"
          & ".kpi{"
          & "flex:1;"
          & "min-width:0;"
          & "padding:6px 8px;"
          & "border-radius:6px;"
          & "text-align:center;"
          & "box-sizing:border-box;"
          & "display:flex;"
          & "flex-direction:column;"
          & "align-items:center;"
          & "justify-content:center;"
          & "}"
          & ".kpiValue{"
          & "font-size:16px;"
          & "font-weight:700;"
          & "line-height:16px;"
          & "color:#666666;"
          & "white-space:nowrap;"
          & "}"
          & ".filteredValue{"
          & "font-size:11px;"
          & "font-weight:600;"
          & "font-style:italic;"
          & "color:#797775;"
          & "line-height:16px;"
          & "}"
          & ".kpiLabel{"
          & "font-size:10px;"
          & "font-weight:600;"
          & "color:#003366;"
          & "margin-top:3px;"
          & "white-space:nowrap;"
          & "}"
          & ".list{"
          & "margin:0;"
          & "padding-left:20px;"
          & "font-size:12px;"
          & "line-height:1.4;"
          & "}"
          & ".list li{"
          & "margin-bottom:6px;"
          & "}"
          & ".detail{"
          & "font-size:10px;"
          & "font-weight:400;"
          & "color:#605E5C;"
          & "margin-top:1px;"
          & "}"
          & ".empty{"
          & "font-size:12px;"
          & "color:#A4262C;"
          & "}"
          & "</style>"
          & "<div class='card'>"
          & "<div class='title'>"
          & _title
          & "</div>"
          & "<div class='subtitle'>"
          & _month
          & "</div>"
          & IF(
               LEN( _filterDescription ) > 0,
               "<div class='filterDescription'>"
                    & _filterDescription
                    & "</div>",
               ""
          )
          & "<div class='summary'>"
          & "<div class='kpi' style='background:#E5F1FB;'>"
          & "<div class='kpiValue'>"
          & FORMAT(
               COALESCE( _totalTerms, 0 ),
               "#,##0"
          )
          & "</div>"
          & "<div class='kpiLabel'>"
          & "Total Terms"
          & "</div>"
          & "</div>"
          & "<div class='kpi' style='background:"
          & _voluntaryBackground
          & ";'>"
          & "<div class='"
          & _voluntaryValueClass
          & "'>"
          & _voluntaryDisplay
          & "</div>"
          & "<div class='kpiLabel'>"
          & "Voluntary"
          & "</div>"
          & "</div>"
          & "<div class='kpi' style='background:"
          & _involuntaryBackground
          & ";'>"
          & "<div class='"
          & _involuntaryValueClass
          & "'>"
          & _involuntaryDisplay
          & "</div>"
          & "<div class='kpiLabel'>"
          & "Involuntary"
          & "</div>"
          & "</div>"
          & "</div>"
          & "<div class='subtitle'>"
          & _description
          & "</div>"
          & _detailContent
          & "</div>"
          & "</div>"

```

#### Headcount Sum

##### Dependencies

**Referenced Columns**
- Headcount[Headcount]

```dax
SUM( 'Headcount'[Headcount] )
```

#### About This Report HTML
```dax
"<div style=""font-family:Segoe UI;font-size:18px;line-height:1.3;overflow:hidden;box-sizing:border-box;"">
		<b style=""color:#003B5C;"">Report Summary</b><p>This report analyzes employee terminations, showing volumes by voluntary and involuntary type, termination reason, tenure, project, VP, month, and worker category. It includes demographic breakdowns, first-year termination rates against average headcount, and drillthrough detail for filtered views.</p>
		<b style=""color:#003B5C;"">Data Sources</b><div style=""display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;""><span style=""background:#F3E8FF;color:#6B21A8;padding:4px 10px;border-radius:12px;"">Excel</span></div>
		<div style=""height:20px;""></div><div style=""background:#FDF0D5;border-left:4px solid #E9B949;border-radius:10px;padding:12px;margin-top:8px;""><b>Business Value:</b> Helps stakeholders see where and when terminations concentrate, which reasons and termination types drive them, and how early-tenure exits compare with average headcount. Project, VP, and demographic views help identify areas that may warrant closer review, and month-over-month context shows whether recent activity is above or below the recent average.</div><div style=""height:20px;""></div><b style=""color:#003B5C;"">Top KPIs</b>
		<div style=""display:flex;flex-wrap:wrap;align-items:flex-start;gap:6px;margin-top:6px;""><span style=""background:#DCEBFF;padding:4px 10px;border-radius:12px;display:inline-block;white-space:nowrap;"">Terms</span><span style=""background:#E6F7E6;padding:4px 10px;border-radius:12px;display:inline-block;white-space:nowrap;"">Headcount Sum</span><span style=""background:#FFF4D6;padding:4px 10px;border-radius:12px;display:inline-block;white-space:nowrap;"">First Year Terms</span></div>"
```

## Companies

No description provided.

### Statistics

- Columns: 2
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 1
- Date Columns: 0
- Numeric Columns: 1

### Related Tables

- Projects

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Company Name | string | No | No |  |
| Record ID # | int64 | No | No |  |

## dimdate

No description provided.

### Statistics

- Columns: 16
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 9
- Date Columns: 1
- Numeric Columns: 6

### Related Tables

- Headcount
- Terms for TO details

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Date | dateTime | No | No |  |
| Calendar Year | int64 | No | No |  |
| Month Name | string | No | No |  |
| Month Number | int64 | No | No |  |
| Weekday | string | No | No |  |
| Weekday Number | int64 | No | No |  |
| Quarter | string | No | No |  |
| Month Year | string | No | No |  |
| Is Working Day Date | string | No | No |  |
| Fiscal Year | int64 | No | No |  |
| Fiscal Period | string | No | No |  |
| Fiscal Quarter | string | No | No |  |
| Is Current Fiscal Year | string | No | No |  |
| Is Current Fiscal Period | string | No | No |  |
| Previous Period Index | int64 | No | No |  |
| Month Sort | int64 | No | No |  |

## dimLocationCrosswalk

No description provided.

### Statistics

- Columns: 2
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 2

### Related Tables

- Projects
- dimLocationHierarchy

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| WORKLOC CODE | int64 | No | No |  |
| Related Project | int64 | No | No |  |

## dimLocationHierarchy

No description provided.

### Statistics

- Columns: 21
- Measures: 0
- Relationships: 3
- Hidden Columns: 0

### Summary

- String Columns: 19
- Date Columns: 0
- Numeric Columns: 2

### Related Tables

- Headcount
- Terms for TO details
- dimLocationCrosswalk

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Location | string | No | No |  |
| Product Category | string | No | No |  |
| Type | string | No | No |  |
| SAP Code: Company | int64 | No | No |  |
| SAP Name: Company | string | No | No |  |
| SAP Code: Line of Business | string | No | No |  |
| SAP Name: Line of Business | string | No | No |  |
| SAP Code: Product Category | string | No | No |  |
| SAP Name: Product Category | string | No | No |  |
| SAP Code: Cost Center / Profit Center Roll-up | string | No | No |  |
| SAP Name: Cost Center / Profit Center Roll-up | string | No | No |  |
| SAP Code: Contract Parent (Segment) | string | No | No |  |
| SAP Name: Contract Parent (Segment) | string | No | No |  |
| SAP Code: Cost Center / Profit Center | string | No | No |  |
| SAP Name: Cost Center / Profit Center | string | No | No |  |
| Company | string | No | No |  |
| Cost Center / Profit Center (Roll-up) | string | No | No |  |
| Segment | string | No | No |  |
| Line of Business | string | No | No |  |
| Cost Center / Profit Center | string | No | No |  |
| WORKLOC CODE | int64 | No | No |  |

## Headcount

No description provided.

### Statistics

- Columns: 7
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 2
- Date Columns: 1
- Numeric Columns: 4

### Related Tables

- dimLocationHierarchy
- dimdate

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Headcount | int64 | No | No |  |
| Headcount Percentage | double | No | No |  |
| WORKLOC CODE | int64 | No | No |  |
| Date | dateTime | No | No |  |
| Month | string | No | No |  |
| Year | int64 | No | No |  |
| WORK LOCATION NAME | string | No | No |  |

## IncludeInactiveProject

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
| IncludeInactiveProject |  | No | No |  |

## Projects

No description provided.

### Statistics

- Columns: 12
- Measures: 0
- Relationships: 3
- Hidden Columns: 0

### Summary

- String Columns: 8
- Date Columns: 2
- Numeric Columns: 2

### Related Tables

- Companies
- ProjectsContractPeriod
- dimLocationCrosswalk

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Project Name | string | No | No |  |
| PD Name | string | No | No |  |
| VP Name | string | No | No |  |
| Status | string | No | No |  |
| Category | string | No | No |  |
| Related Company | int64 | No | No |  |
| Project Code | string | No | No |  |
| Contract Period | string | No | No |  |
| Type RD | string | No | No |  |
| Contract Start | dateTime | No | No |  |
| Contract End | dateTime | No | No |  |
| Record ID # | int64 | No | No |  |

## ProjectsContractPeriod

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 1
- Date Columns: 2
- Numeric Columns: 0

### Related Tables

- Projects

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Project Name | string | No | No |  |
| Contract Start | dateTime | No | No |  |
| Contract End | dateTime | No | No |  |

## Termination Demographics

No description provided.

### Statistics

- Columns: 4
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
| Termination Demographics |  | No | No | 'Termination Demographics Order' |
| Termination Demographics Fields |  | No | No | 'Termination Demographics Order' |
| Termination Demographics Order |  | No | No |  |
| Demographic |  | No | No | 'Termination Demographics Order' |

## Terms for TO details

No description provided.

### Statistics

- Columns: 55
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 49
- Date Columns: 3
- Numeric Columns: 3

### Related Tables

- dimLocationHierarchy
- dimdate

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Employee ID | string | No | No |  |
| Employee Preferred Name | string | No | No |  |
| Employee Legal Name | string | No | No |  |
| EEO1 | string | No | No |  |
| Job | string | No | No |  |
| Department | string | No | No |  |
| Work Location State/Territory | string | No | No |  |
| Work Location City | string | No | No |  |
| Work Location Name | string | No | No |  |
| Work Location Category | string | No | No |  |
| Company Code | string | No | No |  |
| Business Unit | string | No | No |  |
| Employee Status | string | No | No |  |
| Manager Preferred Name | string | No | No |  |
| Manager Legal Name | string | No | No |  |
| Hire/Rehire Date | dateTime | No | No |  |
| Termination Date | dateTime | No | No |  |
| Tenure | double | No | No |  |
| Termination Type | string | No | No |  |
| Termination Reason | string | No | No |  |
| Age Band | string | No | No |  |
| Position ID | string | No | No |  |
| Rate Type | string | No | No |  |
| Org Level | string | No | No |  |
| Tenure Band | string | No | No |  |
| Termination Action | string | No | No |  |
| Is Manager | string | No | No |  |
| Job Function | string | No | No |  |
| Job Level | string | No | No |  |
| FLSA Status | string | No | No |  |
| Cost Number | string | No | No |  |
| Race/Ethnicity | string | No | No |  |
| Gender for Insurance Coverage | string | No | No |  |
| Gender (Self ID) | string | No | No |  |
| Veteran Status | string | No | No |  |
| Disability Status | string | No | No |  |
| Business Category | string | No | No |  |
| Adjusted Service Date | string | No | No |  |
| Credited Service Date | string | No | No |  |
| Hire Type | string | No | No |  |
| Worker Category | string | No | No |  |
| Seniority Date | dateTime | No | No |  |
| Job Class | string | No | No |  |
| Generation | string | No | No |  |
| Home Location City | string | No | No |  |
| Home Location State | string | No | No |  |
| Performance Rating | string | No | No |  |
| Management Position | string | No | No |  |
| Work Location Country | string | No | No |  |
| Home Location Country | string | No | No |  |
| Pay Grade | string | No | No |  |
| Home Location Zip Code | int64 | No | No |  |
| WORKLOC CODE | int64 | No | No |  |
| Total | string | No | No |  |
| 1st Year Terms | string | No | No |  |

# Relationships

| From | To | Cardinality | Direction | Active |
|---|---|---|---|---:|
| ProjectsContractPeriod[Project Name] | Projects[Project Name] | one to one | bothDirections | Yes |
| Terms for TO details[Termination Date] | dimdate[Date] | many to one | oneDirection | Yes |
| Projects[Related Company] | Companies[Record ID #] | many to one | oneDirection | Yes |
| Headcount[WORKLOC CODE] | dimLocationHierarchy[WORKLOC CODE] | many to one | oneDirection | Yes |
| Terms for TO details[WORKLOC CODE] | dimLocationHierarchy[WORKLOC CODE] | many to one | oneDirection | Yes |
| dimLocationCrosswalk[WORKLOC CODE] | dimLocationHierarchy[WORKLOC CODE] | one to one | bothDirections | Yes |
| dimLocationCrosswalk[Related Project] | Projects[Record ID #] | many to one | oneDirection | Yes |
| Headcount[Date] | dimdate[Date] | many to one | oneDirection | Yes |

# Validation

- Model parsed successfully: Yes
- Errors: 0
- Warnings: 0
