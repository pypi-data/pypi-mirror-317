from pathlib import Path

import polars as pl


def soc_absorption_spectrum(orca_output: Path) -> pl.DataFrame:
    lines = Path(orca_output).read_text().splitlines()

    TABLE_HEADER = (
        "SOC CORRECTED ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"
    )
    TABLE_HEADER_OFFSET = 5

    table_start_idx = next(
        i for i, line in enumerate(lines) if TABLE_HEADER in line.strip()
    )
    table_start_idx += TABLE_HEADER_OFFSET

    # Collect table
    rows = []
    for row in lines[table_start_idx:]:
        # Stop on empty line
        if not row.strip():
            break

        rows.append(row)

    # Process table
    processed_rows = []
    for row in rows:
        row = row.replace("A", "").replace("B", "").replace("->", "")
        to_state, to_spin = row.split()[1].split("-")
        processed_row = [to_state, to_spin] + row.split()[2:]
        processed_rows.append(processed_row)

    df = pl.DataFrame(
        processed_rows,
        orient="row",
        schema={
            "State": pl.Int64,
            "Multiplicity": pl.Float64,
            "Energy [ev].": pl.Float64,
            "Energy [1/cm].": pl.Float64,
            "Wavelength [nm]": pl.Float64,
            "Osc. Strength": pl.Float64,
            "D2": pl.Float64,
            "DX": pl.Float64,
            "DY": pl.Float64,
            "DZ": pl.Float64,
        },
    )

    df = df.with_columns(
        (pl.col("Osc. Strength") / pl.col("Osc. Strength").max()).alias(
            "Rel. Intensity"
        )
    )

    return df
