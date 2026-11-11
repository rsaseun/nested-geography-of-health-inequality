#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S21. Model (2) estimated for each SDG3-PI dimension

Location : Supplementary Material
Inputs   : cached analysis results (Section 6 econometrics)
Outputs  : outputs/tables/Table_S21.csv and outputs/tables_docx/Table_S21.docx
Run      : python scripts/tables/table_S21_dimension_models.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S21."""
    E = R["E"]
    vv = CORE + ZS
    d21 = {"Variable": [LABEL[v] for v in vv] + ["Adjusted R²"]}
    for k, (tab, r2, n) in E["dimres"].items():
        d21[k] = [_star(*tab.loc[v, ["beta", "se", "p"]]) for v in vv] + [_f(r2, 3)]
    return ("Table S21", "Model (2) estimated for each SDG3-PI dimension", pd.DataFrame(d21),
                "Note: Standardised coefficients, robust s.e. in parentheses; *** p < 0.01, ** p < 0.05, * p < 0.10.", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
