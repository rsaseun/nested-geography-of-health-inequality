#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S30. Health Belief Model extension: health-belief proxies, service uptake and mortality

Location : Supplementary Material
Inputs   : cached analysis results (Section 8 Health Belief Model extension)
Outputs  : outputs/tables/Table_S30.csv and outputs/tables_docx/Table_S30.docx
Run      : python scripts/tables/table_S30_health_belief_model.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S30."""
    H = R["H"]
    return ("Table S30", "Health Belief Model extension: health-belief proxies, service uptake and mortality",
                pd.DataFrame({"Outcome": H.Outcome, "Type": H.Type, "n": H.n.astype(str),
                              "C-C β (p)": [f"{_f(b_, 3)} ({_p(p)})" for b_, p in zip(H["C-C β"], H["C-C p"])],
                              "C-A β (p)": [f"{_f(b_, 3)} ({_p(p)})" for b_, p in zip(H["C-A β"], H["C-A p"])],
                              "X₂ β (p)": [f"{_f(b_, 3)} ({_p(p)})" for b_, p in zip(H["X₂ β"], H["X₂ p"])],
                              "X₂×C-C β (p)": [f"{_f(b_, 3)} ({_p(p)})" for b_, p in zip(H["X₂×C-C β"], H["X₂×C-C p"])],
                              "Adj. R²": H["Adj. R²"].map(lambda x: _f(x, 3))}),
                "Note: Standardised OLS, HC3 errors pooled over 20 imputations; controls: environmental deprivation (X₂), governance, ln GDP per capita and female schooling. Mortality outcomes are reversed so that positive coefficients mean better health. C-C proxies perceived benefits and trust; C-A proxies perceived barriers and low self-efficacy for women.", True)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
