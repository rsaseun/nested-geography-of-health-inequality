#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S25. All path coefficients and indirect, direct and total effects of the mediation system

Location : Supplementary Material
Inputs   : cached analysis results (Section 7 mediation)
Outputs  : outputs/tables/Table_S25.csv and outputs/tables_docx/Table_S25.docx
Run      : python scripts/tables/table_S25_mediation_effects.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S25."""
    M = R["M"]
    bb = M["base"]
    return ("Table S25", "All path coefficients and indirect, direct and total effects of the mediation system",
                pd.DataFrame({"Effect": bb.Effect, "Estimate": bb.Estimate.map(lambda x: _f(x, 3)), "95% BC CI": [_ci(a, b_) for a, b_ in zip(bb["CI low"], bb["CI high"])],
                              "CI excludes 0": bb["CI excludes 0"]}), "", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
