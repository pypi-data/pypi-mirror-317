from pathlib import Path

import polars as pl

import blackfish as bf


class ORCA:
    def __init__(self, output_file: Path):
        self.output_file = output_file

    @property
    def ir_spectrum(self) -> pl.DataFrame:
        return bf.parsing.ir_spectrum(self.output_file)

    @property
    def roots(self) -> pl.DataFrame:
        return bf.parsing.roots(self.output_file)

    @property
    def soc_absorption_spectrum(self) -> pl.DataFrame:
        return bf.parsing.soc_absorption_spectrum(self.output_file)

    @property
    def soc_states(self) -> pl.DataFrame:
        return bf.parsing.soc_states(self.output_file)

    @property
    def soc_absorption_spectrum_plot(self) -> None:
        return bf.plotting.soc_absorption_spectrum_plot(self.soc_absorption_spectrum)
