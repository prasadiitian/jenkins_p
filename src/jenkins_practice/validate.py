from __future__ import annotations

import argparse
import html
from pathlib import Path

from .validator import validate_two_number_csv


def _write_text_report(out_path: Path, *, input_path: Path, result) -> None:
    lines: list[str] = []
    lines.append(f"Input: {input_path}")
    lines.append(f"OK: {result.ok}")
    lines.append(f"Total rows: {result.total_rows}")
    lines.append(f"Valid rows: {result.valid_rows}")
    lines.append("")

    if result.errors:
        lines.append("Errors:")
        for err in result.errors:
            lines.append(f"- {err}")
    else:
        lines.append("No errors.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_html_report(out_path: Path, *, input_path: Path, result) -> None:
    title = "Validation Report"
    status = "PASS" if result.ok else "FAIL"

    error_items = "".join(f"<li>{html.escape(e)}</li>" for e in result.errors) or "<li>None</li>"

    page = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; }}
    .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; max-width: 900px; }}
    .status {{ font-weight: 700; padding: 2px 10px; border-radius: 999px; display: inline-block; }}
    .pass {{ background: #e7f7ee; color: #0b6b2d; }}
    .fail {{ background: #fdecec; color: #9a1c1c; }}
    code {{ background: #f6f8fa; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <div class=\"card\">
    <p><strong>Input</strong>: <code>{html.escape(str(input_path))}</code></p>
    <p><strong>Status</strong>: <span class=\"status {'pass' if result.ok else 'fail'}\">{status}</span></p>
    <p><strong>Total rows</strong>: {result.total_rows} &nbsp; | &nbsp; <strong>Valid rows</strong>: {result.valid_rows}</p>
    <h2>Errors</h2>
    <ul>
      {error_items}
    </ul>
  </div>
</body>
</html>
"""

    out_path.write_text(page, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an uploaded CSV/txt input file and generate reports.")
    parser.add_argument("--input", required=True, help="Path to input file (CSV with 2 numeric columns: a,b)")
    parser.add_argument("--outdir", default="reports", help="Output directory for reports")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    result = validate_two_number_csv(input_path)

    _write_text_report(outdir / "validation.txt", input_path=input_path, result=result)
    _write_html_report(outdir / "validation.html", input_path=input_path, result=result)

    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
