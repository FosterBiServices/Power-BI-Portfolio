from pathlib import Path
from .markdown_writer import write_context
from .parser import TmdlParser
from .pbip_resolver import resolve_pbip
from .privacy import PrivacyOptions, apply_privacy
from .validation import validate_model
class ContextService:
  def build(self, pbip_path: Path, output_path: Path|None=None, privacy_options: PrivacyOptions|None=None) -> Path:
    model=TmdlParser().parse(resolve_pbip(pbip_path)); safe=apply_privacy(model,privacy_options or PrivacyOptions()); result=validate_model(safe)
    return write_context(safe,result,output_path or pbip_path.with_suffix('.semantic-context.md'))
