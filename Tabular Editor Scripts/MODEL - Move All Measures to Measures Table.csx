// Ensure a table named '__Measures' exists
var measuresTableName = "__Measures";
var measuresTable = Model.Tables.FirstOrDefault(t => t.Name == measuresTableName);

if (measuresTable == null)
{
    // Create the '__Measures' table if it doesn't exist
    measuresTable = Model.AddCalculatedTable(measuresTableName, "SELECTCOLUMNS( { }, \"Dummy\", 0 )");
    measuresTable.IsHidden = true; // Hide the table to reduce clutter
}

// Iterate through all measures in the model
foreach (var measure in Model.AllMeasures.ToList()) // Use ToList to avoid modifying the collection during iteration
{
    // Store the current table name
    var originalTableName = measure.Table.Name;

    // Move the measure to the '__Measures' table
    measure.MoveTo(measuresTable);

    // Set the display folder to the original table name
    measure.DisplayFolder = originalTableName;
}

