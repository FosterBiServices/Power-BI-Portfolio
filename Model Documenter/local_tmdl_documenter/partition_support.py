from __future__ import annotations

import re
import textwrap


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
  source_pattern = re.compile(r"^\s*source\s*(?:=\s*(.*?))?\s*$", re.IGNORECASE)

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
      source_match = source_pattern.match(line)
      if source_match:
        source_start = relative_index
        first_source_line = (source_match.group(1) or "").strip()
        break
      property_match = property_pattern.match(line)
      if property_match:
        properties[property_match.group(1).casefold()] = property_match.group(2).strip()

    expression = ""
    source_properties = {}
    if source_start is not None:
      source_line = block[source_start]
      source_indent = _indent(source_line)
      source_lines = []
      if first_source_line.startswith("```"):
        # Fenced source: everything up to the closing fence belongs to the source.
        remainder = first_source_line[3:]
        if remainder.rstrip().endswith("```"):
          source_lines.append(remainder.rstrip()[:-3])
        else:
          if remainder.strip():
            source_lines.append(remainder)
          for line in block[source_start + 1:]:
            if line.strip().endswith("```"):
              source_lines.append(line.rstrip()[:-3])
              break
            source_lines.append(line)
      else:
        if first_source_line:
          source_lines.append(first_source_line)
        # Unfenced source: the body is every line indented deeper than `source`.
        for line in block[source_start + 1:]:
          if line.strip() and _indent(line) <= source_indent:
            break
          source_lines.append(line)
      expression = textwrap.dedent("\n".join(source_lines)).strip()
      if not first_source_line:
        # `source` with no `=` (entity / Direct Lake partitions) holds properties.
        for line in source_lines:
          property_match = property_pattern.match(line)
          if property_match:
            source_properties[property_match.group(1).casefold()] = property_match.group(2).strip()

    yield {
      "name": _clean_name(header.group("name")),
      "source_type": (header.group("kind") or "").strip(),
      "mode": properties.get("mode", ""),
      "expression": expression,
      "source_properties": source_properties,
      "line_number": start_index + 1,
    }


def _indent(line: str) -> int:
  return len(line) - len(line.lstrip())


def _clean_name(value: str) -> str:
  value = value.strip()
  if len(value) > 1 and value[0] == value[-1] == "'":
    return value[1:-1].replace("''", "'")
  return value


UNDETECTED = "Other / not detected"

# First match wins. Databases and services are checked before file formats, and
# file formats before generic transports, so Excel.Workbook(File.Contents(...))
# reports "Excel Workbook" rather than "File".
_M_CONNECTORS = (
  # Quickbase custom connectors vary in name (Quickbased, QuickBase.Contents, ...);
  # a quickbase.com URL also identifies Web.Contents calls to its API.
  (r"\bQuick_?Base\w*(?:\.\w+)?\s*\(|quickbase\.com", "Quickbase"),
  (r"\bSql\.Databases?\s*\(", "SQL Server"),
  (r"\bOracle\.Database\s*\(", "Oracle"),
  (r"\bPostgreSQL\.Database\s*\(", "PostgreSQL"),
  (r"\bMySQL\.Database\s*\(", "MySQL"),
  (r"\bSnowflake\.Databases\s*\(", "Snowflake"),
  (r"\b(?:Databricks|DatabricksMultiCloud)\.\w+\s*\(", "Databricks"),
  (r"\bGoogleBigQuery\.Database\s*\(", "Google BigQuery"),
  (r"\bAmazonRedshift\.Database\s*\(", "Amazon Redshift"),
  (r"\bTeradata\.Database\s*\(", "Teradata"),
  (r"\bSapHana\.Database\s*\(", "SAP HANA"),
  (r"\bSapBusinessWarehouse\.\w+\s*\(", "SAP BW"),
  (r"\bDB2\.Database\s*\(", "IBM Db2"),
  (r"\bSybase\.Database\s*\(", "Sybase"),
  (r"\bAnalysisServices\.Databases?\s*\(", "Analysis Services"),
  (r"\b(?:AzureDataExplorer|Kusto)\.\w+\s*\(", "Azure Data Explorer"),
  (r"\bLakehouse\.Contents\s*\(", "Fabric Lakehouse"),
  (r"\b(?:Fabric\.Warehouse|Warehouse\.Contents)\s*\(", "Fabric Warehouse"),
  (r"\b(?:PowerPlatform|PowerBI)\.Dataflows\s*\(", "Power Platform Dataflow"),
  (r"\b(?:CommonDataService\.Database|Cds\.Entities|Dataverse\.Contents)\s*\(", "Dataverse"),
  (r"\bSalesforce\.(?:Data|Reports)\s*\(", "Salesforce"),
  (r"\bOdbc\.(?:DataSource|Query)\s*\(", "ODBC"),
  (r"\bOleDb\.(?:DataSource|Query)\s*\(", "OLE DB"),
  (r"\bExchange\.Contents\s*\(", "Exchange"),
  (r"\bActiveDirectory\.Domains\s*\(", "Active Directory"),
  (r"\bSharePoint\.(?:Files|Contents|Tables)\s*\(", "SharePoint"),
  (r"\bAzureStorage\.\w+\s*\(", "Azure Storage"),
  (r"\bFolder\.(?:Files|Contents)\s*\(", "Folder"),
  (r"\bExcel\.(?:Workbook|CurrentWorkbook)\s*\(", "Excel Workbook"),
  (r"\bCsv\.Document\s*\(", "CSV"),
  (r"\bParquet\.Document\s*\(", "Parquet"),
  (r"\bAccess\.Database\s*\(", "Access Database"),
  (r"\bPdf\.Tables\s*\(", "PDF"),
  (r"\bOData\.Feed\s*\(", "OData"),
  (r"\bWeb\.(?:Contents|Page|BrowserContents)\s*\(", "Web"),
  (r"\bJson\.Document\s*\(", "JSON"),
  (r"\bXml\.(?:Tables|Document)\s*\(", "XML"),
  (r"\bFile\.Contents\s*\(", "File"),
)
_ENTERED_DATA = re.compile(r"\bBinary\.Decompress\s*\(\s*Binary\.FromText\s*\(", re.IGNORECASE)
_GENERATED_M = re.compile(
  r"#table\s*\(|\bTable\.From(?:Rows|Records|List|Columns)\s*\(|\bList\.(?:Dates|Numbers|Generate)\s*\(",
  re.IGNORECASE,
)
_PARAMETER_QUERY = re.compile(r"\bIsParameterQuery\s*=\s*true", re.IGNORECASE)
_M_STEP = re.compile(r'^\s*,?\s*(#"(?:[^"]|"")+"|[A-Za-z_][\w.]*)\s*=(?!=)', re.MULTILINE)
# Quoted identifiers, plain string literals (matched only to be skipped), or bare identifiers.
_M_TOKEN = re.compile(r'#"((?:[^"]|"")+)"|"(?:[^"]|"")*"|(?<![\w.])([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)')


