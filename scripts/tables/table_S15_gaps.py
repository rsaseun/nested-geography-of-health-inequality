#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S15. Absolute and relative gaps between best and worst performers

Location : Supplementary Material
Inputs   : cached analysis results (Section 4 nested inequality)
Outputs  : outputs/tables/Table_S15.csv and outputs/tables_docx/Table_S15.docx
Run      : python scripts/tables/table_S15_gaps.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S15."""
    iq = R["ineq"]
    return ("Table S15", "Absolute and relative gaps between best and worst performers",
                pd.DataFrame({"Indicator": iq.Indicator, "n": iq.n.astype(str), "Best (country)": iq["Best (country)"], "Worst (country)": iq["Worst (country)"],
                              "Absolute gap": iq["Absolute gap"].map(lambda x: _f(x, 1)), "Relative gap": iq["Relative gap"].map(lambda x: _f(x, 1)),
                              "Pop.-weighted mean": iq["Population-weighted mean"].map(lambda x: _f(x, 1)),
                              "AFE mean": iq["AFE mean"].map(lambda x: _f(x, 1)), "AFW mean": iq["AFW mean"].map(lambda x: _f(x, 1))}), "", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
