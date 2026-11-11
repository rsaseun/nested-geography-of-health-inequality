#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table 4. Determinants of SDG3-PI: standardised OLS coefficients (robust standard errors in parentheses)

Location : Manuscript, main text
Inputs   : cached analysis results (Section 6 econometrics)
Outputs  : outputs/tables/Table_4.csv and outputs/tables_docx/Table_4.docx
Run      : python scripts/tables/table_04_determinants.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table 4."""
    E = R["E"]
    order = ["M1", "X2", "X1", "X1_HAZ", "X1_CHRI", "TREELOSS", "lnHEPC", "URBAN", "lnGDP", "GOV", "FSCH", "C_A", "C_B", "C_C", "C_D"]
    t3 = {"Variable": [LABEL[v] for v in order] + ["Adjusted R²", "n"]}
    for k, (tab, r2, n) in E["res"].items():
        t3[k] = [(_star(*tab.loc[v, ["beta", "se", "p"]]) if v in tab.index else "") for v in order] + [_f(r2, 3), str(n)]
    return ("Table 4", "Determinants of SDG3-PI: standardised OLS coefficients (robust standard errors in parentheses)",
               pd.DataFrame(t3), "Note: HC3 standard errors pooled across 20 imputations with Rubin's rules. *** p < 0.01, ** p < 0.05, * p < 0.10. Diagnostics in Table S23, spatial models in Table S24, dimension-level models in Table S21.", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
