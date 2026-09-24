---
contextType: Power BI Semantic Model
schemaVersion: 1.0
generator: Semantic Model Context Builder
modelName: Power BI Resume Steven Foster
generatedUtc: 2026-09-24T18:13:10+00:00
---

# Semantic Model Instructions

Treat this file as the authoritative structural reference for this model.
Do not invent tables, columns, measures, or relationships that are not listed.
Use exact object names when proposing DAX.

# Model Summary

- Model: Power BI Resume Steven Foster
- Storage mode: Unknown
- Tables: 12
- Measure-Only Tables Remaining: 1
- Columns: 52
- Measures: 28
- Relationships: 7

## Model Profile

### Measure Dependencies Found

- Total Dependencies: 81

### Data Type Distribution

- Unknown: 40
- string: 8
- int64: 4

### Most Connected Tables

1. Work Experience (5 relationships)
2. Date (2 relationships)
3. Job Skills (2 relationships)
4. Achievements (1 relationships)
5. Assets (1 relationships)
6. Projects (1 relationships)
7. Skills (1 relationships)
8. Work Descriptions (1 relationships)
9. _Measures (0 relationships)
10. Certifications (0 relationships)

# Tables

## _Measures

No description provided.

### Statistics

- Columns: 0
- Measures: 28
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

#### Current Role

##### Dependencies

**Referenced Columns**
- Work Experience[JobTitle]
- Work Experience[Status]

```dax
CALCULATE (
    MAX ( 'Work Experience'[JobTitle] ),
    'Work Experience'[Status] = "Current"
)
```

#### Current Company

##### Dependencies

**Referenced Columns**
- Work Experience[Company]
- Work Experience[Status]

```dax
CALCULATE (
    MAX ( 'Work Experience'[Company] ),
    'Work Experience'[Status] = "Current"
)
```

#### Experience Count
```dax
COUNTROWS ( 'Work Experience' )
```

#### Description Count
```dax
COUNTROWS ( 'Work Descriptions' )
```

#### Skill Count

##### Dependencies

**Referenced Columns**
- Skills[SkillId]

```dax
DISTINCTCOUNT ( Skills[SkillId] )
```

#### Selected Job Skill Count

##### Dependencies

**Referenced Columns**
- Job Skills[SkillId]

```dax
DISTINCTCOUNT ( 'Job Skills'[SkillId] )
```

#### Selected Job Title

##### Dependencies

**Referenced Columns**
- Work Experience[JobTitle]

```dax
SELECTEDVALUE ( 'Work Experience'[JobTitle], "Professional Experience" )
```

#### Selected Company

##### Dependencies

**Referenced Columns**
- Work Experience[Company]

```dax
SELECTEDVALUE ( 'Work Experience'[Company], "Career Experience" )
```

#### Selected Job Description

##### Dependencies

**Referenced Columns**
- Work Descriptions[Desc Id]
- Work Descriptions[Desc]

```dax
CONCATENATEX (
    'Work Descriptions',
    "• " & 'Work Descriptions'[Desc],
    UNICHAR ( 10 ),
    'Work Descriptions'[Desc Id], ASC
)
```

#### Selected Job Skills

##### Dependencies

**Referenced Columns**
- Skills[Skill]

```dax
CALCULATE (
    CONCATENATEX (
        VALUES ( Skills[Skill] ),
        Skills[Skill],
        " | ",
        Skills[Skill], ASC
    )
)
```

#### Selected Job Date Range

##### Dependencies

**Referenced Columns**
- Work Experience[End Date]
- Work Experience[Start Date]
- Work Experience[Status]

```dax
VAR StartDate =
    MIN ( 'Work Experience'[Start Date] )
VAR EndDate =
    MAXX (
        'Work Experience',
        IF (
            'Work Experience'[Status] = "Current"
                || ISBLANK ( 'Work Experience'[End Date] ),
            TODAY (),
            'Work Experience'[End Date]
        )
    )
VAR IsCurrent =
    SELECTEDVALUE ( 'Work Experience'[Status] ) = "Current"
RETURN
    IF (
        ISBLANK ( StartDate ),
        BLANK (),
        FORMAT ( StartDate, "MMM yyyy" ) & " – "
            & IF ( IsCurrent, "Present", FORMAT ( EndDate, "MMM yyyy" ) )
    )
```

#### Selected Job Duration

##### Dependencies

**Referenced Columns**
- Work Experience[End Date]
- Work Experience[Start Date]
- Work Experience[Status]

