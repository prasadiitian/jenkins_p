from __future__ import annotations

from pathlib import Path

import pytest

from jenkins_practice.validator import validate_two_number_csv


def test_validate_ok(tmp_path: Path):
    p = tmp_path / "ok.csv"
    p.write_text("1,2\n3.5,4\n", encoding="utf-8")

    result = validate_two_number_csv(p)

    assert result.ok is True
    assert result.total_rows == 2
    assert result.valid_rows == 2
    assert result.errors == []


def test_validate_fails_on_non_numeric(tmp_path: Path):
    p = tmp_path / "bad.csv"
    p.write_text("1,2\nhello,4\n", encoding="utf-8")

    result = validate_two_number_csv(p)

    assert result.ok is False
    assert result.total_rows == 2
    assert result.valid_rows == 1
    assert any("non-numeric" in e for e in result.errors)


def test_validate_fails_on_missing_file(tmp_path: Path):
    p = tmp_path / "missing.csv"

    result = validate_two_number_csv(p)

    assert result.ok is False
    assert result.total_rows == 0
    assert result.valid_rows == 0
    assert result.errors


def test_validate_fails_on_empty_file(tmp_path: Path):
    p = tmp_path / "empty.csv"
    p.write_text("\n\n", encoding="utf-8")

    result = validate_two_number_csv(p)

    assert result.ok is False
    assert result.total_rows == 0
    assert result.valid_rows == 0
    assert any("No data rows" in e for e in result.errors)


@pytest.mark.parametrize("row", ["1\n", "1,\n", ",2\n"])
def test_validate_fails_on_wrong_columns_or_values(tmp_path: Path, row: str):
    p = tmp_path / "weird.csv"
    p.write_text(row, encoding="utf-8")

    result = validate_two_number_csv(p)

    assert result.ok is False
    assert result.errors
