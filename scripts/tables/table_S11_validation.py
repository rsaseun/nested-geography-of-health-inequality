#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table S11. Validation checks for constructs and alternative measures

Location : Supplementary Material
Inputs   : cached analysis results (Section 3 constructs)
Outputs  : outputs/tables/Table_S11.csv and outputs/tables_docx/Table_S11.docx
Run      : python scripts/tables/table_S11_validation.py   (from the repository root)

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
    """Return (label, title, DataFrame, note, landscape) for Table S11."""
    C = R["C"]
    return ("Table S11", "Validation checks for constructs and alternative measures",
                pd.DataFrame({"Check": C["val"].Check, "Value": C["val"].Value.map(lambda x: _f(x, 3))}), "", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
