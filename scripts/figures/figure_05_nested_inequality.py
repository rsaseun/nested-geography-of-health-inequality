#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 5. Nested inequality. (a) Population-weighted Gini index of each SDG 3 indicator across countries,
coloured by dimension. (b) Share of the Theil T index lying between the two World Bank sub-
regions (orange) and between the five African Union regions (blue); the remainder lies between
countries within regions.

Output : outputs/figures/Figure_5.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_05_nested_inequality.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig3_inequality(ineq, path):
    plt = set_style()
    t = ineq[ineq.code != "SDG3PI"].copy()
    dim_of = {v: dim for dim, vs in DIMS.items() for v in vs}
    t["dim"] = t.code.map(dim_of)
    t = t.sort_values("Gini")
    fig, (a, b) = plt.subplots(1, 2, figsize=(W2, W2 * 0.45), gridspec_kw={"width_ratios": [1, 1.15], "wspace": 0.55})
    y = np.arange(len(t))
    a.barh(y, t["Gini"], color=[DIMCOL[x] for x in t.dim], height=0.68)
    a.set_yticks(y); a.set_yticklabels([s.split(" (")[0] for s in t.Indicator])
    a.set_xlabel("Population-weighted Gini index")
    for yi, g in zip(y, t["Gini"]):
        a.text(g + 0.008, yi, f"{g:.2f}", va="center", fontsize=6)
    from matplotlib.patches import Patch
    a.legend(handles=[Patch(color=c, label=k) for k, c in DIMCOL.items()], loc="lower right", fontsize=6)
    a.set_title("(a) Inequality between countries")
    t2 = t.sort_values("Between AU regions (% of T)")
    y2 = np.arange(len(t2))
    b.hlines(y2, t2["Between AFE/AFW (% of T)"], t2["Between AU regions (% of T)"], color="#BBBBBB", lw=1.2)
    b.scatter(t2["Between AFE/AFW (% of T)"], y2, color=OKABE["orange"], s=16, zorder=3, label="Between 2 World Bank sub-regions")
    b.scatter(t2["Between AU regions (% of T)"], y2, color=OKABE["blue"], s=16, zorder=3, label="Between 5 African Union regions")
    b.set_yticks(y2); b.set_yticklabels([s.split(" (")[0] for s in t2.Indicator])
    b.set_xlabel("Share of Theil T lying between regions (%)"); b.set_xlim(0, 75)
    b.legend(loc="lower right", fontsize=6)
    b.set_title("(b) Regional share of inequality")
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_5")
    fig3_inequality(R["ineq"], path)
    print("Fig. 5:", path)


if __name__ == "__main__":
    main()
