#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table 1. Data model: constructs, indicators, treatment and sources (48 countries, most recent available
values)

Location : Manuscript, main text
Inputs   : cached analysis results (Section 3 constructs (PCA variance))
Outputs  : outputs/tables/Table_1.csv and outputs/tables_docx/Table_1.docx
Run      : python scripts/tables/table_01_data_model.py   (from the repository root)

Formatting follows the journals' table requirements: editable Word table, black text, no shading,
horizontal rules only (top, under the header and at the bottom), notes below the table.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _bootstrap import load_results, save_table  # noqa: E402
from sdg3_nested_geography.core import *  # noqa: E402,F401,F403  (pandas as pd, numpy as np, labels, constants)
from sdg3_nested_geography.core import _f, _p, _star, _ci  # noqa: E402,F401  (number formatting)


def build(R):
    """Return (label, title, DataFrame, note, landscape) for Table 1."""
    ve = R["C"]["loads"].groupby("Construct")["Variance explained"].first()
    rows = [
        ("Y – Maternal health", "Maternal mortality ratio (3.1.1); skilled birth attendance (3.1.2); adolescent birth rate (3.7.2); demand for family planning satisfied by modern methods (3.7.1)",
         "Rescaled to 0–100 against 2030 targets; MMR logged", "WHO/MMEIG; UNICEF; UN DESA"),
        ("Y – Child health", "Under-5 mortality (3.2.1); neonatal mortality (3.2.2); DTP3 coverage (3.b.1); stunting (2.2.1)",
         "As above; under-5 mortality logged", "UN IGME; WHO/UNICEF WUENIC; UNICEF/WHO/World Bank JME"),
        ("Y – Communicable disease", "HIV incidence (3.3.1); TB incidence (3.3.2); malaria incidence (3.3.3); malaria mortality",
         "As above; all logged", "UNAIDS; WHO Global TB and World Malaria Reports"),
        ("Y – Universal health coverage", "UHC service coverage index (3.8.1); out-of-pocket share of current health expenditure",
         "As above", "WHO/World Bank UHC monitoring; WHO GHED"),
        ("X₁ – Climate vulnerability", "ND-GAIN exposure, sensitivity and adaptive-capacity deficit; CHRI; temperature anomaly and drought (robustness)",
         "Mean of the three ND-GAIN components (0–1)", "ND-GAIN; World Bank CCKP"),
        ("X₂ – Environmental deprivation", "Population without basic drinking water (6.1.1) or safely managed sanitation (6.2.1); polluting cooking fuels (7.1.2); ambient PM2.5",
         f"First principal component ({ve[BLOCK_LABEL['X2']] * 100:.1f}% of variance)", "WHO/UNICEF JMP; WHO Household Energy Database; GBD"),
        ("M₁ – Poverty", "Extreme poverty headcount ($3.00 a day, 2021 PPP)", "Percentage", "World Bank PIP"),
        ("M₂ – Health-system pressure", "CMNN DALYs per physician, nurse and midwife", "Natural logarithm", "IHME GBD; WHO NHWA"),
        ("Z – Institutional capacity and development", "Government effectiveness, political stability, control of corruption; GDP per capita (PPP); health expenditure per capita; urban share; female mean years of schooling",
         f"Governance = first principal component ({ve[BLOCK_LABEL['GOV']] * 100:.1f}%); money values logged", "WGI; WDI; WHO GHED; UN WPP; UNDP HDR"),
        ("C-A – Gender normative regime", "SIGI 2023; women's participation in own health-care decisions; SDG 5.6.1; child marriage (5.3.1)",
         f"First principal component ({ve[BLOCK_LABEL['C_A']] * 100:.1f}%)", "OECD; DHS; UNFPA; UNICEF"),
        ("C-B – Social cohesion and trust", "Interpersonal and institutional trust; politically excluded population; exclusion by social group; ethnic fractionalisation",
         f"First principal component ({ve[BLOCK_LABEL['C_B']] * 100:.1f}%)", "Afrobarometer; EPR; V-Dem; HIEF"),
        ("C-C – Health-cultural orientation", "Vaccine confidence; trust in doctors, nurses and scientists",
         f"First principal component ({ve[BLOCK_LABEL['C_C']] * 100:.1f}%)", "Wellcome Global Monitor"),
        ("C-D – Cultural-ecological practice", "Kinship intensity and ancestral subsistence; households where women or girls collect water",
         f"First principal component ({ve[BLOCK_LABEL['C_D']] * 100:.1f}%)", "Giuliano and Nunn (2018); WHO/UNICEF JMP"),
    ]
    return ("Table 1", "Data model: constructs, indicators, treatment and sources (48 countries, most recent available values)",
               pd.DataFrame(rows, columns=["Construct", "Indicators (SDG code)", "Treatment", "Source"]),
               "Note: SDG3-PI = geometric mean of the four Y dimensions. Missing values (at most 10 per variable) were multiply imputed (m = 20). Full mapping of workbook columns in Table S1; source appraisal in Table S3.", False)


def main():
    return save_table(build(load_results()))


if __name__ == "__main__":
    main()
