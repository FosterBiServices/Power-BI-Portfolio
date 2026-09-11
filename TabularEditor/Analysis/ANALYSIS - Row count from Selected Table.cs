// This script counts rows in a selected table and displays the result in a pop-up info box.
// It does not write any changes to this model.
//
// Use this script when you want to check whether a table was loaded or how many rows it has.
//
// Get table name
string _TableName = 
    Selected.Table.DaxObjectFullName;

// Count table rows
string _dax = 
    "{ FORMAT( COUNTROWS (" + _TableName + "), \"#,##0\" ) }";

// Evaluate DAX
string _TableRows = 
    Convert.ToString(EvaluateDax( _dax ));

// Return output in pop-up
Info ( "Number of rows in " + _TableName + ": " + _TableRows);
