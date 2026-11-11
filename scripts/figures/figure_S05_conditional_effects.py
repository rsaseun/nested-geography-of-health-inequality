#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S5. Conditional indirect effects at the 10th, 50th and 90th percentiles of each cultural construct
(95% bias-corrected intervals). Circles: burden pathway IE₂; squares: livelihood pathway IE₁;
filled markers exclude zero.

Output : outputs/figures/Figure_S5.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S05_conditional_effects.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def figS5_conditional(M, path):
    plt = set_style()
    fig, axes = plt.subplots(1, 4, figsize=(W2, W2 * 0.3), sharey=True)
    for ax, C in zip(axes, ["C_A", "C_B", "C_C", "C_D"]):
        t = M["mod"][C].set_index("Effect")
        for j, (pref, colr, mk, off) in enumerate([("IE₂", OKABE["verm"], "o", -0.12), ("IE₁", "#777777", "s", 0.12)]):
            for i, q in enumerate(["P10", "P50", "P90"]):
                r = t.loc[f"{pref}(C) at {q}"]
                ax.plot([i + off] * 2, [r["CI low"], r["CI high"]], color=colr, lw=0.9)
                ax.plot(i + off, r["Estimate"], mk, ms=3.6, color=colr if r["CI excludes 0"] == "Yes" else "white", mec=colr)
        ax.axhline(0, color="#999", lw=0.5, ls="--")
        ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["P10", "P50", "P90"]); ax.set_title(LABEL[C].replace(" ", "\n", 1), fontsize=6.8)
    axes[0].set_ylabel("Conditional indirect effect (95% BC CI)")
    axes[-1].plot([], [], "o", color=OKABE["verm"], label="IE₂ burden pathway")
    axes[-1].plot([], [], "s", color="#777", label="IE₁ livelihood pathway")
    axes[-1].legend(loc="lower right", fontsize=6)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S5")
    figS5_conditional(R["M"], path)
    print("Fig. S5:", path)


if __name__ == "__main__":
    main()