```dax
VAR StartDate =
    MIN ( 'Work Experience'[Start Date] )
VAR EndDate =
    MAXX (
        'Work Experience',
        IF (
            'Work Experience'[Status] = "Current"
                || ISBLANK ( 'Work Experience'[End Date] ),
            TODAY (),
            'Work Experience'[End Date]
        )
    )
VAR TotalMonths =
    DATEDIFF ( StartDate, EndDate, MONTH )
VAR Years =
    QUOTIENT ( TotalMonths, 12 )
VAR Months =
    MOD ( TotalMonths, 12 )
RETURN
    SWITCH (
        TRUE (),
        Years > 0 && Months > 0,
            Years & IF ( Years = 1, " year ", " years " )
                & Months & IF ( Months = 1, " month", " months" ),
        Years > 0, Years & IF ( Years = 1, " year", " years" ),
        Months > 0, Months & IF ( Months = 1, " month", " months" ),
        "< 1 month"
    )
```

#### Selected Job Header

##### Dependencies

**Referenced Columns**
- Work Experience[Company]
- Work Experience[JobTitle]

```dax
VAR JobTitle =
    SELECTEDVALUE ( 'Work Experience'[JobTitle] )
VAR Company =
    SELECTEDVALUE ( 'Work Experience'[Company] )
RETURN
    IF (
        NOT ISBLANK ( JobTitle ) && NOT ISBLANK ( Company ),
        JobTitle & " | " & Company,
        "Professional Experience"
    )
```

#### Professional Experience HTML

##### Dependencies

**Referenced Columns**
- Achievements[AchievementId]
- Achievements[Achievement]
- Achievements[MetricPrefix]
- Achievements[MetricUnit]
- Achievements[MetricValue]
- Achievements[Type]
- Job Nav[Start Year]
- Skills[Skill]
- Work Descriptions[Desc Id]
- Work Descriptions[Desc]
- Work Experience[Company]
- Work Experience[End Date]
- Work Experience[JobTitle]
- Work Experience[Start Date]
- Work Experience[Status]

