#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sdg3_nested_geography.core
==========================

Shared library for the repository "Nested geography of health inequality: environmental
deprivation, development inequality and the uneven pursuit of SDG 3 across Sub-Saharan Africa".

It holds the analysis (Sections 1-8) and the helpers that the table and figure scripts share
(plot style, map base layer, number formatting and the Word table writer). Each manuscript
table and figure has its own script in scripts/tables and scripts/figures.

    Section 1  Data screening and cleaning
    Section 2  SDG 3 Performance Index (SDG3-PI)
    Section 3  Explanatory constructs and multiple imputation
    Section 4  Nested inequality (Gini, Theil decomposition)
    Section 5  Spatial dependence and typology
    Section 6  Econometric models and income deviants
    Section 7  Moderated serial-parallel mediation
    Section 8  Health Belief Model extension
    run_analysis()  runs Sections 1-8 and returns one results dictionary
"""
from __future__ import annotations

import argparse
import json
import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
pd.set_option("display.width", 250)

# =============================================================================
# 0. Configuration shared by all stages
# =============================================================================
AFE = ["Angola", "Burundi", "Botswana", "Congo, Dem. Rep.", "Comoros", "Eritrea", "Ethiopia", "Kenya",
       "Lesotho", "Madagascar", "Mozambique", "Mauritius", "Malawi", "Namibia", "Rwanda", "Sudan", "Somalia",
       "South Sudan", "São Tomé and Príncipe", "Eswatini", "Seychelles", "Tanzania", "Uganda", "South Africa",
       "Zambia", "Zimbabwe"]
AU = {
    "Central": ["Burundi", "Cameroon", "Central African Republic", "Chad", "Congo, Rep.", "Congo, Dem. Rep.",
                "Equatorial Guinea", "Gabon", "São Tomé and Príncipe"],
    "Eastern": ["Comoros", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Mauritius", "Rwanda", "Seychelles",
                "Somalia", "South Sudan", "Sudan", "Tanzania", "Uganda"],
    "Northern": ["Mauritania"],
    "Southern": ["Angola", "Botswana", "Eswatini", "Lesotho", "Malawi", "Mozambique", "Namibia", "South Africa",
                 "Zambia", "Zimbabwe"],
    "Western": ["Benin", "Burkina Faso", "Cabo Verde", "Côte d'Ivoire", "Gambia, The", "Ghana", "Guinea",
                "Guinea-Bissau", "Liberia", "Mali", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo"],
}


def wb_region(c):
    """World Bank sub-region: Africa Eastern & Southern (AFE) or Western & Central (AFW)."""
    return "AFE" if c in AFE else "AFW"


def au_region(c):
    for k, v in AU.items():
        if c in v:
            return k
    raise KeyError(c)


DIMS = {
    "Maternal health": ["MMR", "SBA", "ABR", "FP"],
    "Child health": ["U5MR", "NMR", "DTP3", "STUNT"],
    "Communicable disease": ["HIV", "TB", "MAL_INC", "MAL_MORT"],
    "UHC": ["SCI", "OOP"],
}
LABEL = {  # readable names used in tables and figures
    "MMR": "Maternal mortality ratio", "SBA": "Skilled birth attendance", "ABR": "Adolescent birth rate",
    "FP": "FP demand satisfied (modern)", "U5MR": "Under-5 mortality", "NMR": "Neonatal mortality",
    "DTP3": "DTP3 coverage", "STUNT": "Stunting", "HIV": "HIV incidence", "TB": "TB incidence",
    "MAL_INC": "Malaria incidence", "MAL_MORT": "Malaria mortality", "SCI": "UHC service coverage index",
    "OOP": "Out-of-pocket share",
    "Y": "SDG3-PI", "X1": "X₁ Climate vulnerability (ND-GAIN)", "X2": "X₂ Environmental deprivation",
    "M1": "M₁ Poverty", "M2": "M₂ Health-system pressure", "lnHEPC": "ln health expenditure pc",
    "URBAN": "Urban share", "lnGDP": "ln GDP pc", "GOV": "Governance", "FSCH": "Female schooling",
    "X1_HAZ": "X₁ Observed hazard (temperature + drought)", "X1_CHRI": "X₁ Climate vulnerability (CHRI)",
    "X1_EXP": "X₁ ND-GAIN exposure", "X1_TEMP": "X₁ Temperature anomaly", "TREELOSS": "Tree-cover loss 2000–2025",
    "ND_E": "ND-GAIN exposure", "ND_S": "ND-GAIN sensitivity", "ND_AC": "ND-GAIN capacity deficit",
    "C_A": "C-A Restrictive gender norms", "C_B": "C-B Social cohesion & trust",
    "C_C": "C-C Health-cultural orientation", "C_D": "C-D Cultural-ecological practice",
}


def ensure(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return Path(path)


# =============================================================================
# 1. Data screening and cleaning  (Table S1)
# =============================================================================
COLMAP = {
    "Maternal mortality ratio (SDG 3.1.1)": "MMR", "Skilled birth attendance (3.1.2)": "SBA",
    "Adolescent birth rate (3.7.2);": "ABR",
    "Demand for family planning satisfied by modern methods (3.7.1)": "FP",
    "Under-5 mortality (3.2.1)": "U5MR", "Neonatal mortality (3.2.2)": "NMR",
    "DTP3 immunisation (3.b.1)": "DTP3", "MCV1 immunisation (3.b.1)": "MCV1", "Stunting (2.2.1)": "STUNT",
    "HIV incidence (3.3.1)": "HIV", "TB incidence (3.3.2)": "TB", "Malaria incidence (3.3.3)": "MAL_INC",
    "Malaria mortality rate": "MAL_MORT", "UHC service coverage index (3.8.1)": "SCI",
    "Financial hardship in health and components (3.8.2, 2024 definition) >10% of total budget on health (%)": "FINHARD",
    "Out-of-pocket (OOP) share of current health expenditure": "OOP",
    "Safely managed drinking water (6.1.1) - at least basic drinking water": "WATER_B",
    "Safely managed sanitation (6.2.1a)": "SAN_SM", "Clean cooking fuels (7.1.2)": "CLEANFUEL",
    "Ambient PM2.5": "PM25", "Tree-cover loss (%) - 2000-2025": "TREELOSS",
    "Recent Annual Temperature Anomaly (°C)": "TEMPANOM", "Drought (SPEI)": "SPEI",
    "ND-GAIN Exposure": "ND_E", "ND-GAIN Sensitivity": "ND_S", "ND-GAIN Adaptive capacity": "ND_AC",
    "CHRI Exposure": "CH_E", "CHRI Sensitivity": "CH_S", "CHRI Adaptive capacity": "CH_AC",
    "Communicable, maternal, neonatal and nutritional (CMNN) DALYs": "CMNN_DALY",
    "Air Pollution Mortality (3.9.1)": "AP_MORT", "Unsafe WASH Mortality (3.9.2)": "WASH_DEATHS",
    "GDP per capita (PPP)": "GDPPC", "Extreme poverty ($3.00/day, 2021 PPP); ": "POV_A", "Gini": "GINI",
    "Unemployment": "UNEMP", "Government expenditure (% GDP)": "GOVEXP",
    "Prevalence of undernourishment (2.1.1)": "POU_A", "Moderate or severe food insecurity (2.1.2)": "FIES",
    "Population growth": "POPGROW", "Fertility": "TFR", "Urban share": "URBAN", "Density": "DENSITY",
    "Age dependency": "AGEDEP", "Demographic (in millions)": "POP_M",
    "Female mean years of schooling": "FSCH_A", "Female labour-force participation": "FLFP_A",
    "Gender Inequality Index": "GII", "HDI": "HDI", "Government effectiveness index": "GOVEFF",
    "Political stability": "POLSTAB", "Control of corruption": "CORRUPT",
    "Health expenditure per capita": "HEPC", " Physicians per 10,000": "PHYS",
    "Nurses & midwives per 10,001": "NURSE", "Extreme poverty headcount ($3.00/day, 2021 PPP)": "POV",
    "Prevalence of undernourishment (2.1.1).1": "POU_B", "Female mean years of schooling (years)": "FSCH",
    "Female labour-force participation.1": "FLFP", "Social Institutions and Gender Index (SIGI) 2023": "SIGI",
    "DHS women's health-decision participation": "DHSDEC",
    "SDG 5.6.1 - women aged 15–49 (married or in a union) who make their own informed decisions regarding sexual relations, contraceptive use, and reproductive health care": "SDG561",
    "Child marriage - SDG 5.3.1": "CHILDMAR",
    "Interpersonal and institutional trust (incl. health services)": "TRUST",
    "Politically excluded population share": "EXCL_EPR", "Exclusion by social group": "EXCL_VDEM",
    "Ethnic fractionalisation": "ETHFRAC", "Vaccine confidence (safety, effectiveness, importance)": "VACCONF",
    "Trust in doctors, nurses and scientists": "TRUSTDOC", "Religious composition and religiosity": "RELIG",
    "Kinship intensity, matrilineality, ancestral subsistence mode": "KINSHIP",
    "Share of households where women or girls collect water": "WATERCOLL",
}
CONSTRUCT_MAP = {  # code: (workbook heading, framework construct, assessment)
    "MMR": ("Maternal health", "Y – Maternal health", "Fit"), "SBA": ("Maternal health", "Y – Maternal health", "Fit"),
    "ABR": ("Maternal health", "Y – Maternal health", "Fit"), "FP": ("Maternal health", "Y – Maternal health", "Fit"),
    "U5MR": ("Child health", "Y – Child health", "Fit"), "NMR": ("Child health", "Y – Child health", "Fit"),
    "DTP3": ("Child health", "Y – Child health", "Fit"), "MCV1": ("Child health", "Not used", "Redundant with DTP3"),
    "STUNT": ("Child health", "Y – Child health", "Fit"), "HIV": ("Communicable disease", "Y – Communicable", "Fit"),
    "TB": ("Communicable disease", "Y – Communicable", "Fit"), "MAL_INC": ("Communicable disease", "Y – Communicable", "Fit; structural zeros"),
    "MAL_MORT": ("Communicable disease", "Y – Communicable", "Fit"), "SCI": ("Universal health coverage", "Y – UHC", "Fit"),
    "FINHARD": ("Universal health coverage", "Descriptive only", "Fit"), "OOP": ("Universal health coverage", "Y – UHC", "Fit"),
    "WATER_B": ("Environmental deprivation", "X₂", "Fit (at least basic service)"), "SAN_SM": ("Environmental deprivation", "X₂", "Fit"),
    "CLEANFUEL": ("Environmental deprivation", "X₂", "Fit"), "PM25": ("Environmental deprivation", "X₂", "Fit"),
    "TREELOSS": ("Environmental deprivation", "Land degradation (robustness)", "Fit"),
    "TEMPANOM": ("Environmental deprivation", "X₁ observed hazard (robustness)", "Fit"),
    "SPEI": ("Environmental deprivation", "X₁ observed hazard (robustness)", "Fit"),
    "ND_E": ("Climate-health vulnerability", "X₁ (exposure)", "Fit"), "ND_S": ("Climate-health vulnerability", "X₁ (sensitivity)", "Fit"),
    "ND_AC": ("Climate-health vulnerability", "X₁ (capacity deficit)", "Fit"),
    "CH_E": ("Climate-health vulnerability", "X₁ robustness (CHRI)", "Fit (banded)"),
    "CH_S": ("Climate-health vulnerability", "X₁ robustness (CHRI)", "Fit (embeds health status)"),
    "CH_AC": ("Climate-health vulnerability", "X₁ robustness (CHRI)", "Fit (banded)"),
    "CMNN_DALY": ("Burden of disease", "M₂ numerator", "Fit"), "AP_MORT": ("Burden of disease", "Not used (outcome-like)", "Fit"),
    "WASH_DEATHS": ("Burden of disease", "X₂ validation (as rate)", "Counts converted to rate"),
    "GDPPC": ("Economic conditions", "Z", "Fit"), "POV_A": ("Economic conditions", "M₁ (duplicate)", "Duplicate"),
    "GINI": ("Economic conditions", "Descriptive", "Fit"), "UNEMP": ("Economic conditions", "Descriptive", "Fit"),
    "GOVEXP": ("Economic conditions", "Descriptive", "Fit"), "POU_A": ("Food security", "M₁ (second indicator)", "Fit"),
    "FIES": ("Food security", "Descriptive", "Fit"), "POPGROW": ("Gender and social inequality", "Z – demographic", "Mis-grouped"),
    "TFR": ("Gender and social inequality", "Z – demographic", "Mis-grouped"), "URBAN": ("Gender and social inequality", "Z", "Mis-grouped"),
    "DENSITY": ("Gender and social inequality", "Z – demographic", "Mis-grouped"), "AGEDEP": ("Gender and social inequality", "Z – demographic", "Mis-grouped"),
    "POP_M": ("Gender and social inequality", "Population weights", "Mis-grouped"),
    "FSCH_A": ("Gender and social inequality", "Not used", "Label/value mismatch"), "FLFP_A": ("Gender and social inequality", "Not used", "Duplicate"),
    "GII": ("Gender and social inequality", "Removed", "Circular with Y"), "HDI": ("Gender and social inequality", "Removed", "Circular with Y"),
    "GOVEFF": ("Institutional capacity", "Z (governance)", "Fit"), "POLSTAB": ("Institutional capacity", "Z (governance)", "Fit"),
    "CORRUPT": ("Institutional capacity", "Z (governance)", "Fit"), "HEPC": ("Institutional capacity", "Z", "Fit (current US$)"),
    "PHYS": ("Institutional capacity", "M₂ denominator", "Fit"), "NURSE": ("Institutional capacity", "M₂ denominator", "Fit"),
    "POV": ("Poverty", "M₁", "Fit"), "POU_B": ("Poverty", "Not used", "Duplicate"), "FSCH": ("Gender structure", "Z", "Fit"),
    "FLFP": ("Gender structure", "Z", "Fit"), "SIGI": ("Gender structure", "C-A", "Fit"),
    "DHSDEC": ("Gender structure", "C-A", "Fit (DHS countries)"), "SDG561": ("Gender structure", "C-A", "Fit (DHS countries)"),
    "CHILDMAR": ("Gender structure", "C-A", "Fit"), "TRUST": ("Social cohesion & trust", "C-B", "Fit"),
    "EXCL_EPR": ("Social cohesion & trust", "C-B", "Fit"), "EXCL_VDEM": ("Social cohesion & trust", "C-B", "Fit"),
    "ETHFRAC": ("Social cohesion & trust", "C-B", "Fit"), "VACCONF": ("Health-cultural orientation", "C-C", "Fit"),
    "TRUSTDOC": ("Health-cultural orientation", "C-C", "Fit"), "RELIG": ("Health-cultural orientation", "Descriptive", "Does not load with C-C"),
    "KINSHIP": ("Cultural-ecological practice", "C-D", "Fit"), "WATERCOLL": ("Cultural-ecological practice", "C-D", "Fit"),
}


def stage1_clean(xlsx):
    raw = pd.read_excel(xlsx, sheet_name="Data Composites", header=1).dropna(how="all")
    raw = raw.set_index("Country Name")
    num = raw.apply(pd.to_numeric, errors="coerce")
    num.index = [i.replace("’", "'") for i in num.index]
    d = num.rename(columns=COLMAP)[list(COLMAP.values())]
    screen = []

    def flag(var, issue, action):
        screen.append({"Variable": var, "Issue found": issue, "Action taken": action})

    d = d.drop(index="Djibouti")
    orig = d.copy()
    flag("Sample", "Djibouti listed; the World Bank classifies it outside Sub-Saharan Africa", "Excluded; n = 48")
    flag("WATER_B", "Column holds 'at least basic' drinking water (safely managed missing for many countries); "
         f"corrected values verified (Equatorial Guinea {d.loc['Equatorial Guinea','WATER_B']:.1f}%, "
         f"São Tomé and Príncipe {d.loc['São Tomé and Príncipe','WATER_B']:.1f}%)", "Used as the water indicator")
    flag("TREELOSS", f"Cumulative tree-cover loss 2000–2025, % of 2000 cover ({d.TREELOSS.min():.1f}–{d.TREELOSS.max():.1f})",
         "Tested as land degradation (robustness)")
    flag("TEMPANOM, SPEI", f"Recent annual temperature anomaly in °C ({d.TEMPANOM.min():.1f}–{d.TEMPANOM.max():.1f}) and drought index",
         "Combined into an observed-hazard alternative for X₁")
    for c in ["Lesotho", "Mauritius", "Seychelles"]:
        if pd.isna(d.loc[c, "MAL_INC"]):
            d.loc[c, "MAL_INC"] = 0.0
    flag("MAL_INC", "Blank for Lesotho, Mauritius and Seychelles (non-endemic)", "Set to 0 (structural zero)")
    d["WASH_RATE"] = d["WASH_DEATHS"] / (d["POP_M"] * 1e6) * 1e5
    flag("WASH_DEATHS", "Absolute number of deaths, not a rate", "Converted to deaths per 100,000; validation of X₂ only")
    d["POV"] = d["POV"].fillna(d["POV_A"])
    flag("POV_A / POV", "Duplicate poverty columns", "POV used; gaps filled from POV_A")
    flag("POU_A / POU_B", "Duplicate undernourishment columns (identical)", "POU_A used")
    flag("FINHARD", "SDG 3.8.2, 2024 definition", "Descriptive only")
    flag("FSCH_A", "Labelled mean years of schooling but values match school-life expectancy", "FSCH (UNDP mean years) used")
    flag("FLFP_A / FLFP", "Duplicate labour-force columns", "FLFP used")
    flag("GII, HDI", "Contain maternal mortality, adolescent births or life expectancy (circular with SDG3-PI)", "Excluded")
    flag("GOVEFF, POLSTAB, CORRUPT", "WGI estimate scale (−2.5 to +2.5)", "Combined by principal components")
    flag("HEPC", "Current US$, not PPP", "Logged")
    flag("ND-GAIN components", "Adaptive capacity scored as a deficit; South Sudan blank",
         "X₁ = mean(exposure, sensitivity, capacity deficit); South Sudan imputed")
    flag("CHRI components", "Banded 0–100; sensitivity embeds health status", "CHRI = E + S − AC; robustness only")
    nC = {v: int(d[v].notna().sum()) for v in ["SIGI", "DHSDEC", "SDG561", "CHILDMAR"]}
    flag("C-A gender indicators", f"SIGI 2023 (n = {nC['SIGI']}), DHS health decisions (n = {nC['DHSDEC']}), "
         f"SDG 5.6.1 (n = {nC['SDG561']}), child marriage (n = {nC['CHILDMAR']})", "Gaps multiply imputed")
    flag("All indicators", "Most recent available value per country; reference years not recorded",
         "Analysed as a latest-available-value cross-section")
    inv = {v: k for k, v in COLMAP.items()}
    cmap = pd.DataFrame([{"Code": v, "Workbook column": inv[v].strip(), "Workbook heading": h,
                          "Framework construct": c, "n (of 48)": int(orig[v].notna().sum()), "Assessment": a}
                         for v, (h, c, a) in CONSTRUCT_MAP.items()])
    return d, orig, pd.DataFrame(screen), cmap


# =============================================================================
# 2. SDG 3 Performance Index  (Tables S3-S8)
# =============================================================================
DIRECTION = {"MMR": -1, "SBA": 1, "ABR": -1, "FP": 1, "U5MR": -1, "NMR": -1, "DTP3": 1, "STUNT": -1,
             "HIV": -1, "TB": -1, "MAL_INC": -1, "MAL_MORT": -1, "SCI": 1, "OOP": -1}
IS_RATE = {"MMR", "ABR", "U5MR", "NMR", "HIV", "TB", "MAL_INC", "MAL_MORT"}
UNITS = {"MMR": "per 100,000 live births", "SBA": "%", "ABR": "per 1,000 women 15–19", "FP": "%",
         "U5MR": "per 1,000 live births", "NMR": "per 1,000 live births", "DTP3": "%", "STUNT": "% under-5",
         "HIV": "per 1,000 uninfected", "TB": "per 100,000", "MAL_INC": "per 1,000 at risk",
         "MAL_MORT": "per 100,000", "SCI": "index 0–100", "OOP": "% of CHE"}


def stage2_index(d):
    def best5(v):
        s = d[v].dropna()
        return float(s.nsmallest(5).mean()) if DIRECTION[v] < 0 else float(s.nlargest(5).mean())

    target = {"MMR": (70, "SDG 3.1"), "SBA": (100, "Universal coverage"),
              "ABR": (best5("ABR"), "Mean of 5 best SSA performers"), "FP": (75, "SDG benchmark (75%)"),
              "U5MR": (25, "SDG 3.2"), "NMR": (12, "SDG 3.2"), "DTP3": (90, "IA2030 (90%)"),
              "STUNT": (best5("STUNT"), "Mean of 5 best SSA performers"),
              "HIV": (best5("HIV"), "Mean of 5 best SSA performers"),
              "TB": (best5("TB"), "Mean of 5 best SSA performers"),
              "MAL_INC": (1.0, "Pre-elimination threshold"), "MAL_MORT": (1.0, "Near-elimination floor"),
              "SCI": (100, "Universal coverage"), "OOP": (15, "WHO financial-protection benchmark")}
    steps, norm = [], pd.DataFrame(index=d.index)
    for dim, vs in DIMS.items():
        for v in vs:
            x = d[v].astype(float)
            s = x.dropna()
            ratio = s.max() / max(s.min(), 1e-9)
            sk = float(s.skew())
            use_log = (v in IS_RATE) and (ratio > 10 or sk > 1)       # log rule (Section 3.2)
            t, tsrc = target[v]
            w = float(np.nanpercentile(s, 97.5)) if DIRECTION[v] < 0 else float(np.nanpercentile(s, 2.5))
            if use_log:
                score = 100 * (np.log(w) - np.log(np.maximum(x, t))) / (np.log(w) - np.log(t))
            elif DIRECTION[v] > 0:
                score = 100 * (x - w) / (t - w)
            else:
                score = 100 * (w - x) / (w - t)
            score = score.clip(0, 100)
            norm[v] = score
            steps.append({"Dimension": dim, "Indicator": LABEL[v], "code": v, "Unit": UNITS[v],
                          "Direction": "+" if DIRECTION[v] > 0 else "−", "n": int(s.size),
                          "Min": s.min(), "Max": s.max(), "Max/min": ratio if np.isfinite(ratio) and s.min() > 0 else np.nan,
                          "Skewness": sk, "Logged": "Yes" if use_log else "No", "Target t": t, "Basis of t": tsrc,
                          "Worst w": w, "Basis of w": "97.5th percentile" if DIRECTION[v] < 0 else "2.5th percentile",
                          "Mean score": float(score.mean()), "% at target": float((score >= 99.999).mean() * 100)})
    steps = pd.DataFrame(steps)

    # within-dimension weights: squared first-principal-component loadings (equal if loadings differ in sign)
    weights, wrows = {}, []
    for dim, vs in DIMS.items():
        R = norm[vs].corr(min_periods=10).values
        ev, evec = np.linalg.eigh(R)
        pc1 = evec[:, -1]
        if pc1.sum() < 0:
            pc1 = -pc1
        expl = ev[-1] / ev.sum()
        wts, rule = pc1 ** 2 / (pc1 ** 2).sum(), "PCA (squared PC1 loadings)"
        if (pc1 < 0).any():
            wts, rule = np.repeat(1 / len(vs), len(vs)), "Equal (PC1 loadings of mixed sign)"
        weights[dim] = dict(zip(vs, wts))
        for v, l, ww in zip(vs, pc1, wts):
            wrows.append({"Dimension": dim, "Indicator": LABEL[v], "code": v, "PC1 loading": l,
                          "Variance explained by PC1": expl, "Rule applied": rule, "Weight used": ww})
    wtab = pd.DataFrame(wrows)

    def dim_scores(wdict, min_share=0.75):
        out = pd.DataFrame(index=norm.index)
        for dim, vs in DIMS.items():
            W = pd.Series(wdict[dim])
            M = norm[vs]
            avail = M.notna()
            sc = (M.fillna(0) * W).sum(axis=1) / (avail * W).sum(axis=1)
            sc[avail.sum(axis=1) < int(np.ceil(min_share * len(vs)))] = np.nan
            out[dim] = sc
        return out

    def geo(ds, floor=1.0):  # geometric mean limits compensation between dimensions
        return np.exp(np.log(ds.clip(lower=floor)).mean(axis=1, skipna=False))

    D = dim_scores(weights)
    D["SDG3-PI"] = geo(D[list(DIMS)])
    eq = {dim: {v: 1 / len(vs) for v in vs} for dim, vs in DIMS.items()}
    ent = {}
    for dim, vs in DIMS.items():
        P = norm[vs].dropna() + 1e-6
        P = P / P.sum()
        E = -(1 / np.log(len(P))) * (P * np.log(P)).sum()
        ent[dim] = dict(zip(vs, (1 - E) / (1 - E).sum()))
    D["SDG3-PI (equal weights)"] = geo(dim_scores(eq)[list(DIMS)])
    D["SDG3-PI (entropy weights)"] = geo(dim_scores(ent)[list(DIMS)])
    D["SDG3-PI (arithmetic)"] = D[list(DIMS)].mean(axis=1)
    D["Rank"] = D["SDG3-PI"].rank(ascending=False, method="min")
    D["Distance to 2030"] = 100 - D["SDG3-PI"]
    wtab["Entropy weight (robustness)"] = [ent[r.Dimension][r.code] for r in wtab.itertuples()]
    rob = []
    for c, lab in [("SDG3-PI (equal weights)", "Equal weights within dimensions"),
                   ("SDG3-PI (entropy weights)", "Entropy weights within dimensions"),
                   ("SDG3-PI (arithmetic)", "Arithmetic mean of dimensions")]:
        rob.append({"Alternative aggregation": lab,
                    "Spearman ρ with main index": stats.spearmanr(D["SDG3-PI"], D[c]).statistic,
                    "Largest rank shift": int(np.abs(D["SDG3-PI"].rank(ascending=False) - D[c].rank(ascending=False)).max())})
    # worked example (Kenya)
    kx = []
    for dim, vs in DIMS.items():
        for v in vs:
            st = steps.set_index("code").loc[v]
            kx.append({"Dimension": dim, "Indicator": LABEL[v], "Raw value": d.loc["Kenya", v],
                       "Score (0–100)": norm.loc["Kenya", v], "Weight": weights[dim][v],
                       "Target t": st["Target t"], "Worst w": st["Worst w"], "Logged": st["Logged"]})
    return D, norm, steps, wtab, pd.DataFrame(rob), pd.DataFrame(kx)


# =============================================================================
# 3. Explanatory constructs and multiple imputation  (Table 1, Tables S9-S12)
# =============================================================================
BLOCKS = {  # construct: (indicators, orientation)
    "X2": (["UNSAFE_WATER", "UNSAFE_SAN", "POLLFUEL", "PM25"], [1, 1, 1, 1]),
    "X2_EXT": (["UNSAFE_WATER", "UNSAFE_SAN", "POLLFUEL", "PM25", "TREELOSS"], [1, 1, 1, 1, 1]),
    "X2_OLD": (["POLLFUEL", "PM25", "lnWASH"], [1, 1, 1]),
    "C_A": (["SIGI", "CHILDMAR", "DHSDEC", "SDG561"], [1, 1, -1, -1]),
    "GOV": (["GOVEFF", "POLSTAB", "CORRUPT"], [1, 1, 1]),
    "C_B": (["TRUST", "EXCL_EPR", "EXCL_VDEM", "ETHFRAC"], [1, -1, -1, -1]),
    "C_C": (["VACCONF", "TRUSTDOC"], [1, 1]),
    "C_D": (["KINSHIP", "WATERCOLL"], [1, 1]),
    "X1_HAZ": (["TEMPANOM", "SPEI"], [1, -1]),
}
BLOCK_LABEL = {"X2": "X₂ Environmental deprivation", "X2_EXT": "X₂ extended with tree-cover loss (robustness)",
               "X2_OLD": "X₂ with unsafe-WASH deaths (robustness)", "C_A": "C-A Restrictive gender norms",
               "GOV": "Z Governance", "C_B": "C-B Social cohesion & trust", "C_C": "C-C Health-cultural orientation",
               "C_D": "C-D Cultural-ecological practice", "X1_HAZ": "X₁ Observed climate hazard (robustness)"}
IND_LABEL = {"UNSAFE_WATER": "Without basic drinking water (%)", "UNSAFE_SAN": "Without safely managed sanitation (%)",
             "POLLFUEL": "Polluting cooking fuels (%)", "PM25": "Ambient PM2.5 (µg/m³)",
             "TREELOSS": "Tree-cover loss 2000–2025 (%)", "lnWASH": "ln unsafe-WASH deaths per 100,000",
             "SIGI": "SIGI 2023", "CHILDMAR": "Child marriage (SDG 5.3.1, %)",
             "DHSDEC": "Women participating in own health-care decisions (%)",
             "SDG561": "Women's informed reproductive decisions (SDG 5.6.1, %)",
             "GOVEFF": "Government effectiveness", "POLSTAB": "Political stability", "CORRUPT": "Control of corruption",
             "TRUST": "Interpersonal and institutional trust", "EXCL_EPR": "Politically excluded population share",
             "EXCL_VDEM": "Exclusion by social group (V-Dem)", "ETHFRAC": "Ethnic fractionalisation",
             "VACCONF": "Vaccine confidence", "TRUSTDOC": "Trust in doctors, nurses and scientists",
             "KINSHIP": "Kinship intensity / ancestral traits", "WATERCOLL": "Households where women or girls collect water (%)",
             "TEMPANOM": "Recent annual temperature anomaly (°C)", "SPEI": "Drought severity (−SPEI)"}


def stage3_constructs(d, D, m_imp=20):
    from sklearn.experimental import enable_iterative_imputer  # noqa: F401
    from sklearn.impute import IterativeImputer
    from sklearn.linear_model import BayesianRidge

    base = pd.DataFrame(index=d.index)
    for v in ["ND_E", "ND_S", "ND_AC", "CH_E", "CH_S", "CH_AC", "SPEI", "TEMPANOM", "TREELOSS", "PM25"]:
        base[v] = d[v]
    base["POLLFUEL"] = 100 - d["CLEANFUEL"]
    base["UNSAFE_WATER"] = 100 - d["WATER_B"]
    base["UNSAFE_SAN"] = 100 - d["SAN_SM"]
    base["lnWASH"] = np.log(d["WASH_RATE"])
    base["POV"] = d["POV"]
    base["POU"] = d["POU_A"]
    base["lnDALY_HW"] = np.log(d["CMNN_DALY"] / (10 * (d["PHYS"] + d["NURSE"])))  # M2 health-system pressure
    base["lnHW"] = np.log(d["PHYS"] + d["NURSE"])
    base["lnGDP"] = np.log(d["GDPPC"])
    for v in ["GOVEFF", "POLSTAB", "CORRUPT", "URBAN", "FSCH", "FLFP", "AGEDEP", "SIGI", "DHSDEC", "SDG561",
              "CHILDMAR", "TRUST", "EXCL_EPR", "EXCL_VDEM", "ETHFRAC", "VACCONF", "TRUSTDOC", "RELIG",
              "KINSHIP", "WATERCOLL"]:
        base[v] = d[v]
    base["lnHEPC"] = np.log(d["HEPC"])
    base["SDG3PI"] = D["SDG3-PI"]
    for dim in DIMS:
        base["DIM_" + dim.split()[0].upper()] = D[dim]
    cols = list(base.columns)
    imp0 = IterativeImputer(estimator=BayesianRidge(), max_iter=50, random_state=0)
    B0 = pd.DataFrame(imp0.fit_transform(base[cols]), index=base.index, columns=cols)

    spec, load_rows = {}, []
    for name, (vs, sign) in BLOCKS.items():
        Z = B0[vs]
        mu, sd = Z.mean(), Z.std(ddof=1)
        Zs = (Z - mu) / sd * np.array(sign)
        ev, evec = np.linalg.eigh(np.corrcoef(Zs.values.T))
        l = evec[:, -1]
        if l.sum() < 0:
            l = -l
        spec[name] = dict(vars=vs, sign=sign, mu=mu, sd=sd, load=l)
        for v, s, li in zip(vs, sign, l):
            load_rows.append({"Construct": BLOCK_LABEL[name], "Indicator": IND_LABEL[v],
                              "Orientation": "+" if s > 0 else "reversed", "PC1 loading": li,
                              "Variance explained": ev[-1] / ev.sum()})

    def make(B):
        out = pd.DataFrame(index=B.index)
        for name, sp in spec.items():
            out[name] = ((B[sp["vars"]] - sp["mu"]) / sp["sd"] * np.array(sp["sign"])).values @ sp["load"]
        out["X1"] = (B["ND_E"] + B["ND_S"] + B["ND_AC"]) / 3
        out["X1_EXP"] = B["ND_E"]
        out["X1_CHRI"] = B["CH_E"] + B["CH_S"] - B["CH_AC"]
        out["X1_TEMP"] = B["TEMPANOM"]
        for v in ["ND_E", "ND_S", "ND_AC", "TEMPANOM", "TREELOSS", "SPEI", "RELIG"]:
            out[v] = B[v]
        out["M1"] = B["POV"]
        out["M2"] = B["lnDALY_HW"]
        for v in ["lnGDP", "lnHEPC", "URBAN", "FSCH", "FLFP", "AGEDEP", "lnHW"]:
            out[v] = B[v]
        out["Y"] = B["SDG3PI"]
        for c in B.columns:
            if c.startswith("DIM_"):
                out[c] = B[c]
        return out

    K0 = make(B0)
    mi = []
    for m in range(m_imp):  # chained-equation imputation with posterior draws, m = 20
        imp = IterativeImputer(estimator=BayesianRidge(), max_iter=50, sample_posterior=True, random_state=100 + m)
        Bm = pd.DataFrame(imp.fit_transform(base[cols]), index=base.index, columns=cols)
        Bm = Bm.where(base[cols].isna(), base[cols])
        mi.append(make(Bm))
    corr = lambda a, b: float(pd.concat([a, b], axis=1).corr().iloc[0, 1])
    val = pd.DataFrame([
        ("corr(X₁ ND-GAIN composite, CHRI composite)", corr(K0.X1, K0.X1_CHRI)),
        ("corr(ND-GAIN exposure, CHRI exposure)", corr(B0.ND_E, B0.CH_E)),
        ("corr(ND-GAIN sensitivity, CHRI sensitivity)", corr(B0.ND_S, B0.CH_S)),
        ("corr(ND-GAIN capacity deficit, CHRI capacity)", corr(B0.ND_AC, B0.CH_AC)),
        ("corr(X₁ ND-GAIN composite, ln GDP pc)", corr(K0.X1, K0.lnGDP)),
        ("corr(X₁ ND-GAIN composite, SDG3-PI)", corr(K0.X1, K0.Y)),
        ("corr(X₁ observed hazard, ND-GAIN composite)", corr(K0.X1_HAZ, K0.X1)),
        ("corr(X₁ observed hazard, SDG3-PI)", corr(K0.X1_HAZ, K0.Y)),
        ("corr(CHRI composite, SDG3-PI)", corr(K0.X1_CHRI, K0.Y)),
        ("corr(tree-cover loss, X₂)", corr(K0.TREELOSS, K0.X2)),
        ("corr(tree-cover loss, SDG3-PI)", corr(K0.TREELOSS, K0.Y)),
        ("corr(X₂, X₂ extended)", corr(K0.X2, K0.X2_EXT)),
        ("corr(X₂, ln unsafe-WASH deaths)", corr(K0.X2, B0.lnWASH)),
        ("corr(poverty, undernourishment)", corr(B0.POV, B0.POU)),
        ("corr(C-A, SIGI) [observed values]", corr(K0.C_A, base.SIGI)),
        ("corr(DHS health decisions, SDG 5.6.1) [observed values]", corr(base.DHSDEC, base.SDG561)),
        ("corr(religiosity, vaccine confidence)", corr(B0.RELIG, B0.VACCONF)),
    ], columns=["Check", "Value"])
    dv = {"X1": "X₁ Climate vulnerability (ND-GAIN composite, 0–1)", "X1_HAZ": "X₁ Observed hazard (PC score)",
          "TREELOSS": "Tree-cover loss 2000–2025 (%)", "X2": "X₂ Environmental deprivation (PC score)",
          "M1": "M₁ Poverty ($3.00/day, %)", "M2": "M₂ ln CMNN DALYs per health worker",
          "lnGDP": "Z ln GDP per capita (PPP)", "GOV": "Z Governance (PC score)",
          "lnHEPC": "Z ln health expenditure per capita (US$)", "URBAN": "Z Urban share (%)",
          "FSCH": "Z Female mean years of schooling", "C_A": "C-A Restrictive gender norms (PC score)",
          "C_B": "C-B Social cohesion & trust (PC score)", "C_C": "C-C Health-cultural orientation (PC score)",
          "C_D": "C-D Cultural-ecological practice (PC score)", "Y": "Y SDG3-PI (0–100)"}
    desc = K0[list(dv)].describe().T[["mean", "std", "min", "50%", "max"]]
    desc.columns = ["Mean", "SD", "Min", "Median", "Max"]
    desc.index = [dv[i] for i in desc.index]
    cvars = ["Y", "X1", "X2", "M1", "M2", "lnGDP", "GOV", "lnHEPC", "URBAN", "FSCH", "C_A", "C_B", "C_C", "C_D"]
    cm = K0[cvars].corr()
    short = {"Y": "Y", "X1": "X₁", "X2": "X₂", "M1": "M₁", "M2": "M₂", "lnGDP": "lnGDP", "GOV": "GOV",
             "lnHEPC": "lnHE", "URBAN": "Urban", "FSCH": "FSch", "C_A": "C-A", "C_B": "C-B", "C_C": "C-C", "C_D": "C-D"}
    cm.index = [short[i] for i in cm.index]
    cm.columns = [short[i] for i in cm.columns]
    miss = base.isna().sum()
    return dict(base=base, B0=B0, K0=K0, mi=mi, loads=pd.DataFrame(load_rows), val=val, desc=desc, corr=cm,
                miss=miss)


# =============================================================================
# 4. Nested inequality  (Table 2, Tables S13-S15)
# =============================================================================
def wgini(x, w):
    w = w / w.sum()
    mu = np.sum(w * x)
    return float(np.sum(w[:, None] * w[None, :] * np.abs(x[:, None] - x[None, :])) / (2 * mu))


def wtheil(x, w):
    w = w / w.sum()
    mu = np.sum(w * x)
    r = x / mu
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(r > 0, r * np.log(r), 0.0)
    return float(np.sum(w * t)), mu


def theil_between(x, w, g):
    """Theil T and its between-group component (Shorrocks, 1980)."""
    T, mu = wtheil(x, w)
    W = w / w.sum()
    TB = 0.0
    for gg in np.unique(g):
        m = g == gg
        Pg = W[m].sum()
        mug = np.sum(W[m] * x[m]) / Pg
        if mug > 0:
            TB += Pg * mug / mu * np.log(mug / mu)
    return T, TB


def stage4_inequality(d, D):
    d = d.copy()
    d["WB"] = [wb_region(c) for c in d.index]
    d["AU"] = [au_region(c) for c in d.index]
    d["SDG3PI"] = D["SDG3-PI"]
    inds = [("MMR", -1, "Maternal mortality ratio (per 100,000)"), ("SBA", 1, "Skilled birth attendance (%)"),
            ("ABR", -1, "Adolescent birth rate (per 1,000)"), ("FP", 1, "FP demand satisfied, modern (%)"),
            ("U5MR", -1, "Under-5 mortality (per 1,000)"), ("NMR", -1, "Neonatal mortality (per 1,000)"),
            ("DTP3", 1, "DTP3 coverage (%)"), ("STUNT", -1, "Stunting (%)"),
            ("HIV", -1, "HIV incidence (per 1,000)"), ("TB", -1, "TB incidence (per 100,000)"),
            ("MAL_INC", -1, "Malaria incidence (per 1,000 at risk)"), ("MAL_MORT", -1, "Malaria mortality (per 100,000)"),
            ("SCI", 1, "UHC service coverage index"), ("OOP", -1, "Out-of-pocket share (%)"),
            ("SDG3PI", 1, "SDG3-PI (0–100)")]
    targets = {"MMR": ("≤", 70), "U5MR": ("≤", 25), "NMR": ("≤", 12), "DTP3": ("≥", 90),
               "FP": ("≥", 75), "SBA": ("≥", 90), "OOP": ("≤", 15)}
    rows = []
    for v, sgn, lab in inds:
        s = d[[v, "POP_M", "WB", "AU"]].dropna()
        x, w = s[v].values.astype(float), s["POP_M"].values.astype(float)
        bi = s[v].idxmin() if sgn < 0 else s[v].idxmax()
        wi = s[v].idxmax() if sgn < 0 else s[v].idxmin()
        best, worst = s.loc[bi, v], s.loc[wi, v]
        ratio = (worst / best if sgn < 0 else best / worst) if min(best, worst) > 0 else np.nan
        T, TB = theil_between(x, w, s["WB"].values)
        _, TBA = theil_between(x, w, s["AU"].values)
        r = {"Indicator": lab, "code": v, "n": len(s), "Best (country)": f"{best:,.4g} ({bi})",
             "Worst (country)": f"{worst:,.4g} ({wi})", "Absolute gap": abs(worst - best), "Relative gap": ratio,
             "Population-weighted mean": np.sum(w * x) / w.sum(),
             "AFE mean": s.loc[s.WB == "AFE", v].mean(), "AFW mean": s.loc[s.WB == "AFW", v].mean(),
             "Gini": wgini(x, w), "Theil T": T, "Between AFE/AFW (% of T)": 100 * TB / T,
             "Between AU regions (% of T)": 100 * TBA / T, "Countries at 2030 benchmark": ""}
        if v in targets:
            op, tv = targets[v]
            met = (s[v] <= tv) if op == "≤" else (s[v] >= tv)
            r["Countries at 2030 benchmark"] = f"{int(met.sum())} of {len(s)} ({op}{tv})"
        rows.append(r)
    ineq = pd.DataFrame(rows)
    comp = []
    for c in ["SDG3-PI", "Maternal health", "Child health", "Communicable disease", "UHC"]:
        a, b = D.loc[d.index[d.WB == "AFE"], c], D.loc[d.index[d.WB == "AFW"], c]
        comp.append({"Measure": c, "AFE mean (n = 26)": a.mean(), "AFW mean (n = 22)": b.mean(),
                     "Difference": a.mean() - b.mean(), "Welch t p": stats.ttest_ind(a, b, equal_var=False).pvalue,
                     "Mann–Whitney p": stats.mannwhitneyu(a, b).pvalue,
                     "AFE SE": a.std(ddof=1) / np.sqrt(len(a)), "AFW SE": b.std(ddof=1) / np.sqrt(len(b))})
    comp = pd.DataFrame(comp)
    au = D.join(d["AU"]).groupby("AU")[["SDG3-PI", "Maternal health", "Child health", "Communicable disease", "UHC"]].mean()
    au.insert(0, "n", d.groupby("AU").size())
    return ineq, comp, au, d[["WB", "AU"]]


# =============================================================================
# 5. Spatial dependence and typology  (Tables S16-S18)
# =============================================================================
def africa_geometries(countries):
    """48 SSA countries from Natural Earth (lowres); island states drawn as small discs."""
    import geopandas as gpd
    from shapely.geometry import Point
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    af = world[world.continent == "Africa"].copy()
    nm = {"Central African Rep.": "Central African Republic", "Congo": "Congo, Rep.", "Dem. Rep. Congo": "Congo, Dem. Rep.",
          "Eq. Guinea": "Equatorial Guinea", "Gambia": "Gambia, The", "S. Sudan": "South Sudan", "eSwatini": "Eswatini",
          "Somaliland": "Somalia"}
    af["country"] = af["name"].replace(nm)
    af = af.dissolve(by="country", as_index=False)[["country", "geometry"]]
    islands = {"Cabo Verde": (-23.6, 15.1), "Comoros": (43.9, -11.9), "Mauritius": (57.6, -20.3),
               "São Tomé and Príncipe": (6.6, 0.2), "Seychelles": (55.5, -4.7)}
    isl = gpd.GeoDataFrame({"country": list(islands)}, geometry=[Point(*v).buffer(0.9) for v in islands.values()], crs=af.crs)
    geo = pd.concat([af, isl], ignore_index=True)
    ssa = geo[geo.country.isin(countries)].set_index("country").loc[list(countries)].rename_axis("country").reset_index()
    assert len(ssa) == len(countries)
    context = af[~af.country.isin(countries)]
    return ssa, context


def spatial_weights(ssa):
    """Queen contiguity united with 4 nearest neighbours (keeps island states connected), row-standardised."""
    from libpysal.weights import Queen, KNN, w_union
    proj = ssa.to_crs("ESRI:102022")  # Africa Albers equal-area
    wq = Queen.from_dataframe(proj, use_index=False, silence_warnings=True)
    wk = KNN.from_array(np.column_stack([proj.geometry.centroid.x, proj.geometry.centroid.y]), k=4)
    W = w_union(wq, wk, silence_warnings=True)
    W.transform = "r"
    return W


def stage5_spatial(K0, D, n_ref=100):
    from esda.moran import Moran, Moran_Local
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    ssa, context = africa_geometries(K0.index)
    W = spatial_weights(ssa)
    winfo = {"mean neighbours": float(np.mean(list(W.cardinalities.values()))),
             "min neighbours": int(min(W.cardinalities.values()))}
    V = {"SDG3-PI": D.loc[K0.index, "SDG3-PI"], "Maternal health": D.loc[K0.index, "Maternal health"],
         "Child health": D.loc[K0.index, "Child health"], "Communicable disease": D.loc[K0.index, "Communicable disease"],
         "UHC": D.loc[K0.index, "UHC"], "X₁ climate vulnerability (ND-GAIN)": K0["X1"],
         "X₂ environmental deprivation": K0["X2"], "M₁ poverty": K0["M1"], "M₂ health-system pressure": K0["M2"],
         "Temperature anomaly (°C)": K0["TEMPANOM"], "Tree-cover loss 2000–2025 (%)": K0["TREELOSS"],
         "C-A restrictive gender norms": K0["C_A"], "C-B social cohesion": K0["C_B"],
         "C-C health-cultural orientation": K0["C_C"], "C-D cultural-ecological practice": K0["C_D"]}
    np.random.seed(12345)
    moran = pd.DataFrame([{"Variable": k, "Moran's I": (mi := Moran(v.values, W, permutations=9999)).I,
                           "E[I]": mi.EI, "z (permutation)": mi.z_sim, "p (9,999 permutations)": mi.p_sim}
                          for k, v in V.items()])
    lisa = Moran_Local(V["SDG3-PI"].values, W, permutations=9999, seed=12345)
    qlab = {1: "High–High", 2: "Low–High", 3: "Low–Low", 4: "High–Low"}
    ssa["LISA"] = [qlab[q] if p < 0.05 else "Not significant" for q, p in zip(lisa.q, lisa.p_sim)]
    ssa["SDG3PI"] = V["SDG3-PI"].values
    z = (ssa["SDG3PI"] - ssa["SDG3PI"].mean()) / ssa["SDG3PI"].std(ddof=0)
    ssa["z"], ssa["lag_z"] = z.values, W.sparse @ z.values
    # k-means typology (k from the gap statistic; Tibshirani et al., 2001)
    F = pd.DataFrame({"SDG3-PI": V["SDG3-PI"].values, "X₁ climate vulnerability": K0["X1"].values,
                      "Health-system capacity (ln HW/10k)": K0["lnHW"].values,
                      "C-A restrictive gender norms": K0["C_A"].values, "C-B social cohesion": K0["C_B"].values,
                      "C-C health-cultural orientation": K0["C_C"].values,
                      "C-D cultural-ecological practice": K0["C_D"].values}, index=K0.index)
    Fz = (F - F.mean()) / F.std(ddof=0)
    rng = np.random.default_rng(7)
    sil, gap, gse, inertia = {}, {}, {}, {}
    lo, hi = Fz.min().values, Fz.max().values
    for k in range(2, 7):
        km = KMeans(n_clusters=k, n_init=100, random_state=0).fit(Fz)
        sil[k], inertia[k] = silhouette_score(Fz, km.labels_), km.inertia_
        ref = np.array([np.log(KMeans(n_clusters=k, n_init=10, random_state=b).fit(rng.uniform(lo, hi, size=Fz.shape)).inertia_)
                        for b in range(n_ref)])
        gap[k] = ref.mean() - np.log(km.inertia_)
        gse[k] = ref.std(ddof=0) * np.sqrt(1 + 1 / n_ref)
    ks = sorted(gap)
    k_gap = next((k for k in ks[:-1] if gap[k] >= gap[k + 1] - gse[k + 1]), ks[-1])
    kchoice = pd.DataFrame({"k": ks, "Silhouette": [sil[k] for k in ks], "Gap": [gap[k] for k in ks],
                            "Gap s.e.": [gse[k] for k in ks], "Within-cluster SS": [inertia[k] for k in ks]})
    km = KMeans(n_clusters=k_gap, n_init=200, random_state=0).fit(Fz)
    lab = pd.Series(km.labels_, index=K0.index)
    order = F.groupby(lab)["SDG3-PI"].mean().sort_values(ascending=False).index
    lab = lab.map({old: i + 1 for i, old in enumerate(order)})
    prof = F.groupby(lab).mean()
    prof.insert(0, "n", lab.value_counts().sort_index())
    profz = Fz.groupby(lab).mean()
    members = lab.groupby(lab).apply(lambda s: ", ".join(sorted(s.index)))
    ssa["cluster"] = lab.values
    return dict(ssa=ssa, context=context, W=W, winfo=winfo, moran=moran, kchoice=kchoice, k=k_gap,
                k_sil=max(sil, key=sil.get), prof=prof, profz=profz, members=members, cluster=lab)


# =============================================================================
# 6. Econometric models and deviants  (Tables 3, 5, S19-S22)
# =============================================================================
def _z(df):
    return (df - df.mean()) / df.std(ddof=1)


def pool(dfs, y, xs):
    """Standardised OLS with HC3 errors, pooled across imputations with Rubin's rules."""
    import statsmodels.api as sm
    ests, vars_, r2 = [], [], []
    for df in dfs:
        sub = df[[y] + xs].dropna()
        r = sm.OLS(_z(sub[[y]])[y], sm.add_constant(_z(sub[xs]))).fit(cov_type="HC3")
        ests.append(r.params.values)
        vars_.append(np.diag(r.cov_params().values))
        r2.append(r.rsquared_adj)
    Q, U, m = np.array(ests), np.array(vars_), len(dfs)
    qbar, ubar, b = Q.mean(0), U.mean(0), Q.var(0, ddof=1)
    T = ubar + (1 + 1 / m) * b
    rm = (1 + 1 / m) * b / np.where(ubar > 0, ubar, 1e-12)
    dfree = (m - 1) * (1 + 1 / np.where(rm > 0, rm, 1e-12)) ** 2
    se = np.sqrt(T)
    p = 2 * stats.t.sf(np.abs(qbar / se), dfree)
    return pd.DataFrame({"beta": qbar, "se": se, "p": p}, index=["const"] + xs), float(np.mean(r2)), int(len(sub))


