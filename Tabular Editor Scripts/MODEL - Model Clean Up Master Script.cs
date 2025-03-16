// Hide all columns on many side of a join

foreach (var r in Model.Relationships)
{ // hide all columns on the many side of a join
    var c = r.FromColumn.Name;
    var t = r.FromTable.Name;
    Model.Tables[t].Columns[c].IsHidden = true;
}

// Hide all columns ending with "Key" in selected tables from report

var keySuffix = "Key";

// Loop through all currently selected tables:
foreach(var t in Model.Tables)
{
    // Loop through all columns ending with "Key" on the current table:
    foreach(var k in t.Columns.Where(c => c.Name.EndsWith(keySuffix)))
    {
        k.IsHidden = true;
    }
}
// Format Dates as ShortDate 
foreach(var c in Model.AllColumns.Where(a => a.DataType == DataType.DateTime)) {
	c.FormatString = "m/d/yyyy";
}

// Format All Measures 

Model.AllMeasures.FormatDax();


// Column Clean up 
var sb = new System.Text.StringBuilder();
string newline = Environment.NewLine;

// Remove default Agg functions

foreach(var c in Model.AllColumns.Where(a => a.DataType == DataType.Int64 || a.DataType == DataType.Decimal || a.DataType == DataType.Double)) {
	c.SummarizeBy = AggregateFunction.None;

// Place columns in TableColumn Display folder 
}
foreach(var c in Model.AllColumns) {
c.DisplayFolder = "TableColumns";
}

// Place measures in KPI display folder 
foreach(var m in Model.AllMeasures) {
 if(m.DisplayFolder == "")
    {
m.DisplayFolder = "KPIs";

    }

// Loop through all tables and move calculated columns to the "_TableCalculatedColumns" folder
foreach (var t in Model.Tables)
{
    foreach (var calcColumn in t.CalculatedColumns)
    {
        calcColumn.DisplayFolder = "TableCalculatedColumns";
    }
}

};