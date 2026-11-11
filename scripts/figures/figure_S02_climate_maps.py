#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S2. (a) Climate vulnerability (ND-GAIN composite); (b) recent annual temperature anomaly (°C); (c)
tree-cover loss 2000–2025 (% of 2000 cover). Map lines do not necessarily depict accepted
national boundaries.

Output : outputs/figures/Figure_S2.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S02_climate_maps.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def figS2_climate_maps(ssa, context, K0, path):
    plt = set_style()
    fig, axes = plt.subplots(1, 3, figsize=(W2, W2 * 0.36))
    for ax, (v, cm, t) in zip(axes, [("X1", "PuRd", "(a) Climate vulnerability (ND-GAIN)"),
                                     ("TEMPANOM", "YlOrRd", "(b) Temperature anomaly (°C)"),
                                     ("TREELOSS", "YlGn", "(c) Tree-cover loss (%)")]):
        _basemap(ax, context)
        g = ssa.copy(); g["v"] = K0[v].values
        g.plot(column="v", ax=ax, cmap=cm, edgecolor="white", linewidth=0.3, legend=True,
               legend_kwds={"orientation": "horizontal", "shrink": 0.62, "pad": 0.01, "aspect": 28})
        ax.set_title(t, fontsize=7.2)
        fig.axes[-1].tick_params(labelsize=6, width=0.4, length=2)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S2")
    figS2_climate_maps(R["SP"]["ssa"], R["SP"]["context"], R["C"]["K0"], path)
    print("Fig. S2:", path)


if __name__ == "__main__":
    main()
