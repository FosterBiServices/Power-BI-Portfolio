#r "Microsoft.VisualBasic"
using Microsoft.VisualBasic;
using System.Linq;
using System.Collections.Generic;

// Get all available measures in the model
var allMeasures = Model.AllMeasures.ToList();

// Prompt user to select multiple numerator measures at once
var numeratorMeasureNames = Interaction.InputBox(
    "Enter the names of numerator measures separated by commas:", 
    "Select Numerator Measures", 
    string.Join(", ", allMeasures.Select(m => m.Name))
);

// Process user input
var selectedNumeratorNames = numeratorMeasureNames
    .Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(name => name.Trim())
    .ToList();

// Validate numerator measures
var numeratorMeasures = allMeasures
    .Where(m => selectedNumeratorNames.Contains(m.Name))
    .ToList();

if (numeratorMeasures.Count == 0) {
    Error("No valid numerator measures selected.");
    return;
}

// Prompt user to select a single denominator measure
var denominatorMeasure = SelectMeasure(label: "Select denominator measure");
if (denominatorMeasure == null) {
    Error("No denominator measure selected.");
    return;
}

// Get the table where measures will be created
var targetTable = numeratorMeasures.First().Table;

// Get existing measure names to avoid duplication
var existingMeasureNames = targetTable.Measures.Select(m => m.Name).ToHashSet();

// Create a new measure for each numerator
foreach (var numMeasure in numeratorMeasures) {
    // Define measure name
    string measureName = $"{numMeasure.Name} % to total";

    // Ensure uniqueness
    if (existingMeasureNames.Contains(measureName)) {
        int counter = 1;
        string newMeasureName;
        do {
            newMeasureName = $"{measureName} ({counter})";
            counter++;
        } while (existingMeasureNames.Contains(newMeasureName));
        measureName = newMeasureName;
    }

    // Define DAX expression
    string daxExpression = $"DIVIDE({numMeasure.DaxObjectFullName}, {denominatorMeasure.DaxObjectFullName})";

    // Create the measure
    var newMeasure = targetTable.AddMeasure(
        measureName,  // Measure Name
        daxExpression // DAX Formula
    );

    // Set format to percentage
    newMeasure.FormatString = "0.00%";

    // Add documentation
    newMeasure.Description = $"This measure calculates {numMeasure.Name} as a percentage of {denominatorMeasure.Name}.";

    // Register new measure name to avoid duplicates in next iteration
    existingMeasureNames.Add(measureName);
}
