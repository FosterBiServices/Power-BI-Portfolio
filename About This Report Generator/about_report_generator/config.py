from dataclasses import dataclass

SOURCE_COLORS = (
  ("#F3E8FF", "#6B21A8"), ("#CCFBF1", "#115E59"),
  ("#FFE4E6", "#9F1239"), ("#FFEDD5", "#9A3412"),
  ("#E2E8F0", "#334155"), ("#F5D0FE", "#86198F"),
  ("#CFFAFE", "#155E75"), ("#FDE68A", "#78350F"),
  ("#D1FAE5", "#065F46"), ("#E7E5E4", "#44403C"),
)
KPI_COLORS = (
  "#DCEBFF", "#E6F7E6", "#FFF4D6", "#FCE4EC", "#EDE7F6",
  "#D9F3F0", "#FDE2D2", "#E8EAF6", "#F3E5F5", "#E0F7FA",
)
EXCLUDED_SOURCE_NAMES = frozenset({"Other / not detected", "JSON"})
EXCLUDED_MEASURE_TOKENS = (
  "background color", "font color", "text color", "color", "display label",
  "label", "html", "selected", "title", "format", "switch", "metric value",
  "last refresh",
)
EXCLUDED_FOLDER_TOKENS = ("format", "html", "color", "label", "metadata", "helper", "switch")
COMPOUND_FUNCTIONS = ("DIVIDE(", "SWITCH(", "FORMAT(")

@dataclass(frozen=True)
class GeneratorConfig:
  MaxKpis: int = 5
  FontSize: int = 18
  MeasureName: str = "About This Report HTML"
  MeasureTable: str = "_Measures"

  def __post_init__(self):
    if not 1 <= self.MaxKpis <= 10:
      raise ValueError("MaxKpis must be between 1 and 10.")
    if self.FontSize < 10:
      raise ValueError("FontSize cannot be less than 10.")
    if not self.MeasureName.strip() or not self.MeasureTable.strip():
      raise ValueError("MeasureName and MeasureTable cannot be blank.")
