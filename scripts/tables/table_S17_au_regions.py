#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S17. Mean scores by African Union region (robustness grouping)

Location : Supplementary Material
Inputs   : cached analysis results (Section 4 nested inequality)
Outputs  : outputs/tables/Table_S17.csv and outputs/tables_docx/Table_S17.docx
Run      : python scripts/tables/table_S17_au_regions.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S17."""
    au = R["au"]
    return ("Table S17", "Mean scores by African Union region (robustness grouping)",
                pd.concat([pd.Series(au.index, name="AU region"), pd.Series(au.n.astype(str).values, name="n"),
                           au.drop(columns="n").reset_index(drop=True).map(lambda x: _f(x, 1))], axis=1),
                "Note: Mauritania forms the AU Northern group on its own.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
