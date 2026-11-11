#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S4. SDG3-PI indicators: properties and log-transformation decision

Location : Supplementary Material
Inputs   : cached analysis results (Section 2 index)
Outputs  : outputs/tables/Table_S4.csv and outputs/tables_docx/Table_S4.docx
Run      : python scripts/tables/table_S04_index_indicators.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S4."""
    st = R["steps"]
    return ("Table S4", "SDG3-PI indicators: properties and log-transformation decision",
               pd.DataFrame({"Dimension": st.Dimension, "Indicator": st.Indicator, "Unit": st.Unit, "Direction": st.Direction, "n": st.n.astype(str),
                             "Range": [f"{_f(a, 2)}–{_f(b_, 2)}" for a, b_ in zip(st.Min, st.Max)],
                             "Max/min": st["Max/min"].map(lambda x: _f(x, 1) if np.isfinite(x) else "∞ (zeros)"),
                             "Skewness": st.Skewness.map(lambda x: _f(x, 2)), "Logged": st.Logged}),
               "Note: A rate was logged if its max/min ratio exceeded 10 or its skewness exceeded 1.", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
