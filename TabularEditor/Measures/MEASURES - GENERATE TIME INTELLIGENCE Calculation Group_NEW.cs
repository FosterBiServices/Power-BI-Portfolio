#r "Microsoft.VisualBasic"
using Microsoft.VisualBasic;
//
// CHANGELOG:
// '2021-05-01 / B.Agullo / 
// '2021-05-17 / B.Agullo / added affected measure table
// '2021-06-19 / B.Agullo / data label measures
// '2021-07-10 / B.Agullo / added flag expression to avoid breaking already special format strings
// '2021-09-23 / B.Agullo / added code to prompt for parameters (code credit to Daniel Otykier) 
// '2021-09-27 / B.Agullo / added code for general name 
// '2022-10-11 / B.Agullo / added MMT and MWT calc item groups
// '2024-01-22 / S.Foster / Removed MMMT and MWT calc item groups, Added "Leveled" Measures 
// If you do not have those fields, you can remove the calculations with errors after saving the updates. The script WILL error due to missing fields.

// by Bernat Agulló
// twitter: @AgulloBernat
// www.esbrina-ba.com/blog

// REFERENCE: 
// Check out https://www.esbrina-ba.com/time-intelligence-the-smart-way/ where this script is introduced

// FEATURED: 
// this script featured in GuyInACube https://youtu.be/_j0iTUo2HT0

// THANKS:
// shout out to Johnny Winter for the base script and SQLBI for daxpatterns.com

//select the measures that you want to be affected by the calculation group
//before running the script. 
//measure names can also be included in the following array (no need to select them) 
string[] preSelectedMeasures = {}; //include measure names in double quotes, like: {"Profit","Total Cost"};

//AT LEAST ONE MEASURE HAS TO BE AFFECTED!, 
//either by selecting it or typing its name in the preSelectedMeasures Variable

//
// ----- do not modify script below this line -----
//

string affectedMeasures = "{";

int i = 0;

for (i = 0; i < preSelectedMeasures.GetLength(0); i++) {

  if (affectedMeasures == "{") {
    affectedMeasures = affectedMeasures + "\"" + preSelectedMeasures[i] + "\"";
  } else {
    affectedMeasures = affectedMeasures + ",\"" + preSelectedMeasures[i] + "\"";
  };

};

if (Selected.Measures.Count != 0) {

  foreach(var m in Selected.Measures) {
    if (affectedMeasures == "{") {
      affectedMeasures = affectedMeasures + "\"" + m.Name + "\"";
    } else {
      affectedMeasures = affectedMeasures + ",\"" + m.Name + "\"";
    };
  };
};

//check that by either method at least one measure is affected
if (affectedMeasures == "{") {
  Error("No measures affected by calc group");
  return;
};

string calcGroupName;
string columnName;

if (Model.CalculationGroups.Any(cg => cg.GetAnnotation("@AgulloBernat") == "Time Intel Calc Group")) {
  calcGroupName = Model.CalculationGroups.Where(cg => cg.GetAnnotation("@AgulloBernat") == "Time Intel Calc Group").First().Name;

} else {
  calcGroupName = Interaction.InputBox("Provide a name for your Calc Group", "Calc Group Name", "Time Intelligence", 740, 400);
};

if (calcGroupName == "") return;

if (Model.CalculationGroups.Any(cg => cg.GetAnnotation("@AgulloBernat") == "Time Intel Calc Group")) {
  columnName = Model.Tables.Where(cg => cg.GetAnnotation("@AgulloBernat") == "Time Intel Calc Group").First().Columns.First().Name;

} else {
  columnName = Interaction.InputBox("Provide a name for your Calc Group Column", "Calc Group Column Name", calcGroupName, 740, 400);
};

if (columnName == "") return;

string affectedMeasuresTableName;

if (Model.Tables.Any(t => t.GetAnnotation("@AgulloBernat") == "Time Intel Affected Measures Table")) {
  affectedMeasuresTableName = Model.Tables.Where(t => t.GetAnnotation("@AgulloBernat") == "Time Intel Affected Measures Table").First().Name;

} else {
  affectedMeasuresTableName = Interaction.InputBox("Provide a name for affected measures table", "Affected Measures Table Name", calcGroupName + " Affected Measures", 740, 400);

};

if (affectedMeasuresTableName == "") return;

