from pathlib import Path

import polars as pl

def ir_spectrum(orca_output: Path) -> pl.DataFrame:
    lines = Path(orca_output).read_text().splitlines()

    TABLE_HEADER = "IR SPECTRUM"
    TABLE_HEADER_OFFSET = 5

    table_start_idx = next(i for i, line in enumerate(lines) if TABLE_HEADER in line.strip())
    table_start_idx += TABLE_HEADER_OFFSET

    # Collect table
    rows = []
    for row in lines[table_start_idx:]:
        # Stop on empty line
        if not row.strip():
            break

        rows.append(row)

    processed_rows = [row.replace(":", "").replace("(", "").replace(")", "").strip().split() for row in rows]

    df = pl.DataFrame(
        processed_rows,
        orient='row',
        schema={
            "Mode": pl.Int64,
            "Frequency [1/cm]": pl.Float64,
            "Epsilon [L/(mol*cm)]": pl.Float64,
            "Intensity [km/mol]": pl.Float64,
            "T2": pl.Float64,
            "TX": pl.Float64,
            "TY": pl.Float64,
            "TZ": pl.Float64
        }
    )

    df = df.with_columns(
        (pl.col("Intensity [km/mol]") / pl.col("Intensity [km/mol]").max()).alias("Rel. Intensity")
    )

    return df
