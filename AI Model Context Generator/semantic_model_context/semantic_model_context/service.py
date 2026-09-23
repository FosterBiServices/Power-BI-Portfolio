"""Application service used by every interface."""

from pathlib import Path

from .markdown_writer import write_context
from .parser import TmdlParser
from .pbip_resolver import resolve_pbip
from .privacy import PrivacyOptions, apply_privacy
from .validation import validate_model


class ContextService:
  def __init__(self, parser: TmdlParser | None = None) -> None:
    self._parser = parser or TmdlParser()

  def build(
    self,
    pbip_path: Path,
    output_path: Path | None = None,
    privacy_options: PrivacyOptions | None = None,
  ) -> Path:
    resolved = resolve_pbip(pbip_path)
    model = self._parser.parse(resolved)
    safe_model = apply_privacy(model, privacy_options or PrivacyOptions())
    validation = validate_model(safe_model)
    target = output_path or pbip_path.with_suffix(".semantic-context.md")
    return write_context(safe_model, validation, target)