CORE = ["M1", "X2", "X1", "lnHEPC", "URBAN"]
ZS = ["lnGDP", "GOV", "FSCH"]
MAIN_SPECS = {
    "(1) Core equation": CORE,
    "(2) + structural controls Z": CORE + ZS,
    "(3) X₁ = observed hazard": ["M1", "X2", "X1_HAZ", "lnHEPC", "URBAN"] + ZS,
    "(4) X₁ = CHRI": ["M1", "X2", "X1_CHRI", "lnHEPC", "URBAN"] + ZS,
    "(5) + tree-cover loss": CORE + ZS + ["TREELOSS"],
    "(6) + cultural constructs": CORE + ZS + ["C_A", "C_B", "C_C", "C_D"],
}
SUPP_SPECS = {
    "(S1) X₁ = ND-GAIN exposure only": ["M1", "X2", "X1_EXP", "lnHEPC", "URBAN"] + ZS,
    "(S2) ND-GAIN components entered separately": ["M1", "X2", "ND_E", "ND_S", "ND_AC", "lnHEPC", "URBAN"] + ZS,
    "(S3) X₁ = temperature anomaly": ["M1", "X2", "X1_TEMP", "lnHEPC", "URBAN"] + ZS,
    "(S4) Outcome = ln SDG3-PI": CORE + ZS,
}


