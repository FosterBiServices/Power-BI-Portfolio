#r "Microsoft.VisualBasic"
using Microsoft.VisualBasic;
using System.Linq;
using System.Collections.Generic;

// Gets table and column to be used in filters. 
var factTable = SelectTable(label: "Select your table");
if (factTable == null) {
    Error("You just aborted the script.");
    return;
};

var factTableColumn = SelectColumn(factTable.Columns, label: "Select the column to be used as a filter");
if (factTableColumn == null) {
    Error("You just aborted the script.");
    return;
};

string factTableName = factTable.Name;
string factTableColumnName = factTableColumn.Name;
string factTablewithColumn = $"'{factTableName}'[{factTableColumnName}]";

// *** TEMPORARY SOLUTION ***
// Since we can't access actual column values, prompt the user to enter values manually.
string userInput = Interaction.InputBox("Enter unique values for the selected column, separated by commas:", 
                                        "Enter Values", "Value1,Value2,Value3");
if (string.IsNullOrWhiteSpace(userInput)) {
    Error("No values were entered.");
    return;
}

// Convert input to a list of unique values.
var uniqueValues = userInput.Split(',')
                            .Select(v => v.Trim())
                            .Where(v => !string.IsNullOrEmpty(v))
                            .Distinct()
                            .ToList();

if (uniqueValues.Count == 0) {
    Error("No valid unique values found.");
    return;
}

// Get existing measure names to avoid duplication issues.
var existingMeasureNames = factTable.Measures.Select(m => m.Name).ToHashSet();

// Create a measure for each unique value in the selected column.
foreach (var c in Selected.Measures) {
    foreach (var value in uniqueValues) {
        string measureName = $"{c.Name} - {value}";

        // Ensure the measure name is unique
        if (existingMeasureNames.Contains(measureName)) {
            int counter = 1;
            string newMeasureName;
            do {
                newMeasureName = $"{measureName} ({counter})";
                counter++;
            } while (existingMeasureNames.Contains(newMeasureName));
            measureName = newMeasureName;
        }

        // Create the DAX expression for the measure.
        string daxExpression = $"CALCULATE({c.DaxObjectFullName}, {factTablewithColumn} = \"{value}\")";

        var newMeasure = c.Table.AddMeasure(
            measureName,    // Unique measure name
            daxExpression   // DAX expression
        );

        // Set the format string on the new measure:
        newMeasure.FormatString = "#,#";

        // Provide some documentation:
        newMeasure.Description = $"This measure is {c.Name} where {factTablewithColumn} equals {value}.";

        // Hide the base column:
        c.IsHidden = false;

        // Add the measure name to the existing names collection:
        existingMeasureNames.Add(measureName);
    }
}
