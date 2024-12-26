from pathlib import Path

from blackfish.parsing import ir_spectrum, roots, soc_absorption_spectrum, soc_states

ROOT = Path(__file__).parent


def test_parsing_ir_spectrum():
    df = ir_spectrum(ROOT / "data/ir_spectrum.txt")
    assert len(df) == 237
    assert df.columns == [
        "Mode",
        "Frequency [1/cm]",
        "Epsilon [L/(mol*cm)]",
        "Intensity [km/mol]",
        "T2",
        "TX",
        "TY",
        "TZ",
        "Rel. Intensity",
    ]


def test_parsing_roots():
    df = roots(ROOT / "data/roots.txt")
    assert len(df) == 180
    assert df.columns == [
        "Root",
        "Multiplicity",
        "Donor",
        "Acceptor",
        "Weight",
        "Energy [1/cm]",
    ]


def test_parsing_soc_absorption_spectrum():
    df = soc_absorption_spectrum(ROOT / "data/soc_absorption_spectrum.txt")
    assert len(df) == 64
    assert df.columns == [
        "State",
        "Multiplicity",
        "Energy [ev].",
        "Energy [1/cm].",
        "Wavelength [nm]",
        "Osc. Strength",
        "D2",
        "DX",
        "DY",
        "DZ",
        "Rel. Intensity",
    ]


def test_parsing_soc_states():
    df = soc_states(ROOT / "data/soc_states.txt")
    assert len(df) == 9
    assert df.columns == [
        "State",
        "Spin",
        "Root",
        "Weight",
        "Energy [1/cm]",
    ]
