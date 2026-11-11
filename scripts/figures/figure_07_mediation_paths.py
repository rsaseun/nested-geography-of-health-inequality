#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 7. Estimated serial–parallel mediation system (standardised). Coloured arrows and asterisks mark
paths whose 95% bias-corrected bootstrap interval excludes zero (blue positive, vermilion
negative); grey arrows do not. Controls: ln GDP per capita, governance and female schooling.

Output : outputs/figures/Figure_7.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_07_mediation_paths.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig6_paths(M, path):
    plt = set_style()
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    t = M["base"].set_index("Effect")
    fig, ax = plt.subplots(figsize=(W2, W2 * 0.46)); ax.set_xlim(0, 100); ax.set_ylim(0, 46); ax.axis("off")
    nodes = {"X1": (4, 30, "X₁ Climate\nvulnerability"), "X2": (4, 6, "X₂ Environmental\ndeprivation"),
             "M1": (40, 30, "M₁ Poverty"), "M2": (40, 6, "M₂ Health-system\npressure"), "Y": (78, 18, "SDG3-PI")}
    bw, bh = 18, 9
    for k, (x, y, s) in nodes.items():
        ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc="#F4F6F8" if k != "Y" else "#FBF1DC", ec="#444", lw=0.8))
        ax.text(x + bw / 2, y + bh / 2, s, ha="center", va="center", fontsize=7.5, fontweight="bold")

    def edge(a, b, key, lab_xy, rad=0.0, side=(0, 0)):
        r = t.loc["path " + key]
        sig = r["CI excludes 0"] == "Yes"
        xa, ya, _ = nodes[a]; xb, yb, _ = nodes[b]
        p0 = (xa + bw, ya + bh / 2 + side[0]); p1 = (xb, yb + bh / 2 + side[1])
        if a == "M1" and b == "M2":
            p0, p1 = (xa + bw / 2, ya), (xb + bw / 2, yb + bh)
        colr = OKABE["verm"] if (sig and r["Estimate"] < 0) else (OKABE["blue"] if sig else "#A0A0A0")
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>,head_length=0.5,head_width=0.25", mutation_scale=9,
                                     color=colr, lw=2.0 if sig else 0.9, connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1))
        names = {"a11": "a₁₁", "a12": "a₁₂", "a21": "a₂₁", "a22": "a₂₂", "d21": "d₂₁",
                 "b1": "b₁", "b2": "b₂", "c1": "c′₁", "c2": "c′₂"}
        ax.text(*lab_xy, f"{names[key]} = {r['Estimate']:.2f}{'*' if sig else ''}\n[{r['CI low']:.2f}, {r['CI high']:.2f}]",
                ha="center", va="center", fontsize=6.2, color=colr if sig else "#555",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    edge("X1", "M1", "a11", (31, 37.4))
    edge("X2", "M2", "a22", (31, 13.4))
    edge("X1", "M2", "a21", (26.2, 27.3), side=(-3, 2))
    edge("X2", "M1", "a12", (26.2, 17.7), side=(3, -2))
    edge("M1", "M2", "d21", (54.2, 22.5))
    edge("M1", "Y", "b1", (69, 31.5))
    edge("M2", "Y", "b2", (69, 9.0))

    def direct(key, xa, ya, yr, yb_end, lab_y):  # orthogonal route outside the boxes
        r = t.loc["path " + key]
        sig = r["CI excludes 0"] == "Yes"
        colr = OKABE["verm"] if (sig and r["Estimate"] < 0) else (OKABE["blue"] if sig else "#A0A0A0")
        lw = 2.0 if sig else 0.9
        xe = nodes["Y"][0] + bw - 3
        ax.plot([xa, xa, xe], [ya, yr, yr], color=colr, lw=lw, solid_capstyle="butt")
        ax.add_patch(FancyArrowPatch((xe, yr), (xe, yb_end), arrowstyle="-|>,head_length=0.5,head_width=0.25",
                                     mutation_scale=9, color=colr, lw=lw, shrinkA=0, shrinkB=1))
        nm = {"c1": "c\u2032\u2081", "c2": "c\u2032\u2082"}[key]
        ax.text(50, lab_y, f"{nm} = {r['Estimate']:.2f}{'*' if sig else ''}  [{r['CI low']:.2f}, {r['CI high']:.2f}]  (direct)",
                ha="center", va="center", fontsize=6.2, color=colr if sig else "#555",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    direct("c1", nodes["X1"][0] + bw / 2, nodes["X1"][1] + bh, 43.0, nodes["Y"][1] + bh, 43.0)
    direct("c2", nodes["X2"][0] + bw / 2, nodes["X2"][1], 2.2, nodes["Y"][1], 2.2)
    ie1, ie2 = t.loc["IE₁ livelihood pathway"], t.loc["IE₂ burden pathway"]
    tot = t.loc["X₂ total effect"]
    ax.text(61.5, 41.8, f"IE₁ livelihood = {ie1['Estimate']:.3f} [{ie1['CI low']:.3f}, {ie1['CI high']:.3f}]\n"
            f"IE₂ burden = {ie2['Estimate']:.3f} [{ie2['CI low']:.3f}, {ie2['CI high']:.3f}]\n"
            f"X₂ total effect = {tot['Estimate']:.3f} [{tot['CI low']:.3f}, {tot['CI high']:.3f}]",
            ha="left", va="top", fontsize=6.3, linespacing=1.4)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_7")
    fig6_paths(R["M"], path)
    print("Fig. 7:", path)


if __name__ == "__main__":
    main()
