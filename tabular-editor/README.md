# Tabular Editor Scripts

C# scripts for [Tabular Editor](https://tabulareditor.com/) (2 or 3) that automate repetitive semantic-model work. Open a model, select the objects a script works on, then run it from the **C# Script** window. Some scripts write files: update the `<USER>` path placeholders first.

## Model hygiene and formatting

Clean-up and best-practice scripts I run on every model.

- [CREATE Table Groups](model/MODEL%20-%20CREATE%20Table%20Groups.csx)
- [Clean Up Columns Measures](model/MODEL%20-%20Clean%20Up%20Columns%20Measures.cs)
- [Convert CamelCased to Proper Case](model/MODEL%20-%20Convert%20CamelCased%20to%20Proper%20Case.cs)
- [Create Measures Table](model/MODEL%20-%20Create%20Measures%20Table.cs)
- [Discourage Implicit Measures](model/MODEL%20-%20Discourage%20Implicit%20Measures.cs)
- [Format All Measures](model/MODEL%20-%20Format%20All%20Measures.cs)
- [Format All Power Query Tables](model/MODEL%20-%20Format%20All%20Power%20Query%20Tables.cs)
- [Format Dates as mdyyyy](model/MODEL%20-%20Format%20Dates%20as%20mdyyyy.cs)
- [Format Power Query](model/MODEL%20-%20Format%20Power%20Query.cs)
- [Format Selected Column as Short Date](model/MODEL%20-%20Format%20Selected%20Column%20as%20Short%20Date.cs)
- [Format Selected Measure as Currency](model/MODEL%20-%20Format%20Selected%20Measure%20as%20Currency.cs)
- [Format Selected Measure as Whole Number Thousands Separator](model/MODEL%20-%20Format%20Selected%20Measure%20as%20Whole%20Number%20Thousands%20Separator.cs)
- [Format Selected Measures as Percentage (No Decimal)](model/MODEL%20-%20Format%20Selected%20Measures%20as%20Percentage%20%28No%20Decimal%29.cs)
- [Format Selected Measures with Thousands Separator no decimals](model/MODEL%20-%20Format%20Selected%20Measures%20with%20Thousands%20Separator%20no%20decimals.cs)
- [Format Selected Measures with Thousands Separator one decimals](model/MODEL%20-%20Format%20Selected%20Measures%20with%20Thousands%20Separator%20one%20decimals.cs)
- [Format Selected Measures with Thousands Separator two decimals](model/MODEL%20-%20Format%20Selected%20Measures%20with%20Thousands%20Separator%20two%20decimals.cs)
- [Hide Columns Ending with 'Key' in Selected Tables](model/MODEL%20-%20Hide%20Columns%20Ending%20with%20%27Key%27%20in%20Selected%20Tables.cs)
- [Hide Columns on Many Side of relationship](model/MODEL%20-%20Hide%20Columns%20on%20Many%20Side%20of%20relationship.cs)
- [Import Descriptions](model/MODEL%20-%20Import%20Descriptions.cs)
- [Model Clean Up Master Script](model/MODEL%20-%20Model%20Clean%20Up%20Master%20Script.cs)
- [Move All Measures to Measures Table](model/MODEL%20-%20Move%20All%20Measures%20to%20Measures%20Table.csx)
- [Move Selected Measures to Display Folder](model/MODEL%20-%20Move%20Selected%20Measures%20to%20Display%20Folder.cs)
- [REMOVE - Measures with Errors](model/MODEL%20-%20REMOVE%20-%20Measures%20with%20Errors.cs)

## Measure generation

Generate families of measures, calculation groups and field parameters from a selection.

- [ADD Description to Measures (overwrites existing)](measures/MEASURES%20-%20ADD%20Description%20to%20Measures%20%28overwrites%20existing%29.cs)
- [FORMAT based on Name](measures/MEASURES%20-%20FORMAT%20based%20on%20Name.cs)
- [GENERATE Dummy Measure from Calculation Item](measures/MEASURES%20-%20GENERATE%20Dummy%20Measure%20from%20Calculation%20Item.cs)
- [GENERATE Field Parameter](measures/MEASURES%20-%20GENERATE%20Field%20Parameter.cs)
- [GENERATE Filtered Measure From Another Measure](measures/MEASURES%20-%20GENERATE%20Filtered%20Measure%20From%20Another%20Measure.cs)
- [GENERATE Iterated measure with user input](measures/MEASURES%20-%20GENERATE%20Iterated%20measure%20with%20user%20input.cs)
- [GENERATE Measure from Time Intelligence Calc Group](measures/MEASURES%20-%20GENERATE%20Measure%20from%20Time%20Intelligence%20Calc%20Group.cs)
- [GENERATE Measures From Columns](measures/MEASURES%20-%20GENERATE%20Measures%20From%20Columns.cs)
- [GENERATE PERCENT TO TOTAL Measure From TWO Measure](measures/MEASURES%20-%20GENERATE%20PERCENT%20TO%20TOTAL%20Measure%20From%20TWO%20Measure.cs)
- [GENERATE TIME INTELLIGENCE Calculation Group (v1)](measures/MEASURES%20-%20GENERATE%20TIME%20INTELLIGENCE%20Calculation%20Group%20%28v1%29.cs)
- [GENERATE TIME INTELLIGENCE Calculation Group](measures/MEASURES%20-%20GENERATE%20TIME%20INTELLIGENCE%20Calculation%20Group.cs)
- [GENERATE TIME INTELLIGENCE MEASURES](measures/MEASURES%20-%20GENERATE%20TIME%20INTELLIGENCE%20MEASURES.cs)
- [GENERATE TRENDING MEASURES](measures/MEASURES%20-%20GENERATE%20TRENDING%20MEASURES.cs)
- [Change String in Measures](measures/UPDATE%20-%20Change%20String%20in%20Measures.cs)

## Analysis

Quick inventories of a model.

- [Calculated Column Count](analysis/ANALYSIS%20-%20Calculated%20Column%20Count.cs)
- [List of Source Columns in Table](analysis/ANALYSIS%20-%20List%20of%20Source%20Columns%20in%20Table.cs)
- [Measure Value based on Column Selections](analysis/ANALYSIS%20-%20Measure%20Value%20based%20on%20Column%20Selections.cs)
- [Number of Measures in Model](analysis/ANALYSIS%20-%20Number%20of%20Measures%20in%20Model.cs)
- [Number of Model Objects](analysis/ANALYSIS%20-%20Number%20of%20Model%20Objects.cs)
- [Row count from Selected Table](analysis/ANALYSIS%20-%20Row%20count%20from%20Selected%20Table.cs)
- [Measure Dependencies](analysis/OUTPUT%20-%20Measure%20Dependencies.cs)

## Documentation

Export model metadata for documentation and review.

- [Export All Partition Expressions](documentation/DOCUMENTATION%20-%20Export%20All%20Partition%20Expressions.cs)
- [Export Measures](documentation/DOCUMENTATION%20-%20Export%20Measures.cs)
- [Export Objects and Descriptions](documentation/DOCUMENTATION%20-%20Export%20Objects%20and%20Descriptions.cs)
