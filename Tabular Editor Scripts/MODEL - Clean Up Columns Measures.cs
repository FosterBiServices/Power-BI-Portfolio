//
//
// by Tommy Puglia
// twitter: @tommypuglia
// pugliabi.com
//
// Cleans up Columns & Measures, mainly
// Columns:
// ---- Changes Any Date Column to a better FormatString 
// ---- Updates any Column that is number to not be summed
// ---- Adds All Columns to a TableColumns Display Folder ---Updatedname 8.26.2023 SF
//
// Measures:
// ---- Updates Measures that have no format to Whole Number
// ---- Adds Description to measures (DAX)
// ---- Adds measures to a Display Folder (KPIs) ---Updatedname 8.26.2023 SF
//

var sb = new System.Text.StringBuilder();
string newline = Environment.NewLine;

foreach(var c in Model.AllColumns.Where(a => a.DataType == DataType.DateTime)) {
	c.FormatString = "m/d/yyyy";


}
foreach(var c in Model.AllColumns.Where(a => a.DataType == DataType.Int64 || a.DataType == DataType.Decimal || a.DataType == DataType.Double)) {
	c.SummarizeBy = AggregateFunction.None;

}
foreach(var c in Model.AllColumns) {
c.DisplayFolder = "TableColumns";
}



foreach(var m in Model.AllMeasures) {
//	if(string.IsNullOrEmpty(m.FormatStringExpression)) // added 8.26.2023 SF to reduce format conflicts
//		{
//		string colFomratString = "";
//			if (m.FormatString == colFomratString) {
//			m.FormatString = "#,0";
//			} 
//	}
//     if(string.IsNullOrEmpty(m.Description))
//    {
//       m.Description =m.Expression;
//
//    }
 if(m.DisplayFolder == "")
    {
m.DisplayFolder = "KPIs";

    }

}