from __future__ import annotations
import json, re
from pathlib import Path
from .domain import Column, Expression, Measure, Partition, Project, Relationship, ReportPage, Table, Visual
from .partition_support import detect_source_kind, parse_partition_blocks

_ID = r"(?:'(?:''|[^'])*'|[^.\s]+)"
_ENDPOINT = re.compile(rf"^\s*(fromColumn|toColumn)\s*:\s*({_ID})\.({_ID})\s*$", re.I)
_DECL = re.compile(r"^(\s*)(table|column|measure|relationship|expression)\s+(.+?)(?:\s*=\s*(.*))?$", re.I)
_PROP = re.compile(r"^\s*([A-Za-z][A-Za-z0-9]*)\s*:\s*(.*?)\s*$")
_COLUMN_REF = re.compile(r"(?:'((?:''|[^'])+)'|([A-Za-z_][\w ]*))\s*\[([^\]]+)\]")
_MEASURE_REF = re.compile(r"(?<![\w'])\[([^\]]+)\]")

class ProjectError(Exception): pass

def clean(value: str) -> str:
  value = value.strip()
  if len(value) > 1 and value[0] == value[-1] == "'": return value[1:-1].replace("''", "'")
  return value

def discover(selected: Path) -> tuple[Path, Path | None]:
  selected = selected.expanduser().resolve()
  if not selected.is_dir(): raise ProjectError(f"Folder does not exist: {selected}")
  semantic_candidates = [selected] if selected.name == "definition" and any(selected.rglob("*.tmdl")) else []
  semantic_candidates += list(selected.glob("*.SemanticModel/definition")) + list(selected.rglob("*.SemanticModel/definition"))
  if selected.name.endswith(".SemanticModel") and (selected / "definition").is_dir(): semantic_candidates.insert(0, selected / "definition")
  semantic = next((p for p in semantic_candidates if p.is_dir() and any(p.rglob("*.tmdl"))), None)
  if semantic is None and any(selected.rglob("*.tmdl")): semantic = selected
  if semantic is None: raise ProjectError("No semantic model TMDL definition was found.")
  search_root = selected if not selected.name.endswith("definition") else selected.parent.parent
  report_candidates = list(search_root.glob("*.Report/definition")) + list(search_root.rglob("*.Report/definition"))
  report = next((p for p in report_candidates if p.is_dir()), None)
  return semantic, report

def read(path: Path) -> str:
  for encoding in ("utf-8-sig", "cp1252"):
    try: return path.read_text(encoding=encoding)
    except UnicodeDecodeError: continue
    except OSError as error: raise ProjectError(f"Cannot read {path}: {error}") from error
  raise ProjectError(f"Cannot decode {path}.")

def blocks(text: str):
  lines = text.splitlines(); index = 0
  while index < len(lines):
    match = _DECL.match(lines[index])
    if not match:
      index += 1; continue
    indent = len(match.group(1)); start = index; index += 1
    while index < len(lines):
      candidate = _DECL.match(lines[index])
      if candidate and len(candidate.group(1)) <= indent: break
      index += 1
    yield start + 1, lines[start:index], match

def properties(block: list[str]) -> dict[str, str]:
  output = {}
  for line in block[1:]:
    match = _PROP.match(line)
    if match: output[match.group(1).casefold()] = match.group(2).strip()
  return output

def expression_body(block: list[str], header_match) -> str:
  first = header_match.group(4) or ""
  body = [first] if first else []
  base = len(header_match.group(1))
  for line in block[1:]:
    if _PROP.match(line) and len(line) - len(line.lstrip()) <= base + 2: break
    body.append(line[base + 2:] if len(line) >= base + 2 else line)
  return "\n".join(body).strip().strip("`")

# These folders restate table/measure names (translations, perspective
# membership, role permissions) without defining them.
_NON_DEFINITION_FOLDERS = {"cultures", "perspectives", "roles"}

def model_files(project: Project) -> list[Path]:
  files = []
  for path in project.semantic_root.rglob("*.tmdl"):
    parts = {part.casefold() for part in path.relative_to(project.semantic_root).parts[:-1]}
    if not parts & _NON_DEFINITION_FOLDERS: files.append(path)
  return sorted(files, key=lambda p: str(p).casefold())

