#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S6. Exposure juncture: standardised association of each cultural construct with environmental
deprivation, controlling for ln GDP per capita and governance (95% confidence intervals; filled
markers p < 0.05).

Output : outputs/figures/Figure_S6.png  (600 dpi, Elsevier 1.5-column (140 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S06_exposure_juncture.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def figS6_exposure(M, path):
    plt = set_style()
    e = M["expo"]
    fig, ax = plt.subplots(figsize=(W15, W15 * 0.42))
    _forest(ax, list(e["Cultural construct"]), e["β on X₂"], e["s.e."], e["p"], OKABE["purple"])
    ax.set_xlabel("Standardised association with environmental deprivation (95% CI)")
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S6")
    figS6_exposure(R["M"], path)
    print("Fig. S6:", path)


if __name__ == "__main__":
    main()
