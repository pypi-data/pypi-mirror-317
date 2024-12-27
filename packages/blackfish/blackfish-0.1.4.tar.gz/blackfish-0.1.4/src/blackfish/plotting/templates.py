import plotly.graph_objects as go

plotly_template = go.layout.Template(
    dict(
        layout=go.Layout(
            title=dict(font_family="verdana", font_size=20, x=0.5, xanchor="center"),
            width=1280,
            height=480,
            margin=dict(l=75, r=75, t=100, b=75),
            plot_bgcolor="whitesmoke",
            xaxis=dict(
                mirror=True,
                showline=True,
                ticks="inside",
                zeroline=False,
                showgrid=False,
                linewidth=2,
            ),
            yaxis=dict(
                mirror=True,
                showline=True,
                ticks="inside",
                zeroline=True,
                zerolinewidth=2,
                showgrid=False,
                linewidth=2,
            ),
            showlegend=True,
            legend=dict(
                x=0.99,
                y=0.99,
                xanchor="right",
                yanchor="top",
                bordercolor="grey",
                borderwidth=1,
                bgcolor="white",
            ),
            barcornerradius="40%",
            # hovermode="closest",
            hovermode="x",
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                # font_family="Rockwell"
                font_family="Arial",
            ),
        )
    )
)