```dax
VAR ScrollH = 480
VAR TotalJobs = COUNTROWS ( ALL ( 'Work Experience' ) )
VAR HasSelection = COUNTROWS ( 'Work Experience' ) < TotalJobs
VAR SelectedStarts = VALUES ( 'Work Experience'[Start Date] )
VAR PageYear =
    SELECTEDVALUE (
        'Job Nav'[Start Year],
        MINX ( ALL ( 'Job Nav' ), 'Job Nav'[Start Year] )
    )
VAR PageNum =
    COUNTROWS ( FILTER ( ALL ( 'Job Nav' ), 'Job Nav'[Start Year] <= PageYear ) )

// Timeline selection wins; otherwise show the role that starts in the selected year
VAR ShowRows =
    FILTER (
        ALL ( 'Work Experience' ),
        IF (
            HasSelection,
            'Work Experience'[Start Date] IN SelectedStarts,
            YEAR ( 'Work Experience'[Start Date] ) = PageYear
        )
    )

VAR StatusText =
    IF (
        HasSelection,
        "Showing selection from timeline",
        "Role " & PageNum & " of " & TotalJobs
    )

VAR Jobs =
    CONCATENATEX (
        ShowRows,

        VAR Title =
            SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( 'Work Experience'[JobTitle] & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
        VAR Company =
            SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( 'Work Experience'[Company] & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )

        VAR StartDate = 'Work Experience'[Start Date]
        VAR IsCurrent =
            'Work Experience'[Status] = "Current" || ISBLANK ( 'Work Experience'[End Date] )
        VAR EndDate = IF ( IsCurrent, TODAY (), 'Work Experience'[End Date] )
        VAR DateRange =
            FORMAT ( StartDate, "mmm yyyy" ) & " – "
                & IF ( IsCurrent, "Present", FORMAT ( EndDate, "mmm yyyy" ) )
        VAR TotalMonths = DATEDIFF ( StartDate, EndDate, MONTH )
        VAR Yrs = QUOTIENT ( TotalMonths, 12 )
        VAR Mos = MOD ( TotalMonths, 12 )
        VAR Duration =
            SWITCH (
                TRUE (),
                Yrs > 0 && Mos > 0,
                    Yrs & IF ( Yrs = 1, " year ", " years " ) & Mos & IF ( Mos = 1, " month", " months" ),
                Yrs > 0, Yrs & IF ( Yrs = 1, " year", " years" ),
                Mos > 0, Mos & IF ( Mos = 1, " month", " months" ),
                "< 1 month"
            )

        VAR SkillChips =
            CONCATENATEX (
                RELATEDTABLE ( 'Skills' ),
                "<span class='chip'>"
                    & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( 'Skills'[Skill] & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
                    & "</span>",
                "",
                'Skills'[Skill], ASC
            )
        VAR Chips =
            IF ( SkillChips = "", "", "<div class='chips'>" & SkillChips & "</div>" )

        VAR BulletItems =
            CONCATENATEX (
                RELATEDTABLE ( 'Work Descriptions' ),
                IF (
                    TRIM ( 'Work Descriptions'[Desc] & "" ) = "",
                    "",
                    "<li>"
                        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( 'Work Descriptions'[Desc] & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
                        & "</li>"
                ),
                "",
                'Work Descriptions'[Desc Id], DESC
            )
        VAR Bullets =
            IF ( BulletItems = "", "", "<ul>" & BulletItems & "</ul>" )

        // Key results from the Achievements table: metrics first (big number, optional "up to"), then awards (trophy), then other results (star)
        VAR AchItems =
            CONCATENATEX (
                RELATEDTABLE ( Achievements ),
                VAR Val = Achievements[MetricValue]
                VAR Unit = TRIM ( Achievements[MetricUnit] & "" )
                VAR Prefix = TRIM ( Achievements[MetricPrefix] & "" )
                VAR IsAward = Achievements[Type] = "Award"
                VAR IsPct = LEFT ( Unit, 1 ) = "%"
                VAR Num =
                    SWITCH (
                        TRUE (),
                        NOT ISBLANK ( Val ),
                            IF ( Prefix = "", "", "<small>" & Prefix & " </small>" )
                                & IF ( IsPct, Val & "%", Val & "" ),
                        IsAward, "&#127942;",
                        "&#9733;"
                    )
                VAR UnitLbl = IF ( IsPct, TRIM ( MID ( Unit, 2, 200 ) ), Unit )
                VAR Txt =
                    SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( Achievements[Achievement] & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
                RETURN
                    "<div class='ki'><span class='kn" & IF ( ISBLANK ( Val ), " star", "" ) & "'>" & Num & "</span>"
                        & "<span class='kt'>" & Txt
                        & IF ( ISBLANK ( Val ) || UnitLbl = "", "", "<span class='ku'> &mdash; " & UnitLbl & "</span>" )
                        & "</span></div>",
                "",
                IF ( NOT ISBLANK ( Achievements[MetricValue] ), 0, IF ( Achievements[Type] = "Award", 1, 2 ) ), ASC,
                Achievements[AchievementId], ASC
            )
        VAR Results =
            IF ( AchItems = "", "", "<div class='kr'><div class='krh'>Key Results</div>" & AchItems & "</div>" )

        RETURN
            "<div class='job'>"
                & "<div class='top'>"
                & "<div><div class='role'>" & Title & "</div><div class='co'>" & Company & "</div></div>"
                & "<div class='meta'><div class='dates'>" & DateRange & "</div><div class='dur'>" & Duration & "</div></div>"
                & "</div>"
                & Chips
                & Results
                & Bullets
                & "</div>",
        "",
        'Work Experience'[Start Date], DESC
    )

VAR Css =
    "<style>"
        & ".pe{font-family:'Segoe UI',Arial,sans-serif;color:#003f88;box-sizing:border-box;padding:0 4px}"
        & ".hd{display:flex;justify-content:space-between;align-items:baseline;margin:0 0 14px;padding-bottom:8px;border-bottom:1px solid #d5dde8}"
        & ".hd h2{font-size:20px;font-weight:600;margin:0}"
        & ".st{font-size:12px;color:#6b7f99}"
        & ".scroll{max-height:" & ScrollH & "px;overflow-y:auto;padding-right:10px}"
        & ".job{border-left:4px solid #f5a800;padding-left:14px;margin-bottom:22px}"
        & ".top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}"
        & ".role{font-size:18px;font-weight:600;line-height:1.25}"
        & ".co{font-size:14px;color:#4a6a94;margin-top:2px}"
        & ".meta{text-align:right;white-space:nowrap}"
        & ".dates{font-size:13px}"
        & ".dur{font-size:12px;color:#6b7f99;margin-top:2px}"
        & ".chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}"
        & ".chip{font-size:11px;padding:3px 10px;border:1px solid #c5d3e6;border-radius:12px;background:#f2f6fb}"
        & ".kr{background:#f2f6fb;border-radius:6px;padding:8px 12px;margin:0 0 12px}"
        & ".krh{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.4px;color:#4a6a94;margin-bottom:4px}"
        & ".ki{display:flex;gap:10px;align-items:baseline;margin:3px 0}"
        & ".kn{min-width:46px;font-size:18px;font-weight:700;color:#f5a800;line-height:1.2;white-space:nowrap}"
        & ".kn small{font-size:10px;font-weight:600;color:#4a6a94;text-transform:uppercase;letter-spacing:.4px}"
        & ".kn.star{font-size:13px;text-align:center}"
        & ".kt{font-size:13px;font-weight:600;color:#1f3a5f;line-height:1.4}"
        & ".ku{font-weight:400;color:#4a6a94}"
        & ".pe ul{margin:0;padding-left:18px}"
        & ".pe li{font-size:13px;line-height:1.5;margin-bottom:4px;color:#1f3a5f}"
        & "</style>"

RETURN
    IF (
        Jobs = "",
        BLANK (),
        Css
            & "<div class='pe'>"
            & "<div class='hd'><h2>Professional Experience</h2><span class='st'>" & StatusText & "</span></div>"
            & "<div class='scroll'>" & Jobs & "</div></div>"
    )
```

