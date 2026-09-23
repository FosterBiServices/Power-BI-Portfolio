import re
from dataclasses import replace
from .config import COMPOUND_FUNCTIONS, EXCLUDED_FOLDER_TOKENS, EXCLUDED_MEASURE_TOKENS, KPI_COLORS

_REFERENCE = re.compile(r"(?<![A-Za-z0-9_])\[([^\]]+)\]")

def _has(Value, Tokens): return any(Token in Value.casefold() for Token in Tokens)
def _compound(Measure):
  Expression = Measure.Expression.upper().replace(" ", "")
  if any(Function in Expression for Function in COMPOUND_FUNCTIONS): return True
  References = {Item.casefold() for Item in _REFERENCE.findall(Measure.Expression)} - {Measure.Name.casefold()}
  return len(References) >= 2 or bool(re.search(r"\[[^\]]+\]\s*[+\-*/]\s*\[[^\]]+\]", Measure.Expression))

def SelectKpis(Measures, MaxKpis):
  Candidates = []
  for Measure in Measures:
    IsCompound = _compound(Measure)
    Score = (Measure.VisualCount * 10) + (len(Measure.UsedBy) * 5)
    Enriched = replace(Measure, IsCompound=IsCompound, Score=Score)
    if not IsCompound and not _has(Measure.Name, EXCLUDED_MEASURE_TOKENS) and not _has(Measure.DisplayFolder, EXCLUDED_FOLDER_TOKENS):
      Candidates.append(Enriched)
  Ranked = sorted(Candidates, key=lambda Item: (-Item.Score, -Item.VisualCount, -len(Item.UsedBy), Item.Name.casefold()))
  return tuple(replace(Item, Color=KPI_COLORS[Index % len(KPI_COLORS)]) for Index, Item in enumerate(Ranked[:MaxKpis]))
