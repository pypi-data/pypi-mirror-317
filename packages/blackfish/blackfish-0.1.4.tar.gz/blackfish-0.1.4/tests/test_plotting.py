from pathlib import Path

import plotly.graph_objects as go

from blackfish.plotting import plotly_template

ROOT = Path(__file__).parent


def test_plotly_template_works():
    template = plotly_template()
    fig = go.Figure(template=template)
    assert isinstance(fig, go.Figure)
