#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S18. Global spatial autocorrelation (Moran's I)

Location : Supplementary Material
Inputs   : cached analysis results (Section 5 spatial analysis)
Outputs  : outputs/tables/Table_S18.csv and outputs/tables_docx/Table_S18.docx
Run      : python scripts/tables/table_S18_morans_i.py   (from the repository root)

Formatting follows the journals' table requirements: editable Word table, black text, no shading,
horizontal rules only (top, under the header and at the bottom), notes below the table.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, save_table  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (pandas as pd, numpy as np, labels, constants)
from sdg3_nested_geography.core import _f, _p, _star, _ci  # noqa: E402,F401  (number formatting)


def build(R):
    """Return (label, title, DataFrame, note, landscape) for Table S18."""
    SP = R["SP"]
    mo = SP["moran"]
    return ("Table S18", "Global spatial autocorrelation (Moran's I)",
                pd.DataFrame({"Variable": mo.Variable, "Moran's I": mo["Moran's I"].map(lambda x: _f(x, 3)), "E[I]": mo["E[I]"].map(lambda x: _f(x, 3)),
                              "z (permutation)": mo["z (permutation)"].map(lambda x: _f(x, 2)), "p (9,999 permutations)": mo["p (9,999 permutations)"].map(_p)}),
                f"Note: Weights combine queen contiguity with four nearest neighbours (minimum {SP['winfo']['min neighbours']}, mean {SP['winfo']['mean neighbours']:.1f} neighbours), row-standardised.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
