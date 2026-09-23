"""Parse Power BI TMDL metadata into the Context Builder domain model.

This implementation is adapted from the Local TMDL Documenter parser. The
Context Builder resolver remains responsible for PBIP -> report -> semantic model
resolution. This module only parses the resolved semantic model definition.
"""

from __future__ import annotations

import re
from pathlib import Path

from .domain import Column, DataSource, Measure, Relationship, SemanticModel, Table
from .exceptions import ModelParseError
from .pbip_resolver import ResolvedProject

_IDENTIFIER = r"(?:'(?:''|[^'])*'|[^.\s]+)"
_ENDPOINT = re.compile(
  rf"^\s*(fromColumn|toColumn)\s*:\s*({_IDENTIFIER})\.({_IDENTIFIER})\s*$",
  re.IGNORECASE,
)
_DECLARATION = re.compile(
  r"^(\s*)(table|column|measure|relationship|expression)\s+(.+?)(?:\s*=\s*(.*))?$",
  re.IGNORECASE,
)
_PROPERTY = re.compile(r"^\s*([A-Za-z][A-Za-z0-9]*)\s*:\s*(.*?)\s*$")


def _clean(value: str) -> str:
  value = value.strip()
  if len(value) > 1 and value[0] == value[-1] == "'":
    return value[1:-1].replace("''", "'")
  return value


def _read(path: Path) -> str:
  for encoding in ("utf-8-sig", "cp1252"):
    try:
      return path.read_text(encoding=encoding)
    except UnicodeDecodeError:
      continue
    except OSError as error:
      raise ModelParseError(f"Cannot read {path}: {error}") from error
  raise ModelParseError(f"Cannot decode {path}.")


def _blocks(text: str):
  lines = text.splitlines()
  index = 0
  while index < len(lines):
    match = _DECLARATION.match(lines[index])
    if not match:
      index += 1
      continue
    indent = len(match.group(1))
    start = index
    index += 1
    while index < len(lines):
      candidate = _DECLARATION.match(lines[index])
      if candidate and len(candidate.group(1)) <= indent:
        break
      index += 1
    yield start + 1, lines[start:index], match


def _properties(block: list[str]) -> dict[str, str]:
  output: dict[str, str] = {}
  for line in block[1:]:
    match = _PROPERTY.match(line)
    if match:
      output[match.group(1).casefold()] = match.group(2).strip()
  return output


def _expression_body(block: list[str], header_match: re.Match[str]) -> str:
  first = header_match.group(4) or ""
  body = [first] if first else []
  base = len(header_match.group(1))
  for line in block[1:]:
    if _PROPERTY.match(line) and len(line) - len(line.lstrip()) <= base + 2:
      break
    body.append(line[base + 2:] if len(line) >= base + 2 else line)
  return "\n".join(body).strip().strip("`")


def _bool_property(properties: dict[str, str], name: str, default: bool) -> bool:
  value = properties.get(name.casefold())
  if value is None:
    return default
  return value.casefold() == "true"


def _parse_tables_and_objects(files: list[Path]) -> dict[str, Table]:
  tables: dict[str, Table] = {}

  # First pass creates all tables so nested objects can be assigned deterministically.
  for path in files:
    for _, _, match in _blocks(_read(path)):
      if match.group(2).casefold() == "table":
        name = _clean(match.group(3))
        tables.setdefault(name, Table(name=name))

  # Second pass preserves the parent table for nested columns and measures.
  for path in files:
    lines = _read(path).splitlines()
    current_table: Table | None = None
    table_indent = -1
    index = 0
    while index < len(lines):
      match = _DECLARATION.match(lines[index])
      if not match:
        index += 1
        continue

      indent = len(match.group(1))
      kind = match.group(2).casefold()
      name = _clean(match.group(3))

      if kind == "table":
        current_table = tables.setdefault(name, Table(name=name))
        table_indent = indent
        property_lines = [lines[index]]
        look_ahead = index + 1
        while look_ahead < len(lines):
          candidate = _DECLARATION.match(lines[look_ahead])
          if candidate:
            break
          property_lines.append(lines[look_ahead])
          look_ahead += 1
        properties = _properties(property_lines)
        current_table.description = properties.get("description", "")
        current_table.is_hidden = _bool_property(properties, "ishidden", False)
        index += 1
        continue

      if current_table and indent > table_indent and kind in {"column", "measure"}:
        start = index
        index += 1
        while index < len(lines):
          candidate = _DECLARATION.match(lines[index])
          if candidate and len(candidate.group(1)) <= indent:
            break
          index += 1
        block = lines[start:index]
        properties = _properties(block)
        expression = _expression_body(block, match)

        if kind == "column":
          current_table.columns.append(
            Column(
              name=name,
              data_type=properties.get("datatype", "Unknown"),
              description=properties.get("description", ""),
              format_string=properties.get("formatstring", ""),
              is_hidden=_bool_property(properties, "ishidden", False),
              is_key=_bool_property(properties, "iskey", False),
              sort_by_column=properties.get("sortbycolumn", ""),
              summarize_by=properties.get("summarizeby", ""),
              expression=expression,
            )
          )
        else:
          current_table.measures.append(
            Measure(
              name=name,
              expression=expression,
              description=properties.get("description", ""),
              format_string=properties.get("formatstring", ""),
              display_folder=properties.get("displayfolder", ""),
              is_hidden=_bool_property(properties, "ishidden", False),
            )
          )
        continue

      index += 1

  return tables


