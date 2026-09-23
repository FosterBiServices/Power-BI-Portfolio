"""Command-line interface."""

import argparse
from pathlib import Path

from .exceptions import ContextBuilderError
from .logging_config import configure_logging
from .privacy import PrivacyOptions
from .service import ContextService


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="semantic-context")
  subparsers = parser.add_subparsers(dest="command", required=True)
  build = subparsers.add_parser("build", help="Build a semantic model context file.")
  build.add_argument("pbip", type=Path, help="Path to an actual .pbip file.")
  build.add_argument("--output", type=Path)
  build.add_argument("--include-hidden", action="store_true")
  build.add_argument("--exclude-dax", action="store_true")
  build.add_argument("--include-source-locations", action="store_true")
  return parser


def main() -> int:
  configure_logging()
  arguments = build_parser().parse_args()
  options = PrivacyOptions(
    include_hidden_objects=arguments.include_hidden,
    include_dax=not arguments.exclude_dax,
    include_data_source_locations=arguments.include_source_locations,
  )
  try:
    output = ContextService().build(arguments.pbip, arguments.output, options)
  except ContextBuilderError as error:
    print(f"Error: {error}")
    return 1
  print(f"Semantic model context created: {output}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
