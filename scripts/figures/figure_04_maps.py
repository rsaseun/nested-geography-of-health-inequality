#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 4. Geography of SDG 3 performance and environmental deprivation in 48 Sub-Saharan African countries
(most recent available values). (a) SDG3-PI; (b)–(e) its four dimensions, scored from 0 (worst
observed) to 100 (2030 target); (f) environmental deprivation (first principal component of
unsafe water, unsafe sanitation, polluting cooking fuel and ambient PM2.5; darker = more
deprived). Island states are drawn as discs. Each panel has its own colour scale. Map lines do
not necessarily depict accepted national boundaries.

Output : outputs/figures/Figure_4.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_04_maps.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig2_maps(ssa, context, D, K0, path):
    plt = set_style()
    fig, axes = plt.subplots(2, 3, figsize=(W2, W2 * 0.66))
    panels = [("SDG3-PI", D.loc[K0.index, "SDG3-PI"], "YlGnBu", "(a) SDG3-PI (0–100)"),
              ("Maternal health", D.loc[K0.index, "Maternal health"], "YlGnBu", "(b) Maternal health"),
              ("Child health", D.loc[K0.index, "Child health"], "YlGnBu", "(c) Child health"),
              ("Communicable disease", D.loc[K0.index, "Communicable disease"], "YlGnBu", "(d) Communicable disease"),
              ("UHC", D.loc[K0.index, "UHC"], "YlGnBu", "(e) Universal health coverage"),
              ("X2", K0["X2"], "OrRd", "(f) Environmental deprivation (X₂, PC score)")]
    for ax, (k, v, cm, t) in zip(axes.flat, panels):
        _basemap(ax, context)
        g = ssa.copy(); g["v"] = v.values
        g.plot(column="v", ax=ax, cmap=cm, edgecolor="white", linewidth=0.3, legend=True,
               legend_kwds={"orientation": "horizontal", "shrink": 0.62, "pad": 0.01, "aspect": 28})
        ax.set_title(t, fontsize=7.5)
        cb = ax.get_figure().axes[-1]; cb.tick_params(labelsize=6, width=0.4, length=2)
    fig.subplots_adjust(wspace=0.02, hspace=0.12)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_4")
    fig2_maps(R["SP"]["ssa"], R["SP"]["context"], R["D"], R["C"]["K0"], path)
    print("Fig. 4:", path)


if __name__ == "__main__":
    main()
