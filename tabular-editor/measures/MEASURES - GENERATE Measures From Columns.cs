// Get reference to the __Measures table
var measuresTable = Model.Tables.FirstOrDefault(t => t.Name == "__Measures");

if(measuresTable == null) {
    throw new Exception("Table '__Measures' not found.");
}

foreach(var c in Selected.Columns) {
    var oldName = c.Name;
    var newName = new System.Text.StringBuilder();

    for(int i = 0; i < oldName.Length; i++) {
        if(i == 0) {
            newName.Append(Char.ToUpper(oldName[i]));
        }
        else if(i + 2 < oldName.Length && Char.IsLower(oldName[i + 2]) && Char.IsUpper(oldName[i + 1]) && Char.IsUpper(oldName[i])) {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }
        else if(i + 1 < oldName.Length && Char.IsLower(oldName[i]) && Char.IsUpper(oldName[i+1])) {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }
        else {
            newName.Append(oldName[i]);
        }
    }

    var derivedTableName = c.Table.Name;

    var newMeasure = measuresTable.AddMeasure(
        newName.ToString(),                      // Name
        "SUM(" + c.DaxObjectFullName + ")",      // DAX expression
        derivedTableName                         // Display Folder named after original table
    );

    newMeasure.FormatString = "#,##";

    newMeasure.Description = "This measure is the sum of column " + c.DaxObjectFullName;

    c.IsHidden = true;
}
