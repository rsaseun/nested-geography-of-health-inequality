#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 3. Data provenance and index robustness. (a) Status of each analysis variable in each country:
observed, structural zero (non-endemic malaria) or multiply imputed; variables are grouped by
framework construct and countries ordered by SDG3-PI. (b) Rank of each country on SDG3-PI (dots)
and the range of its rank across three alternative aggregations (equal weights, entropy weights,
arithmetic mean; bars).

Output : outputs/figures/Figure_3.png  (600 dpi, Elsevier double-column (190 mm) width)
Inputs : cached analysis results (created on first run from data/Study_Data_Sources_updated_v1.xlsx)
Run    : python scripts/figures/figure_03_provenance_robustness.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, figure_path  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (constants, labels, style)
from sdg3_nested_geography.core import _save, _basemap, _forest  # noqa: E402,F401  (shared plot helpers)

def fig_data_quality(orig, d, D, path):
    """Data provenance matrix (a) and index rank robustness (b) (Fig. 3)."""
    plt = set_style()
    from matplotlib.colors import ListedColormap
    groups = [("Y outcomes", ["MMR", "SBA", "ABR", "FP", "U5MR", "NMR", "DTP3", "STUNT", "HIV", "TB", "MAL_INC", "MAL_MORT", "SCI", "OOP"]),
              ("X₁ climate", ["ND_E", "ND_S", "ND_AC", "CH_E", "CH_S", "CH_AC", "TEMPANOM", "SPEI"]),
              ("X₂ deprivation", ["WATER_B", "SAN_SM", "CLEANFUEL", "PM25", "TREELOSS", "WASH_DEATHS"]),
              ("M poverty, system", ["POV", "POU_A", "CMNN_DALY", "PHYS", "NURSE"]),
              ("Z controls", ["GDPPC", "HEPC", "GOVEFF", "POLSTAB", "CORRUPT", "URBAN", "FSCH"]),
              ("C culture", ["SIGI", "DHSDEC", "SDG561", "CHILDMAR", "TRUST", "EXCL_EPR", "EXCL_VDEM", "ETHFRAC",
                             "VACCONF", "TRUSTDOC", "KINSHIP", "WATERCOLL"])]
    vars_ = [v for _, vs in groups for v in vs]
    order = D["SDG3-PI"].sort_values(ascending=False).index
    O = orig.loc[order, vars_]
    Dd = d.loc[order, vars_]
    status = np.where(O.notna(), 0, np.where(Dd.notna(), 1, 2))  # 0 observed, 1 structural zero / filled, 2 imputed
    fig = plt.figure(figsize=(W2, W2 * 0.98))
    gs = fig.add_gridspec(2, 1, height_ratios=[2.15, 1], hspace=0.42)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1])
    cmap = ListedColormap(["#2B5C8A", "#7FB3D5", "#E69F00"])
    a.imshow(status.T, aspect="auto", cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
    a.set_xticks(range(len(order))); a.set_xticklabels([c.replace("São Tomé and Príncipe", "São Tomé & P.").replace("Central African Republic", "CAR")
                                                     .replace("Congo, Dem. Rep.", "DR Congo") for c in order], rotation=90, fontsize=4.6)
    a.set_yticks(range(len(vars_))); a.set_yticklabels(vars_, fontsize=4.6)
    pos = 0
    for gname, vs in groups:
        if pos:
            a.axhline(pos - 0.5, color="white", lw=1.6)
        a.text(len(order) + 0.8, pos + len(vs) / 2 - 0.5, gname, fontsize=5.6, va="center", ha="left", fontweight="bold")
        pos += len(vs)
    a.spines[:].set_visible(False); a.tick_params(length=0)
    obs = (status == 0).mean() * 100
    n_imp = int((status == 2).sum()); n_sz = int((status == 1).sum())
    from matplotlib.patches import Patch
    a.legend(handles=[Patch(color="#2B5C8A", label=f"Observed ({obs:.1f}%)"), Patch(color="#7FB3D5", label=f"Structural zero ({n_sz})"),
                      Patch(color="#E69F00", label=f"Multiply imputed ({n_imp})")], loc="upper center",
             bbox_to_anchor=(0.5, 1.07), ncol=3, fontsize=6)
    a.set_title("(a) Data provenance: 52 analysis variables × 48 countries", pad=16)
    alts = ["SDG3-PI (equal weights)", "SDG3-PI (entropy weights)", "SDG3-PI (arithmetic)"]
    rk = pd.DataFrame({c: D[c].rank(ascending=False) for c in ["SDG3-PI"] + alts}).loc[order]
    x = np.arange(len(order))
    b.vlines(x, rk[alts].min(axis=1), rk[alts].max(axis=1), color="#E69F00", lw=2.2, alpha=0.8, label="Range across alternative aggregations")
    b.scatter(x, rk["SDG3-PI"], s=9, color="#2B5C8A", zorder=3, label="Rank on SDG3-PI")
    b.set_ylim(49.5, -0.5); b.set_yticks([1, 10, 20, 30, 40, 48]); b.set_xlim(-1, len(order))
    b.set_xticks(x); b.set_xticklabels(a.get_xticklabels(), rotation=90, fontsize=4.6)
    b.set_ylabel("Rank (1 = best)"); b.legend(loc="lower left", fontsize=6)
    b.set_title("(b) Index robustness: rank under alternative weighting and aggregation")
    _save(fig, path)


def main():
    R = load_results()
    path = figure_path("Figure_3")
    fig_data_quality(R["orig"], R["d"], R["D"], path)
    print("Fig. 3:", path)


if __name__ == "__main__":
    main()
