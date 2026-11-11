#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S29. Sensitivity of the indirect effects to unmeasured mediator–outcome confounding

Location : Supplementary Material
Inputs   : cached analysis results (Section 7 mediation)
Outputs  : outputs/tables/Table_S29.csv and outputs/tables_docx/Table_S29.docx
Run      : python scripts/tables/table_S29_sensitivity.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S29."""
    M = R["M"]
    return ("Table S29", "Sensitivity of the indirect effects to unmeasured mediator–outcome confounding",
                pd.DataFrame({"Mediator": M["sens"].Mediator, "ρ* at which the indirect effect falls to zero": M["sens"].iloc[:, 1].map(lambda x: _f(x, 3))}),
                "Note: ρ* is the residual correlation between mediator and outcome at which the mediated association would vanish (Imai et al., 2010).", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
