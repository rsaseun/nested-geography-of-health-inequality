#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S16. SDG3-PI and dimensions in Africa Eastern & Southern (AFE) versus Western & Central (AFW)

Location : Supplementary Material
Inputs   : cached analysis results (Section 4 nested inequality)
Outputs  : outputs/tables/Table_S16.csv and outputs/tables_docx/Table_S16.docx
Run      : python scripts/tables/table_S16_afe_afw.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S16."""
    cp = R["comp"]
    return ("Table S16", "SDG3-PI and dimensions in Africa Eastern & Southern (AFE) versus Western & Central (AFW)",
                pd.DataFrame({"Measure": cp.Measure, "AFE mean (n = 26)": cp.iloc[:, 1].map(lambda x: _f(x, 1)), "AFW mean (n = 22)": cp.iloc[:, 2].map(lambda x: _f(x, 1)),
                              "Difference": cp.Difference.map(lambda x: _f(x, 1)), "Welch t p": cp["Welch t p"].map(_p), "Mann–Whitney p": cp["Mann–Whitney p"].map(_p)}), "", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
