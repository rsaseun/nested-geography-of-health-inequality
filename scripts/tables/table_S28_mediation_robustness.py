#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S28. Robustness of the mediation results to alternative climate and deprivation measures

Location : Supplementary Material
Inputs   : cached analysis results (Section 7 mediation)
Outputs  : outputs/tables/Table_S28.csv and outputs/tables_docx/Table_S28.docx
Run      : python scripts/tables/table_S28_mediation_robustness.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S28."""
    M = R["M"]
    arows = []
    for lab, t in M["alt"].items():
        tt = t.set_index("Effect")
        for k, nm in [("path a22", "a₂₂ X₂ → M₂"), ("path a11", "a₁₁ X₁ → M₁"), ("IE₁ livelihood pathway", "IE₁ livelihood pathway"),
                      ("IE₂ burden pathway", "IE₂ burden pathway"), ("X₁ total effect", "X₁ total effect"), ("X₂ total effect", "X₂ total effect")]:
            arows.append({"Alternative measure": lab, "Quantity": nm, "Estimate": _f(tt.loc[k, "Estimate"], 3),
                          "95% BC CI": _ci(tt.loc[k, "CI low"], tt.loc[k, "CI high"]), "CI excludes 0": tt.loc[k, "CI excludes 0"]})
    return ("Table S28", "Robustness of the mediation results to alternative climate and deprivation measures", pd.DataFrame(arows),
                "Note: Unsafe-WASH deaths are themselves a health burden, so the last variant partly measures the mediator.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
