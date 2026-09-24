"""Static DAX checks and reference extraction (adapted from Model Documenter)."""

from __future__ import annotations

from dataclasses import dataclass
import re

_IDENT_CHARS = re.compile(r"[A-Za-z0-9_.]")
_VAR_NAME = re.compile(r"\bVAR\s+([A-Za-z_]\w*)", re.IGNORECASE)
_KEYWORDS = {
  "return", "var", "in", "not", "and", "or", "true", "false", "asc", "desc",
  "define", "evaluate", "measure", "order", "by", "column", "table",
}
_CLOSERS = {")": "(", "}": "{"}


@dataclass(frozen=True)
class _Token:
  kind: str  # string, table, bracket, ident, punct
  text: str
  start: int
  end: int


class DaxSyntaxError(Exception):
  pass


def tokenize(expression: str) -> list[_Token]:
  """Tokenize DAX enough to validate nesting and object references.

  Raises DaxSyntaxError for unterminated strings, identifiers, or comments.
  """
  tokens: list[_Token] = []
  index = 0
  length = len(expression)

  def scan_quoted(quote: str, closer: str, label: str) -> int:
    end = index + 1
    while end < length:
      if expression[end] == closer:
        if end + 1 < length and expression[end + 1] == closer:
          end += 2
          continue
        return end
      end += 1
    raise DaxSyntaxError(f"Unterminated {label} starting with {quote}{expression[index + 1:index + 25]!s}")

  while index < length:
    char = expression[index]
    pair = expression[index:index + 2]
    if char.isspace():
      index += 1
    elif pair in ("//", "--"):
      end = expression.find("\n", index)
      index = length if end == -1 else end
    elif pair == "/*":
      end = expression.find("*/", index + 2)
      if end == -1:
        raise DaxSyntaxError("Unterminated /* comment.")
      index = end + 2
    elif char == '"':
      end = scan_quoted('"', '"', "string literal")
      tokens.append(_Token("string", expression[index + 1:end].replace('""', '"'), index, end + 1))
      index = end + 1
    elif char == "'":
      end = scan_quoted("'", "'", "quoted table name")
      tokens.append(_Token("table", expression[index + 1:end].replace("''", "'"), index, end + 1))
      index = end + 1
    elif char == "[":
      end = scan_quoted("[", "]", "bracket reference")
      tokens.append(_Token("bracket", expression[index + 1:end].replace("]]", "]"), index, end + 1))
      index = end + 1
    elif char.isalpha() or char == "_":
      end = index + 1
      while end < length and _IDENT_CHARS.match(expression[end]):
        end += 1
      tokens.append(_Token("ident", expression[index:end], index, end))
      index = end
    else:
      tokens.append(_Token("punct", char, index, index + 1))
      index += 1
  return tokens


def _nesting_error(tokens: list[_Token]) -> str | None:
  stack: list[str] = []
  for token in tokens:
    if token.kind != "punct":
      continue
    if token.text in "({":
      stack.append(token.text)
    elif token.text in _CLOSERS:
      if not stack or stack[-1] != _CLOSERS[token.text]:
        return f"Unexpected '{token.text}' with no matching '{_CLOSERS[token.text]}'."
      stack.pop()
  if stack:
    return f"{len(stack)} unclosed '{stack[-1]}'."
  return None


def _qualifier(tokens: list[_Token], position: int, variables: set[str]) -> str | None:
  """Return the table qualifying the bracket token at `position`, if any."""
  previous = tokens[position - 1] if position else None
  if previous and previous.kind == "table":
    return previous.text
  if (
    previous and previous.kind == "ident" and previous.end == tokens[position].start
    and previous.text.casefold() not in _KEYWORDS
    and previous.text.casefold() not in variables
  ):
    return previous.text
  return None


def measure_references(expression: str) -> tuple[list[str], list[str]]:
  """Return (qualified Table[Column] references, unqualified [Name] references).

  Comments, strings, hierarchy levels, and names defined inside the expression
  (ADDCOLUMNS aliases, GENERATESERIES [Value]) are excluded.
  """
  try:
    tokens = tokenize(expression or "")
  except DaxSyntaxError:
    return [], []
  local_names = {token.text.casefold() for token in tokens if token.kind == "string"}
  variables = {name.casefold() for name in _VAR_NAME.findall(expression)}
  qualified, unqualified = set(), set()
  for position, token in enumerate(tokens):
    if token.kind != "bracket":
      continue
    previous = tokens[position - 1] if position else None
    if previous and previous.kind == "punct" and previous.text == ".":
      continue
    qualifier = _qualifier(tokens, position, variables)
    name = token.text.strip()
    if qualifier is not None:
      qualified.add(f"{qualifier}[{name}]")
    elif name.casefold() not in local_names and not re.fullmatch(r"value\d*", name.casefold()):
      unqualified.add(name)
  return sorted(qualified, key=str.casefold), sorted(unqualified, key=str.casefold)


def check_measure(measure_name: str, expression: str, model_tables) -> list[str]:
  """Return error messages for one measure, resolving names against the whole model.

  These are static checks: they catch syntax problems and references to objects
  that do not exist, not every error the engine could raise.
  """
  if not (expression or "").strip():
    return ["Measure has no DAX expression."]
  try:
    tokens = tokenize(expression)
  except DaxSyntaxError as error:
    return [f"DAX syntax error: {error}"]
  if not tokens:
    return ["Measure has no DAX expression (only comments)."]

  errors = []
  nesting = _nesting_error(tokens)
  if nesting:
    errors.append(f"DAX syntax error: {nesting}")

  tables = {table.name.casefold(): table for table in model_tables}
  fields_by_table = {
    name: {item.name.casefold() for item in [*table.columns, *table.measures]}
    for name, table in tables.items()
  }
  all_measures = {m.name.casefold() for table in model_tables for m in table.measures}
  all_columns = {c.name.casefold() for table in model_tables for c in table.columns}
  # Names introduced inside the expression (ADDCOLUMNS/SELECTCOLUMNS aliases,
  # GENERATESERIES/table-constructor Value columns) are valid bracket targets.
  local_names = {token.text.casefold() for token in tokens if token.kind == "string"}
  variables = {name.casefold() for name in _VAR_NAME.findall(expression)}

  unknown_tables, unknown_fields, unknown_refs = [], [], []
  for position, token in enumerate(tokens):
    if token.kind != "bracket":
      continue
    previous = tokens[position - 1] if position else None
    name = token.text.strip()
    key = name.casefold()
    if previous and previous.kind == "punct" and previous.text == ".":
      continue  # Date hierarchy level, e.g. 'Date'[Date].[Year]
    qualifier = _qualifier(tokens, position, variables)
    if qualifier is not None:
      table_key = qualifier.casefold()
      if table_key not in tables:
        unknown_tables.append(qualifier)
      elif key not in fields_by_table[table_key]:
        unknown_fields.append(f"'{qualifier}'[{name}]")
      continue
    if key == measure_name.casefold():
      errors.append("Measure references itself.")
    elif (
      key not in all_measures and key not in all_columns and key not in local_names
      and not re.fullmatch(r"value\d*", key)
    ):
      unknown_refs.append(f"[{name}]")

  if unknown_tables:
    errors.append("References table(s) not in the model: " + ", ".join(sorted(set(unknown_tables))) + ".")
  if unknown_fields:
    errors.append("References column(s)/measure(s) that do not exist: " + ", ".join(sorted(set(unknown_fields))) + ".")
  if unknown_refs:
    errors.append("References unknown measure(s)/column(s): " + ", ".join(sorted(set(unknown_refs))) + ".")
  return errors
