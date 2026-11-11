#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. S3. Mean SDG3-PI and dimension scores in Africa Eastern & Southern and Africa Western & Central (95%
confidence intervals). Welch t-test: *** p < 0.001, ** p < 0.01, * p < 0.05, n.s. not
significant.

Output : outputs/figures/Figure_S3.png  (600 dpi, Elsevier 1.5-column (140 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_S03_afe_afw.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def figS3_afe_afw(comp, path):
    plt = set_style()
    fig, ax = plt.subplots(figsize=(W15, W15 * 0.55))
    x = np.arange(len(comp)); w = 0.36
    ax.bar(x - w / 2, comp["AFE mean (n = 26)"], w, yerr=1.96 * comp["AFE SE"], color=OKABE["blue"], capsize=2,
           error_kw={"lw": 0.6}, label="Africa Eastern & Southern (n = 26)")
    ax.bar(x + w / 2, comp["AFW mean (n = 22)"], w, yerr=1.96 * comp["AFW SE"], color=OKABE["orange"], capsize=2,
           error_kw={"lw": 0.6}, label="Africa Western & Central (n = 22)")
    for i, r in comp.iterrows():
        p = r["Welch t p"]
        s = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
        top = max(r["AFE mean (n = 26)"] + 1.96 * r["AFE SE"], r["AFW mean (n = 22)"] + 1.96 * r["AFW SE"])
        ax.text(i, top + 2.5, s, ha="center", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels(comp["Measure"].str.replace("Communicable disease", "Communicable\ndisease"))
    ax.set_ylabel("Mean score (95% CI)"); ax.set_ylim(0, 85); ax.legend(loc="upper right", fontsize=6.5)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_S3")
    figS3_afe_afw(R["comp"], path)
    print("Fig. S3:", path)


if __name__ == "__main__":
    main()
