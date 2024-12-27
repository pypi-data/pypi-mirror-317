import marimo

__generated_with = "0.10.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import blackfish as bf
    return bf, mo


@app.cell
def _(bf):
    orca = bf.orca.ORCA("/Users/freddy/Documents/Projects/group10_triazole_azides/Group10_Triazole_Azide_Complexes/rerun/calculations/singlet/azide/tddft/pd/tddft.out")
    return (orca,)


@app.cell
def _(orca):
    orca.soc_absorption_spectrum
    return


@app.cell
def _(orca):
    plot = orca.soc_absorption_spectrum_plot
    return (plot,)


@app.cell
def _(plot):
    plot
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
