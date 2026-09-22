from __future__ import annotations

import re


def parse_partition_blocks(text: str):
  """Yield indentation-aware TMDL partition objects.

  Returns dictionaries with name, mode, source type, expression, and source line.
  The parser supports the common PBIP form:

    partition Name = m
      mode: import
      source =
        let
          ...
        in
          ...
  """
  lines = text.splitlines()
  partition_pattern = re.compile(
    r"^(?P<indent>\s*)partition\s+(?P<name>.+?)(?:\s*=\s*(?P<kind>\S+))?\s*$",
    re.IGNORECASE,
  )
  declaration_pattern = re.compile(
    r"^(?P<indent>\s*)(table|column|measure|hierarchy|partition|relationship|expression|role|perspective)\b",
    re.IGNORECASE,
  )
  property_pattern = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9]*)\s*:\s*(.*?)\s*$"
  )
  source_pattern = re.compile(r"^\s*source\s*=\s*(.*?)\s*$", re.IGNORECASE)

  index = 0
  while index < len(lines):
    header = partition_pattern.match(lines[index])
    if not header:
      index += 1
      continue

    start_index = index
    base_indent = len(header.group("indent"))
    index += 1
    block = [lines[start_index]]
    while index < len(lines):
      candidate = declaration_pattern.match(lines[index])
      if candidate and len(candidate.group("indent")) <= base_indent:
        break
      block.append(lines[index])
      index += 1

    properties = {}
    source_start = None
    first_source_line = ""
    for relative_index, line in enumerate(block[1:], start=1):
      property_match = property_pattern.match(line)
      if property_match:
        properties[property_match.group(1).casefold()] = property_match.group(2).strip()
      source_match = source_pattern.match(line)
      if source_match:
        source_start = relative_index
        first_source_line = source_match.group(1).strip()
        break

    source_lines = []
    if source_start is not None:
      source_line = block[source_start]
      source_indent = len(source_line) - len(source_line.lstrip())
      if first_source_line:
        source_lines.append(first_source_line)
      for line in block[source_start + 1:]:
        if not line.strip():
          source_lines.append("")
          continue
        indent = len(line) - len(line.lstrip())
        if indent <= source_indent and property_pattern.match(line):
          break
        trim = min(len(line), source_indent + 2)
        source_lines.append(line[trim:])

    expression = "\n".join(source_lines).strip()
    if expression.startswith("```") and expression.endswith("```"):
      expression = expression[3:-3].strip()

    yield {
      "name": _clean_name(header.group("name")),
      "source_type": (header.group("kind") or "").strip(),
      "mode": properties.get("mode", ""),
      "expression": expression,
      "line_number": start_index + 1,
    }


def _clean_name(value: str) -> str:
  value = value.strip()
  if len(value) > 1 and value[0] == value[-1] == "'":
    return value[1:-1].replace("''", "'")
  return value


def detect_source_kind(expression: str) -> str:
  """Return a descriptive source family from explicit M connector calls."""
  patterns = (
    (r"\bSql\.Database\s*\(", "SQL Server"),
    (r"\bSharePoint\.(?:Files|Contents)\s*\(", "SharePoint"),
    (r"\bExcel\.Workbook\s*\(", "Excel Workbook"),
    (r"\bCsv\.Document\s*\(", "CSV"),
    (r"\bJson\.Document\s*\(", "JSON"),
    (r"\bWeb\.Contents\s*\(", "Web"),
    (r"\bOData\.Feed\s*\(", "OData"),
    (r"\bPowerPlatform\.Dataflows\s*\(", "Power Platform Dataflow"),
    (r"\bAnalysisServices\.Database\s*\(", "Analysis Services"),
  )
  for pattern, label in patterns:
    if re.search(pattern, expression, re.IGNORECASE):
      return label
  return "Other / not detected"