#### PagerYear

##### Dependencies

**Referenced Columns**
- Job Nav[Start Year]

```dax
SELECTEDVALUE (
    'Job Nav'[Start Year],
    MINX ( ALL ( 'Job Nav' ), 'Job Nav'[Start Year] )
)
```

#### Current Project Id

##### Dependencies

**Referenced Columns**
- Projects[ProjectId]

```dax
SELECTEDVALUE (
    Projects[ProjectId],
    MINX ( ALL ( Projects ), Projects[ProjectId] )
)
```

#### Project Gallery HTML

##### Dependencies

**Referenced Measures**
- Current Project Id

**Referenced Columns**
- Assets[Caption]
- Assets[ImageId]
- Assets[ProjectId]
- Assets[ScreenshotUrl]
- Projects[Business Value]
- Projects[Name]
- Projects[ProjectId]
- Projects[Summary]
- Projects[Tools]

```dax
VAR CurId = [Current Project Id]
VAR P = FILTER ( ALL ( Projects ), Projects[ProjectId] = CurId )
VAR ToolDelim = ", "

VAR _Name =
    SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( MAXX ( P, Projects[Name] ) & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
VAR Summary =
    SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( MAXX ( P, Projects[Summary] ) & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
VAR BizValue =
    SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( MAXX ( P, Projects[Business Value] ) & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
VAR Tools =
    SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( MAXX ( P, Projects[Tools] ) & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )

// Tools are comma-separated; a leading * marks a tool built by me (gold chip)
VAR vChipItems =
    SUBSTITUTE (
        "<span class='chip'>"
            & SUBSTITUTE ( Tools, ToolDelim, "</span><span class='chip'>" )
            & "</span>",
        "<span class='chip'>*",
        "<span class='chip mine'>"
    )
VAR vLegend =
    IF (
        CONTAINSSTRING ( Tools, "*" ),
        "<span class='legend'><span class='chip mine'>Built by me</span></span>",
        ""
    )
VAR vChips =
    IF (
        Tools = "",
        "",
        "<div class='chips'>" & vChipItems & vLegend & "</div>"
    )

VAR BizValueHtml =
    IF ( BizValue = "", "", "<div class='sum'>" & BizValue & "</div>" )

// Grid tiles (2 columns): each screenshot sits in a fixed 16:10 frame (object-fit: contain) and links to the full-size image
VAR Shots =
    CONCATENATEX (
        FILTER ( ALL ( Assets ), Assets[ProjectId] = CurId ),
        "<figure class='shot'><a class='frame' href='" & Assets[ScreenshotUrl] & "' target='_blank'><img src='" & Assets[ScreenshotUrl] & "'/></a>"
            & IF (
                TRIM ( Assets[Caption] & "" ) = "",
                "",
                "<figcaption>"
                    & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( Assets[Caption] & "", "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" )
                    & "</figcaption>"
            )
            & "</figure>",
        "",
        Assets[ImageId], ASC
    )

VAR Css =
    "<style>"
        & ".pg{font-family:'Segoe UI',Arial,sans-serif;color:#003f88;box-sizing:border-box;padding:0 4px}"
        & ".hd{display:flex;justify-content:space-between;align-items:baseline;margin:0 0 14px;padding-bottom:8px;border-bottom:1px solid #d5dde8}"
        & ".hd h2{font-size:20px;font-weight:600;margin:0}"
        & ".st{font-size:12px;color:#6b7f99}"
        & ".proj{border-left:4px solid #f5a800;padding-left:14px}"
        & ".pname{font-size:18px;font-weight:600;line-height:1.25}"
        & ".sum{font-size:13px;line-height:1.5;color:#1f3a5f;margin-top:6px}"
        & ".chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}"
        & ".chip{font-size:11px;padding:3px 10px;border:1px solid #c5d3e6;border-radius:12px;background:#f2f6fb}"
        & ".shots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;padding:4px 0 10px}"
        & ".shot{margin:0;min-width:0}"
        & ".shot .frame{display:flex;align-items:center;justify-content:center;aspect-ratio:16/10;background:#f2f6fb;border:1px solid #d5dde8;border-radius:4px;overflow:hidden;padding:6px;box-sizing:border-box}"
        & ".shot .frame:hover{border-color:#f5a800}"
        & ".shot img{max-width:100%;max-height:100%;object-fit:contain;display:block}"
        & ".shot figcaption{font-size:12px;font-weight:600;color:#4a6a94;margin-top:6px;text-align:center}"
        & ".chip.mine{border-color:#f5a800;background:#fff8e6}"
        & ".legend{margin-left:auto}"
        & "</style>"

RETURN
    IF (
        _Name = "",
        BLANK (),
        Css
            & "<div class='pg'>"
            & "<div class='hd'><h2>Project Portfolio</h2><span class='st'>Sample data - names and identifiers changed</span></div>"
            & "<div class='proj'><div class='pname'>" & _Name & "</div>"
            & "<div class='sum'>" & Summary & "</div>"
            & BizValueHtml
            & vChips
            & "<div class='shots'>" & Shots & "</div></div></div>"
    )
```