def stage6_econometrics(mi, K0, W):
    import statsmodels.api as sm
    import spreg
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.stats.diagnostic import het_breuschpagan, linear_reset
    from esda.moran import Moran
    res = {k: pool(mi, "Y", xs) for k, xs in MAIN_SPECS.items()}
    mi_log = [df.assign(lnY=np.log(df["Y"])) for df in mi]
    sres = {k: (pool(mi_log, "lnY", xs) if "ln SDG3-PI" in k else pool(mi, "Y", xs)) for k, xs in SUPP_SPECS.items()}
    dimres = {lab: pool(mi, dv, CORE + ZS) for dv, lab in [("DIM_MATERNAL", "Maternal health"), ("DIM_CHILD", "Child health"),
                                                         ("DIM_COMMUNICABLE", "Communicable disease"), ("DIM_UHC", "UHC")]}
    xs = CORE + ZS
    X = sm.add_constant(_z(K0[xs]))
    ols = sm.OLS(_z(K0[["Y"]])["Y"], X).fit()
    vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])], index=xs)
    cooks = pd.Series(ols.get_influence().cooks_distance[0], index=K0.index)
    mr = Moran(ols.resid.values, W, permutations=9999)
    yv, xv = _z(K0[["Y"]]).values, _z(K0[xs]).values
    sols = spreg.OLS(yv, xv, w=W, spat_diag=True, name_x=xs, name_y="Y")
    lagm = spreg.ML_Lag(yv, xv, w=W, name_x=xs, name_y="Y")
    errm = spreg.ML_Error(yv, xv, w=W, name_x=xs, name_y="Y")
    diag = pd.DataFrame([
        ("Maximum VIF", f"{vif.max():.2f} ({vif.idxmax()})"),
        ("Breusch–Pagan p", f"{het_breuschpagan(ols.resid, X)[1]:.3f}"),
        ("Ramsey RESET p", f"{float(linear_reset(ols, power=2, use_f=True).pvalue):.3f}"),
        ("Jarque–Bera p", f"{stats.jarque_bera(ols.resid).pvalue:.3f}"),
        ("Moran's I of residuals (p)", f"{mr.I:.3f} ({mr.p_sim:.3f})"),
        ("LM lag p / robust LM lag p", f"{sols.lm_lag[1]:.3f} / {sols.rlm_lag[1]:.3f}"),
        ("LM error p / robust LM error p", f"{sols.lm_error[1]:.3f} / {sols.rlm_error[1]:.3f}"),
        ("AIC: OLS / spatial lag / spatial error", f"{2 * (len(xs) + 1) - 2 * ols.llf:.1f} / {lagm.aic:.1f} / {errm.aic:.1f}"),
        ("Influential countries (Cook's D > 4/n)", ", ".join(cooks[cooks > 4 / len(cooks)].sort_values(ascending=False).index)),
    ], columns=["Diagnostic", "Value"])
    spat = pd.DataFrame({"Spatial lag β": list(lagm.betas.flatten()), "Spatial lag p": list(np.array(lagm.z_stat)[:, 1])},
                        index=["const"] + xs + ["ρ (spatial lag)"])
    spe = pd.DataFrame({"Spatial error β": list(errm.betas.flatten()), "Spatial error p": list(np.array(errm.z_stat)[:, 1])},
                       index=["const"] + xs + ["λ (spatial error)"])
    spat = spat.join(spe, how="outer").loc[xs + ["ρ (spatial lag)", "λ (spatial error)"]]
    dvm = sm.OLS(K0["Y"], sm.add_constant(K0[["lnGDP"]])).fit()
    dev = pd.DataFrame({"SDG3-PI": K0["Y"], "GDP pc (PPP)": np.exp(K0["lnGDP"]), "Predicted": dvm.fittedvalues,
                        "Residual": dvm.resid}).sort_values("Residual", ascending=False)
    return dict(res=res, sres=sres, dimres=dimres, diag=diag, spat=spat, dev=dev,
                dev_info={"slope": float(dvm.params["lnGDP"]), "R2": float(dvm.rsquared)}, vif=vif)


