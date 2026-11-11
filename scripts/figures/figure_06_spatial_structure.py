#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 6. Spatial structure of SDG 3 performance. (a) Moran scatterplot of SDG3-PI against its spatial lag
(weights: queen contiguity united with four nearest neighbours); outlined points are significant
local clusters. (b) Local indicators of spatial association (p < 0.05, 9,999 permutations). (c)
Health–environment–culture typology from k-means clustering. Map lines do not necessarily depict
accepted national boundaries.

Output : outputs/figures/Figure_6.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_06_spatial_structure.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig4_spatial(SP, path):
    plt = set_style()
    from matplotlib.patches import Patch
    ssa, context = SP["ssa"], SP["context"]
    fig = plt.figure(figsize=(W2, W2 * 0.38))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1.2, 1.2], wspace=0.12)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1]); c = fig.add_subplot(gs[2])
    sig = ssa.LISA != "Not significant"
    col = {"High–High": OKABE["blue"], "Low–Low": OKABE["verm"], "High–Low": OKABE["sky"],
           "Low–High": "#F4A582", "Not significant": "#D5D8DC"}
    a.scatter(ssa.z[~sig], ssa.lag_z[~sig], s=10, color="#AAAAAA", edgecolor="none")
    a.scatter(ssa.z[sig], ssa.lag_z[sig], s=16, color=[col[x] for x in ssa.LISA[sig]], edgecolor="k", lw=0.3)
    m, k = np.polyfit(ssa.z, ssa.lag_z, 1)
    xx = np.linspace(ssa.z.min(), ssa.z.max(), 10); a.plot(xx, m * xx + k, color=OKABE["ink"], lw=0.8)
    a.axhline(0, color="#999", lw=0.4); a.axvline(0, color="#999", lw=0.4)
    I = SP["moran"].set_index("Variable").loc["SDG3-PI"]
    mi_val, mi_p = I["Moran's I"], I["p (9,999 permutations)"]
    a.text(0.03, 0.97, f"Moran's I = {mi_val:.3f}\np = {mi_p:.3f}", transform=a.transAxes, va="top", fontsize=6.5)
    a.set_xlabel("SDG3-PI (z)"); a.set_ylabel("Spatial lag of SDG3-PI (z)"); a.set_title("(a) Moran scatterplot")
    _basemap(b, context)
    for cat, cc in col.items():
        sub = ssa[ssa.LISA == cat]
        if len(sub):
            sub.plot(ax=b, color=cc, edgecolor="white", linewidth=0.3)
    b.legend(handles=[Patch(color=cc, label=f"{k_} ({(ssa.LISA == k_).sum()})") for k_, cc in col.items() if (ssa.LISA == k_).sum()],
             loc="lower left", fontsize=5.8, handlelength=1.0, borderaxespad=0.0)
    b.set_title("(b) LISA clusters (p < 0.05)")
    _basemap(c, context)
    for cl in sorted(ssa.cluster.unique()):
        ssa[ssa.cluster == cl].plot(ax=c, color=CLUCOL[cl], edgecolor="white", linewidth=0.3)
    c.legend(handles=[Patch(color=CLUCOL[cl], label=f"Cluster {cl} (n = {(ssa.cluster == cl).sum()})") for cl in sorted(ssa.cluster.unique())],
             loc="lower left", fontsize=5.8, handlelength=1.0, borderaxespad=0.0)
    c.set_title(f"(c) Typology (k-means, k = {SP['k']})")
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_6")
    fig4_spatial(R["SP"], path)
    print("Fig. 6:", path)


if __name__ == "__main__":
    main()
