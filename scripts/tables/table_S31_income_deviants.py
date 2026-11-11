#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S31. Countries performing furthest above and below the level predicted by income

Location : Supplementary Material
Inputs   : cached analysis results (Section 6 income-deviant regression)
Outputs  : outputs/tables/Table_S31.csv and outputs/tables_docx/Table_S31.docx
Run      : python scripts/tables/table_S31_income_deviants.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S31."""
    E = R["E"]
    dv = E["dev"]
    top, bot = dv.head(6), dv.tail(6).iloc[::-1]
    t5 = pd.DataFrame({"Positive deviant": top.index, "SDG3-PI": top["SDG3-PI"].map(lambda x: _f(x, 1)),
                       "Predicted": top["Predicted"].map(lambda x: _f(x, 1)), "Residual": top["Residual"].map(lambda x: "+" + _f(x, 1)),
                       "Cluster": [str(R["SP"]["cluster"][c]) for c in top.index],
                       "Negative deviant": list(bot.index), "SDG3-PI ": list(bot["SDG3-PI"].map(lambda x: _f(x, 1))),
                       "Predicted ": list(bot["Predicted"].map(lambda x: _f(x, 1))), "Residual ": list(bot["Residual"].map(lambda x: _f(x, 1))),
                       "Cluster ": [str(R["SP"]["cluster"][c]) for c in bot.index]})
    return ("Table S31", "Countries performing furthest above and below the level predicted by income",
               t5, f"Note: Residuals from a regression of SDG3-PI on ln GDP per capita (slope {E['dev_info']['slope']:.1f} points per log unit; R² = {E['dev_info']['R2']:.2f}). Cluster = health–environment–culture typology (Fig. 6c).", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
