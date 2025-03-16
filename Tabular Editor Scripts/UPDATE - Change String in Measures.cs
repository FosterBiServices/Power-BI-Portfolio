var FromString = "DATESYTD(DATEADD(dimDates[DateValue], -1, YEAR))";
var ToString = "ALL(dimDates), DATESYTD(DATEADD(dimDates[DateValue], -1, YEAR))";

foreach(var c in Selected.Measures)
{
c.Expression = c.Expression.Replace(FromString,ToString);
/* Cycle over all measures in model and replaces the
FromString with the ToString */
}