# =============================================================================
# 7. Moderated serial-parallel mediation  (Table 4, Tables S23-S28)
# =============================================================================
ZMED = ["lnGDP", "GOV", "FSCH"]


def _ols(y, X):
    X1 = np.column_stack([np.ones(len(y)), X])
    b, *_ = np.linalg.lstsq(X1, y, rcond=None)
    return b[1:], y - X1 @ b


def _system(df, C=None):
    X1, X2, M1, M2, Y = (df[v].values for v in ["X1", "X2", "M1", "M2", "Y"])
    Zm = df[ZMED].values
    o = {}
    if C is None:
        b, _ = _ols(M1, np.column_stack([X1, X2, Zm])); o.update(a11=b[0], a12=b[1])
        b, _ = _ols(M2, np.column_stack([X1, X2, M1, Zm])); o.update(a21=b[0], a22=b[1], d21=b[2])
        b, _ = _ols(Y, np.column_stack([X1, X2, M1, M2, Zm])); o.update(c1=b[0], c2=b[1], b1=b[2], b2=b[3])
    else:
        c = df[C].values
        b, _ = _ols(M1, np.column_stack([X1, X2, c, X1 * c, Zm])); o.update(a11=b[0], a12=b[1], a11c=b[3])
        b, _ = _ols(M2, np.column_stack([X1, X2, M1, c, Zm])); o.update(a21=b[0], a22=b[1], d21=b[2])
        b, _ = _ols(Y, np.column_stack([X1, X2, M1, M2, c, M1 * c, M2 * c, Zm]))
        o.update(c1=b[0], c2=b[1], b1=b[2], b2=b[3], b1c=b[5], b2c=b[6])
    return o