if (Model.Tables.Any(t => t.GetAnnotation("@AgulloBernat") == "Time Intel Affected Measures Table")) {
  affectedMeasuresColumnName = Model.Tables.Where(t => t.GetAnnotation("@AgulloBernat") == "Time Intel Affected Measures Table").First().Columns.First().Name;

} else {
  affectedMeasuresColumnName = Interaction.InputBox("Provide a name for affected measures column", "Affected Measures Table Column Name", "Measure", 740, 400);

};

string affectedMeasuresColumnName = Interaction.InputBox("Provide a name for affected measures table column name", "Affected Measures Table Column Name", "Measure", 740, 400);

if (affectedMeasuresColumnName == "") return;
//string affectedMeasuresColumnName = "Measure"; 

string labelAsValueMeasureName = "Label as Value Measure";
string labelAsFormatStringMeasureName = "Label as format string";

// '2021-09-24 / B.Agullo / model object selection prompts! 
var factTable = SelectTable(label: "Select your fact table");
if (factTable == null) return;

var factTableDateColumn = SelectColumn(factTable.Columns, label: "Select the main date column");
if (factTableDateColumn == null) return;

Table dateTableCandidate = null;

if (Model.Tables.Any(x => x.GetAnnotation("@AgulloBernat") == "Time Intel Date Table" ||
    x.Name == "dimDate" ||
    x.Name == "dimDates" ||
    x.Name == "Calendar")) {
  dateTableCandidate = Model.Tables.Where(x => x.GetAnnotation("@AgulloBernat") == "Time Intel Date Table" ||
    x.Name == "dimDate" ||
    x.Name == "dimDates" ||
    x.Name == "Calendar").First();

};

var dateTable =
  SelectTable(
    label: "Select your date table",
    preselect: dateTableCandidate);

if (dateTable == null) {
  Error("You just aborted the script");
  return;
} else {
  dateTable.SetAnnotation("@AgulloBernat", "Time Intel Date Table");
};

Column dateTableDateColumnCandidate = null;

if (dateTable.Columns.Any(x => x.GetAnnotation("@AgulloBernat") == "Time Intel Date Table Date Column" 
    || x.Name == "Fiscal Date"
    || x.Name == "DateValue")) {
  dateTableDateColumnCandidate = dateTable.Columns.Where(x => x.GetAnnotation("@AgulloBernat") == "Time Intel Date Table Date Column" 
  || x.Name == "Fiscal Date"
  || x.Name == "DateValue").First();
};

var dateTableDateColumn =
  SelectColumn(
    dateTable.Columns,
    label: "Select the date column",
    preselect: dateTableDateColumnCandidate);

if (dateTableDateColumn == null) {
  Error("You just aborted the script");
  return;
} else {
  dateTableDateColumn.SetAnnotation("@AgulloBernat", "Time Intel Date Table Date Column");
};


Column dateTableYearColumnCandidate = null;
if (dateTable.Columns.Any(x => x.GetAnnotation("@AgulloBernat") == "Time Intel Date Table Year Column" 
  || x.Name == "Year Number"
  || x.Name == "YearNumber")) {
  dateTableYearColumnCandidate = dateTable.Columns.Where(x => x.GetAnnotation("@AgulloBernat") == "Time Intel Date Table Year Column" 
  || x.Name == "Year Number"
  || x.Name == "YearNumber").First();
};

var dateTableYearColumn =
  SelectColumn(
    dateTable.Columns,
    label: "Select the year column",
    preselect: dateTableYearColumnCandidate);

if (dateTableYearColumn == null) {
  Error("You just abourted the script");
  return;
} else {
  dateTableYearColumn.SetAnnotation("@AgulloBernat", "Time Intel Date Table Year Column");
};

//these names are for internal use only, so no need to be super-fancy, better stick to datpatterns.com model
string ShowValueForDatesMeasureName = "ShowValueForDates";
string dateWithSalesColumnName = "DateWith" + factTable.Name;
string dateWithSalesColumnNameFlag = "DateWith" + factTable.Name + "Flag";
//string MonthWithSalesColumnName = "MonthWith" + factTable.Name;
//string MonthWithSalesColumnNameFlag = "MonthWith" + factTable.Name + "Flag";

// '2021-09-24 / B.Agullo / I put the names back to variables so I don't have to tough the script
string factTableName = factTable.Name;
string factTableDateColumnName = factTableDateColumn.Name;
string dateTableName = dateTable.Name;
string dateTableDateColumnName = dateTableDateColumn.Name;

string dateTableYearColumnName = dateTableYearColumn.Name;

// '2021-09-24 / B.Agullo / this is for internal use only so better leave it as is 
string flagExpression = "UNICHAR( 8204 )";

