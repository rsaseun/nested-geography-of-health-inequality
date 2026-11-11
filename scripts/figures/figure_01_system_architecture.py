#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 1. System architecture of the open pipeline. Seventy-two fields from 18 families of international
sources pass through ingestion and rule-based screening, harmonisation, multiple imputation and
the index engine before feeding six analytic modules. A quality-assurance layer logs every
decision and check, and a reproducibility layer regenerates each table and figure from its own
script.

Output : outputs/figures/Figure_1.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_01_system_architecture.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig_architecture(path):
    """System architecture of the pipeline (Fig. 1)."""
    plt = set_style()
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    W, H = 100, 60
    fig = plt.figure(figsize=(W2, W2 * H / W))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    INK, MUT = "#1d1d1f", "#4d5157"
    fs = 5.8

    def box(x, y, w, h, fc, ec, lw=0.9):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.9", fc=fc, ec=ec, lw=lw))

    def txt(x, y, t, size=fs, weight="normal", color=INK, ha="center", style="normal", ls=1.25):
        ax.text(x, y, t, fontsize=size, fontweight=weight, color=color, ha=ha, va="center", fontstyle=style, linespacing=ls)

    def arrow(p0, p1, color=INK, lw=1.1, ls="-"):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>,head_length=0.45,head_width=0.22", mutation_scale=8,
                                     color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0))
    # sources
    box(1, 20, 15.5, 33, "#F2F2F2", "#7A7A7A")
    txt(8.75, 50.6, "SOURCES", size=fs + 0.6, weight="bold")
    txt(8.75, 48.4, "18 source families", size=fs - 0.4, color=MUT, style="italic")
    txt(8.75, 35.2, "WHO GHO · UN IGME\nUNAIDS · IHME GBD\nWorld Bank WDI, PIP,\nWGI, CCKP (CHRI)\nWHO/UNICEF JMP\n"
        "ND-GAIN · OECD SIGI\nAfrobarometer · DHS\nEPR · V-Dem · HIEF\nWellcome Global Monitor\nAncestral-traits data",
        size=fs - 0.6, color=MUT, ls=1.35)
    stages = [
        ("INGEST &\nSCREEN", "#E4EBF3", "#3f5f80", "72 fields mapped to\n13 constructs\nrule-based screening\nexclusion of circular\nfields (GII, HDI)"),
        ("HARMONISE", "#E4EBF3", "#3f5f80", "counts → rates\norientation\nstructural zeros\nsubstitution of\nsparse series"),
        ("IMPUTE", "#E4EBF3", "#3f5f80", "chained equations\nm = 20 posterior\ndraws\nRubin's rules\ndownstream"),
        ("INDEX\nENGINE", "#FBF1DC", "#9a7426", "fixed goalposts\nlog rule\nPCA weights +\nsign rule\ngeometric mean"),
    ]
    x0, w, gap = 20.5, 12.6, 2.2
    for i, (h, fc, ec, b) in enumerate(stages):
        x = x0 + i * (w + gap)
        box(x, 27, w, 26, fc, ec)
        txt(x + w / 2, 49.0, h, size=fs + 0.4, weight="bold", color=ec, ls=1.1)
        txt(x + w / 2, 36.0, b, size=fs - 0.5, color=MUT, ls=1.3)
        if i == 0:
            arrow((16.5, 40), (x, 40))
        else:
            arrow((x - gap, 40), (x, 40))
    xa = x0 + 4 * (w + gap)
    arrow((xa - gap, 40), (xa, 40))
    box(xa, 20, 100 - xa - 1, 33, "#E6F0E3", "#4f7a45")
    txt(xa + (99 - xa) / 2, 50.6, "ANALYTIC MODULES", size=fs + 0.6, weight="bold", color="#4f7a45")
    mods = ["Nested inequality (Gini, Theil)", "Spatial: Moran's I, LISA", "Typology: k-means + gap", "Regression: pooled HC3",
            "Mediation: MI × bootstrap", "Health Belief Model test"]
    for j, m in enumerate(mods):
        yy = 46.6 - j * 4.3
        box(xa + 1.2, yy - 1.6, 99 - xa - 3.4, 3.2, "white", "#4f7a45", lw=0.6)
        txt(xa + (99 - xa) / 2 - 0.5, yy, m, size=fs - 0.4)
    # QA lane
    box(20.5, 20, 4 * w + 3 * gap, 5.0, "#EFE7F5", "#6a3d8f")
    txt(20.5 + (4 * w + 3 * gap) / 2, 22.5, "QUALITY ASSURANCE & PROVENANCE\ndecision log · source appraisal · validation "
        "correlations · robustness of weights and aggregation", size=fs - 0.6, color="#6a3d8f", weight="bold")
    # outputs
    box(1, 2.5, 98, 13.5, "#FFFFFF", "#1d1d1f", lw=1.0)
    txt(50, 13.6, "REPRODUCIBILITY LAYER AND OUTPUTS", size=fs + 0.6, weight="bold")
    outs = [("Cached results", "one run → all scripts"), ("36 table scripts", "CSV + editable Word"),
            ("17 figure scripts", "600-dpi images"), ("results.json", "numbers quoted in text"), ("Open repository", "MIT licence, fixed seeds")]
    for k, (a, b) in enumerate(outs):
        xx = 3 + k * 19.2
        box(xx, 4.0, 17.6, 7.4, "#F7F7F7", "#7A7A7A", lw=0.6)
        txt(xx + 8.8, 8.9, a, size=fs, weight="bold"); txt(xx + 8.8, 6.1, b, size=fs - 0.6, color=MUT)
    arrow((xa + (99 - xa) / 2, 20), (xa + (99 - xa) / 2, 16.0))
    arrow((20.5 + 2 * (w + gap), 20), (20.5 + 2 * (w + gap), 16.0), color="#6a3d8f", lw=0.9, ls=(0, (3, 2)))
    txt(50, 57.6, "Open informatics pipeline for nested SDG 3 inequality analysis (48 countries)", size=fs + 1.2, weight="bold")
    _save(fig, path)


def main():
    path = figure_path("Figure_1")
    fig_architecture(path)
    print("Fig. 1:", path)


if __name__ == "__main__":
    main()
