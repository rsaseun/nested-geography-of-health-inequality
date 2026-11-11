#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table 5. Serial–parallel mediation of environmental risk through poverty and health-system pressure
(standardised estimates)

Location : Manuscript, main text
Inputs   : cached analysis results (Section 7 mediation)
Outputs  : outputs/tables/Table_5.csv and outputs/tables_docx/Table_5.docx
Run      : python scripts/tables/table_05_mediation.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table 5."""
    M = R["M"]
    b = M["base"].set_index("Effect")
    keep = [("path a12", "a₁₂  X₂ → M₁"), ("path a22", "a₂₂  X₂ → M₂"), ("path a11", "a₁₁  X₁ → M₁"),
            ("path b1", "b₁  M₁ → Y"), ("path b2", "b₂  M₂ → Y"), ("path d21", "d₂₁  M₁ → M₂"),
            ("IE₁ livelihood pathway", "IE₁ livelihood pathway (a₁₁b₁ + a₁₁d₂₁b₂)"),
            ("IE₂ burden pathway", "IE₂ burden pathway (a₂₂b₂)"), ("Contrast IE₁ − IE₂", "Contrast IE₁ − IE₂"),
            ("X₂ total indirect", "X₂ total indirect effect"), ("X₂ direct (c′₂)", "X₂ direct effect (c′₂)"),
            ("X₂ total effect", "X₂ total effect"), ("X₁ total effect", "X₁ total effect")]
    t4 = pd.DataFrame([{"Path or effect": lab, "Estimate": _f(b.loc[k, "Estimate"], 3), "95% bias-corrected CI": _ci(b.loc[k, "CI low"], b.loc[k, "CI high"]),
                        "CI excludes 0": b.loc[k, "CI excludes 0"]} for k, lab in keep])
    return ("Table 5", "Serial–parallel mediation of environmental risk through poverty and health-system pressure (standardised estimates)",
               t4, "Note: Controls Z = ln GDP per capita, governance and female schooling in every equation. Intervals from 5,000 bootstrap resamples of countries (250 per imputation). Full set of indirect effects in Table S25.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
