#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphical abstract. Graphical abstract: the pipeline, four system insights and the SDG3-PI map; 26 x 10 cm (at least
1328 x 531 px).

Output : outputs/figures/Graphical_Abstract.png  (600 dpi, Elsevier graphical-abstract width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/graphical_abstract.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def graphical_abstract_ih(SP, D, path):
    """Graphical abstract for Informatics and Health: pipeline (left to right) with the map and four system insights."""
    plt = set_style()
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    fig = plt.figure(figsize=(26 / 2.54, 10 / 2.54))
    fig.text(0.5, 0.955, "An auditable informatics pipeline for SDG 3 inequality across 48 Sub-Saharan African countries",
             ha="center", fontsize=11, fontweight="bold")
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.92]); ax.set_xlim(0, 100); ax.set_ylim(0, 40); ax.axis("off")

    def bx(x, y, w, h, fc, ec, head, body, fsz=7.2):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.9", fc=fc, ec=ec, lw=1.0))
        ax.text(x + w / 2, y + h - 2.2, head, ha="center", va="center", fontsize=fsz + 0.6, fontweight="bold", color=ec)
        ax.text(x + w / 2, y + (h - 3.6) / 2, body, ha="center", va="center", fontsize=fsz, linespacing=1.3, color="#1d1d1f")

    def ar(p0, p1, c="#1d1d1f"):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>,head_length=0.5,head_width=0.25", mutation_scale=9, color=c, lw=1.4))
    stages = [("Ingest", "72 fields\n18 sources\n18 logged\ndecisions"),
              ("Provenance", "97.7% cells\nobserved\n54 imputed\n(m = 20)"),
              ("Index engine", "14 indicators\nfixed goalposts\nsign-ruled\nPCA weights"),
              ("Analytics", "Theil · Moran\nk-means · OLS\nMI × bootstrap\nmediation")]
    x0, w, gap, y0, h = 1.0, 11.0, 2.2, 21.5, 14.5
    for i, (hd, bd) in enumerate(stages):
        x = x0 + i * (w + gap)
        bx(x, y0, w, h, "#E4EBF3" if i < 2 else ("#FBF1DC" if i == 2 else "#E6F0E3"), "#3f5f80" if i < 2 else ("#9a7426" if i == 2 else "#4f7a45"), hd, bd)
        if i:
            ar((x - gap, y0 + h / 2), (x, y0 + h / 2))
    ax.add_patch(FancyBboxPatch((1, 13.5), 4 * w + 3 * gap, 5.6, boxstyle="round,pad=0,rounding_size=0.9", fc="white", ec="#1d1d1f", lw=1.0))
    ax.text(1 + (4 * w + 3 * gap) / 2, 16.3, "Reproducibility: 36 table + 17 figure scripts · fixed seeds · clean rerun identical",
            ha="center", va="center", fontsize=7.0, fontweight="bold")
    ax.text(1, 11.2, "System insights", fontsize=8.2, fontweight="bold", va="center")
    ins = ["• Missingness clusters at both tails: complete cases would drop 16 of 48 countries",
           "• Mixed-sign loadings (HIV vs malaria) need a weighting guardrail; ranks robust (ρ ≥ 0.990)",
           "• Scale matters: sub-regions hold 45% of maternal-mortality but 28% of overall inequality",
           "• Climate indices disagree on exposure (r = −0.05): run alternative measures as modules"]
    ax.text(1, 9.0, "\n".join(ins), fontsize=6.9, va="top", linespacing=1.55)
    a = fig.add_axes([0.585, 0.06, 0.25, 0.80])
    _basemap(a, SP["context"])
    g = SP["ssa"].copy(); g["v"] = D.loc[g.country, "SDG3-PI"].values
    g.plot(column="v", ax=a, cmap="YlGnBu", edgecolor="white", linewidth=0.3, vmin=15, vmax=90)
    a.set_title("SDG3-PI (mean 46.4 of 100)", fontsize=8.5)
    sm_ = plt.cm.ScalarMappable(cmap="YlGnBu", norm=plt.Normalize(15, 90))
    cax = fig.add_axes([0.61, 0.07, 0.20, 0.022]); cb = fig.colorbar(sm_, cax=cax, orientation="horizontal")
    cb.ax.tick_params(labelsize=6.5); cb.set_label("0 = worst observed, 100 = 2030 target", fontsize=6.5)
    bx(86.5, 21.5, 13, 14.5, "#FBE3D6", OKABE["verm"], "Decision use", "deprivation\nβ = −0.58\ngovernance\nβ = +0.45")
    bx(86.5, 4.0, 13, 14.5, "#EDF6F3", "#00796b", "Targeting", "Sahel–Central\nlow cluster;\n2/3 of gaps\nwithin regions")
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Graphical_Abstract")
    graphical_abstract_ih(R["SP"], R["D"], path)
    print("Graphical abstract:", path)


if __name__ == "__main__":
    main()