def _effects(p, cvals=None):
    e = {}
    if "a11c" not in p:
        e["X₁ → M₁ → Y (a₁₁·b₁)"] = p["a11"] * p["b1"]
        e["X₁ → M₂ → Y (a₂₁·b₂)"] = p["a21"] * p["b2"]
        e["X₁ → M₁ → M₂ → Y (a₁₁·d₂₁·b₂)"] = p["a11"] * p["d21"] * p["b2"]
        e["X₂ → M₁ → Y (a₁₂·b₁)"] = p["a12"] * p["b1"]
        e["X₂ → M₂ → Y (a₂₂·b₂)"] = p["a22"] * p["b2"]
        e["X₂ → M₁ → M₂ → Y (a₁₂·d₂₁·b₂)"] = p["a12"] * p["d21"] * p["b2"]
        e["IE₁ livelihood pathway"] = p["a11"] * p["b1"] + p["a11"] * p["d21"] * p["b2"]
        e["IE₂ burden pathway"] = p["a22"] * p["b2"]
        e["Contrast IE₁ − IE₂"] = e["IE₁ livelihood pathway"] - e["IE₂ burden pathway"]
        t1 = p["a11"] * p["b1"] + p["a21"] * p["b2"] + p["a11"] * p["d21"] * p["b2"]
        t2 = p["a12"] * p["b1"] + p["a22"] * p["b2"] + p["a12"] * p["d21"] * p["b2"]
        e["X₁ total indirect"], e["X₁ direct (c′₁)"], e["X₁ total effect"] = t1, p["c1"], t1 + p["c1"]
        e["X₂ total indirect"], e["X₂ direct (c′₂)"], e["X₂ total effect"] = t2, p["c2"], t2 + p["c2"]
        for k in ["a11", "a12", "a21", "a22", "d21", "b1", "b2", "c1", "c2"]:
            e["path " + k] = p[k]
    else:
        for lab, cv in cvals.items():
            A, B1, B2 = p["a11"] + p["a11c"] * cv, p["b1"] + p["b1c"] * cv, p["b2"] + p["b2c"] * cv
            e[f"IE₁(C) at {lab}"] = A * (B1 + p["d21"] * B2)
            e[f"IE₂(C) at {lab}"] = p["a22"] * B2
        e["Index of moderated mediation, IE₂ (a₂₂·b₂ᶜ)"] = p["a22"] * p["b2c"]
        e["IE₁ difference (P90 − P10)"] = e["IE₁(C) at P90"] - e["IE₁(C) at P10"]
        e["a₁₁ᶜ buffering (X₁×C → M₁)"] = p["a11c"]
        e["b₁ᶜ conversion (M₁×C → Y)"] = p["b1c"]
        e["b₂ᶜ interpretation (M₂×C → Y)"] = p["b2c"]
    return e


