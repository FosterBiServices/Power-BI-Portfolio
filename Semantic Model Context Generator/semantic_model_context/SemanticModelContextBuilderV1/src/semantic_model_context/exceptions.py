"""Application-specific exceptions."""


class ContextBuilderError(Exception):
  """Base exception for expected application failures."""


class PbipResolutionError(ContextBuilderError):
  """Raised when a PBIP project cannot be resolved safely."""


class ModelParseError(ContextBuilderError):
  """Raised when semantic model metadata cannot be parsed."""


class ValidationError(ContextBuilderError):
  """Raised when blocking validation issues are found."""
