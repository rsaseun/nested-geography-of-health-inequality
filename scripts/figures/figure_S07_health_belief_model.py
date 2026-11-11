#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S7. Health Belief Model extension: standardised associations of (a) health-cultural orientation and
(b) restrictive gender norms with service uptake (shaded) and mortality, net of environmental
deprivation, governance, income and schooling (95% confidence intervals; filled markers p <
0.05).

Output : outputs/figures/Figure_S7.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S07_health_belief_model.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def figS7_hbm(H, path):
    plt = set_style()
    fig, axes = plt.subplots(1, 2, figsize=(W2, W2 * 0.32), sharey=True)
    labs = [f"{o}" for o in H["Outcome"]]
    _forest(axes[0], labs, H["C-C β"], H["C-C se"], H["C-C p"], OKABE["green"])
    axes[0].set_title("(a) C-C Health-cultural orientation\n(perceived benefits, trust)", fontsize=7)
    _forest(axes[1], labs, H["C-A β"], H["C-A se"], H["C-A p"], OKABE["purple"])
    axes[1].set_title("(b) C-A Restrictive gender norms\n(perceived barriers, low self-efficacy)", fontsize=7)
    for ax in axes:
        ax.set_xlabel("Standardised coefficient (95% CI)")
        ax.axhspan(1.5, 4.5, color="#F2F7F5", zorder=0)
    axes[0].text(0.02, 0.97, "uptake", transform=axes[0].transAxes, fontsize=6, va="top", color="#2E7D63")
    axes[0].text(0.02, 0.06, "mortality", transform=axes[0].transAxes, fontsize=6, color="#555")
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S7")
    figS7_hbm(R["H"], path)
    print("Fig. S7:", path)


if __name__ == "__main__":
    main()
