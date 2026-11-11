# Data

`Study_Data_Sources_updated_v1.xlsx`, sheet **Data Composites**: one row per country (49 rows; Djibouti is
dropped in the analysis because the World Bank classifies it outside Sub-Saharan Africa), one column per
indicator, holding the most recent value published by each custodian agency at compilation. Columns are read
by name (see `COLMAP` in `src/sdg3_nested_geography/core.py`). Full screening decisions are in Table S2 and the
source appraisal in Table S3.

| Code | Workbook column | Use in the framework |
|---|---|---|
| `MMR` | Maternal mortality ratio (SDG 3.1.1) | Y – Maternal health |
| `SBA` | Skilled birth attendance (3.1.2) | Y – Maternal health |
| `ABR` | Adolescent birth rate (3.7.2); | Y – Maternal health |
| `FP` | Demand for family planning satisfied by modern methods (3.7.1) | Y – Maternal health |
| `U5MR` | Under-5 mortality (3.2.1) | Y – Child health |
| `NMR` | Neonatal mortality (3.2.2) | Y – Child health |
| `DTP3` | DTP3 immunisation (3.b.1) | Y – Child health |
| `MCV1` | MCV1 immunisation (3.b.1) | Not used |
| `STUNT` | Stunting (2.2.1) | Y – Child health |
| `HIV` | HIV incidence (3.3.1) | Y – Communicable |
| `TB` | TB incidence (3.3.2) | Y – Communicable |
| `MAL_INC` | Malaria incidence (3.3.3) | Y – Communicable |
| `MAL_MORT` | Malaria mortality rate | Y – Communicable |
| `SCI` | UHC service coverage index (3.8.1) | Y – UHC |
| `FINHARD` | Financial hardship in health and components (3.8.2, 2024 definition) >10% of total budget on health (%) | Descriptive only |
| `OOP` | Out-of-pocket (OOP) share of current health expenditure | Y – UHC |
| `WATER_B` | Safely managed drinking water (6.1.1) - at least basic drinking water | X₂ |
| `SAN_SM` | Safely managed sanitation (6.2.1a) | X₂ |
| `CLEANFUEL` | Clean cooking fuels (7.1.2) | X₂ |
| `PM25` | Ambient PM2.5 | X₂ |
| `TREELOSS` | Tree-cover loss (%) - 2000-2025 | Land degradation (robustness) |
| `TEMPANOM` | Recent Annual Temperature Anomaly (°C) | X₁ observed hazard (robustness) |
| `SPEI` | Drought (SPEI) | X₁ observed hazard (robustness) |
| `ND_E` | ND-GAIN Exposure | X₁ (exposure) |
| `ND_S` | ND-GAIN Sensitivity | X₁ (sensitivity) |
| `ND_AC` | ND-GAIN Adaptive capacity | X₁ (capacity deficit) |
| `CH_E` | CHRI Exposure | X₁ robustness (CHRI) |
| `CH_S` | CHRI Sensitivity | X₁ robustness (CHRI) |
| `CH_AC` | CHRI Adaptive capacity | X₁ robustness (CHRI) |
| `CMNN_DALY` | Communicable, maternal, neonatal and nutritional (CMNN) DALYs | M₂ numerator |
| `AP_MORT` | Air Pollution Mortality (3.9.1) | Not used (outcome-like) |
| `WASH_DEATHS` | Unsafe WASH Mortality (3.9.2) | X₂ validation (as rate) |
| `GDPPC` | GDP per capita (PPP) | Z |
| `POV_A` | Extreme poverty ($3.00/day, 2021 PPP); | M₁ (duplicate) |
| `GINI` | Gini | Descriptive |
| `UNEMP` | Unemployment | Descriptive |
| `GOVEXP` | Government expenditure (% GDP) | Descriptive |
| `POU_A` | Prevalence of undernourishment (2.1.1) | M₁ (second indicator) |
| `FIES` | Moderate or severe food insecurity (2.1.2) | Descriptive |
| `POPGROW` | Population growth | Z – demographic |
| `TFR` | Fertility | Z – demographic |
| `URBAN` | Urban share | Z |
| `DENSITY` | Density | Z – demographic |
| `AGEDEP` | Age dependency | Z – demographic |
| `POP_M` | Demographic (in millions) | Population weights |
| `FSCH_A` | Female mean years of schooling | Not used |
| `FLFP_A` | Female labour-force participation | Not used |
| `GII` | Gender Inequality Index | Removed |
| `HDI` | HDI | Removed |
| `GOVEFF` | Government effectiveness index | Z (governance) |
| `POLSTAB` | Political stability | Z (governance) |
| `CORRUPT` | Control of corruption | Z (governance) |
| `HEPC` | Health expenditure per capita | Z |
| `PHYS` | Physicians per 10,000 | M₂ denominator |
| `NURSE` | Nurses & midwives per 10,001 | M₂ denominator |
| `POV` | Extreme poverty headcount ($3.00/day, 2021 PPP) | M₁ |
| `POU_B` | Prevalence of undernourishment (2.1.1).1 | Not used |
| `FSCH` | Female mean years of schooling (years) | Z |
| `FLFP` | Female labour-force participation.1 | Z |
| `SIGI` | Social Institutions and Gender Index (SIGI) 2023 | C-A |
| `DHSDEC` | DHS women's health-decision participation | C-A |
| `SDG561` | SDG 5.6.1 - women aged 15–49 (married or in a union) who make their own informed decisions regarding sexual relations, contraceptive use, and reproductive health care | C-A |
| `CHILDMAR` | Child marriage - SDG 5.3.1 | C-A |
| `TRUST` | Interpersonal and institutional trust (incl. health services) | C-B |
| `EXCL_EPR` | Politically excluded population share | C-B |
| `EXCL_VDEM` | Exclusion by social group | C-B |
| `ETHFRAC` | Ethnic fractionalisation | C-B |
| `VACCONF` | Vaccine confidence (safety, effectiveness, importance) | C-C |
| `TRUSTDOC` | Trust in doctors, nurses and scientists | C-C |
| `RELIG` | Religious composition and religiosity | Descriptive |
| `KINSHIP` | Kinship intensity, matrilineality, ancestral subsistence mode | C-D |
| `WATERCOLL` | Share of households where women or girls collect water | C-D |
