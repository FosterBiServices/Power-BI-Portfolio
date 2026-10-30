// Export properties for the currently selected objects:
var tsv = ExportProperties(Selected);
// Output the results to a dialog box pop up on the screen (can copy to clipboard from the dialog box)
tsv.Output();

// Output the results to a tab separated file at filepath/filename
// SaveFile(@"C:\Users\<USER>\Desktop\Exported Properties 1.tsv", tsv);