#### Repo Link

##### Dependencies

**Referenced Measures**
- Current Project Id

**Referenced Columns**
- Projects[ProjectId]
- Projects[RepoUrl]

```dax
VAR CurId = [Current Project Id]
RETURN
    MAXX (
        FILTER ( ALL ( Projects ), Projects[ProjectId] = CurId ),
        Projects[RepoUrl]
    )
```

#### Report Link

##### Dependencies

**Referenced Measures**
- Current Project Id

**Referenced Columns**
- Projects[FileUrl]
- Projects[ProjectId]

```dax
VAR CurId = [Current Project Id]
RETURN
    MAXX (
        FILTER ( ALL ( Projects ), Projects[ProjectId] = CurId ),
        Projects[FileUrl]
    )
```

#### Years of Experience

##### Dependencies

**Referenced Columns**
- Work Experience[Start Date]

```dax
VAR StartDate =
    MINX ( ALL ( 'Work Experience' ), 'Work Experience'[Start Date] )
VAR TotalMonths =
    DATEDIFF ( StartDate, TODAY (), MONTH )
RETURN
    DIVIDE ( TotalMonths, 12 )
```

#### Certification Count
```dax
COUNTROWS ( Certifications )
```

#### Active Certification Count

##### Dependencies

**Referenced Columns**
- Certifications[ExpirationDate]
- Certifications[IssueDate]

```dax
COUNTROWS (
    FILTER (
        Certifications,
        NOT ISBLANK ( Certifications[IssueDate] )
            && (
                ISBLANK ( Certifications[ExpirationDate] )
                    || Certifications[ExpirationDate] >= TODAY ()
            )
    )
) + 0
```

#### Expired Certification Count

##### Dependencies

**Referenced Columns**
- Certifications[ExpirationDate]

```dax
COUNTROWS (
    FILTER (
        Certifications,
        NOT ISBLANK ( Certifications[ExpirationDate] )
            && Certifications[ExpirationDate] < TODAY ()
    )
) + 0
```

#### Profile Header HTML

##### Dependencies

**Referenced Measures**
- Current Company
- Current Role

**Referenced Columns**
- Profile[Location]
- Profile[Summary]

```dax
VAR Esc = "&amp;"
VAR Loc = SUBSTITUTE ( MAX ( Profile[Location] ), "&", Esc )
VAR Summary = SUBSTITUTE ( MAX ( Profile[Summary] ), "&", Esc )
VAR Email = "fosterbiservices@gmail.com"
VAR RoleLine =
    SUBSTITUTE ( [Current Role] & " at " & [Current Company], "&", Esc )

// Name and headline live in the page header band (Header Band HTML); this card is the About section
VAR Css =
    "<style>"
        & ".ph{font-family:'Segoe UI',Arial,sans-serif;color:#003f88;box-sizing:border-box;padding:0 4px}"
        & ".ph h2{font-size:18px;font-weight:600;margin:0 0 10px;padding-bottom:8px;border-bottom:1px solid #d5dde8}"
        & ".ph .meta{display:flex;gap:18px;flex-wrap:wrap;font-size:13px;color:#6b7f99}"
        & ".ph .meta b{color:#003f88;font-weight:600}"
        & ".ph .sum{border-left:4px solid #f5a800;padding:2px 0 2px 14px;margin-top:14px;font-size:14px;line-height:1.55;color:#1f3a5f}"
        & "</style>"

RETURN
    Css
        & "<div class='ph'>"
        & "<h2>About</h2>"
        & "<div class='meta'><span><b>Currently:</b> " & RoleLine & "</span><span><b>Location:</b> " & Loc & "</span><span><b>Email:</b> " & Email & "</span></div>"
        & "<div class='sum'>" & Summary & "</div>"
        & "</div>"
```

#### Key Achievements HTML

##### Dependencies

**Referenced Columns**
- Achievements[Achievement]
- Achievements[JobId]
- Achievements[MetricPrefix]
- Achievements[MetricUnit]
- Achievements[MetricValue]
- Achievements[Type]
- Work Experience[Company]

