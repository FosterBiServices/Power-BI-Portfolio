/*
 * Title: Copy DAX Expression into the measure's description field.
 * 
 * Author: Reid Havens, https://www.havensconsulting.net/ 
 * 
 * This script, when executed, will loop through all the measures in the model and
 * copy the DAX epression into the field's description for documentation purposes.
 * This will overwrite any existing expressions
 */

foreach (var m in Model.AllMeasures) {
  m.Description = m.Expression;
}