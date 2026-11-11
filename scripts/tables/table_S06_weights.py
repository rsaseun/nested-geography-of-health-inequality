#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S6. Weights within SDG3-PI dimensions

Location : Supplementary Material
Inputs   : cached analysis results (Section 2 index)
Outputs  : outputs/tables/Table_S6.csv and outputs/tables_docx/Table_S6.docx
Run      : python scripts/tables/table_S06_weights.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S6."""
    wt = R["wtab"]
    return ("Table S6", "Weights within SDG3-PI dimensions",
               pd.DataFrame({"Dimension": wt.Dimension, "Indicator": wt.Indicator, "PC1 loading": wt["PC1 loading"].map(lambda x: _f(x, 3)),
                             "Variance explained by PC1": wt["Variance explained by PC1"].map(lambda x: f"{x * 100:.1f}%"), "Rule applied": wt["Rule applied"],
                             "Weight used": wt["Weight used"].map(lambda x: _f(x, 3)), "Entropy weight (robustness)": wt["Entropy weight (robustness)"].map(lambda x: _f(x, 3))}),
               "Note: In the communicable-disease dimension HIV and TB load opposite to malaria, so a pre-stated rule applies equal weights.", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
