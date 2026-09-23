from .config import EXCLUDED_SOURCE_NAMES, SOURCE_COLORS
from .models import SourceInfo

def AssignSourceColors(Sources):
  Clean = [Source for Source in Sources if Source.Name.strip() and Source.Name not in EXCLUDED_SOURCE_NAMES]
  Result = []
  for Index, Source in enumerate(Clean):
    Background, Foreground = SOURCE_COLORS[Index % len(SOURCE_COLORS)]
    Result.append(SourceInfo(Source.Name, Source.TableCount, Background, Foreground))
  return tuple(Result)