string calcItemProtection = "<CODE>"; //default value if user has selected no measures
string calcItemFormatProtection = "<CODE>"; //default value if user has selected no measures

// check if there's already an affected measure table
if (Model.Tables.Any(t => t.GetAnnotation("@AgulloBernat") == "Time Intel Affected Measures Table")) {
  //modifying an existing calculated table is not risk-free
  Info("Make sure to include measure names to the table " + affectedMeasuresTableName);
} else {
  // create calculated table containing all names of affected measures
  // this is why you need to enable 
  if (affectedMeasures != "{") {

    affectedMeasures = affectedMeasures + "}";

    string affectedMeasureTableExpression =
      "SELECTCOLUMNS(" + affectedMeasures + ",\"" + affectedMeasuresColumnName + "\",[Value])";

    var affectedMeasureTable =
      Model.AddCalculatedTable(affectedMeasuresTableName, affectedMeasureTableExpression);

    affectedMeasureTable.FormatDax();
    affectedMeasureTable.Description =
      "Measures affected by " + calcGroupName + " calculation group.";

    affectedMeasureTable.SetAnnotation("@AgulloBernat", "Time Intel Affected Measures Table");

    // this causes error
    // affectedMeasureTable.Columns[affectedMeasuresColumnName].SetAnnotation("@AgulloBernat","Time Intel Affected Measures Table Column");

    affectedMeasureTable.IsHidden = true;

  };
};

//if there where selected or preselected measures, prepare protection code for expresion and formatstring
string affectedMeasuresValues = "VALUES('" + affectedMeasuresTableName + "'[" + affectedMeasuresColumnName + "])";

calcItemProtection =
  "SWITCH(" +
  "   TRUE()," +
  "   SELECTEDMEASURENAME() IN " + affectedMeasuresValues + "," +
  "   <CODE> ," +
  "   ISSELECTEDMEASURE([" + labelAsValueMeasureName + "])," +
  "   <LABELCODE> ," +
  "   SELECTEDMEASURE() " +
  ")";

calcItemFormatProtection =
  "SWITCH(" +
  "   TRUE() ," +
  "   SELECTEDMEASURENAME() IN " + affectedMeasuresValues + "," +
  "   <CODE> ," +
  "   ISSELECTEDMEASURE([" + labelAsFormatStringMeasureName + "])," +
  "   <LABELCODEFORMATSTRING> ," +
  "   SELECTEDMEASUREFORMATSTRING() " +
  ")";


string dateColumnWithTable = "'" + dateTableName + "'[" + dateTableDateColumnName + "]";
string yearColumnWithTable = "'" + dateTableName + "'[" + dateTableYearColumnName + "]";
string factDateColumnWithTable = "'" + factTableName + "'[" + factTableDateColumnName + "]";
string dateWithSalesWithTable = "'" + dateTableName + "'[" + dateWithSalesColumnName + "]";
string calcGroupColumnWithTable = "'" + calcGroupName + "'[" + columnName + "]";

//check to see if a table with this name already exists
//if it doesnt exist, create a calculation group with this name
if (!Model.Tables.Contains(calcGroupName)) {
  var cg = Model.AddCalculationGroup(calcGroupName);
  cg.Description = "Calculation group for time intelligence. Availability of data is taken from " + factTableName + ".";
  cg.SetAnnotation("@AgulloBernat", "Time Intel Calc Group");
};

//set variable for the calc group
Table calcGroup = Model.Tables[calcGroupName];

//if table already exists, make sure it is a Calculation Group type
if (calcGroup.SourceType.ToString() != "CalculationGroup") {
  Error("Table exists in Model but is not a Calculation Group. Rename the existing table or choose an alternative name for your Calculation Group.");
  return;
};

//adds the two measures that will be used for label as value, label as format string 
var labelAsValueMeasure = calcGroup.AddMeasure(labelAsValueMeasureName, "");
labelAsValueMeasure.Description = "Use this measure to show the year evaluated in tables";

var labelAsFormatStringMeasure = calcGroup.AddMeasure(labelAsFormatStringMeasureName, "0");
labelAsFormatStringMeasure.Description = "Use this measure to show the year evaluated in charts";

//by default the calc group has a column called Name. If this column is still called Name change this in line with specfied variable
if (calcGroup.Columns.Contains("Name")) {
  calcGroup.Columns["Name"].Name = columnName;

};

calcGroup.Columns[columnName].Description = "Select value(s) from this column to apply time intelligence calculations.";
calcGroup.Columns[columnName].SetAnnotation("@AgulloBernat", "Time Intel Calc Group Column");

