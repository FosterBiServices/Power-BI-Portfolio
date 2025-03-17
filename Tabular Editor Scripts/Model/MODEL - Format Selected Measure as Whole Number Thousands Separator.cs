// Loop through all selected measures in the Tabular Editor
foreach(var measure in Selected.Measures)
{
    // Set the format string to "#,0; (#,0)" for each selected measure
    measure.FormatString = "#,0; (#,0)";
}
