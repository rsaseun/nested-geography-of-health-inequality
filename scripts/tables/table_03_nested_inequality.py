#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table 3. Nested inequality in SDG 3 indicators: population-weighted Gini and Theil indices and the share
of inequality lying between regions

Location : Manuscript, main text
Inputs   : cached analysis results (Section 4 nested inequality)
Outputs  : outputs/tables/Table_3.csv and outputs/tables_docx/Table_3.docx
Run      : python scripts/tables/table_03_nested_inequality.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table 3."""
    iq = R["ineq"]
    t2 = pd.DataFrame({"Indicator": iq.Indicator, "Gini": iq.Gini.map(lambda x: _f(x, 3)), "Theil T": iq["Theil T"].map(lambda x: _f(x, 3)),
                       "Between AFE/AFW (% of T)": iq["Between AFE/AFW (% of T)"].map(lambda x: _f(x, 1)),
                       "Between AU regions (% of T)": iq["Between AU regions (% of T)"].map(lambda x: _f(x, 1)),
                       "Countries at 2030 benchmark": iq["Countries at 2030 benchmark"].replace("", "–")})
    return ("Table 3", "Nested inequality in SDG 3 indicators: population-weighted Gini and Theil indices and the share of inequality lying between regions",
               t2, "Note: Inequality is measured on original rates, weighted by population. The between-region share is the between-group component of Theil T for two partitions: the World Bank sub-regions (AFE, 26 countries; AFW, 22) and the five African Union regions. Absolute and relative gaps in Table S15.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
