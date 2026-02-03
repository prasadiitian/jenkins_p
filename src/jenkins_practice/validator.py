from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    total_rows: int
    valid_rows: int
    errors: list[str]


def validate_two_number_csv(file_path: str | Path) -> ValidationResult:
    """Validate a CSV with two numeric columns: a,b

    Rules:
    - Must be readable as CSV
    - Must contain at least 1 data row
    - Each row must have at least 2 columns
    - First two columns must parse as floats

    Returns a ValidationResult with human-readable errors.
    """

    path = Path(file_path)
    errors: list[str] = []

    if not path.exists():
        return ValidationResult(ok=False, total_rows=0, valid_rows=0, errors=[f"File not found: {path}"])

    total_rows = 0
    valid_rows = 0

    try:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row_index, row in enumerate(reader, start=1):
                # Skip completely empty lines
                if not row or all(cell.strip() == "" for cell in row):
                    continue

                total_rows += 1

                if len(row) < 2:
                    errors.append(f"Row {row_index}: expected 2 columns, got {len(row)}")
                    continue

                a_raw, b_raw = row[0].strip(), row[1].strip()
                try:
                    float(a_raw)
                    float(b_raw)
                except ValueError:
                    errors.append(f"Row {row_index}: non-numeric values: a='{a_raw}', b='{b_raw}'")
                    continue

                valid_rows += 1

    except UnicodeDecodeError:
        return ValidationResult(
            ok=False,
            total_rows=0,
            valid_rows=0,
            errors=["File is not UTF-8 text. Please upload a UTF-8 encoded .csv or .txt file."],
        )

    if total_rows == 0:
        errors.append("No data rows found (expected at least 1 row with 2 numeric columns).")

    ok = (len(errors) == 0)
    return ValidationResult(ok=ok, total_rows=total_rows, valid_rows=valid_rows, errors=errors)