def _bc_ci(est, boots, alpha=0.05):
    boots = np.asarray(boots)
    z0 = stats.norm.ppf(np.clip((boots < est).mean(), 1e-4, 1 - 1e-4))
    lo = stats.norm.cdf(2 * z0 + stats.norm.ppf(alpha / 2))
    hi = stats.norm.cdf(2 * z0 + stats.norm.ppf(1 - alpha / 2))
    return np.quantile(boots, lo), np.quantile(boots, hi)


def _run_mediation(mi, rng, B, C=None):
    point, boot = [], []
    for df in mi:
        s = _z(df[["X1", "X2", "M1", "M2", "Y"] + ZMED + ([C] if C else [])])
        cvals = None
        if C:
            q = np.percentile(s[C], [10, 50, 90])
            cvals = {"P10": q[0], "P50": q[1], "P90": q[2]}
        point.append(_effects(_system(s, C), cvals))
        n = len(s)
        for _ in range(B):  # nonparametric bootstrap of whole countries
            boot.append(_effects(_system(s.iloc[rng.integers(0, n, n)], C), cvals))
    pt, bt = pd.DataFrame(point).mean(), pd.DataFrame(boot)
    rows = []
    for k in pt.index:
        lo, hi = _bc_ci(pt[k], bt[k].values)
        rows.append({"Effect": k, "Estimate": pt[k], "CI low": lo, "CI high": hi,
                     "CI excludes 0": "Yes" if (lo > 0 or hi < 0) else "No"})
    return pd.DataFrame(rows)


def stage7_mediation(mi, B=250):
    import statsmodels.api as sm
    rng = np.random.default_rng(2026)
    base = _run_mediation(mi, rng, B)
    alt = {}
    for lab, swap in [("ND-GAIN exposure only", {"X1": "X1_EXP"}), ("CHRI (E + S − AC)", {"X1": "X1_CHRI"}),
                      ("Observed hazard (temperature + drought)", {"X1": "X1_HAZ"}),
                      ("X₂ with unsafe-WASH deaths", {"X2": "X2_OLD"})]:
        alt[lab] = _run_mediation([df.assign(**{k: df[v] for k, v in swap.items()}) for df in mi], rng, B)
    mod = {C: _run_mediation(mi, rng, B, C) for C in ["C_A", "C_B", "C_C", "C_D"]}
    rho1, rho2 = [], []
    for df in mi:  # residual correlation at which each indirect effect vanishes (Imai et al., 2010)
        s = _z(df[["X1", "X2", "M1", "M2", "Y"] + ZMED])
        Zm = s[ZMED].values
        _, eM1 = _ols(s.M1.values, np.column_stack([s.X1, s.X2, Zm]))
        _, eY1 = _ols(s.Y.values, np.column_stack([s.X1, s.X2, Zm]))
        _, eM2 = _ols(s.M2.values, np.column_stack([s.X1, s.X2, s.M1, Zm]))
        _, eY2 = _ols(s.Y.values, np.column_stack([s.X1, s.X2, s.M1, Zm]))
        rho1.append(np.corrcoef(eM1, eY1)[0, 1]); rho2.append(np.corrcoef(eM2, eY2)[0, 1])
    sens = pd.DataFrame({"Mediator": ["M₁ poverty", "M₂ health-system pressure"],
                         "ρ* at which the indirect effect falls to zero": [np.mean(rho1), np.mean(rho2)]})
    expo = []
    for C in ["C_A", "C_B", "C_C", "C_D"]:  # exposure juncture: does culture sort countries into deprivation?
        bs, ses = [], []
        for df in mi:
            s = _z(df[["X2", C, "lnGDP", "GOV"]])
            r = sm.OLS(s["X2"], sm.add_constant(s[[C, "lnGDP", "GOV"]])).fit(cov_type="HC3")
            bs.append(r.params[C]); ses.append(r.bse[C])
        bs, ses = np.array(bs), np.array(ses)
        T = (ses ** 2).mean() + (1 + 1 / len(bs)) * bs.var(ddof=1)
        expo.append({"Cultural construct": LABEL[C], "code": C, "β on X₂": bs.mean(), "s.e.": np.sqrt(T),
                     "p": 2 * stats.norm.sf(abs(bs.mean() / np.sqrt(T)))})
    return dict(base=base, alt=alt, mod=mod, sens=sens, expo=pd.DataFrame(expo))


# =============================================================================
# 8. Health Belief Model extension  (Table S29)
# =============================================================================
def stage8_hbm(mi, d):
    """Do health-belief proxies (C-C: vaccine confidence and trust in health workers, i.e. perceived benefits;
    C-A: restrictive gender norms, i.e. perceived barriers and low self-efficacy) relate more strongly to
    behaviour-dependent service uptake than to mortality, net of deprivation, governance, income and schooling?"""
    outs = [("DTP3", "DTP3 coverage (%)", "Uptake"), ("SBA", "Skilled birth attendance (%)", "Uptake"),
            ("FP", "FP demand satisfied, modern (%)", "Uptake"), ("lnMMR", "ln maternal mortality ratio (reversed)", "Mortality"),
            ("lnU5MR", "ln under-5 mortality (reversed)", "Mortality")]
    add = pd.DataFrame({"DTP3": d["DTP3"], "SBA": d["SBA"], "FP": d["FP"],
                        "lnMMR": -np.log(d["MMR"]), "lnU5MR": -np.log(d["U5MR"])})
    rows = []
    for v, lab, kind in outs:
        dfs = [df.join(add) for df in mi]
        t, r2, n = pool(dfs, v, ["C_C", "C_A", "X2", "GOV", "lnGDP", "FSCH"])
        ti, _, _ = pool([df.assign(X2xCC=_z(df["X2"]) * _z(df["C_C"])) for df in dfs], v,
                        ["C_C", "C_A", "X2", "GOV", "lnGDP", "FSCH", "X2xCC"])
        rows.append({"Outcome": lab, "Type": kind, "n": n,
                     "C-C β": t.loc["C_C", "beta"], "C-C p": t.loc["C_C", "p"],
                     "C-A β": t.loc["C_A", "beta"], "C-A p": t.loc["C_A", "p"],
                     "X₂ β": t.loc["X2", "beta"], "X₂ p": t.loc["X2", "p"],
                     "X₂×C-C β": ti.loc["X2xCC", "beta"], "X₂×C-C p": ti.loc["X2xCC", "p"],
                     "Adj. R²": r2, "C-C se": t.loc["C_C", "se"], "C-A se": t.loc["C_A", "se"]})
    return pd.DataFrame(rows)