```dax
VAR Items =
    CONCATENATEX (
        Achievements,
        VAR Txt = SUBSTITUTE ( Achievements[Achievement], "&", "&amp;" )
        VAR Co = SUBSTITUTE ( RELATED ( 'Work Experience'[Company] ), "&", "&amp;" )
        VAR Val = Achievements[MetricValue]
        VAR Unit = TRIM ( Achievements[MetricUnit] & "" )
        VAR Prefix = TRIM ( Achievements[MetricPrefix] & "" )
        VAR IsAward = Achievements[Type] = "Award"
        VAR IsPct = LEFT ( Unit, 1 ) = "%"
        VAR BigNum = IF ( IsPct, Val & "%", Val & "" )
        // non-breaking hyphen keeps words like "on-time" together
        VAR UnitLbl =
            SUBSTITUTE ( IF ( IsPct, TRIM ( MID ( Unit, 2, 200 ) ), Unit ), "-", "&#8209;" )
        VAR Metric =
            SWITCH (
                TRUE (),
                NOT ISBLANK ( Val ),
                    "<div class='num'>"
                        & IF ( Prefix = "", "", "<span class='pre'>" & Prefix & "</span>" )
                        & BigNum & "</div>",
                IsAward, "<div class='ico'>&#127942;</div>",
                "<div class='ico'>&#9733;</div>"
            )
        VAR Detail =
            IF ( ISBLANK ( Val ), "", " <span class='unit'>&mdash; " & UnitLbl & "</span>" )
        RETURN
            "<div class='ach'>" & Metric
                & "<div><div class='txt'>" & Txt & Detail & "</div>"
                & "<div class='co'>" & Co & "</div></div></div>",
        "",
        // metrics first, then awards, then other results; newest role first within each group
        IF ( NOT ISBLANK ( Achievements[MetricValue] ), 0, IF ( Achievements[Type] = "Award", 1, 2 ) ), ASC,
        Achievements[JobId], DESC
    )

VAR Css =
    "<style>"
        & ".ka{font-family:'Segoe UI',Arial,sans-serif;color:#003f88;box-sizing:border-box;padding:0 4px}"
        & ".ka h2{font-size:18px;font-weight:600;margin:0 0 10px;padding-bottom:8px;border-bottom:1px solid #d5dde8}"
        & ".ach{display:flex;gap:12px;align-items:flex-start;margin-bottom:8px}"
        & ".num{min-width:56px;font-size:22px;font-weight:700;color:#f5a800;line-height:1.1}"
        & ".pre{display:block;font-size:9px;font-weight:600;color:#4a6a94;text-transform:uppercase;letter-spacing:.4px;line-height:1.1}"
        & ".ico{min-width:56px;font-size:16px;color:#f5a800;line-height:1.3;text-align:center}"
        & ".txt{font-size:13px;font-weight:600;line-height:1.35;color:#1f3a5f}"
        & ".unit{font-weight:400;color:#4a6a94}"
        & ".co{font-size:10px;color:#6b7f99;margin-top:1px;text-transform:uppercase;letter-spacing:.4px}"
        & "</style>"

RETURN
    IF (
        Items = "",
        BLANK (),
        Css & "<div class='ka'><h2>Key Achievements</h2>" & Items & "</div>"
    )
```

#### Skills by Category HTML

##### Dependencies

**Referenced Columns**
- Skills[Category]
- Skills[SkillId]
- Skills[Skill]

```dax
VAR Groups =
    CONCATENATEX (
        VALUES ( Skills[Category] ),
        VAR Cat = Skills[Category]
        VAR Chips =
            CONCATENATEX (
                FILTER ( ALL ( Skills ), Skills[Category] = Cat ),
                "<span class='chip'>" & SUBSTITUTE ( Skills[Skill], "&", "&amp;" ) & "</span>",
                "",
                Skills[SkillId], ASC
            )
        RETURN
            "<div class='grp'><div class='cat'>" & SUBSTITUTE ( Cat, "&", "&amp;" ) & "</div>"
                & "<div class='chips'>" & Chips & "</div></div>",
        "",
        CALCULATE ( MIN ( Skills[SkillId] ) ), ASC
    )

VAR Css =
    "<style>"
        & ".sk{font-family:'Segoe UI',Arial,sans-serif;color:#003f88;box-sizing:border-box;padding:0 4px}"
        & ".sk h2{font-size:18px;font-weight:600;margin:0 0 12px;padding-bottom:8px;border-bottom:1px solid #d5dde8}"
        & ".grp{margin-bottom:12px}"
        & ".cat{font-size:11px;font-weight:600;color:#4a6a94;text-transform:uppercase;letter-spacing:.4px;margin-bottom:5px}"
        & ".chips{display:flex;flex-wrap:wrap;gap:6px}"
        & ".chip{font-size:12px;padding:3px 10px;border:1px solid #c5d3e6;border-radius:12px;background:#f2f6fb;color:#003f88}"
        & "</style>"

RETURN
    IF (
        Groups = "",
        BLANK (),
        Css & "<div class='sk'><h2>Core Skills</h2>" & Groups & "</div>"
    )
```

