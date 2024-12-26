from pathlib import Path
from typing import Iterator

import polars as pl


def _parse_single_root(root_lines: list[str]) -> dict:
    """Parse a single root block into a dictionary."""
    # Parse header line
    header = root_lines[0].strip()
    state_num = int(header[5 : header.index(":")])
    parts = header.strip().split()
    energy_ev = float(parts[5])
    energy_cm = float(parts[7])
    spin_expectation_value = float(parts[11])
    multiplicity = int(parts[13])

    # Parse root contributions
    orbital_transitions = []
    for line in root_lines[1:]:
        parts = line.replace("->", "").replace(":", "").replace(")", "").strip().split()
        orbital_transitions.append(
            {
                "Donor": str(parts[0]),
                "Acceptor": str(parts[1]),
                "Weight": float(parts[2]),
            }
        )

    return {
        "Root": state_num,
        "Energy [eV]": energy_ev,
        "Energy [1/cm]": energy_cm,
        "<S**2>": spin_expectation_value,
        "Multiplicity": multiplicity,
        "Orbital Transitions": orbital_transitions,
    }


def _iter_roots(lines: list[str]) -> Iterator[list[str]]:
    """Iterate over root blocks in the input text."""
    current_state = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            if lines[i + 1].strip().startswith("STATE"):
                continue
            else:
                break

        if line.startswith("STATE"):
            if current_state:
                yield current_state
            current_state = [line]
        elif current_state:
            current_state.append(line)

    if current_state:  # Don't forget the last state
        yield current_state


def roots(orca_output: Path) -> pl.DataFrame:
    """Parse roots from ORCA output into a Polars DataFrame."""
    # Read file content
    content = Path(orca_output).read_text().splitlines()

    # Find the start of root section(s)
    start_indicies = []
    for line in content:
        if "TD-DFT/TDA EXCITED STATES" in line or "TD-DFT EXCITED STATES" in line:
            start_indicies.append(content.index(line))
            # Find the custom offset (different for different tables..)
            while not content[start_indicies[-1]].startswith("STATE"):
                start_indicies[-1] += 1

    # Parse roots
    roots = []
    for start_idx in start_indicies:
        for root_lines in _iter_roots(content[start_idx:]):
            root_data = _parse_single_root(root_lines)
            roots.append(root_data)

    # Flatten the data structure
    flattened_roots = []
    for root in roots:
        for orb_contrib in root["Orbital Transitions"]:
            flattened_roots.append(
                {
                    "Root": root["Root"],
                    "Multiplicity": root["Multiplicity"],
                    "Donor": orb_contrib["Donor"],
                    "Acceptor": orb_contrib["Acceptor"],
                    "Weight": orb_contrib["Weight"],
                    "Energy [1/cm]": root["Energy [1/cm]"],
                }
            )

    # Create and transform DataFrame
    df = pl.DataFrame(flattened_roots)
    return df.sort("Root", "Weight", descending=[False, True])