def parse_tmdl(project: Project):
  files = model_files(project)
  if not files: raise ProjectError("No TMDL files found.")
  for path in files:
    text = read(path)
    for line_number, block, match in blocks(text):
      kind, raw_name = match.group(2).casefold(), match.group(3)
      name = clean(raw_name)
      props = properties(block)
      if kind == "table":
        project.tables.setdefault(name, Table(name=name, description=props.get("description", ""), is_hidden=props.get("ishidden", "false").casefold()=="true"))
      elif kind == "relationship":
        ends = {}
        for line in block[1:]:
          endpoint = _ENDPOINT.match(line)
          if endpoint: ends[endpoint.group(1).casefold()] = (clean(endpoint.group(2)), clean(endpoint.group(3)))
        if "fromcolumn" not in ends or "tocolumn" not in ends:
          project.warnings.append(f"{path.name}:{line_number}: relationship {name} missing endpoint")
          continue
        ft, fc = ends["fromcolumn"]; tt, tc = ends["tocolumn"]
        project.relationships.append(Relationship(name, ft, fc, tt, tc, props.get("fromcardinality","many"), props.get("tocardinality","one"), props.get("crossfilteringbehavior","oneDirection"), props.get("isactive","true").casefold() != "false"))
      elif kind == "expression": project.expressions.append(Expression(name, expression_body(block, match)))
  # Second pass preserves parent table for nested objects.
  for path in files:
    lines = read(path).splitlines(); current_table = None; table_indent = -1; index = 0
    while index < len(lines):
      match = _DECL.match(lines[index])
      if not match: index += 1; continue
      indent = len(match.group(1)); kind = match.group(2).casefold(); name = clean(match.group(3))
      if kind == "table": current_table = project.tables.setdefault(name, Table(name)); table_indent = indent; index += 1; continue
      if current_table and indent > table_indent and kind in {"column", "measure"}:
        start = index; index += 1
        while index < len(lines):
          nxt = _DECL.match(lines[index])
          if nxt and len(nxt.group(1)) <= indent: break
          index += 1
        block = lines[start:index]; props = properties(block)
        if kind == "column":
          current_table.columns.append(Column(name=name, data_type=props.get("datatype",""), format_string=props.get("formatstring",""), description=props.get("description",""), summarize_by=props.get("summarizeby",""), sort_by=props.get("sortbycolumn",""), source_column=props.get("sourcecolumn",""), is_hidden=props.get("ishidden","false").casefold()=="true", is_key=props.get("iskey","false").casefold()=="true"))
        else:
          dax = expression_body(block, match)
          column_refs = sorted({f"{a or b}[{c}]" for a,b,c in _COLUMN_REF.findall(dax)})
          all_brackets = set(_MEASURE_REF.findall(dax)); column_names = {c for _,_,c in _COLUMN_REF.findall(dax)}
          measure_refs = sorted(all_brackets - column_names - {name})
          current_table.measures.append(Measure(name=name, expression=dax, format_string=props.get("formatstring",""), display_folder=props.get("displayfolder",""), description=props.get("description",""), is_hidden=props.get("ishidden","false").casefold()=="true", column_refs=column_refs, measure_refs=measure_refs))
        continue
      index += 1
  model_file = project.semantic_root / "model.tmdl"
  if model_file.exists():
    text = read(model_file)
    level = re.search(r"compatibilityLevel\s*:\s*(\d+)", text, re.I); culture = re.search(r"culture\s*:\s*([^\s]+)", text, re.I)
    project.compatibility_level = level.group(1) if level else ""; project.culture = culture.group(1) if culture else ""

def walk_values(value):
  if isinstance(value, dict):
    for key, child in value.items():
      yield key, child
      yield from walk_values(child)
  elif isinstance(value, list):
    for child in value: yield from walk_values(child)

def parse_visual_fields(data) -> list[str]:
  refs = set()
  text = json.dumps(data, ensure_ascii=False)
  for table, column in re.findall(r'"Entity"\s*:\s*"([^"]+)".*?"Property"\s*:\s*"([^"]+)"', text): refs.add(f"{table}[{column}]")
  for table, measure in re.findall(r'"Entity"\s*:\s*"([^"]+)".*?"Measure"\s*:\s*"([^"]+)"', text): refs.add(f"{table}[{measure}]")
  return sorted(refs)

