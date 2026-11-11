#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S19. Choosing the number of clusters

Location : Supplementary Material
Inputs   : cached analysis results (Section 5 spatial analysis)
Outputs  : outputs/tables/Table_S19.csv and outputs/tables_docx/Table_S19.docx
Run      : python scripts/tables/table_S19_cluster_number.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S19."""
    SP = R["SP"]
    kc = SP["kchoice"]
    return ("Table S19", "Choosing the number of clusters",
                pd.DataFrame({"k": kc.k.astype(str), "Silhouette": kc.Silhouette.map(lambda x: _f(x, 3)), "Gap": kc.Gap.map(lambda x: _f(x, 3)),
                              "Gap s.e.": kc["Gap s.e."].map(lambda x: _f(x, 3)), "Within-cluster SS": kc["Within-cluster SS"].map(lambda x: _f(x, 1))}),
                f"Note: The silhouette favours k = {SP['k_sil']} (a trivial split); the gap statistic (Tibshirani et al., 2001) favours k = {SP['k']}, which was adopted.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
