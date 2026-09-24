from __future__ import annotations

import json

from pathlib import Path


class PbipResolutionError(Exception):
    pass


def resolve_pbip(pbip_path: Path) -> dict:
    """
    Resolve SemanticModel and Report references
    directly from PBIP contents.
    """

    if not pbip_path.exists():
        raise PbipResolutionError(
            f"PBIP file not found:\n{pbip_path}"
        )

    try:
        content = json.loads(
            pbip_path.read_text(
                encoding="utf-8"
            )
        )
    except Exception as error:
        raise PbipResolutionError(
            f"Invalid PBIP:\n{pbip_path}"
        ) from error

    semantic_models = []
    reports = []

    for artifact in content.get("artifacts", []):

        artifact_type = (
            artifact.get("artifactType")
            or artifact.get("type")
            or ""
        )

        artifact_path = artifact.get("path")

        if not artifact_path:
            continue

        resolved = (
            pbip_path.parent
            / artifact_path
        )

        if artifact_type.casefold() == "semanticmodel":
            semantic_models.append(
                resolved.resolve()
            )

        elif artifact_type.casefold() == "report":
            reports.append(
                resolved.resolve()
            )

    if not semantic_models:
        raise PbipResolutionError(
            "No SemanticModel reference found."
        )

    if len(semantic_models) > 1:
        raise PbipResolutionError(
            "Multiple SemanticModel references found."
        )

    semantic_root = semantic_models[0]

    if not semantic_root.exists():
        raise PbipResolutionError(
            f"Missing semantic model:\n{semantic_root}"
        )

    report_root = None

    if reports:
        report_root = reports[0]

        if not report_root.exists():
            report_root = None

    return {
        "PbipPath": pbip_path.resolve(),
        "SemanticRoot": semantic_root,
        "ReportRoot": report_root
    }