def parse_pbir(project: Project):
  if not project.report_root: return
  pages_root = project.report_root / "pages"
  if not pages_root.exists(): pages_root = project.report_root
  for page_dir in sorted([p for p in pages_root.iterdir() if p.is_dir()] if pages_root.exists() else []):
    page_json = page_dir / "page.json"
    try: pdata = json.loads(read(page_json)) if page_json.exists() else {}
    except json.JSONDecodeError as error:
      project.warnings.append(f"Invalid JSON {page_json}: {error}"); continue
    page = ReportPage(name=page_dir.name, display_name=pdata.get("displayName", page_dir.name), width=float(pdata.get("width",1280) or 1280), height=float(pdata.get("height",720) or 720))
    visuals_root = page_dir / "visuals"
    if visuals_root.exists():
      for vdir in sorted(p for p in visuals_root.iterdir() if p.is_dir()):
        path = vdir / "visual.json"
        if not path.exists(): continue
        try: data = json.loads(read(path))
        except json.JSONDecodeError as error:
          project.warnings.append(f"Invalid JSON {path}: {error}"); continue
        pos = data.get("position", {}); visual = data.get("visual", {})
        page.visuals.append(Visual(page.display_name, data.get("name",vdir.name), visual.get("visualType",data.get("visualType","unknown")), float(pos.get("x",0) or 0), float(pos.get("y",0) or 0), float(pos.get("width",0) or 0), float(pos.get("height",0) or 0), parse_visual_fields(data)))
    project.pages.append(page)

def parse_partitions(project: Project):
  """Parse M partition sources from each table TMDL file."""
  files = model_files(project)
  for path in files:
    text = read(path)
    table_names = [
      clean(match.group(1))
      for match in re.finditer(r"^\s*table\s+(.+?)\s*$", text, re.IGNORECASE | re.MULTILINE)
    ]
    if not table_names:
      continue
    table_name = table_names[0]
    table = project.tables.get(table_name)
    if table is None:
      continue
    existing = {partition.name for partition in table.partitions}
    for parsed in parse_partition_blocks(text):
      if parsed["name"] in existing:
        continue
      expression = parsed["expression"]
      table.partitions.append(Partition(
        name=parsed["name"],
        mode=parsed["mode"],
        source_type=parsed["source_type"],
        expression=expression,
        source_file=str(path),
        line_number=parsed["line_number"],
      ))
      existing.add(parsed["name"])
  # Classify after every partition is loaded so M references to staging queries,
  # shared expressions, or other tables can be followed to their connector.
  queries = {expression.name: expression.expression for expression in project.expressions}
  for table in project.tables.values():
    m_partitions = [p for p in table.partitions if p.source_type.casefold() in {"", "m"}]
    if m_partitions and table.name not in queries:
      queries[table.name] = m_partitions[0].expression
  for table in project.tables.values():
    for partition in table.partitions:
      partition.source_kind = detect_source_kind(
        partition.expression, partition.source_type, queries, table.name, partition.mode,
      )
def discover_from_pbip(
    pbip_path: Path
) -> tuple[Path, Path | None]:

    pbip = json.loads(
        read(pbip_path)
    )

    artifacts = pbip.get(
        "artifacts",
        []
    )

    report_root = None

    for artifact in artifacts:

        if "report" in artifact:

            report_path = (
                artifact["report"]
                .get("path")
            )

            if report_path:

                report_root = (
                    pbip_path.parent
                    / report_path
                )

                break

    if report_root is None:
        raise ProjectError(
            "No report reference found in PBIP."
        )

    if not report_root.exists():
        raise ProjectError(
            f"Report path not found:\n"
            f"{report_root}"
        )

    report_definition = (
        report_root
        / "definition.pbir"
    )

    if not report_definition.exists():

        report_definition = (
            report_root
            / "definition"
            / "definition.pbir"
        )

    if not report_definition.exists():
        raise ProjectError(
            f"Cannot locate PBIR:\n"
            f"{report_root}"
        )

    pbir = json.loads(
        read(report_definition)
    )

    semantic_relative = (
        pbir
        .get(
            "datasetReference",
            {}
        )
        .get(
            "byPath",
            {}
        )
        .get(
            "path"
        )
    )

    if not semantic_relative:
        raise ProjectError(
            "PBIR missing datasetReference."
        )

    semantic_root = (
        report_definition.parent
        / semantic_relative
    ).resolve()

    if not semantic_root.exists():
        raise ProjectError(
            f"Semantic model not found:\n"
            f"{semantic_root}"
        )

    semantic_definition = (
        semantic_root
        / "definition"
    )

    if not semantic_definition.exists():
        raise ProjectError(
            f"Semantic definition not found:\n"
            f"{semantic_definition}"
        )

    return (
        semantic_definition,
        report_root
    )

def load_project_from_pbip(pbip_path: Path) -> Project:

    project_folder = pbip_path.parent

    semantic, report = (discover_from_pbip(pbip_path))

    project = Project(
        pbip_path.resolve(),
        semantic,
        report,
        semantic.parent.name.removesuffix(".SemanticModel")
    )

    parse_tmdl(project)
    parse_partitions(project)
    parse_pbir(project)

    return project
