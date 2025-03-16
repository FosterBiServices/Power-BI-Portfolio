// Create a calculated table with a single column which is hidden:
var table = Model.AddCalculatedTable("__Measures", "{0}");
table.Columns[0].IsHidden = true;
