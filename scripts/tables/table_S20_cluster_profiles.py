#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S20. Cluster profiles (means) and member countries

Location : Supplementary Material
Inputs   : cached analysis results (Section 5 spatial analysis)
Outputs  : outputs/tables/Table_S20.csv and outputs/tables_docx/Table_S20.docx
Run      : python scripts/tables/table_S20_cluster_profiles.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S20."""
    SP = R["SP"]
    pf = SP["prof"]
    return ("Table S20", "Cluster profiles (means) and member countries",
                pd.DataFrame({"Cluster": [str(i) for i in pf.index], "n": pf.n.astype(str), "SDG3-PI": pf["SDG3-PI"].map(lambda x: _f(x, 1)),
                              "X₁": pf.iloc[:, 2].map(lambda x: _f(x, 2)), "ln health workers /10k": pf.iloc[:, 3].map(lambda x: _f(x, 2)),
                              "C-A": pf.iloc[:, 4].map(lambda x: _f(x, 2)), "C-B": pf.iloc[:, 5].map(lambda x: _f(x, 2)),
                              "C-C": pf.iloc[:, 6].map(lambda x: _f(x, 2)), "C-D": pf.iloc[:, 7].map(lambda x: _f(x, 2)),
                              "Members": [SP["members"][i] for i in pf.index]}),
                "Note: Cultural constructs are principal-component scores. Clusters ordered by mean SDG3-PI.", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
