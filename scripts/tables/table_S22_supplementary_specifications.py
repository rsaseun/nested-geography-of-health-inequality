#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S22. Supplementary specifications of the SDG3-PI model

Location : Supplementary Material
Inputs   : cached analysis results (Section 6 econometrics)
Outputs  : outputs/tables/Table_S22.csv and outputs/tables_docx/Table_S22.docx
Run      : python scripts/tables/table_S22_supplementary_specifications.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S22."""
    E = R["E"]
    sv = ["M1", "X2", "X1_EXP", "ND_E", "ND_S", "ND_AC", "X1_TEMP", "X1", "lnHEPC", "URBAN", "lnGDP", "GOV", "FSCH"]
    d22 = {"Variable": [LABEL[v] for v in sv] + ["Adjusted R²"]}
    for k, (tab, r2, n) in E["sres"].items():
        d22[k] = [(_star(*tab.loc[v, ["beta", "se", "p"]]) if v in tab.index else "") for v in sv] + [_f(r2, 3)]
    return ("Table S22", "Supplementary specifications of the SDG3-PI model", pd.DataFrame(d22),
                "Note: As Table 3. (S4) uses the natural logarithm of SDG3-PI as the outcome to check functional form.", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
