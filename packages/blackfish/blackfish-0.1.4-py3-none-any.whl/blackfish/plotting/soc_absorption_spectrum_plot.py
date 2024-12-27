import polars as pl

from blackfish.plotting.spectrum import Spectrum, SpectrumType


def soc_absorption_spectrum_plot(df: pl.DataFrame) -> Spectrum:
    return Spectrum(df, SpectrumType.SOC_TDDFT)
