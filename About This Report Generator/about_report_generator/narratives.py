import re
from collections import Counter
STOP_WORDS = frozenset({"the","and","with","from","during","within","number","count","percent","percentage","total","current","selected","value","data","dashboard","export","measure","measures","report","reporting"})

def _terms(Measures, Limit=4):
  Counts = Counter()
  for Measure in Measures:
    Counts.update(Word.casefold() for Word in re.findall(r"[A-Za-z][A-Za-z-]+", Measure.Name) if len(Word) > 3 and Word.casefold() not in STOP_WORDS)
  return [Word for Word, _ in Counts.most_common(Limit)]

def BuildReportSummary(Inventory, Kpis):
  Name = re.sub(r"\s+", " ", re.sub(r"[_-]+", " ", Inventory.ReportName)).strip()
  Terms = _terms(Kpis or Inventory.Measures)
  if not Terms: return f"The {Name} report provides a consolidated view of the documented model metrics.", ("Insufficient business-facing measure names for a more specific summary.",)
  Focus = Terms[0] if len(Terms) == 1 else ", ".join(Terms[:-1]) + f", and {Terms[-1]}"
  return f"The {Name} report provides a consolidated view of {Focus}.", ()

def BuildBusinessValue(Kpis):
  if not Kpis: return "Evidence Gap: No qualifying base KPI measures were identified in the supplied documentation.", ("No qualifying base KPI measures were available.",)
  Names = [Item.Name for Item in Kpis]
  Focus = Names[0] if len(Names) == 1 else ", ".join(Names[:-1]) + f", and {Names[-1]}"
  return "Supports informed review of the model's primary reported outcomes, including " + Focus + ".", ()
