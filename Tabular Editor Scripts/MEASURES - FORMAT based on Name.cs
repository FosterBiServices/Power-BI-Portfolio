// Loop through all selected measures in the Tabular Editor
foreach(var measure in Selected.Measures)
{
    // Define your dynamic condition for the format string
    // Here, as an example, we use a condition based on the measure's name. You can customize this logic.
    string dynamicFormatString = "#,0; (#,0)";  // Default format
    
    // Example: You could have different formats based on measure's name or other conditions.
    if (measure.Name.Contains("Prime Days"))
    {
        dynamicFormatString = "#,0.00; (#,0.00)"; // For 'Prime Days' measure, use 2 decimal places
    }
    // Example: You could have different formats based on measure's name or other conditions.
    else if (measure.Name.Contains("/") && !measure.Name.Contains("%"))
    {
        dynamicFormatString = "#,0.0; (#,0.0)"; // For 'Per something' measures that are not also percentages, use 1 decimal places
    }
    else if (measure.Name.Contains("%"))
    {
        dynamicFormatString = "#,0.0%; (#,0.0%)"; // For '%' measures, use percentage format
    }

    // Set the dynamic format string to each measure
    measure.FormatString = dynamicFormatString;
}
