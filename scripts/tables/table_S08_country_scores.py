#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S8. SDG3-PI and dimension scores by country (0 = worst observed, 100 = 2030 target)

Location : Supplementary Material
Inputs   : cached analysis results (Sections 2 and 5)
Outputs  : outputs/tables/Table_S8.csv and outputs/tables_docx/Table_S8.docx
Run      : python scripts/tables/table_S08_country_scores.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S8."""
    SP = R["SP"]
    Dd = R["D"].sort_values("SDG3-PI", ascending=False)
    return ("Table S8", "SDG3-PI and dimension scores by country (0 = worst observed, 100 = 2030 target)",
               pd.DataFrame({"Rank": [str(int(x)) for x in Dd.Rank], "Country": Dd.index, "Sub-region": [R["reg"].loc[c, "WB"] for c in Dd.index],
                             "AU region": [R["reg"].loc[c, "AU"] for c in Dd.index],
                             "Maternal": Dd["Maternal health"].map(lambda x: _f(x, 1)), "Child": Dd["Child health"].map(lambda x: _f(x, 1)),
                             "Communicable": Dd["Communicable disease"].map(lambda x: _f(x, 1)), "UHC": Dd["UHC"].map(lambda x: _f(x, 1)),
                             "SDG3-PI": Dd["SDG3-PI"].map(lambda x: _f(x, 1)), "Distance to 2030": Dd["Distance to 2030"].map(lambda x: _f(x, 1)),
                             "Cluster": [str(SP["cluster"][c]) for c in Dd.index]}), "", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