def strip_comments(text: str, dax: bool = False) -> str:
  """Remove // and /* */ comments (plus -- for DAX), leaving string literals intact."""
  output = []
  index = 0
  length = len(text)
  while index < length:
    char = text[index]
    pair = text[index:index + 2]
    if char == '"':
      end = index + 1
      while end < length:
        if text[end] == '"':
          if end + 1 < length and text[end + 1] == '"':
            end += 2
            continue
          break
        end += 1
      output.append(text[index:end + 1])
      index = end + 1
    elif pair == "//" or (dax and pair == "--"):
      end = text.find("\n", index)
      index = length if end == -1 else end
    elif pair == "/*":
      end = text.find("*/", index + 2)
      index = length if end == -1 else end + 2
    else:
      output.append(char)
      index += 1
  return "".join(output)


def _without_strings(text: str) -> str:
  return re.sub(r'"(?:[^"]|"")*"', '""', text)


def _classify_dax(expression: str) -> str:
  code = _without_strings(strip_comments(expression, dax=True))
  if re.search(r"\bNAMEOF\s*\(", code, re.IGNORECASE):
    return "Field Parameter (DAX)"
  if re.search(r"\bCALENDAR(?:AUTO)?\s*\(", code, re.IGNORECASE):
    return "Date Table (DAX)"
  if re.search(r"\bGENERATESERIES\s*\(", code, re.IGNORECASE):
    return "Parameter Series (DAX)"
  if re.match(r"\s*(?:\{|DATATABLE\s*\(|ROW\s*\()", code, re.IGNORECASE):
    return "Static Data (DAX)"
  if not code.strip():
    return "Empty Calculated Table"
  return "Calculated Table (DAX)"


def _classify_m(expression, queries, self_name, visited) -> str:
  code = strip_comments(expression)
  # Enter Data tables embed rows via Json.Document(Binary.Decompress(...)).
  if _ENTERED_DATA.search(code):
    return "Entered Data (Power Query)"
  for pattern, label in _M_CONNECTORS:
    if re.search(pattern, code, re.IGNORECASE):
      return label

  # Follow references to other queries (staging queries, shared expressions,
  # or other tables) back to the connector they ultimately use.
  steps = {_unquote_identifier(name) for name in _M_STEP.findall(code)}
  referenced = []
  for quoted, bare in _M_TOKEN.findall(code):
    name = quoted.replace('""', '"') if quoted else bare
    if name and name in queries and name not in steps and name not in referenced:
      referenced.append(name)
  kinds = set()
  for name in referenced:
    if name in visited:
      continue
    target = queries[name]
    if _PARAMETER_QUERY.search(target):
      continue
    kind = _classify_m(target, queries, name, visited | {name})
    if kind != UNDETECTED:
      kinds.add(kind)
  if kinds:
    specific = kinds - {"Generated in Power Query"}
    return " + ".join(sorted(specific or kinds))
  if _GENERATED_M.search(code) or re.search(r"#date\s*\(", code, re.IGNORECASE):
    return "Generated in Power Query"
  return UNDETECTED


def _unquote_identifier(token: str) -> str:
  if token.startswith('#"'):
    return token[2:-1].replace('""', '"')
  return token


def detect_source_kind(expression: str, source_type: str = "", queries=None,
                       self_name: str = "", mode: str = "") -> str:
  """Return a descriptive source family for a partition.

  DAX calculated partitions are classified by their table constructor. M
  partitions are classified by explicit connector calls; when a query only
  references other queries, those references are followed (cycle-safe) until a
  connector is found.
  """
  kind = (source_type or "").strip().casefold()
  if kind == "calculated":
    return _classify_dax(expression or "")
  if kind == "entity" or (mode or "").casefold() == "directlake":
    return "Direct Lake"
  if kind == "calculationgroup":
    return "Calculation Group"
  if kind == "query":
    return "Legacy Provider Query"
  if not (expression or "").strip():
    return UNDETECTED
  queries = queries or {}
  return _classify_m(expression, queries, self_name, {self_name})