# =============================================================================
# 9. Figures  (Figures 1-7, S1-S7, graphical abstract; PNG at 600 dpi)
# =============================================================================
DPI = 600
MM = 1 / 25.4
TIFF = True         # also write a .tif copy of every figure (journal artwork format)
W2 = 190 * MM      # Elsevier double-column width
W15 = 140 * MM     # 1.5-column width
OKABE = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "verm": "#D55E00",
         "sky": "#56B4E9", "purple": "#CC79A7", "yellow": "#F0E442", "grey": "#8C8C8C", "ink": "#1A1A1A"}
DIMCOL = {"Maternal health": OKABE["purple"], "Child health": OKABE["green"],
          "Communicable disease": OKABE["verm"], "UHC": OKABE["blue"]}
CLUCOL = {1: OKABE["blue"], 2: OKABE["green"], 3: OKABE["verm"]}
CLUNAME = {1: "Cluster 1: high performance, high capacity", 2: "Cluster 2: mid performance, cohesive and trusting",
           3: "Cluster 3: low performance, restrictive norms, low cohesion"}


def set_style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
        "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "legend.fontsize": 7, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#333333",
        "savefig.dpi": DPI, "figure.dpi": 150, "pdf.fonttype": 42, "legend.frameon": False,
        "axes.titleweight": "bold", "axes.titlelocation": "left"})
    return plt


def _save(fig, path):
    fig.savefig(path, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.03)
    import matplotlib.pyplot as plt
    plt.close(fig)
    if TIFF:  # journal artwork copy: RGB TIFF, LZW-compressed, same resolution
        from PIL import Image
        with Image.open(path) as im:
            im.convert("RGB").save(Path(path).with_suffix(".tif"), compression="tiff_lzw", dpi=(DPI, DPI))


def _basemap(ax, context):
    context.plot(ax=ax, color="#ECECEC", edgecolor="white", linewidth=0.3)
    ax.set_xlim(-27, 60); ax.set_ylim(-36, 28.5); ax.set_axis_off()


























def _forest(ax, labels, est, se, pvals, color):
    y = np.arange(len(labels))[::-1]
    for yi, b_, s, p in zip(y, est, se, pvals):
        ax.plot([b_ - 1.96 * s, b_ + 1.96 * s], [yi, yi], color=color, lw=1.1)
        ax.plot(b_, yi, "o", ms=4.2, color=color if p < 0.05 else "white", mec=color, mew=1)
    ax.axvline(0, color="#777", lw=0.6, ls="--")
    ax.set_yticks(y); ax.set_yticklabels(labels)














# =============================================================================
# 10. Tables (CSV + Word) and Word exports
# =============================================================================
def _f(x, d=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    if isinstance(x, (int, np.integer)):
        return f"{x:,}"
    if isinstance(x, (float, np.floating)):
        return f"{x:,.{d}f}".replace("-", "−")
    return str(x)


def _p(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def _star(b, se, p, d=3):
    st = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
    return f"{_f(b, d)}{st} ({_f(se, d)})"


def _ci(lo, hi, d=3):
    return f"[{_f(lo, d)}, {_f(hi, d)}]"


SOURCE_APPRAISAL = [
    ("World Bank WDI", "Available, authentic", "Largely republishes other agencies' series", "Retained; original producer cited"),
    ("World Bank CCKP / CHRI", "Available, authentic", "CHRI reported as period snapshots, not annual", "Robustness for X₁ only"),
    ("WHO GHO", "Available, authentic", "UHC index revised in 2025; workforce data sparse", "Latest revision used"),
    ("UN SDG Global Database", "Available, authentic", "Aggregator", "Cross-checking only"),
    ("UNICEF", "Available, authentic", "Skilled birth attendance survey-based, irregular", "Latest available survey value"),
    ("IHME GBD 2023", "Available, authentic", "Modelled; revised each round", "Single vintage"),
    ("WHO/UNICEF JMP", "Available, authentic", "'Safely managed' water missing for many countries", "'At least basic' water used"),
    ("FAO", "Available, authentic", "Three-year averages", "Undernourishment as validation of M₁"),
    ("UNDP HDR", "Available, authentic", "GII embeds MMR and adolescent births (circular with Y)", "GII removed; female schooling retained"),
    ("ND-GAIN", "Available, authentic", "Adaptive capacity reported as deficit", "Composite of three components"),
    ("OECD SIGI", "Available, authentic", "Five editions; 2023 edition covers 39 of 48", "2023 values; gaps imputed"),
    ("Afrobarometer", "Available, authentic", "Not all 48 countries surveyed", "Latest round; gaps imputed and flagged"),
    ("EPR Core; V-Dem", "Available, authentic", "Expert-coded", "Retained"),
    ("HIEF", "Available, authentic", "Ends 2013", "2013 value"),
    ("Wellcome Global Monitor", "Available, authentic", "Vaccine items 2018 only", "2018 values"),
    ("Giuliano & Nunn ancestral data", "Available, authentic", "Time-invariant; ethnic mapping uncertainty", "Cross-sectional use only"),
    ("DHS; UNFPA SDG 5.6.1", "Available, authentic", "DHS countries only; irregular", "Gaps imputed"),
    ("Waste management; hospital beds", "Largely unavailable", "Sparse", "Dropped"),
]




FIG_CAPTIONS = {
    'Figure_1': ('Fig. 1', 'System architecture of the open pipeline. Seventy-two fields from 18 families of international sources pass through ingestion and rule-based screening, harmonisation, multiple imputation and the index engine before feeding six analytic modules. A quality-assurance layer logs every decision and check, and a reproducibility layer regenerates each table and figure from its own script.'),
    'Figure_2': ('Fig. 2', 'Conceptual framework. Environmental risk (X) is linked to SDG 3 performance (Y) directly and through social stratification (M), conditioned by institutional capacity and development inequality (Z). The cultural mediation layer (C) acts at four junctures (1 exposure, 2 buffering, 3 conversion, 4 interpretation), and the Health Belief Model adds a fifth (5 appraisal), at which perceived susceptibility, severity, benefits and barriers, cues to action and self-efficacy govern the uptake of services. Countries are nested in World Bank sub-regions and African Union regions.'),
    'Figure_3': ('Fig. 3', 'Data provenance and index robustness. (a) Status of each analysis variable in each country: observed, structural zero (non-endemic malaria) or multiply imputed; variables are grouped by framework construct and countries ordered by SDG3-PI. (b) Rank of each country on SDG3-PI (dots) and the range of its rank across three alternative aggregations (equal weights, entropy weights, arithmetic mean; bars).'),
    'Figure_4': ('Fig. 4', 'Geography of SDG 3 performance and environmental deprivation in 48 Sub-Saharan African countries (most recent available values). (a) SDG3-PI; (b)–(e) its four dimensions, scored from 0 (worst observed) to 100 (2030 target); (f) environmental deprivation (first principal component of unsafe water, unsafe sanitation, polluting cooking fuel and ambient PM2.5; darker = more deprived). Island states are drawn as discs. Each panel has its own colour scale. Map lines do not necessarily depict accepted national boundaries.'),
    'Figure_5': ('Fig. 5', 'Nested inequality. (a) Population-weighted Gini index of each SDG 3 indicator across countries, coloured by dimension. (b) Share of the Theil T index lying between the two World Bank sub-regions (orange) and between the five African Union regions (blue); the remainder lies between countries within regions.'),
    'Figure_6': ('Fig. 6', 'Spatial structure of SDG 3 performance. (a) Moran scatterplot of SDG3-PI against its spatial lag (weights: queen contiguity united with four nearest neighbours); outlined points are significant local clusters. (b) Local indicators of spatial association (p < 0.05, 9,999 permutations). (c) Health–environment–culture typology from k-means clustering. Map lines do not necessarily depict accepted national boundaries.'),
    'Figure_7': ('Fig. 7', 'Estimated serial–parallel mediation system (standardised). Coloured arrows and asterisks mark paths whose 95% bias-corrected bootstrap interval excludes zero (blue positive, vermilion negative); grey arrows do not. Controls: ln GDP per capita, governance and female schooling.'),
    'Figure_8': ('Fig. 8', 'SDG3-PI against GDP per capita (log scale), coloured by cluster. The line and band show the fitted income gradient and its 95% confidence interval. Labelled countries are the six largest positive and negative deviants from the gradient.'),
    'Figure_S1': ('Fig. S1', 'Country profiles. Bars show SDG3-PI (shaded by World Bank sub-region); dots show the four dimension scores. The dashed line marks the halfway point to the 2030 targets.'),
    'Figure_S2': ('Fig. S2', '(a) Climate vulnerability (ND-GAIN composite); (b) recent annual temperature anomaly (°C); (c) tree-cover loss 2000–2025 (% of 2000 cover). Map lines do not necessarily depict accepted national boundaries.'),
    'Figure_S3': ('Fig. S3', 'Mean SDG3-PI and dimension scores in Africa Eastern & Southern and Africa Western & Central (95% confidence intervals). Welch t-test: *** p < 0.001, ** p < 0.01, * p < 0.05, n.s. not significant.'),
    'Figure_S4': ('Fig. S4', 'Standardised cluster profiles: each bar is the cluster mean in standard deviations from the 48-country mean.'),
    'Figure_S5': ('Fig. S5', 'Conditional indirect effects at the 10th, 50th and 90th percentiles of each cultural construct (95% bias-corrected intervals). Circles: burden pathway IE₂; squares: livelihood pathway IE₁; filled markers exclude zero.'),
    'Figure_S6': ('Fig. S6', 'Exposure juncture: standardised association of each cultural construct with environmental deprivation, controlling for ln GDP per capita and governance (95% confidence intervals; filled markers p < 0.05).'),
    'Figure_S7': ('Fig. S7', 'Health Belief Model extension: standardised associations of (a) health-cultural orientation and (b) restrictive gender norms with service uptake (shaded) and mortality, net of environmental deprivation, governance, income and schooling (95% confidence intervals; filled markers p < 0.05).'),
    'Figure_S8': ('Fig. S8', 'Standardised coefficients (95% confidence intervals) for SDG3-PI from model (2), with structural controls, and model (6), adding the four cultural constructs. Filled markers: p < 0.05. HC3 errors pooled across 20 imputations.'),
}


def _docx_base(landscape=False, font="Times New Roman", size=10):
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.section import WD_ORIENT
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = font; st.font.size = Pt(size)
    st.element.rPr.rFonts.set(__import__("docx.oxml.ns", fromlist=["qn"]).qn("w:eastAsia"), font)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    for m in ["left_margin", "right_margin", "top_margin", "bottom_margin"]:
        setattr(sec, m, Cm(2.0))
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = sec.page_height, sec.page_width
    return doc


def _set_orientation(doc, landscape):
    from docx.enum.section import WD_ORIENT, WD_SECTION
    from docx.shared import Cm
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.orientation = WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
    w, h = (Cm(29.7), Cm(21.0)) if landscape else (Cm(21.0), Cm(29.7))
    sec.page_width, sec.page_height = w, h
    return sec


def _border(cell, **kw):
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.find(qn("w:tcBorders"))
    if b is None:
        b = OxmlElement("w:tcBorders"); tcPr.append(b)
    for edge in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        el = b.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}"); b.append(el)
        if edge in kw:
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(kw[edge])); el.set(qn("w:color"), "000000")
        else:
            el.set(qn("w:val"), "nil")


