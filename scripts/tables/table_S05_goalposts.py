#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S5. Goalposts used to rescale each indicator to 0–100 and resulting scores

Location : Supplementary Material
Inputs   : cached analysis results (Section 2 index)
Outputs  : outputs/tables/Table_S5.csv and outputs/tables_docx/Table_S5.docx
Run      : python scripts/tables/table_S05_goalposts.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S5."""
    st = R["steps"]
    return ("Table S5", "Goalposts used to rescale each indicator to 0–100 and resulting scores",
               pd.DataFrame({"Indicator": st.Indicator, "Target t (score 100)": st["Target t"].map(lambda x: _f(x, 2)), "Basis of t": st["Basis of t"],
                             "Worst w (score 0)": st["Worst w"].map(lambda x: _f(x, 2)), "Basis of w": st["Basis of w"],
                             "Mean score": st["Mean score"].map(lambda x: _f(x, 1)), "% at target": st["% at target"].map(lambda x: _f(x, 1))}),
               "Note: positive x′ = 100(x − w)/(t − w); negative x′ = 100(w − x)/(w − t); negative logged x′ = 100(ln w − ln max(x, t))/(ln w − ln t); bounded to [0, 100].", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
