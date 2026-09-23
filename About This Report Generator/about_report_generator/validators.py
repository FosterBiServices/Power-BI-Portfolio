from bs4 import BeautifulSoup
class ValidationError(ValueError): pass

def ValidateAboutModel(Model):
  if any(Value < 0 for Value in (Model.TableCount, Model.ColumnCount, Model.MeasureCount, Model.RelationshipCount)): raise ValidationError("Model counts cannot be negative.")
  if len({Item.Name.casefold() for Item in Model.Kpis}) != len(Model.Kpis): raise ValidationError("Duplicate KPIs were generated.")
  if len({Item.Name.casefold() for Item in Model.Sources}) != len(Model.Sources): raise ValidationError("Duplicate sources were generated.")

def ValidateHtml(Html):
  Soup = BeautifulSoup(Html, "html.parser")
  Roots = [Node for Node in Soup.contents if getattr(Node, "name", None) == "div"]
  if len(Roots) != 1: raise ValidationError("HTML must have exactly one root div.")
  if "&lt;" in Html or "&gt;" in Html: raise ValidationError("HTML contains encoded structural tags.")

def ValidateDax(Dax):
  if not Dax.startswith("createOrReplace") or "measure '" not in Dax: raise ValidationError("DAX wrapper is invalid.")
  if "&lt;div" in Dax: raise ValidationError("DAX contains encoded HTML tags.")