#### Certifications HTML

##### Dependencies

**Referenced Measures**
- Active Certification Count
- Certification Count
- Expired Certification Count

**Referenced Columns**
- Certifications[CertId]
- Certifications[Certification]
- Certifications[CredentialId]
- Certifications[ExpirationDate]
- Certifications[IssueDate]
- Certifications[Issuer]

```dax
VAR Today = TODAY ()
VAR Items =
    CONCATENATEX (
        Certifications,
        VAR Issued = Certifications[IssueDate]
        VAR Expires = Certifications[ExpirationDate]
        VAR IsExpired = NOT ISBLANK ( Expires ) && Expires < Today
        VAR HasDates = NOT ISBLANK ( Issued ) || NOT ISBLANK ( Expires )
        VAR Badge =
            SWITCH (
                TRUE (),
                IsExpired, "<span class='badge exp'>Expired</span>",
                HasDates, "<span class='badge act'>Active</span>",
                ""
            )
        VAR IssuedTxt =
            IF ( ISBLANK ( Issued ), "", "Issued " & FORMAT ( Issued, "mmm yyyy" ) )
        VAR ExpTxt =
            SWITCH (
                TRUE (),
                ISBLANK ( Expires ), IF ( ISBLANK ( Issued ), "", "No expiration" ),
                IsExpired, "Expired " & FORMAT ( Expires, "mmm yyyy" ),
                "Expires " & FORMAT ( Expires, "mmm yyyy" )
            )
        VAR DateLine =
            IssuedTxt & IF ( IssuedTxt <> "" && ExpTxt <> "", " &middot; ", "" ) & ExpTxt
        VAR CredLine =
            IF (
                Certifications[CredentialId] = "",
                "",
                "<div class='cid'>Credential ID " & Certifications[CredentialId] & "</div>"
            )
        RETURN
            "<div class='cert" & IF ( IsExpired, " old", "" ) & "'>"
                & "<div class='top'><div class='nm'>" & SUBSTITUTE ( Certifications[Certification], "&", "&amp;" ) & "</div>" & Badge & "</div>"
                & "<div class='iss'>" & SUBSTITUTE ( Certifications[Issuer], "&", "&amp;" ) & "</div>"
                & IF ( DateLine = "", "", "<div class='dt'>" & DateLine & "</div>" )
                & CredLine
                & "</div>",
        "",
        IF ( NOT ISBLANK ( Certifications[ExpirationDate] ) && Certifications[ExpirationDate] < Today, 1, 0 ), ASC,
        Certifications[IssueDate], DESC,
        Certifications[CertId], ASC
    )

VAR StatusText =
    [Certification Count] & " total &middot; "
        & [Active Certification Count] & " active &middot; "
        & [Expired Certification Count] & " expired"

VAR Css =
    "<style>"
        & ".ce{font-family:'Segoe UI',Arial,sans-serif;color:#003f88;box-sizing:border-box;padding:0 4px}"
        & ".ce .hd{display:flex;justify-content:space-between;align-items:baseline;margin:0 0 12px;padding-bottom:8px;border-bottom:1px solid #d5dde8}"
        & ".ce h2{font-size:18px;font-weight:600;margin:0}"
        & ".ce .st{font-size:12px;color:#6b7f99}"
        & ".cert{border-left:4px solid #f5a800;padding:2px 0 2px 12px;margin-bottom:14px}"
        & ".cert.old{border-left-color:#c8c6c4}"
        & ".cert.old .nm,.cert.old .iss{color:#8a8886}"
        & ".top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}"
        & ".nm{font-size:14px;font-weight:600;line-height:1.3;color:#1f3a5f}"
        & ".iss{font-size:13px;color:#4a6a94;margin-top:1px}"
        & ".dt,.cid{font-size:12px;color:#6b7f99;margin-top:1px}"
        & ".badge{font-size:10px;font-weight:600;padding:2px 8px;border-radius:10px;white-space:nowrap;text-transform:uppercase;letter-spacing:.4px}"
        & ".badge.act{background:#e3f4e8;color:#1b7a3a;border:1px solid #9fd5b0}"
        & ".badge.exp{background:#f3f2f1;color:#8a8886;border:1px solid #d2d0ce}"
        & "</style>"

RETURN
    IF (
        Items = "",
        BLANK (),
        Css
            & "<div class='ce'><div class='hd'><h2>Licenses &amp; Certifications</h2><span class='st'>" & StatusText & "</span></div>"
            & Items & "</div>"
    )
```

#### Header Band HTML

##### Dependencies

**Referenced Columns**
- Profile[Headline]
- Profile[Name]

