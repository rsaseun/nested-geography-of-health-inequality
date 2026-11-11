#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 2. Conceptual framework. Environmental risk (X) is linked to SDG 3 performance (Y) directly and
through social stratification (M), conditioned by institutional capacity and development
inequality (Z). The cultural mediation layer (C) acts at four junctures (1 exposure, 2
buffering, 3 conversion, 4 interpretation), and the Health Belief Model adds a fifth (5
appraisal), at which perceived susceptibility, severity, benefits and barriers, cues to action
and self-efficacy govern the uptake of services. Countries are nested in World Bank sub-regions
and African Union regions.

Output : outputs/figures/Figure_2.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_02_conceptual_framework.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig1_framework(path):
    """Conceptual framework with the cultural mediation layer and the Health Belief Model appraisal juncture."""
    plt = set_style()
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
    W, H = 100, 78
    fig = plt.figure(figsize=(W2, W2 * H / W))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    INK, MUT = "#1d1d1f", "#4d5157"
    P1, P2, CU, HB, GR = "#1f5f8b", "#b4521b", "#6a3d8f", "#00796b", "#8a8f96"
    F = {"env": ("#e6f0e3", "#4f7a45"), "str": ("#e4ebf3", "#3f5f80"), "out": ("#f7ecd4", "#9a7426"),
         "ins": ("#eeeeee", "#6b6b6b"), "cul": ("#efe7f5", "#6a3d8f"), "hbm": ("#e0f2ef", "#00796b")}
    fs = 5.6  # base font size at 190 mm

    def box(x, y, w, h, key, lw=0.8, r=0.8, z=2, fc=None):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                    fc=fc or F[key][0], ec=F[key][1], lw=lw, zorder=z))

    def txt(x, y, s, size=fs, weight="normal", color=INK, ha="center", style="normal", ls=1.2, z=6):
        ax.text(x, y, s, fontsize=size, fontweight=weight, color=color, ha=ha, va="center", fontstyle=style,
                linespacing=ls, zorder=z)

    def arrow(p0, p1, color=INK, lw=1.0, ls="-", rad=0.0, z=4):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>,head_length=0.45,head_width=0.22", mutation_scale=8,
                                     color=color, lw=lw, ls=ls, connectionstyle=f"arc3,rad={rad}", zorder=z,
                                     shrinkA=0, shrinkB=0))

    def badge(x, y, n, color):
        ax.add_patch(plt.Circle((x, y), 0.95, color=color, zorder=8))
        ax.text(x, y - 0.05, str(n), ha="center", va="center", fontsize=fs - 0.6, color="white", fontweight="bold", zorder=9)

    def lab(x, y, s, color, size=fs):
        ax.text(x, y, s, fontsize=size, color=color, ha="center", va="center", fontweight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

    ax.add_patch(Rectangle((0.6, 0.6), W - 1.2, H - 1.2, fc="none", ec=MUT, lw=0.6, ls=(0, (5, 3)), zorder=1))
    txt(W / 2, H - 2.4, "NESTED SOCIO-SPATIAL CONTEXT  ·  48 countries within 2 World Bank sub-regions (AFE / AFW) and "
        "5 African Union regions  ·  latest available values  ·  spatial dependence and typology",
        size=fs, weight="bold", color=MUT)
    box(19, 64.0, 62, 8.2, "ins")
    txt(50, 69.9, "INSTITUTIONAL CAPACITY AND DEVELOPMENT INEQUALITY  (Z)", size=fs + 0.8, weight="bold")
    txt(50, 66.5, "Government effectiveness · control of corruption · political stability · GDP per capita\n"
        "health expenditure per capita · health-worker density · urbanisation · female schooling", color=MUT)
    arrow((32, 64.0), (32, 56.6), color=GR, lw=0.8); arrow((68, 64.0), (68, 56.6), color=GR, lw=0.8)
    txt(50, 62.6, "conditions all paths (controls)", size=fs - 0.4, color=GR, style="italic")
    lx, ly = 2.0, 73.0
    txt(lx, ly, "Legend", weight="bold", ha="left")
    for i, (c, ls, lw, s) in enumerate([(P1, "-", 1.4, "Pathway 1: livelihood route"), (P2, "-", 1.4, "Pathway 2: burden route"),
                                        (GR, "-", 0.9, "Cross-paths / controls"), (CU, (0, (4, 2)), 1.1, "Cultural moderation"),
                                        (HB, (0, (4, 2)), 1.1, "Health-belief appraisal"), (INK, (0, (1, 1.6)), 1.0, "Direct effect / feedback")]):
        yy = ly - 1.75 * (i + 1)
        ax.plot([lx, lx + 3.2], [yy, yy], color=c, ls=ls, lw=lw, zorder=6)
        txt(lx + 3.8, yy, s, size=fs - 0.4, ha="left")
    txt(82.6, 73.0, "Theoretical anchors", weight="bold", ha="left")
    txt(82.6, 67.6, "Political ecology of health\nSocial determinants of health\nRelational geography of place\n"
        "PEN-3 cultural model\nHealth Belief Model\nThree delays model", size=fs - 0.4, ha="left", color=MUT, ls=1.3)
    for cx, s, col in [(15, "ENVIRONMENTAL RISK  (X)", F["env"][1]), (50, "SOCIAL STRATIFICATION  (M)", F["str"][1]),
                       (85, "UNEVEN SDG 3 ACHIEVEMENT  (Y)", F["out"][1])]:
        txt(cx, 60.6, s, size=fs + 0.8, weight="bold", color=col)
    box(3, 44.2, 24, 12.0, "env"); txt(15, 53.6, "X₁  Climate vulnerability", size=fs + 0.6, weight="bold")
    txt(15, 48.6, "Exposure + sensitivity\n+ adaptive-capacity deficit\nND-GAIN · CHRI · observed hazard", color=MUT)
    box(3, 29.6, 24, 12.0, "env"); txt(15, 39.0, "X₂  Environmental deprivation", size=fs + 0.6, weight="bold")
    txt(15, 34.0, "Unsafe water and sanitation\npolluting cooking fuels · ambient PM2.5\nJMP · WHO · GBD", color=MUT)
    box(38, 44.2, 24, 12.0, "str"); txt(50, 53.6, "M₁  Poverty", size=fs + 0.6, weight="bold")
    txt(50, 48.6, "Extreme poverty headcount\n($3.00/day, 2021 PPP)\nlivelihood disruption · food insecurity", color=MUT)
    box(38, 29.6, 24, 12.0, "str"); txt(50, 39.0, "M₂  Health-system pressure", size=fs + 0.6, weight="bold")
    txt(50, 34.0, "CMNN DALYs per health worker\nburden relative to capacity\nGBD · WHO NHWA", color=MUT)
    box(73, 29.6, 24, 26.6, "out", lw=1.0); txt(85, 53.6, "SDG 3 Performance Index", size=fs + 0.6, weight="bold")
    txt(85, 51.2, "(SDG3-PI, 0–100; distance to 2030)", color=MUT)
    for i, dname in enumerate(["Maternal health", "Child health", "Communicable disease", "Universal health coverage"]):
        yy = 47.6 - i * 3.5
        box(75.2, yy - 1.3, 19.6, 2.6, "out", lw=0.6, r=0.5, z=3, fc="white"); txt(85, yy, dname, z=7)
    txt(85, 32.0, "Nested inequality\nGini · Theil (between / within)", size=fs - 0.4, color=MUT, style="italic")
    arrow((27, 50.2), (38, 50.2), color=P1, lw=1.5); lab(32.5, 51.6, "a₁₁", P1)
    arrow((62, 48.2), (73, 48.2), color=P1, lw=1.5); lab(64.6, 49.6, "b₁", P1)
    arrow((27, 35.6), (38, 35.6), color=P2, lw=1.5); lab(35.4, 34.2, "a₂₂", P2)
    arrow((62, 35.6), (73, 35.6), color=P2, lw=1.5); lab(64.6, 34.2, "b₂", P2)
    arrow((27, 46.0), (38, 39.8), color=GR, lw=0.8); arrow((27, 39.8), (38, 46.0), color=GR, lw=0.8)
    lab(29.4, 43.6, "a₂₁", GR, size=fs - 0.4); lab(29.4, 41.0, "a₁₂", GR, size=fs - 0.4)
    arrow((50, 44.2), (50, 41.6), color=P1, lw=1.3); lab(52.2, 42.9, "d₂₁", P1)
    arrow((15, 56.2), (85, 56.2), color=INK, lw=0.9, ls=(0, (1, 1.6)), rad=-0.07); lab(50, 58.6, "c′₁, c′₂  direct effects", INK, size=fs - 0.4)
    arrow((73, 54.0), (62, 54.0), color=INK, lw=0.9, ls=(0, (1, 1.6)), rad=0.45); txt(67.5, 57.0, "feedback", size=fs - 0.6, style="italic")
    # cultural mediation layer (C) and the Health Belief Model box
    box(3, 3.0, 66.5, 18.6, "cul", lw=1.0)
    txt(36.25, 19.6, "CULTURAL MEDIATION LAYER  (C)  —  culture as constraint and resource (PEN-3)", size=fs + 0.6, weight="bold", color=CU)
    cults = [("A  Gender normative regime", "SIGI · women's health\ndecisions · SDG 5.6.1\nchild marriage"),
             ("B  Social cohesion & trust", "Afrobarometer trust\nethnic exclusion (EPR,\nV-Dem) · fractionalisation"),
             ("C  Health-cultural orientation", "Vaccine confidence\ntrust in doctors and\nnurses · religiosity"),
             ("D  Cultural-ecological practice", "Kinship and ancestral\nsubsistence · who\ncollects water")]
    cw, gp, x0 = 15.2, 0.9, 4.2
    for i, (h, b) in enumerate(cults):
        xx = x0 + i * (cw + gp)
        box(xx, 4.2, cw, 12.4, "cul", lw=0.6, r=0.6, z=3, fc="white")
        txt(xx + cw / 2, 14.4, h.replace("  ", "\n", 1) if len(h) > 24 else h, size=fs - 0.2, weight="bold", color=CU)
        txt(xx + cw / 2, 8.6, b, size=fs - 0.5, color=MUT, ls=1.25)
    box(73.0, 3.0, 24.0, 18.6, "hbm", lw=1.0)
    txt(84.75, 19.4, "HEALTH BELIEF MODEL", size=fs + 0.6, weight="bold", color=HB)
    txt(84.75, 17.2, "individual appraisal of risk and action", size=fs - 0.5, color=HB, style="italic")
    txt(84.75, 10.6, "Perceived susceptibility\nPerceived severity\nPerceived benefits\nPerceived barriers\n"
        "Cues to action · self-efficacy", size=fs - 0.3, color=MUT, ls=1.3)
    txt(84.75, 4.6, "→ care-seeking and uptake\n(immunisation, contraception, birth care)", size=fs - 0.6, color=HB, ls=1.2)
    arrow((69.5, 10.0), (73.0, 10.0), color=HB, lw=1.0, ls=(0, (4, 2)))
    txt(71.25, 13.2, "modifying\nfactors", size=fs - 1.4, color=HB, ls=1.0)
    for xf, yt, m in [(15.0, 29.6, 1), (32.5, 50.2, 2), (68.6, 48.2, 3), (66.0, 35.6, 4)]:
        arrow((xf, 21.6), (xf, yt), color=CU, lw=1.1, ls=(0, (4, 2)), z=5)
        ax.plot([xf], [yt], marker="o", ms=2.6, color=CU, zorder=8)
    arrow((90.5, 21.6), (90.5, 29.6), color=HB, lw=1.1, ls=(0, (4, 2)), z=5)
    ax.plot([90.5], [29.6], marker="o", ms=2.6, color=HB, zorder=8)
    for x, n, s, c, yy in [(7.0, 1, "Exposure", CU, 23.4), (21.4, 2, "Buffering (a₁₁)", CU, 23.4),
                           (51.8, 4, "Interpretation (b₂)", CU, 23.4), (71.6, 3, "Conversion (b₁)", CU, 23.4),
                           (78.6, 5, "Appraisal (uptake)", HB, 26.2)]:
        badge(x, yy, n, c)
        txt(x + 1.6, yy, s, size=fs - 0.2, color=c, weight="bold", ha="left")
    _save(fig, path)


def main():
    path = figure_path("Figure_2")
    fig1_framework(path)
    print("Fig. 2:", path)


if __name__ == "__main__":
    main()
