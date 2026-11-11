#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S4. Standardised cluster profiles: each bar is the cluster mean in standard deviations from the
48-country mean.

Output : outputs/figures/Figure_S4.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S04_cluster_profiles.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def figS4_cluster_profiles(profz, path):
    plt = set_style()
    fig, ax = plt.subplots(figsize=(W2, W2 * 0.36))
    feats = list(profz.columns); x = np.arange(len(feats)); w = 0.26
    for i, cl in enumerate(profz.index):
        ax.bar(x + (i - 1) * w, profz.loc[cl], w, color=CLUCOL[cl], label=CLUNAME[cl])
    ax.axhline(0, color="#555", lw=0.6)
    wrap = {"SDG3-PI": "SDG3-PI", "X₁ climate vulnerability": "X₁ climate\nvulnerability",
            "Health-system capacity (ln HW/10k)": "Health-system\ncapacity\n(ln HW/10k)",
            "C-A restrictive gender norms": "C-A restrictive\ngender norms", "C-B social cohesion": "C-B social\ncohesion",
            "C-C health-cultural orientation": "C-C health-\ncultural\norientation",
            "C-D cultural-ecological practice": "C-D cultural-\necological\npractice"}
    ax.set_xticks(x); ax.set_xticklabels([wrap.get(f, f) for f in feats], fontsize=6.3)
    ax.set_ylabel("Cluster mean (SD from 48-country mean)"); ax.legend(loc="upper right", fontsize=6.2)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S4")
    figS4_cluster_profiles(R["SP"]["profz"], path)
    print("Fig. S4:", path)


if __name__ == "__main__":
    main()