def _parse_relationships(files: list[Path]) -> tuple[list[Relationship], list[str]]:
  relationships: list[Relationship] = []
  warnings: list[str] = []
  for path in files:
    for line_number, block, match in _blocks(_read(path)):
      if match.group(2).casefold() != "relationship":
        continue
      name = _clean(match.group(3))
      properties = _properties(block)
      endpoints: dict[str, tuple[str, str]] = {}
      for line in block[1:]:
        endpoint = _ENDPOINT.match(line)
        if endpoint:
          endpoints[endpoint.group(1).casefold()] = (
            _clean(endpoint.group(2)),
            _clean(endpoint.group(3)),
          )
      if "fromcolumn" not in endpoints or "tocolumn" not in endpoints:
        warnings.append(f"{path.name}:{line_number}: relationship {name} missing endpoint")
        continue

      from_table, from_column = endpoints["fromcolumn"]
      to_table, to_column = endpoints["tocolumn"]
      from_cardinality = properties.get("fromcardinality", "many")
      to_cardinality = properties.get("tocardinality", "one")
      relationships.append(
        Relationship(
          name=name,
          from_table=from_table,
          from_column=from_column,
          to_table=to_table,
          to_column=to_column,
          cardinality=f"{from_cardinality} to {to_cardinality}",
          cross_filter_direction=properties.get(
            "crossfilteringbehavior",
            "oneDirection",
          ),
          is_active=_bool_property(properties, "isactive", True),
        )
      )
  return relationships, warnings


def _parse_model_properties(definition_path: Path) -> tuple[str, str]:
  model_path = definition_path / "model.tmdl"
  if not model_path.is_file():
    return "Unknown", ""
  text = _read(model_path)
  mode = re.search(r"defaultMode\s*:\s*([^\s]+)", text, re.IGNORECASE)
  culture = re.search(r"culture\s*:\s*([^\s]+)", text, re.IGNORECASE)
  return (_clean(mode.group(1)) if mode else "Unknown", _clean(culture.group(1)) if culture else "")


def _detect_source_kind(expression: str) -> str:
  detectors = (
    ("SQL Server", r"Sql\.Database\s*\("),
    ("Power BI dataflow", r"PowerPlatform\.Dataflows|PowerBI\.Dataflows"),
    ("SharePoint", r"SharePoint\.(?:Files|Contents|Tables)\s*\("),
    ("Excel", r"Excel\.Workbook\s*\("),
    ("Folder", r"Folder\.(?:Files|Contents)\s*\("),
    ("Web", r"Web\.(?:Contents|BrowserContents)\s*\("),
    ("OData", r"OData\.Feed\s*\("),
  )
  for source_type, pattern in detectors:
    if re.search(pattern, expression, re.IGNORECASE):
      return source_type
  return "Other / not detected"


def _parse_data_sources(files: list[Path]) -> list[DataSource]:
  sources: list[DataSource] = []
  seen: set[tuple[str, str]] = set()
  partition_pattern = re.compile(
    r"^\s*partition\s+.+?\s*=\s*m\s*$",
    re.IGNORECASE | re.MULTILINE,
  )
  for path in files:
    text = _read(path)
    if not partition_pattern.search(text):
      continue
    source_type = _detect_source_kind(text)
    key = (source_type, str(path))
    if key not in seen:
      sources.append(DataSource(source_type=source_type, path=str(path)))
      seen.add(key)
  return sources


class TmdlParser:
  """Convert a resolved TMDL definition into Context Builder objects."""

  def parse(self, project: ResolvedProject) -> SemanticModel:
    try:
      files = sorted(
        project.definition_path.rglob("*.tmdl"),
        key=lambda path: str(path).casefold(),
      )
      if not files:
        raise ModelParseError("No TMDL files found.")

      tables = _parse_tables_and_objects(files)
      relationships, warnings = _parse_relationships(files)
      storage_mode, _culture = _parse_model_properties(project.definition_path)
      data_sources = _parse_data_sources(files)

      model = SemanticModel(
        name=project.semantic_model_path.name.removesuffix(".SemanticModel"),
        pbip_path=project.pbip_path,
        semantic_model_path=project.semantic_model_path,
        storage_mode=storage_mode,
        tables=list(tables.values()),
        relationships=relationships,
        data_sources=data_sources,
      )
      # Parser warnings are non-blocking. Validation independently checks endpoints.
      if warnings and not model.tables:
        raise ModelParseError("; ".join(warnings))
      return model
    except ModelParseError:
      raise
    except (OSError, ValueError, TypeError, re.error) as error:
      raise ModelParseError(
        f"Unable to parse semantic model at {project.definition_path}: {error}"
      ) from error
