"""Write one AI-readable Markdown context file."""

from datetime import UTC, datetime
from pathlib import Path

from .domain import SemanticModel
from .validation import ValidationResult


def _safe_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def write_context(
    model: SemanticModel,
    validation: ValidationResult,
    output_path: Path,
) -> Path:

    generated_utc = datetime.now(UTC).isoformat(timespec="seconds")

    measure_count = sum(
        len(table.measures)
        for table in model.tables
    )

    column_count = sum(
        len(table.columns)
        for table in model.tables
    )

    # ==========================================
    # Model Profile Statistics
    # ==========================================

    data_type_counts: dict[str, int] = {}
    
    for table in model.tables:
        for column in table.columns:

            data_type = (
                column.data_type
                if column.data_type
                else "Unknown"
            )

            data_type_counts[data_type] = (
                data_type_counts.get(
                    data_type,
                    0
                )
                + 1
            )

    table_relationship_counts = {}

    for table in model.tables:

        relationship_count = sum(
            1
            for relationship in model.relationships
            if relationship.from_table == table.name
            or relationship.to_table == table.name
        )

        table_relationship_counts[
            table.name
        ] = relationship_count

    most_connected_tables = sorted(
        table_relationship_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:10]

    measure_only_tables = sum(
        1
        for table in model.tables
        if (
            len(table.columns) == 0
            and len(table.measures) > 0
        )
    )

    lines = [
        "---",
        "contextType: Power BI Semantic Model",
        "schemaVersion: 1.0",
        "generator: Semantic Model Context Builder",
        f"modelName: {_safe_cell(model.name)}",
        f"generatedUtc: {generated_utc}",
        "---",
        "",
        "# Semantic Model Instructions",
        "",
        "Treat this file as the authoritative structural reference for this model.",
        "Do not invent tables, columns, measures, or relationships that are not listed.",
        "Use exact object names when proposing DAX.",
        "",
        "# Model Summary",
        "",
        f"- Model: {model.name}",
        f"- Storage mode: {model.storage_mode}",
        f"- Tables: {len(model.tables)}",
        f"- Measure-Only Tables Remaining: {measure_only_tables}",
        f"- Columns: {column_count}",
        f"- Measures: {measure_count}",
        f"- Relationships: {len(model.relationships)}",
    ]

    # ==========================================
    # Model Profile
    # ==========================================

    lines.extend([
        "",
        "## Model Profile",
        "",
        "### Data Type Distribution",
        ""
    ])

    for data_type, count in sorted(
        data_type_counts.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        lines.append(
            f"- {data_type}: {count}"
        )

    lines.extend([
        "",
        "### Most Connected Tables",
        ""
    ])

    for rank, (
        table_name,
        relationship_count
    ) in enumerate(
        most_connected_tables,
        start=1
    ):

        lines.append(
            f"{rank}. "
            f"{table_name} "
            f"({relationship_count} relationships)"
        )

    lines.extend([
        "",
        "# Tables",
    ])

    # ==========================================
    # Table Detail
    # ==========================================

    for table in model.tables:

        table_column_count = len(
            table.columns
        )

        table_measure_count = len(
            table.measures
        )

        hidden_column_count = sum(
            1
            for column in table.columns
            if column.is_hidden
        )

        relationship_count = sum(
            1
            for relationship in model.relationships
            if relationship.from_table == table.name
            or relationship.to_table == table.name
        )

        related_tables = sorted(
            {
                relationship.to_table
                for relationship in model.relationships
                if relationship.from_table == table.name
            }
            |
            {
                relationship.from_table
                for relationship in model.relationships
                if relationship.to_table == table.name
            }
        )

        string_columns = sum(
            1
            for column in table.columns
            if (
                column.data_type
                and column.data_type.lower() == "string"
            )
        )

        date_columns = sum(
            1
            for column in table.columns
            if (
                column.data_type
                and column.data_type.lower()
                in ("datetime", "date", "datetime64")
            )
        )

        numeric_columns = sum(
            1
            for column in table.columns
            if (
                column.data_type
                and column.data_type.lower()
                in (
                    "int64",
                    "int32",
                    "double",
                    "decimal",
                    "number"
                )
            )
        )

        lines.extend([
            "",
            f"## {table.name}",
            "",
            table.description
            or "No description provided.",
            "",
            "### Statistics",
            "",
            f"- Columns: {table_column_count}",
            f"- Measures: {table_measure_count}",
            f"- Relationships: {relationship_count}",
            f"- Hidden Columns: {hidden_column_count}",
            "",
            "### Summary",
            "",
            f"- String Columns: {string_columns}",
            f"- Date Columns: {date_columns}",
            f"- Numeric Columns: {numeric_columns}",
        ])

        if related_tables:

            lines.extend([
                "",
                "### Related Tables",
                ""
            ])

            for related_table in related_tables:

                lines.append(
                    f"- {related_table}"
                )

        lines.extend([
            "",
            "### Columns",
            "",
            "| Column | Data Type | Hidden | Key | Sort By |",
            "|---|---|---:|---:|---|",
        ])

        for column in table.columns:

            lines.append(
                f"| {_safe_cell(column.name)} | "
                f"{_safe_cell(column.data_type)} | "
                f"{'Yes' if column.is_hidden else 'No'} | "
                f"{'Yes' if column.is_key else 'No'} | "
                f"{_safe_cell(column.sort_by_column)} |"
            )

        if table.measures:

            lines.extend([
                "",
                "### Measures",
            ])

            for measure in table.measures:

                lines.extend([
                    "",
                    f"#### {measure.name}",
                    "",
                    "```dax",
                    measure.expression,
                    "```",
                ])

    # ==========================================
    # Relationships
    # ==========================================

    lines.extend([
        "",
        "# Relationships",
        "",
        "| From | To | Cardinality | Direction | Active |",
        "|---|---|---|---|---:|",
    ])

    for relationship in model.relationships:

        lines.append(
            f"| {relationship.from_table}[{relationship.from_column}] | "
            f"{relationship.to_table}[{relationship.to_column}] | "
            f"{_safe_cell(relationship.cardinality)} | "
            f"{_safe_cell(relationship.cross_filter_direction)} | "
            f"{'Yes' if relationship.is_active else 'No'} |"
        )

    # ==========================================
    # Validation
    # ==========================================

    lines.extend([
        "",
        "# Validation",
        "",
        f"- Model parsed successfully: {'Yes' if validation.is_valid else 'No'}",
        f"- Errors: {len(validation.errors)}",
        f"- Warnings: {len(validation.warnings)}",
    ])

    for error in validation.errors:
        lines.append(
            f"  - Error: {error}"
        )

    for warning in validation.warnings:
        lines.append(
            f"  - Warning: {warning}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8"
    )

    return output_path