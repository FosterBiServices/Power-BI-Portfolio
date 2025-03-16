#r "Microsoft.VisualBasic"
using Microsoft.VisualBasic;
using System;

string iteratorCondition = Interaction.InputBox("Provider the iterator function", "SUMX", "SUMX", 740, 400);


var factTable = SelectTable(label: "Select the table to iterate");
if (factTable == null) return;
var factTableColumn = SelectColumn(factTable.Columns, label: "Select the column to be iterated through");
if (factTableColumn == null) return;


string factTableName = factTable.Name;
string factTableColumnName = factTableColumn.Name;
string factTablewithColumn = "'" + factTableName + "'[" + factTableColumnName + "]";

{
    var newMeasure = factTable.AddMeasure(
        iteratorCondition + " of " + factTableColumnName.ToString(),                    // Name
        iteratorCondition+ "(" + factTableName + ", " + factTablewithColumn + ")",    // DAX expression
        "KPIs" // Display Folder
    );
    
    // Set the format string on the new measure:
    newMeasure.FormatString = "#,##";

    // Provide some documentation:
    newMeasure.Description = "This measure is the " + iteratorCondition + " of " + factTablewithColumn;

};