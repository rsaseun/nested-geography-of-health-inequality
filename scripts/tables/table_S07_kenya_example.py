#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S7. Worked example of the SDG3-PI computation: Kenya

Location : Supplementary Material
Inputs   : cached analysis results (Section 2 index)
Outputs  : outputs/tables/Table_S7.csv and outputs/tables_docx/Table_S7.docx
Run      : python scripts/tables/table_S07_kenya_example.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S7."""
    kx = R["kx"]
    return ("Table S7", "Worked example of the SDG3-PI computation: Kenya",
               pd.DataFrame({"Dimension": kx.Dimension, "Indicator": kx.Indicator, "Raw value": kx["Raw value"].map(lambda x: _f(x, 2)),
                             "Target t": kx["Target t"].map(lambda x: _f(x, 2)), "Worst w": kx["Worst w"].map(lambda x: _f(x, 2)), "Logged": kx.Logged,
                             "Score": kx["Score (0–100)"].map(lambda x: _f(x, 1)),
                             "Weight": kx.Weight.map(lambda x: _f(x, 3))}),
               "Kenya: dimension scores {} (maternal), {} (child), {} (communicable), {} (UHC); SDG3-PI = geometric mean = {}.".format(
                   *[_f(R["D"].loc["Kenya", c], 1) for c in ["Maternal health", "Child health", "Communicable disease", "UHC", "SDG3-PI"]]), True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
