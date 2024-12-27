from dataclasses import dataclass
from enum import Enum
from typing import Optional

import plotly.graph_objects as go
import polars as pl

from blackfish.plotting.gaussian_broadening import apply_gaussian_filter
from blackfish.plotting.templates import plotly_template

SpectrumType = Enum("SpectrumType", "SOC_TDDFT TDDFT IR")


class Spectrum:
    def __init__(self, df: pl.DataFrame, spectrum_type: SpectrumType):
        self.df = df
        self.spectrum_type = spectrum_type
        self.fig = self.create_figure()

    def create_figure(self):
        match self.spectrum_type:
            case SpectrumType.SOC_TDDFT:
                return self._create_soc_tddft_figure()
            case SpectrumType.TDDFT:
                return self._create_tddft_figure()
            case SpectrumType.IR:
                return self._create_ir_figure()
            case _:
                raise ValueError("Invalid spectrum type")

    def _create_soc_tddft_figure(self):
        fig = go.Figure()
        fig.update_layout(
            template=plotly_template,
            width=1024,
            height=480,
            title="SOC-TDDFT Spectrum",
            xaxis_title="Energy [1/cm]",
            yaxis_title="Rel. Intensity",
        )
        fig.add_trace(SOCTDDFTBarTrace(self.df, name="SOC Absorption").to_plotly())
        fig.add_trace(SOCTDDFTSimulatedTrace(self.df, name="Simulated").to_plotly())
        fig.update_xaxes(autorange="reversed", tickformat="d")
        return fig

    def show(self, **kwargs):
        """Display the spectrum"""
        self.fig.show(**kwargs)


@dataclass
class BaseTrace:
    df: pl.DataFrame
    x: Optional[str] = None
    y: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None

    def to_plotly(self):
        """Convert to plotly trace"""
        raise NotImplementedError


@dataclass
class SOCTDDFTBarTrace(BaseTrace):
    def to_plotly(self) -> go.Bar:
        x_col = self.x or "Energy [1/cm]"
        y_col = self.y or "Rel. Intensity"
        color_col = self.color or "Multiplicity"
        return go.Bar(
            x=self.df[x_col],
            y=self.df[y_col],
            customdata=self.df[
                ["State", "Multiplicity", "Energy [eV]", "Wavelength [nm]"]
            ],
            name=self.name,
            width=100,
            marker=dict(
                color=self.df[color_col],
                colorbar=dict(title=color_col, titleside="right", tickvals=[1, 2, 3]),
            ),
            hovertemplate="State: <b>%{customdata[0]:8d}</b><br>"
            + "Mult: %{customdata[1]:8d}<br>"
            + "Energy: %{x:8.1f} cm<sup>-1</sup><br>"
            + "Energy: %{customdata[2]:8.2f} eV<br>"
            + "Rel. Intensity: %{y:8.2f}<br>"
            + "Wavelength: %{customdata[3]:8d} nm<br>",
        )


@dataclass
class SOCTDDFTSimulatedTrace(BaseTrace):
    def to_plotly(self, fwhm: int = 2000) -> go.Scatter:
        x_col = self.x or "Energy [1/cm]"
        y_col = self.y or "Rel. Intensity"
        color = self.color or "black"
        broadened_df = apply_gaussian_filter(self.df, x_col, y_col, fwhm, 10)
        return go.Scatter(
            x=broadened_df[x_col],
            y=broadened_df[y_col],
            customdata=[10e6 / i for i in broadened_df[x_col]],
            mode="lines",
            line=dict(color=color),
            name=f"FWHM = {fwhm:4d}",
            hovertemplate="Wavelength: %{customdata:.8d} nm",
        )
