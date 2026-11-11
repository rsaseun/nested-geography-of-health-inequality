#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S8. Standardised coefficients (95% confidence intervals) for SDG3-PI from model (2), with structural
controls, and model (6), adding the four cultural constructs. Filled markers: p < 0.05. HC3
errors pooled across 20 imputations.

Output : outputs/figures/Figure_S8.png  (600 dpi, Elsevier 1.5-column (140 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S08_coefficients.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig5_forest(E, path):
    plt = set_style()
    t2, _, _ = E["res"]["(2) + structural controls Z"]
    t6, _, _ = E["res"]["(6) + cultural constructs"]
    order = ["X2", "M1", "X1", "lnHEPC", "URBAN", "lnGDP", "GOV", "FSCH", "C_A", "C_B", "C_C", "C_D"]
    fig, ax = plt.subplots(figsize=(W15, W15 * 0.78))
    y = np.arange(len(order))[::-1]
    for t, off, colr, lab in [(t2, 0.17, OKABE["blue"], "Model (2): + structural controls"),
                              (t6, -0.17, OKABE["orange"], "Model (6): + cultural constructs")]:
        for yi, v in zip(y, order):
            if v not in t.index:
                continue
            b_, se, p = t.loc[v, ["beta", "se", "p"]]
            ax.plot([b_ - 1.96 * se, b_ + 1.96 * se], [yi + off] * 2, color=colr, lw=1.1)
            ax.plot(b_, yi + off, "o", ms=4, color=colr if p < 0.05 else "white", mec=colr, mew=1)
        ax.plot([], [], "o-", color=colr, label=lab, ms=4)
    ax.axvline(0, color="#777", lw=0.6, ls="--")
    ax.set_yticks(y); ax.set_yticklabels([LABEL[v] for v in order])
    ax.set_xlabel("Standardised coefficient (95% CI)")
    ax.legend(loc="upper right", fontsize=6.5)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S8")
    fig5_forest(R["E"], path)
    print("Fig. S8:", path)


if __name__ == "__main__":
    main()