def add_table(doc, label, title, df, note="", size=9, autofit=True, width_cm=17.0):
    """Publication table: black text, no shading, horizontal rules only (top, under header, bottom)."""
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True
    r = p.add_run(label + ". "); r.bold = True; r.font.size = Pt(size + 1)
    r2 = p.add_run(title); r2.font.size = Pt(size + 1)
    n_r, n_c = df.shape[0] + 1, df.shape[1]
    t = doc.add_table(rows=n_r, cols=n_c)
    t.autofit = False
    tblPr = t._tbl.tblPr
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), "5000"); tw.set(qn("w:type"), "pct"); tblPr.append(tw)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    from docx.shared import Cm
    lens = []
    for j, col in enumerate(df.columns):
        cells = [str(v) for v in df.iloc[:, j]]
        mx = max([len(c) for c in cells] + [1]); mean = np.mean([len(c) for c in cells]) if cells else 1
        hw = max((len(w) for w in str(col).split()), default=0) + 2
        lw = max(max((len(w) for w in c.split()), default=1) for c in cells) + 1
        lens.append(max(hw, lw, mx + 1) if mx <= 13 else max(hw, lw, 13 + 0.7 * mean))
    wts = np.clip(np.array(lens, float), 4, 55)
    widths = [Cm(width_cm * w / wts.sum()) for w in wts]
    tw.set(qn("w:w"), str(int(width_cm / 2.54 * 1440))); tw.set(qn("w:type"), "dxa")
    for j, gc in enumerate(t._tbl.tblGrid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[j].cm / 2.54 * 1440)))
    numeric = [all((str(v).replace("−", "").replace(",", "").replace(".", "").replace("%", "").replace("*", "").replace("(", "").replace(")", "")
                    .replace(" ", "").replace("[", "").replace("]", "").replace("+", "").replace("<", "").replace("–", "").isdigit() or str(v) in ("", "–"))
                   for v in df.iloc[:, j]) for j in range(n_c)]
    for j, col in enumerate(df.columns):
        c = t.cell(0, j); c.text = ""; c.width = widths[j]
        run = c.paragraphs[0].add_run(str(col).strip()); run.bold = True; run.font.size = Pt(size)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if (numeric[j] and j > 0) else WD_ALIGN_PARAGRAPH.LEFT
        _border(c, top=8, bottom=6)
    for i in range(df.shape[0]):
        for j in range(n_c):
            c = t.cell(i + 1, j); c.text = ""; c.width = widths[j]
            run = c.paragraphs[0].add_run(str(df.iat[i, j])); run.font.size = Pt(size)
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if (numeric[j] and j > 0) else WD_ALIGN_PARAGRAPH.LEFT
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
            _border(c, bottom=8) if i == df.shape[0] - 1 else _border(c)
    # repeat header row on each page
    trPr = t.rows[0]._tr.get_or_add_trPr(); h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)
    if note:
        pn = doc.add_paragraph(); pn.paragraph_format.space_before = Pt(3)
        rn = pn.add_run(note); rn.font.size = Pt(size - 0.5)
    doc.add_paragraph()


def write_tables_docx(T, path, heading=None):
    doc = _docx_base(landscape=False)
    first = True
    for key, (label, title, df, note, land) in T.items():
        if not first:
            _set_orientation(doc, land)
        elif land:
            from docx.enum.section import WD_ORIENT
            from docx.shared import Cm
            s0 = doc.sections[0]; s0.orientation = WD_ORIENT.LANDSCAPE; s0.page_width, s0.page_height = Cm(29.7), Cm(21.0)
        first = False
        add_table(doc, label, title, df, note, size=9 if land else 10, width_cm=25.7 if land else 17.0)
    doc.save(path)


def write_figures_docx(figdir, keys, path, title=None):
    from docx.shared import Cm, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = _docx_base()
    for i, k in enumerate(keys):
        if i:
            doc.add_page_break()
        doc.add_picture(str(Path(figdir) / f"{k}.png"), width=Cm(17.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        lab, cap = FIG_CAPTIONS[k]
        p = doc.add_paragraph(); r = p.add_run(lab + ". "); r.bold = True; p.add_run(cap)
        p.paragraph_format.space_before = Pt(6)
    doc.save(path)


def write_supplement_docx(S, figdir, path, title):
    from docx.shared import Cm, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = _docx_base()
    h = doc.add_paragraph(); r = h.add_run("Supplementary Material"); r.bold = True; r.font.size = Pt(14)
    p = doc.add_paragraph(); r = p.add_run(title); r.italic = True; r.font.size = Pt(11)
    doc.add_paragraph("Contents").runs[0].bold = True
    for k, (lab, ttl, *_r) in S.items():
        doc.add_paragraph(f"{lab}. {ttl}", style=None).paragraph_format.space_after = Pt(0)
    short = {"Figure_S1": "Country profiles of SDG3-PI and its dimensions", "Figure_S2": "Climate vulnerability, temperature anomaly and tree-cover loss",
             "Figure_S3": "Africa Eastern & Southern versus Western & Central", "Figure_S4": "Standardised cluster profiles",
             "Figure_S5": "Conditional indirect effects by cultural construct", "Figure_S6": "Exposure juncture: culture and environmental deprivation",
             "Figure_S7": "Health Belief Model extension: uptake versus mortality",
             "Figure_S8": "Standardised coefficients of the SDG3-PI models"}
    for k, v in short.items():
        doc.add_paragraph(f"{FIG_CAPTIONS[k][0]}. {v}").paragraph_format.space_after = Pt(0)
    doc.add_paragraph("All tables and figures are reproduced by sdg3_nested_geography.py from the study workbook.").runs[0].italic = True
    for k, (lab, ttl, df, note, land) in S.items():
        _set_orientation(doc, land)
        add_table(doc, lab, ttl, df, note, size=8 if land else 9, width_cm=25.7 if land else 17.0)
    _set_orientation(doc, False)
    for i, k in enumerate([k for k in FIG_CAPTIONS if k.startswith("Figure_S")]):
        if i:
            doc.add_page_break()
        doc.add_picture(str(Path(figdir) / f"{k}.png"), width=Cm(16.5) if k not in ("Figure_S1", "Figure_S8") else Cm(12.5))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        lab, cap = FIG_CAPTIONS[k]
        p = doc.add_paragraph(); r = p.add_run(lab + ". "); r.bold = True; p.add_run(cap)
    doc.save(path)


def headline_numbers(R):
    D, E, M, SP, H = R["D"], R["E"], R["M"], R["SP"], R["H"]
    b = M["base"].set_index("Effect")
    t2 = E["res"]["(2) + structural controls Z"][0]
    t6 = E["res"]["(6) + cultural constructs"][0]
    iq = R["ineq"].set_index("code")
    comp = R["comp"].set_index("Measure")
    out = {
        "PI_mean": D["SDG3-PI"].mean(), "PI_median": D["SDG3-PI"].median(), "PI_sd": D["SDG3-PI"].std(),
        "PI_min": D["SDG3-PI"].min(), "PI_min_country": D["SDG3-PI"].idxmin(), "PI_max": D["SDG3-PI"].max(),
        "PI_max_country": D["SDG3-PI"].idxmax(), "n_halfway": int((D["SDG3-PI"] >= 50).sum()),
        "dim_means": {c: D[c].mean() for c in DIMS}, "AFE_minus_AFW": comp.loc["SDG3-PI", "Difference"],
        "AFE_AFW_p": comp.loc["SDG3-PI", "Welch t p"], "UHC_gap": comp.loc["UHC", "Difference"],
        "theil_between_WB": iq["Between AFE/AFW (% of T)"].to_dict(), "theil_between_AU": iq["Between AU regions (% of T)"].to_dict(),
        "gini": iq["Gini"].to_dict(), "benchmarks": iq["Countries at 2030 benchmark"].to_dict(),
        "moran": SP["moran"].set_index("Variable")[["Moran's I", "p (9,999 permutations)"]].to_dict("index"),
        "lisa": SP["ssa"].groupby("LISA")["country"].apply(list).to_dict(),
        "cluster_profiles": SP["prof"].to_dict("index"), "members": SP["members"].to_dict(),
        "m2": t2.to_dict("index"), "m6": t6.to_dict("index"),
        "adjR2": {k: v[1] for k, v in E["res"].items()},
        "dev": E["dev"].round(2).to_dict("index"), "dev_info": E["dev_info"],
        "mediation": b.round(4).to_dict("index"), "expo": M["expo"].round(4).to_dict("records"),
        "sens": M["sens"].round(4).to_dict("records"), "hbm": H.round(4).to_dict("records"),
        "dimres": {k: v[0].round(4).to_dict("index") for k, v in E["dimres"].items()},
    }
    return json.loads(json.dumps(out, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))


# =============================================================================
# Main
# =============================================================================


# =============================================================================
# Run Sections 1-8
# =============================================================================
def run_analysis(xlsx, boot=250, gapref=100, verbose=True):
    """Run the full analysis on the study workbook and return the results dictionary used by every script."""
    say = print if verbose else (lambda *a, **k: None)
    say("Sections 1-2  screening and SDG3-PI"); d, orig, screen, cmap = stage1_clean(xlsx)
    D, norm, steps, wtab, rob, kx = stage2_index(d)
    say("Section 3     constructs and multiple imputation"); C = stage3_constructs(d, D)
    say("Section 4     nested inequality"); ineq, comp, au, reg = stage4_inequality(d, D)
    say("Section 5     spatial analysis"); SP = stage5_spatial(C["K0"], D, n_ref=gapref)
    say("Section 6     econometrics"); E = stage6_econometrics(C["mi"], C["K0"], SP["W"])
    say("Section 7     mediation (bootstrap)"); M = stage7_mediation(C["mi"], B=boot)
    say("Section 8     Health Belief Model extension"); H = stage8_hbm(C["mi"], d)
    SP = {k: v for k, v in SP.items() if k != "W"}  # spatial weights are not needed downstream
    return dict(d=d, orig=orig, screen=screen, cmap=cmap, D=D, steps=steps, wtab=wtab, rob=rob, kx=kx, C=C, ineq=ineq,
                comp=comp, au=au, reg=reg, SP=SP, E=E, M=M, H=H)
