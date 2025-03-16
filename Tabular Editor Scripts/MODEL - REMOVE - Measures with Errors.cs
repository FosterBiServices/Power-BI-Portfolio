// This script scans the model and shows all measures with errors, giving the option to remove them.
//
// .GetCachedSemantics(...) method is only available in TE3
using System.Windows.Forms;

// Hide the 'Running Macro' spinbox
ScriptHelper.WaitFormVisible = false;

// Get all the measures that have errors
var measuresWithError = Model.AllMeasures.Where(m => m.GetCachedSemantics(ExpressionProperty.Expression).HasError).ToList();
//Prior to Tabular Editor 3.12.0 the GetSemantics method must be used.
//var measuresWithError = Model.AllMeasures.Where(m => m.GetSemantics(ExpressionProperty.Expression).HasError).ToList();

// If no measures with errors, end script with error.
if ( measuresWithError.Count == 0 )
{ 
Info ( "No measures with errors! 👍" );
}

// Handle erroneous measures
else 
{

// View the list of measures with an error
measuresWithError.Output();

//   From the list, you can select 1 or more measures to delete
var _ToDelete = SelectObjects(measuresWithError, measuresWithError, "Select measures to delete.\nYou will be able to export a back-up, later.");

    // Delete the selected measures
    try
    {
        foreach ( var _m in _ToDelete ) 
            {
                _m.Delete();
            }
    
        Info ( 
            "Deleted " + 
            Convert.ToString(_ToDelete.Count()) + 
            " measures with errors." 
        );
    
        // Create an instance of the FolderBrowserDialog class
        FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
        
        // Set the title of the dialog box
        folderBrowserDialog.Description = "Select a directory to output a backup of the deleted measures.";
        
        // Set the root folder of the dialog box
        folderBrowserDialog.RootFolder = Environment.SpecialFolder.MyComputer;
        
        // Show the dialog box and get the result
        DialogResult result = folderBrowserDialog.ShowDialog();
        
        // Check if the user clicked the OK button and get the selected path
        if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(folderBrowserDialog.SelectedPath))
            {
                // Get the output path as a string
                string _outputPath = folderBrowserDialog.SelectedPath;
                
                // Get the properties of the deleted measures
                var _backup = ExportProperties( _ToDelete );
    
                // Save a backup of the deleted measures
                SaveFile( _outputPath + "/DeletedMeasures-" + Model.Name + DateTime.Today.ToString("-yyyy-MM-dd") + ".tsv", _backup);
    
                Info ( 
                    "Exported a backup of " + 
                    Convert.ToString(_ToDelete.Count()) +
                    " Measures to " + 
                    _outputPath
                );
            }
    }
    catch
    // Display an info box if no measure was selected
    {
    Info ( "No measure selected." );
    }
}

