#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S12. Climate-vulnerability components and composites

Location : Supplementary Material
Inputs   : cached analysis results (Section 3 constructs)
Outputs  : outputs/tables/Table_S12.csv and outputs/tables_docx/Table_S12.docx
Run      : python scripts/tables/table_S12_climate_components.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S12."""
    C = R["C"]
    K0 = R["C"]["K0"]
    B0 = C["B0"]
    comps = [("ND-GAIN exposure", B0.ND_E), ("ND-GAIN sensitivity", B0.ND_S), ("ND-GAIN capacity deficit", B0.ND_AC),
             ("ND-GAIN composite (X₁)", K0.X1), ("CHRI exposure", B0.CH_E), ("CHRI sensitivity", B0.CH_S),
             ("CHRI adaptive capacity", B0.CH_AC), ("CHRI composite (E + S − AC)", K0.X1_CHRI), ("Observed hazard (PC score)", K0.X1_HAZ)]
    return ("Table S12", "Climate-vulnerability components and composites",
                pd.DataFrame([{"Component": n, "Mean": _f(v.mean(), 3), "SD": _f(v.std(), 3), "Min": _f(v.min(), 3), "Max": _f(v.max(), 3),
                               "r with ln GDP pc": _f(np.corrcoef(v, K0.lnGDP)[0, 1], 2), "r with SDG3-PI": _f(np.corrcoef(v, K0.Y)[0, 1], 2)} for n, v in comps]),
                "Note: Single-imputation values. ND-GAIN components are 0–1 scores (higher = more vulnerable); CHRI components are banded 0–100 scores.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
