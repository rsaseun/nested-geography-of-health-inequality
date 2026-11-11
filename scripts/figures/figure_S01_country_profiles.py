#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S1. Country profiles. Bars show SDG3-PI (shaded by World Bank sub-region); dots show the four
dimension scores. The dashed line marks the halfway point to the 2030 targets.

Output : outputs/figures/Figure_S1.png  (600 dpi, Elsevier 1.5-column (140 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S01_country_profiles.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def figS1_profiles(D, reg, path):
    plt = set_style()
    t = D.sort_values("SDG3-PI")
    fig, ax = plt.subplots(figsize=(W15, W15 * 1.55))
    y = np.arange(len(t))
    ax.barh(y, t["SDG3-PI"], color=["#BFD7EA" if reg.loc[c, "WB"] == "AFE" else "#F3D9B1" for c in t.index], height=0.72,
            edgecolor="none", zorder=1)
    for dim, cc in DIMCOL.items():
        ax.scatter(t[dim], y, s=7, color=cc, zorder=3, label=dim)
    ax.axvline(50, color="#666", lw=0.6, ls="--")
    ax.set_yticks(y); ax.set_yticklabels(t.index, fontsize=5.8)
    ax.set_xlabel("Score (0 = worst observed, 100 = 2030 target)"); ax.set_xlim(0, 101)
    from matplotlib.patches import Patch
    h = [Patch(color="#BFD7EA", label="SDG3-PI, AFE"), Patch(color="#F3D9B1", label="SDG3-PI, AFW")]
    h += [plt.Line2D([], [], marker="o", ls="", color=cc, label=k, ms=3.5) for k, cc in DIMCOL.items()]
    ax.legend(handles=h, loc="lower right", fontsize=6)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S1")
    figS1_profiles(R["D"], R["reg"], path)
    print("Fig. S1:", path)


if __name__ == "__main__":
    main()
