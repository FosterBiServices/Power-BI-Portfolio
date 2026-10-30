// Check if any measures are selected
if (!Selected.Measures.Any())
{
    Error("No measures selected. Please select at least one measure and run the script again.");
    return;
}

// Prompt the user to select a date table
Table dateTableCandidate = null;

if (Model.Tables.Any(x => 
    x.GetAnnotation("@StevenFoster") == "Time Intel Date Table" ||
    x.Name == "dimDate" ||
    x.Name == "dimDates" ||
    x.Name == "Calendar")) {
    dateTableCandidate = Model.Tables.Where(x => 
        x.GetAnnotation("@StevenFoster") == "Time Intel Date Table" ||
        x.Name == "dimDate" ||
        x.Name == "dimDates" ||
        x.Name == "Calendar").First();
}

var dateTable = SelectTable(
    label: "Select your date table",
    preselect: dateTableCandidate
);

if (dateTable == null) {
    Error("You just aborted the script");
    return;
} else {
    dateTable.SetAnnotation("@StevenFoster", "Time Intel Date Table");
}

// Prompt the user to select a date column
Column dateTableDateColumnCandidate = null;

if (dateTable.Columns.Any(x => 
    x.GetAnnotation("@StevenFoster") == "Time Intel Date Table Date Column" ||
    x.Name == "Fiscal Date" ||
    x.Name == "DateValue")) {
    dateTableDateColumnCandidate = dateTable.Columns.Where(x => 
        x.GetAnnotation("@StevenFoster") == "Time Intel Date Table Date Column" ||
        x.Name == "Fiscal Date" ||
        x.Name == "DateValue").First();
}

var dateTableDateColumn = SelectColumn(
    dateTable.Columns,
    label: "Select the date column",
    preselect: dateTableDateColumnCandidate
);

if (dateTableDateColumn == null) {
    Error("You just aborted the script");
    return;
} else {
    dateTableDateColumn.SetAnnotation("@StevenFoster", "Time Intel Date Table Date Column");
}

// Generate measures for each selected measure
string displayFolder = "TimeIntelligence KPIs";

foreach (var measure in Selected.Measures)
{
    if (measure != null)
    {
        string baseMeasureName = measure.Name;
        string baseExpression = measure.Expression;

        string dateTableRef = $"{dateTable.Name}";
        string dateColumnRef = $"[{dateTableDateColumn.Name}]";

        // Month-to-Date (MTD)
        string mtdMeasureName = baseMeasureName + " MTD";
        string mtdExpression = $@"
CALCULATE(
    {baseExpression},
    DATESMTD({dateTableRef}{dateColumnRef})
)";
        var mtdMeasure = measure.Table.AddMeasure(mtdMeasureName, mtdExpression);
        mtdMeasure.DisplayFolder = displayFolder;

        // Previous Month-to-Date (PMTD)
        string pmtMeasureName = baseMeasureName + " PMTD";
        string pmtExpression = $@"
CALCULATE(
    {baseExpression},
    DATESMTD(DATEADD({dateTableRef}{dateColumnRef}, -1, MONTH))
)";
        var pmtMeasure = measure.Table.AddMeasure(pmtMeasureName, pmtExpression);
        pmtMeasure.DisplayFolder = displayFolder;

        // Year-to-Date (YTD)
        string ytdMeasureName = baseMeasureName + " YTD";
        string ytdExpression = $@"
CALCULATE(
    {baseExpression},
    DATESYTD({dateTableRef}{dateColumnRef})
)";
        var ytdMeasure = measure.Table.AddMeasure(ytdMeasureName, ytdExpression);
        ytdMeasure.DisplayFolder = displayFolder;

        // Previous Year-to-Date (PYTD)
        string pytMeasureName = baseMeasureName + " PYTD";
        string pytExpression = $@"
CALCULATE(
    {baseExpression},
    DATESYTD(DATEADD({dateTableRef}{dateColumnRef}, -1, YEAR))
)";
        var pytMeasure = measure.Table.AddMeasure(pytMeasureName, pytExpression);
        pytMeasure.DisplayFolder = displayFolder;

        // Month-over-Month (MoM) Value
        string momValueMeasureName = baseMeasureName + " MoM Value";
        string momValueExpression = $@"
[{mtdMeasureName}] - [{pmtMeasureName}]
";
        var momValueMeasure = measure.Table.AddMeasure(momValueMeasureName, momValueExpression);
        momValueMeasure.DisplayFolder = displayFolder;

        // Month-over-Month (MoM) Percentage
        string momPercentMeasureName = baseMeasureName + " MoM %";
        string momPercentExpression = $@"
DIVIDE(
    [{momValueMeasureName}],
    [{pmtMeasureName}]
)
";
        var momPercentMeasure = measure.Table.AddMeasure(momPercentMeasureName, momPercentExpression);
        momPercentMeasure.DisplayFolder = displayFolder;

        // Year-over-Year (YoY) Value
        string yoyValueMeasureName = baseMeasureName + " YoY Value";
        string yoyValueExpression = $@"
[{ytdMeasureName}] - [{pytMeasureName}]
";
        var yoyValueMeasure = measure.Table.AddMeasure(yoyValueMeasureName, yoyValueExpression);
        yoyValueMeasure.DisplayFolder = displayFolder;

        // Year-over-Year (YoY) Percentage
        string yoyPercentMeasureName = baseMeasureName + " YoY %";
        string yoyPercentExpression = $@"
DIVIDE(
    [{yoyValueMeasureName}],
    [{pytMeasureName}]
)
";
        var yoyPercentMeasure = measure.Table.AddMeasure(yoyPercentMeasureName, yoyPercentExpression);
        yoyPercentMeasure.DisplayFolder = displayFolder;
    }
}

// Inform the user
Info("MTD, PMTD, YTD, PYTD, MoM Value, MoM %, YoY Value, and YoY % measures created and added to the 'TimeIntelligence KPIs' folder for the selected measures.");
