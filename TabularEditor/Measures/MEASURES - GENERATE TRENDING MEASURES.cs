// Loop through all selected measures in the model
foreach (var measure in Selected.Measures)
{
    // Build the new measure name
    var trendMeasureName = measure.Name + " Trend";

    // Define the DAX expression for the new measure
    var daxExpression = $@"
VAR __Result =
    CALCULATE
    (
        [{measure.Name}],
        ALL( 'dimDates' ),
        'dimDates'[Month Filter] = SELECTEDVALUE( 'Dynamic Slicer'[Month] )
    )
RETURN
    IF
    (
        NOT ISINSCOPE( 'Dynamic Slicer'[Month] ),
        [{measure.Name}],
        IF
        (
            SELECTEDVALUE( 'Dynamic Slicer'[Month Sort] ) <= MAX( 'dimDates'[Month Sort] )
            && SELECTEDVALUE( 'Dynamic Slicer'[Month Sort] ) >= MAX( 'dimDates'[Month Sort] ) - 3,
            __Result
        )
    )";

    // Check if a measure with the same name already exists
    if (measure.Table.Measures.Contains(trendMeasureName))
    {
        // Skip or optionally overwrite the existing measure
        continue;
    }

    // Create the new trend measure in the same table as the selected measure
    var trendMeasure = measure.Table.AddMeasure(trendMeasureName);
    trendMeasure.Expression = daxExpression;
    trendMeasure.FormatString = measure.FormatString; // Optional: use the same format as the original measure
}
