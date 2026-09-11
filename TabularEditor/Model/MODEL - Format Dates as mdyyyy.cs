foreach(var c in Model.AllColumns.Where(a => a.DataType == DataType.DateTime)) {
	c.FormatString = "m/d/yyyy";


}