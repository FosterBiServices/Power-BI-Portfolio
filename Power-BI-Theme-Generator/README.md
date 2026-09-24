# Power BI Dynamic Theme Generator

Generate a reusable Power BI theme from a single JSON template by updating its color palette and running the included Python script.

## Included Files

- `Power BI - Dynamic Template Updates.py`: Opens the template, replaces theme color placeholders, and saves the completed theme as a new JSON file.
- `Dynamic-Theme-Template.json`: The template users update before running the script.

## Requirements

- Python 3
- A desktop environment that supports file-selection windows
- Power BI Desktop for testing and using the generated theme

The script uses only Python standard-library modules: `json` and `tkinter`. No additional Python packages are required.

## Important: Keep the Color Count and Order

The template currently contains **17 colors** in the `dataColors` array. Each position is referenced elsewhere in the template through placeholders such as `{themecolor1}`, `{themecolor9}`, and `{themecolor17}`.

- Keep all 17 color entries unless you also update every related placeholder and theme reference.
- Change the color values, not their positions.
- Use valid six-digit hexadecimal colors in the format `#RRGGBB`.
- Do not remove the quotation marks or commas required by JSON.
- Do not reorder colors unless you intend to change every location that uses that color position.

The position is significant. For example, the first entry maps to `{themecolor1}`, the ninth entry maps to `{themecolor9}`, and the seventeenth entry maps to `{themecolor17}`.

## Update the Theme Colors

1. Make a working copy of `Dynamic-Theme-Template.json`.
2. Open the working copy in a text editor or code editor.
3. Update the theme name near the top of the file:

```json
"name": "FOSTER BI SERVICES"
```

Replace the existing value with a name that describes the company, department, report, or template.

4. Locate the `dataColors` array near the top of the file:

```json
"dataColors": [
  "#6C6BA3",
  "#4C78A8",
  "#9C755F"
]
```

5. Replace the existing hexadecimal values with the desired colors while preserving all 17 entries and their order.
6. Save the updated JSON file.

### Color Position Notes

Some positions have specific uses in the supplied template:

- Color 1 is used broadly for primary accents, labels, icons, and totals.
- Color 9 is used for decrease or unfavorable indicators.
- Color 10 is used for increase or favorable indicators.
- Color 11 is used for other or neutral indicators.
- Colors 15 through 17 are used by light text and element styles.

Because each color can appear in multiple visual settings and embedded icons, test the completed theme in Power BI after generating it.

## Run the Generator

1. Run `Power BI - Dynamic Template Updates.py` with Python.

```bash
python "Power BI - Dynamic Template Updates.py"
```

2. In the **Select Power BI Theme JSON File** window, select the updated copy of `Dynamic-Theme-Template.json`.
3. In the **Save Updated Theme As** window, choose the destination folder.
4. Enter a descriptive output name and save the file as JSON.

The script replaces the template placeholders with the colors from `dataColors` and writes the completed Power BI theme to the selected location.

## Recommended File Naming

Name the generated file for what the theme represents. A clear name makes the theme easier to identify and maintain.

Examples:

- `Contoso-Corporate-Theme.json`
- `Finance-Executive-Report-Theme.json`
- `Sales-Performance-Theme.json`
- `Human-Resources-Template-Theme.json`

You can enter the descriptive name directly in the script's **Save Updated Theme As** window. If you keep the default or temporary name, rename the generated JSON file before distributing or importing it.

## Use the Theme in Power BI

After generating the file, import the completed JSON theme into the intended Power BI report. Review the report pages and confirm that text, backgrounds, data colors, status indicators, icons, and navigation elements have acceptable contrast and match the intended design.

## Validation Checklist

Before distributing the theme, confirm that:

- [ ] The theme name is descriptive.
- [ ] The `dataColors` array contains 17 entries.
- [ ] Every color uses the `#RRGGBB` format.
- [ ] The color order has not changed unintentionally.
- [ ] The updated template is valid JSON.
- [ ] The generator completes without displaying `No file selected.` or `Save cancelled.`
- [ ] The output file has a descriptive `.json` name.
- [ ] The theme imports into Power BI successfully.
- [ ] Report text and data labels remain readable.
- [ ] Favorable, unfavorable, and neutral indicators use the intended colors.
- [ ] Embedded icons display with the expected colors.

## Troubleshooting

### No file selected

The input selection window was closed without choosing a file. Run the script again and select the updated template JSON file.

### Save cancelled

The output window was closed without selecting a destination and file name. Run the script again and complete the save step.

### JSON error when the script runs

The updated template is not valid JSON. Check for:

- Missing or extra commas
- Missing quotation marks
- Invalid hexadecimal color values
- Deleted brackets or braces

A JSON-aware editor can help identify syntax errors before the script is run.

### Placeholders remain in the generated file

A required color position may have been removed from `dataColors`, or the placeholder may reference a color number that no longer exists. Restore all 17 color entries and run the generator again.

### Theme imports but colors are unexpected

Confirm that the color values remained in their intended positions. The generator maps colors by array order, so moving a color changes every placeholder associated with that position.

## How the Script Works

The generator performs the following steps:

1. Prompts the user to select a JSON theme file.
2. Reads the file's `dataColors` array.
3. Builds a placeholder map based on each color's position.
4. Recursively searches dictionaries, lists, and strings in the JSON structure.
5. Replaces matching theme color placeholders.
6. Prompts the user for an output location and file name.
7. Saves the completed theme as formatted JSON.

## File Safety

Keep the original template unchanged as a reusable source. Update a copy for each company, report, or design variation, then save the generated theme under a descriptive name.
