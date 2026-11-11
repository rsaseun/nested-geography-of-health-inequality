#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S24. Spatial lag and spatial error models (maximum likelihood) for model (2)

Location : Supplementary Material
Inputs   : cached analysis results (Section 6 econometrics)
Outputs  : outputs/tables/Table_S24.csv and outputs/tables_docx/Table_S24.docx
Run      : python scripts/tables/table_S24_spatial_models.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S24."""
    E = R["E"]
    sp_ = E["spat"]
    return ("Table S24", "Spatial lag and spatial error models (maximum likelihood) for model (2)",
                pd.DataFrame({"Variable": [LABEL.get(i, i) for i in sp_.index], "Spatial lag β": sp_.iloc[:, 0].map(lambda x: _f(x, 3)),
                              "p": sp_.iloc[:, 1].map(lambda x: _p(x) if pd.notna(x) else "–"),
                              "Spatial error β": sp_.iloc[:, 2].map(lambda x: _f(x, 3)), "p ": sp_.iloc[:, 3].map(lambda x: _p(x) if pd.notna(x) else "–")}), "", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
