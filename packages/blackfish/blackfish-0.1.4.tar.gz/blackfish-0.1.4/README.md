blackfish
=========

Collection of various tools for analyzing ORCA 6 calculation output files.

Installation
------------

```bash
pip install blackfish
```

`marimo`
--------

It is strongly recommended to use [`marimo`](https://marimo.io/).

Usage
-----

```python
from blackfish import ORCA

orca = ORCA('path/to/orca/output')
```

Access table data as `polars` DataFrames or plot them with `plotly`.

Available dataframes:

| *Attribute* | *Description* |
|-----------|-------------|
| `ir_spectrum` | IR Spectrum |
| `roots` | TDDFT roots |
| `soc_states` | SOC-TDDFT states |
| `soc_absorption_spectrum` | SOC-TDDFT absorption spectrum |

Available plots:

| *Attribute* | *Description* |
|-----------|-------------|
| `soc_absorption_spectrum_plot` | Plot SOC-TDDFT absorption spectrum |
