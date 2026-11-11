#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 8. SDG3-PI against GDP per capita (log scale), coloured by cluster. The line and band show the
fitted income gradient and its 95% confidence interval. Labelled countries are the six largest
positive and negative deviants from the gradient.

Output : outputs/figures/Figure_8.png  (600 dpi, Elsevier 1.5-column (140 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_08_income_deviants.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig7_deviants(E, cluster, path):
    plt = set_style()
    import statsmodels.api as sm
    dv = E["dev"].copy(); dv["cluster"] = cluster.loc[dv.index]
    fig, ax = plt.subplots(figsize=(W15, W15 * 0.72))
    x = np.log(dv["GDP pc (PPP)"])
    fit = sm.OLS(dv["SDG3-PI"], sm.add_constant(x)).fit()
    xs = np.linspace(x.min(), x.max(), 100)
    pr = fit.get_prediction(sm.add_constant(xs)).summary_frame(alpha=0.05)
    ax.fill_between(np.exp(xs), pr.mean_ci_lower, pr.mean_ci_upper, color="#DDDDDD", lw=0)
    ax.plot(np.exp(xs), pr["mean"], color="#555", lw=0.9)
    for cl in [1, 2, 3]:
        s = dv[dv.cluster == cl]
        ax.scatter(s["GDP pc (PPP)"], s["SDG3-PI"], s=18, color=CLUCOL[cl], edgecolor="white", lw=0.4, label=f"Cluster {cl}", zorder=3)
    lab = list(dv.index[:6]) + list(dv.index[-6:])
    for c in lab:
        r = dv.loc[c]
        ax.annotate(c.replace("São Tomé and Príncipe", "São Tomé & P.").replace("Central African Republic", "CAR"),
                    (r["GDP pc (PPP)"], r["SDG3-PI"]), xytext=(4, 3 if r.Residual > 0 else -7), textcoords="offset points",
                    fontsize=5.8, color="#222")
    ax.set_xscale("log"); ax.set_xlabel("GDP per capita, PPP (log scale)"); ax.set_ylabel("SDG3-PI (0–100)")
    ax.set_xticks([1000, 2000, 5000, 10000, 20000, 40000]); ax.set_xticklabels(["1,000", "2,000", "5,000", "10,000", "20,000", "40,000"])
    ax.text(0.02, 0.97, f"Slope = {E['dev_info']['slope']:.1f} points per log unit; R² = {E['dev_info']['R2']:.2f}",
            transform=ax.transAxes, va="top", fontsize=6.5)
    ax.legend(loc="lower right", fontsize=6.5)
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_8")
    fig7_deviants(R["E"], R["SP"]["cluster"], path)
    print("Fig. 8:", path)


if __name__ == "__main__":
    main()
