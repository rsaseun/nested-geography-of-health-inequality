#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S14. Correlation matrix of model variables

Location : Supplementary Material
Inputs   : cached analysis results (Section 3 constructs)
Outputs  : outputs/tables/Table_S14.csv and outputs/tables_docx/Table_S14.docx
Run      : python scripts/tables/table_S14_correlations.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S14."""
    C = R["C"]
    cm = C["corr"].copy()
    cmv = cm.map(lambda x: _f(x, 2))
    for i in range(len(cm)):
        for j in range(len(cm)):
            if j > i:
                cmv.iloc[i, j] = ""
    cmv.insert(0, " ", cm.index)
    return ("Table S14", "Correlation matrix of model variables", cmv, "", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
