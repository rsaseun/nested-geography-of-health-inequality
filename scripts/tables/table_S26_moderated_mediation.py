#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S26. Cultural moderation of the mediation pathways (conditional indirect effects at the 10th, 50th
and 90th percentiles)

Location : Supplementary Material
Inputs   : cached analysis results (Section 7 mediation)
Outputs  : outputs/tables/Table_S26.csv and outputs/tables_docx/Table_S26.docx
Run      : python scripts/tables/table_S26_moderated_mediation.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S26."""
    M = R["M"]
    mrows = []
    for Cc, t in M["mod"].items():
        for _, r in t.iterrows():
            mrows.append({"Moderator": LABEL[Cc], "Quantity": r.Effect, "Estimate": _f(r.Estimate, 3), "95% BC CI": _ci(r["CI low"], r["CI high"]),
                          "CI excludes 0": r["CI excludes 0"]})
    return ("Table S26", "Cultural moderation of the mediation pathways (conditional indirect effects at the 10th, 50th and 90th percentiles)",
                pd.DataFrame(mrows), "Note: Each construct entered separately with its main effect in every equation.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