//Only create them if not in place yet (reruns)
if (!Model.Tables[dateTableName].Columns.Any(C => C.GetAnnotation("@AgulloBernat") == "Date with Data Column")) {
  string DateWithSalesCalculatedColumnExpression =
    dateColumnWithTable + " <= MAX ( " + factDateColumnWithTable + ")";

  Column dateWithDataColumn = dateTable.AddCalculatedColumn(dateWithSalesColumnName, DateWithSalesCalculatedColumnExpression);
  dateWithDataColumn.SetAnnotation("@AgulloBernat", "Date with Data Column");
};

string str = @"""Last Date with Data""";

string str2 = @""" - """;
string strforLabel1 = @" & "" vs. "" & ";

string strforLabel3 = @"""Variance: "" &";

if (!Model.Tables[dateTableName].Columns.Any(C => C.GetAnnotation("@AgulloBernat") == "Date with Data Column Value")) {
  string DateWithSalesCalculatedColumnExpressionValue =
    "If (" + dateColumnWithTable + " = MAX ( " + factDateColumnWithTable + ") , " + str + ")";

  Column dateWithDataColumn = dateTable.AddCalculatedColumn(dateWithSalesColumnNameFlag, DateWithSalesCalculatedColumnExpressionValue);
  dateWithDataColumn.SetAnnotation("@AgulloBernat", "Date with Data Column Value");
};

//Only create them if not in place yet (reruns) --New 09/06/2024 Foster 
//if (!Model.Tables[dateTableName].Columns.Any(C => C.GetAnnotation("@AgulloBernat") == "Month with Data Column")) {
//  string MonthWithSalesCalculatedColumnExpression =
//    dateColumnWithTable + " <= MAX ( " + factDateColumnWithTable + ")";
//
//  Column MonthWithDataColumn = dateTable.AddCalculatedColumn(MonthWithSalesColumnName, MonthWithSalesCalculatedColumnExpression);
//  MonthWithDataColumn.SetAnnotation("@AgulloBernat", "Month with Data Column");
//};
//
//string mstr = @"""Last Month with Data""";
//
//string mstr2 = @""" - """;
//string mstrforLabel1 = @" & "" vs. "" & ";
//
//string mstrforLabel3 = @"""Variance: "" &";
//
//if (!Model.Tables[dateTableName].Columns.Any(C => C.GetAnnotation("@AgulloBernat") == "Month with Data Column Value")) {
//  string MonthWithSalesCalculatedColumnExpressionValue =
//        "If ( YEAR(" + dateColumnWithTable + ") = YEAR(MAX ( " + factDateColumnWithTable + ")) && MONTH(" + dateColumnWithTable + ") = MONTH(MAX ( " + factDateColumnWithTable + ")), " + mstr + ")";
//
//  Column MonthWithDataColumn = dateTable.AddCalculatedColumn(MonthWithSalesColumnNameFlag, MonthWithSalesCalculatedColumnExpressionValue);
//  MonthWithDataColumn.SetAnnotation("@AgulloBernat", "Month with Data Column Value");
//};

// End of monthly additions 

if (!Model.Tables[dateTableName].Measures.Any(M => M.Name == ShowValueForDatesMeasureName)) {
  string ShowValueForDatesMeasureExpression =
    "VAR LastDateWithData = " +
    "    CALCULATE ( " +
    "        MAX (  " + factDateColumnWithTable + " ), " +
    "        REMOVEFILTERS () " +
    "    )" +
    "VAR FirstDateVisible = " +
    "    MIN ( " + dateColumnWithTable + " ) " +
    "VAR Result = " +
    "    FirstDateVisible <= LastDateWithData " +
    "RETURN " +
    "    Result ";

  var ShowValueForDatesMeasure = dateTable.AddMeasure(ShowValueForDatesMeasureName, ShowValueForDatesMeasureExpression);

  ShowValueForDatesMeasure.FormatDax();
};

//defining expressions and formatstring for each calc item

string CM =
  "/*CM*/ " +
  "SELECTEDMEASURE()";