```dax
VAR FullName = SUBSTITUTE ( MAX ( Profile[Name] ), "&", "&amp;" )
VAR Headline = SUBSTITUTE ( MAX ( Profile[Headline] ), "&", "&amp;" )
RETURN
    "<div style='font-family:Segoe UI,Arial,sans-serif;display:flex;align-items:baseline;gap:14px;white-space:nowrap;padding-top:6px'>"
        & "<span style='font-size:24px;font-weight:700;color:#FFFFFF;letter-spacing:.3px'>" & FullName & "</span>"
        & "<span style='font-size:14px;color:#c5d3e6'>" & Headline & "</span>"
        & "</div>"
```

## Achievements

No description provided.

### Statistics

- Columns: 7
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Related Tables

- Work Experience

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| AchievementId |  | No | No |  |
| JobId |  | No | No |  |
| Achievement |  | No | No |  |
| MetricValue |  | No | No |  |
| MetricUnit |  | No | No |  |
| MetricPrefix |  | No | No |  |
| Type |  | No | No |  |

## Assets

No description provided.

### Statistics

- Columns: 4
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 2
- Date Columns: 0
- Numeric Columns: 2

### Related Tables

- Projects

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| ImageId | int64 | No | No |  |
| ProjectId | int64 | No | No |  |
| Caption | string | No | No |  |
| ScreenshotUrl | string | No | No | ImageId |

## Certifications

No description provided.

### Statistics

- Columns: 6
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
| CertId |  | No | No |  |
| Certification |  | No | No |  |
| Issuer |  | No | No |  |
| IssueDate |  | No | No |  |
| ExpirationDate |  | No | No |  |
| CredentialId |  | No | No |  |

## Date

No description provided.

### Statistics

- Columns: 5
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Related Tables

- Work Experience

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| Date |  | No | No |  |
| Year |  | No | No |  |
| Month Number |  | No | No |  |
| Month |  | No | No |  |
| Year Month |  | No | No |  |

## Job Nav

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
| Start Year |  | No | No |  |

## Job Skills

No description provided.

### Statistics

- Columns: 2
- Measures: 0
- Relationships: 2
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Related Tables

- Skills
- Work Experience

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| JobId |  | No | No |  |
| SkillId |  | No | No |  |

## Profile

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
| Name |  | No | No |  |
| Headline |  | No | No |  |
| Location |  | No | No |  |
| Summary |  | No | No |  |

## Projects

No description provided.

### Statistics

- Columns: 8
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 6
- Date Columns: 0
- Numeric Columns: 2

### Related Tables

- Assets

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| ProjectId | int64 | No | No |  |
| Name | string | No | No |  |
| RepoUrl | string | No | No |  |
| FileUrl | string | No | No |  |
| Summary | string | No | No |  |
| Business Value | string | No | No |  |
| Tools | string | No | No |  |
| JobId | int64 | No | No |  |

## Skills

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Related Tables

- Job Skills

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| SkillId |  | No | No |  |
| Skill |  | No | No |  |
| Category |  | No | No |  |

## Work Descriptions

No description provided.

### Statistics

- Columns: 3
- Measures: 0
- Relationships: 1
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Related Tables

- Work Experience

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| JobId |  | No | No |  |
| Desc Id |  | No | No |  |
| Desc |  | No | No |  |

## Work Experience

No description provided.

### Statistics

- Columns: 9
- Measures: 0
- Relationships: 5
- Hidden Columns: 0

### Summary

- String Columns: 0
- Date Columns: 0
- Numeric Columns: 0

### Related Tables

- Achievements
- Date
- Job Skills
- Work Descriptions

### Columns

| Column | Data Type | Hidden | Key | Sort By |
|---|---|---:|---:|---|
| JobId |  | No | No |  |
| JobTitle |  | No | No | JobId |
| Company |  | No | No |  |
| StartDate |  | No | No |  |
| EndDate |  | No | No |  |
| Status |  | No | No |  |
| Start Date |  | No | No |  |
| End Date |  | No | No |  |
| Start Year |  | No | No |  |

# Relationships

| From | To | Cardinality | Direction | Active |
|---|---|---|---|---:|
| Work Experience[End Date] | Date[Date] | many to one | oneDirection | No |
| Work Experience[Start Date] | Date[Date] | many to one | oneDirection | Yes |
| Achievements[JobId] | Work Experience[JobId] | many to one | oneDirection | Yes |
| Work Descriptions[JobId] | Work Experience[JobId] | many to one | oneDirection | Yes |
| Assets[ProjectId] | Projects[ProjectId] | many to one | oneDirection | Yes |
| Job Skills[JobId] | Work Experience[JobId] | many to one | oneDirection | Yes |
| Job Skills[SkillId] | Skills[SkillId] | many to one | bothDirections | Yes |

# Validation

- Model parsed successfully: Yes
- Errors: 0
- Warnings: 0