string CMLabel =
  "/*CM*/ " +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   IF ( HASONEVALUE( " + dateColumnWithTable + "), " +
  "       MAX( " + dateColumnWithTable + "), " +
  "           CONCATENATE(" +
  "           CALCULATE(" +
  "               MIN( " + dateColumnWithTable + " ), " +
  "           ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", -0, MONTH ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "       )" +
  "           , CONCATENATE(" + str2 + ", " +
  "           CALCULATE(" +
  "                   MAX( " + dateColumnWithTable + " ), " +
  "               ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", -0, MONTH ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "               )" +
  "           )" +
  "       )" +
  "       )" +
  " )";

string SPLM =
  "/*SPLM*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CM + "," +
  "        ALL(" + dateTableName + "), " +
  "    CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, MONTH ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string SPLMLabel =
  "/*SPLM*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CMLabel + "," +
  "        ALL(" + dateTableName + "), " +
  "       CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, MONTH ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string MTD =
  "/*MTD*/" +
  "IF (" +
  "    [" + ShowValueForDatesMeasureName + "]," +
  "    CALCULATE (" +
  "        " + CM + "," +
  "        ALL(" + dateTableName + "), " +
  "        DATESMTD (" + dateColumnWithTable + " )" +
  "   )" +
  ") ";

string MTDLabel =
  "/*MTD*/ " +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "           CALCULATE(" +
  "               YEAR( MAX(" + dateColumnWithTable + ") ) & " + str2 + " & Month (MAX(" + dateColumnWithTable + ") ), " +
  "           ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", -0, MONTH ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "       )" +
  " )";

string PMTD =
  "/*PMTD*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + MTD + "," +
  "        ALL(" + dateTableName + "), " +
  "    CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, MONTH ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string PMTDLabel =
  "/*PMTD*/ " +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "           CALCULATE(" +
  "              YEAR( MAX(" + dateColumnWithTable + ") ) & " + str2 + " & Month (MAX(" + dateColumnWithTable + ") ), " +
  "           ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", -1, MONTH ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "       )" +
  " )";

string PMTotals =
  "/*PM*/ " +
  "         var __MaxDate = MAX(" + dateColumnWithTable + ")" +
  "         var __SOM = IF ( MONTH(  __MaxDate ) = 1, DATE(YEAR(__MaxDate) - 1, 12, 1), DATE(YEAR(__MaxDate), MONTH(__MaxDate), 1 ))" +
  "         var __EOM = CALCULATE( EOMONTH(__MaxDate, - 1), " +
  "         " + dateColumnWithTable + " = __MaxDate" + 
  "         )" + 
  "   RETURN" +
  "    IF (" +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "    CALCULATE ( " +
  "        " + CM + ", " +
  "        ALL(" + dateTableName + "), " +
  "        " + dateColumnWithTable + ">= __SOM, " +
  "        " + dateColumnWithTable + "<= __EOM, " +
  "        " + dateWithSalesWithTable + " = TRUE " +
  "        ) " +
  ") ";

string PMTotalsLabel = PMTDLabel;

string MOMTD =
  "/*MOMTD*/" +
  "VAR ValueCurrentPeriod = " + MTD + " " +
  "VAR ValuePreviousPeriod = " + PMTD + " " +
  "VAR Result = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod - ValuePreviousPeriod" +
  " ) " +
  "RETURN " +
  "   Result ";

string MOMTDLabel =
  "/*MOMTD*/" +
  "VAR ValueCurrentPeriod = " + MTDLabel + " " +
  "VAR ValuePreviousPeriod = " + PMTDLabel + " " +
  "VAR Result = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod & \" vs \" & ValuePreviousPeriod" +
  " ) " +
  "RETURN " +
  "   Result ";

string MOMTDpct =
  "/*MOMTD%*/" +
  "VAR ValueCurrentPeriod = " + MTD + " " +
  "VAR ValuePreviousPeriod = " + PMTD + " " +
  "VAR CurrentMinusPreviousPeriod = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod - ValuePreviousPeriod" +
  " ) " +
  "VAR Result = " +
  "DIVIDE ( " +
  "    CurrentMinusPreviousPeriod," +
  "    ValuePreviousPeriod" +
  ") " +
  "RETURN " +
  "  Result";

string MOMTDpctLabel =
  "/*MOM%*/ " +
  "VAR ValueCurrentPeriod = " + MTDLabel + " " +
  "VAR ValuePreviousPeriod = " + PMTDLabel + " " +
  "VAR Result = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod & \" vs \" & ValuePreviousPeriod & \" (%)\"" +
  " ) " +
  "RETURN " +
  "  Result";

string CQ =
  "/*CQ*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CM + "," +
  "        ALL(" + dateTableName + "), " +
  "    CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", 0, QUARTER ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string CQLabel =
  "/*CQ*/ " +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "           CONCATENATE(" +
  "           CALCULATE(" +
  "               MIN( " + dateColumnWithTable + " ), " +
  "           ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", 0, QUARTER ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "       )" +
  "           , CONCATENATE(" + str2 + ", " +
  "           CALCULATE(" +
  "                   MAX( " + dateColumnWithTable + " ), " +
  "               ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", 0, QUARTER ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "               )" +
  "           )" +
  "       )" +
  " )";
string SPLQ =
  "/*SPLM*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CQ + "," +
  "        ALL(" + dateTableName + "), " +
  "        CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, QUARTER ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";
string SPLQLabel =
  "/*SPLQ*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CQLabel + "," +
  "        ALL(" + dateTableName + "), " +
  "       CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, QUARTER ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";
string QTD =
  "/*QTD*/" +
  "IF (" +
  "    [" + ShowValueForDatesMeasureName + "]," +
  "    CALCULATE (" +
  "        " + CQ + "," +
  "        ALL(" + dateTableName + "), " +
  "        DATESQTD (" + dateColumnWithTable + " )" +
  "   )" +
  ") ";
string QTDLabel =
  "/*QTD*/ " +
  "        VAR __MaxDate = MAX(" + dateColumnWithTable + ")" +
  "        VAR __SOQ = " +
  "         CALCULATE " + 
  "            (" + 
  "              STARTOFQUARTER( " + dateColumnWithTable + " ) ," + 
  "             " + dateColumnWithTable + "= __MaxDate" + 
  "             )" + 
  "          RETURN " + 
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " + 
  "                 YEAR(__SOQ) &" + str2 + "& QUARTER(__SOQ) " + 
  ") ";

string PQTD =
  "/*PQTD*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + QTD + "," +
  "        ALL(" + dateTableName + "), " +
  "    CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, QUARTER ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string PQTDLabel =
  "/*PQTD*/ " +
  "        VAR __MaxDate = MAX(" + dateColumnWithTable + ")" +
  "        VAR __EOQ = " +
  "         CALCULATE " + 
  "            (" + 
  "              STARTOFQUARTER( " + dateColumnWithTable + " ) - 1 ," + 
  "             " + dateColumnWithTable + "= __MaxDate" + 
  "             )" + 
  "        VAR __SOQ =  " + 
  "              DATE(YEAR(__EOQ), MONTH(__EOQ) - 2 , 1)" +
  "          RETURN " + 
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " + 
  "                 YEAR(__SOQ) &" + str2 + "& QUARTER(__SOQ) " + 
  ") ";

string PQTotal =
  "/*PQTotals*/ " +
  "        VAR __MaxDate = MAX(" + dateColumnWithTable + ")" +
  "        VAR __EOQ = " +
  "         CALCULATE " + 
  "            (" + 
  "              STARTOFQUARTER( " + dateColumnWithTable + " ) - 1 ," + 
  "             " + dateColumnWithTable + "= __MaxDate" + 
  "             )" + 
  "        VAR __SOQ =  " + 
  "              DATE(YEAR(__EOQ), MONTH(__EOQ) - 2 , 1)" +
  "          RETURN " + 
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " + 
  "                 CALCULATE" + 
  "                 ( " +
  "                    " + CQ + "," + 
  "                      ALL(" + dateTableName + " )," + 
  "                "   +  dateColumnWithTable + ">= __SOQ," + 
  "                "   +  dateColumnWithTable + "<= __EOQ," + 
  "                " + dateWithSalesWithTable + " = TRUE " +
  "                ) " + 
  ") ";

string PQTotalLabel = PQTDLabel;

string QOQTD =
  "/*QOQTD*/" +
  "VAR ValueCurrentPeriod = " + QTD + " " +
  "VAR ValuePreviousPeriod = " + PQTD + " " +
  "VAR Result = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod - ValuePreviousPeriod" +
  " ) " +
  "RETURN " +
  "   Result ";
string QOQTDLabel =
  "/*QOQTD*/" +
  QTDLabel + strforLabel1 + PQTDLabel;

string QOQTDpct =
  "/*QOQTD%*/" +
  "VAR ValueCurrentPeriod = " + QTD + " " +
  "VAR ValuePreviousPeriod = " + PQTD + " " +
  "VAR CurrentMinusPreviousPeriod = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod - ValuePreviousPeriod" +
  " ) " +
  "VAR Result = " +
  "DIVIDE ( " +
  "    CurrentMinusPreviousPeriod," +
  "    ValuePreviousPeriod" +
  ") " +
  "RETURN " +
  "  Result";

string QOQTDpctLabel =
  "/*QOQ%*/" +
  strforLabel3 + QTDLabel + strforLabel1 + PQTDLabel;

string CY =
  "/*CY*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CM + "," +
  "        ALL(" + dateTableName + "), " +
  "    CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", 0, YEAR ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string CYLabel =
  "/*CY*/ " +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "           CONCATENATE(" +
  "           CALCULATE(" +
  "               MIN( " + dateColumnWithTable + " ), " +
  "           ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", 0, YEAR ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "       )" +
  "           , CONCATENATE(" + str2 + ", " +
  "           CALCULATE(" +
  "                   MAX( " + dateColumnWithTable + " ), " +
  "               ALL(" + dateTableName + "), " +
  "           DATEADD ( " + dateColumnWithTable + ", 0, YEAR ), " +
  "       " + dateWithSalesWithTable + "= TRUE" +
  "               )" +
  "           )" +
  "       )" +
  " )";
string SPLY =
  "/*SPLY*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CY + "," +
  "        ALL(" + dateTableName + "), " +
  "    CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, YEAR ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string SPLYLabel =
  "/*SPLM*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + CYLabel + "," +
  "        ALL(" + dateTableName + "), " +
  "       CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, YEAR ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string YTD =
  "/*YTD*/" +
  "IF (" +
  "    [" + ShowValueForDatesMeasureName + "]," +
  "    CALCULATE (" +
  "        " + CY + "," +
  "        ALL(" + dateTableName + "), " +
  "            DATESYTD (" + dateColumnWithTable + " )" +
  "   )" +
  ") ";
string YTDLabel =
  "/*YTD*/ " +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "         SELECTEDVALUE( " + yearColumnWithTable + ")" +
  "        )";

string PYTD =
  "/*PYTD*/" +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "   CALCULATE ( " +
  "       " + YTD + "," +
  "        ALL(" + dateTableName + "), " +
  "    CALCULATETABLE ( " +
  "        DATEADD ( " + dateColumnWithTable + ", -1, YEAR ), " +
  "       " + dateWithSalesWithTable + " = TRUE " +
  "       )" +
  "   )" +
  ") ";

string PYTDLabel =
  "/*YTD*/ " +
  "IF ( " +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "         SELECTEDVALUE( " + yearColumnWithTable + ") - 1" +
  "        )";
string YOYTD =
  "/*YOYTD*/" +
  "VAR ValueCurrentPeriod = " + YTD + " " +
  "VAR ValuePreviousPeriod = " + PYTD + " " +
  "VAR Result = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod - ValuePreviousPeriod" +
  " ) " +
  "RETURN " +
  "   Result ";

string YOYTDLabel =
  "/*YOYTD*/" +
  YTDLabel + strforLabel1 + PYTDLabel;

string YOYTDpct =
  "/*YOYTD%*/" +
  "VAR ValueCurrentPeriod = " + YTD + " " +
  "VAR ValuePreviousPeriod = " + PYTD + " " +
  "VAR CurrentMinusPreviousPeriod = " +
  "IF ( " +
  "    NOT ISBLANK ( ValueCurrentPeriod ) && NOT ISBLANK ( ValuePreviousPeriod ), " +
  "     ValueCurrentPeriod - ValuePreviousPeriod" +
  " ) " +
  "VAR Result = " +
  "DIVIDE ( " +
  "    CurrentMinusPreviousPeriod," +
  "    ValuePreviousPeriod" +
  ") " +
  "RETURN " +
  "  Result";

string YOYTDpctLabel =
  "/*YOYTD*/" +
  strforLabel3 + YTDLabel + strforLabel1 + PYTDLabel;

string PYTotals =
  "/*PY*/ " +
  "var __MaxDate = MAX(" + dateColumnWithTable + ")" +
  "var __EOY = CALCULATE( MAX( '" + dateTableName + "' [" + dateTableYearColumnName + "] ) - 1, " + dateColumnWithTable + "= __MaxDate)" +
  "   RETURN" +
  "    IF (" +
  "    [" + ShowValueForDatesMeasureName + "], " +
  "    CALCULATE ( " +
  "        " + CM + ", " +
  "        ALL(" + dateTableName + "), " +
  "            '" + dateTableName + "' [" + dateTableYearColumnName + "]  = __EOY, " +
  dateWithSalesWithTable + " = TRUE " +
  "        ) " +
  ") ";
  

string PYTotalsLabel = PYTDLabel;

string defFormatString = "SELECTEDMEASUREFORMATSTRING()";

//if the flag expression is already present in the format string, do not change it, otherwise apply % format. 
string pctFormatString =
  "IF(" +
  "\n	FIND( " + flagExpression + ", SELECTEDMEASUREFORMATSTRING(), 1, - 1 ) <> -1," +
  "\n	SELECTEDMEASUREFORMATSTRING()," +
  "\n	\"#,##0.# %\"" +
  "\n)";

//the order in the array also determines the ordinal position of the item    
string[, ] calcItems = {
  {
    "CM",
    CM,
    defFormatString,
    "Selected Measure",
    CMLabel
  },
  {
    "SPLM",
    SPLM,
    defFormatString,
    "Same period Last Month",
    SPLMLabel
  },
  {
    "CQ",
    CQ,
    defFormatString,
    "Current Quarter",
    CQLabel
  },
  {
    "SPLQ",
    SPLQ,
    defFormatString,
    "Same period Last Quarter",
    SPLQLabel
  },
  {
    "CY",
    CY,
    defFormatString,
    "Current",
    CYLabel
  },
  {
    "SPLY",
    SPLY,
    defFormatString,
    "Same period Last Year",
    SPLYLabel
  },
  {
    "MTD",
    MTD,
    defFormatString,
    "Month-to-date",
    MTDLabel
  },
  {
    "PMTD",
    PMTD,
    defFormatString,
    "Previous Month-to-date",
    PMTDLabel
  },
  {
    "MOMTD",
    MOMTD,
    defFormatString,
    "Month-over-Month-to-date",
    MOMTDLabel
  },
  {
    "MOMTD%",
    MOMTDpct,
    pctFormatString,
    "Month-over-Month-to-date%",
    MOMTDpctLabel
  },
  {
    "PMTotals",
    PMTotals,
    defFormatString,
    "Full Previous month total",
    PMTotalsLabel
  },
  {
    "QTD",
    QTD,
    defFormatString,
    "Quarter-to-date",
    QTDLabel
  },
  {
    "PQTD",
    PQTD,
    defFormatString,
    "Previous Quarter-to-date",
    PQTDLabel
  },
  {
    "QOQTD",
    QOQTD,
    defFormatString,
    "Quarter-over-Quarter-to-date",
    QOQTDLabel
  },
  {
    "QOQTD%",
    QOQTDpct,
    pctFormatString,
    "Quarter-over-Quarter-to-date%",
    QOQTDpctLabel
  },
  {
    "PQTotal",
    PQTotal,
    defFormatString,
    "Full Previous quarter total",
    PQTotalLabel
  },
  {
    "YTD",
    YTD,
    defFormatString,
    "Year-to-date",
    YTDLabel
  },
  {
    "PYTD",
    PYTD,
    defFormatString,
    "Previous year-to-date",
    PYTDLabel
  },
  {
    "YOYTD",
    YOYTD,
    defFormatString,
    "Year-over-year-to-date",
    YOYTDLabel
  },
  {
    "YOYTD%",
    YOYTDpct,
    pctFormatString,
    "Year-over-year-to-date%",
    YOYTDpctLabel
  },
  {
    "PYTotals",
    PYTotals,
    defFormatString,
    "Full Previous year total",
    PYTotalsLabel
  },

};

int j = 0;

//create calculation items for each calculation with formatstring and description
foreach(var cg in Model.CalculationGroups) {
  if (cg.Name == calcGroupName) {
    for (j = 0; j < calcItems.GetLength(0); j++) {

      string itemName = calcItems[j, 0];

      string itemExpression = calcItemProtection.Replace("<CODE>", calcItems[j, 1]);
      itemExpression = itemExpression.Replace("<LABELCODE>", calcItems[j, 4]);

      string itemFormatExpression = calcItemFormatProtection.Replace("<CODE>", calcItems[j, 2]);
      itemFormatExpression = itemFormatExpression.Replace("<LABELCODEFORMATSTRING>", "\"\"\"\" & " + calcItems[j, 4] + " & \"\"\"\"");

      //if(calcItems[j,2] != defFormatString) {
      //    itemFormatExpression = calcItemFormatProtection.Replace("<CODE>",calcItems[j,2]);
      //};

      string itemDescription = calcItems[j, 3];

      if (!cg.CalculationItems.Contains(itemName)) {
        var nCalcItem = cg.AddCalculationItem(itemName, itemExpression);
        nCalcItem.FormatStringExpression = itemFormatExpression;
        nCalcItem.FormatDax();
        nCalcItem.Ordinal = j;
        nCalcItem.Description = itemDescription;

      };

    };

  };
};