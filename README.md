# Nested geography of health inequality in Sub-Saharan Africa

Code and data for the article **"Nested geography of health inequality: environmental deprivation, development
inequality and the uneven pursuit of SDG 3 across Sub-Saharan Africa"**.

An open, provenance-aware informatics pipeline (ingestion and screening, harmonisation, multiple imputation,
index engine, six analytic modules, quality-assurance and reproducibility layers; manuscript Fig. 1 and Table 2).
It builds a 14-indicator SDG 3 Performance Index (SDG3-PI) for 48 Sub-Saharan African countries, records the
provenance of every data cell, and relates performance to environmental deprivation, climate vulnerability, poverty, health-system pressure, governance,
culture and health beliefs, using nested Theil decomposition, spatial autocorrelation, k-means typology,
multiply imputed regression and moderated serial-parallel mediation. Every number, table and figure in the
manuscript and its Supplementary Material is produced by the scripts in this repository. Version 1.1.0 follows the numbering
of the Informatics and Health submission.

## Repository structure

```
sdg3-nested-geography/
|-- data/
|   |-- Study_Data_Sources_updated_v1.xlsx   study workbook (48 countries, latest available values)
|   `-- README.md                            variables and original sources
|-- src/sdg3_nested_geography/
|   `-- core.py                              analysis library (Sections 1-8) and shared helpers
|-- scripts/
|   |-- 00_run_analysis.py                   runs Sections 1-8 and caches the results
|   |-- make_all.py                          rebuilds every table, figure and Word file
|   |-- _bootstrap.py                        shared paths, cache loader and writers
|   |-- tables/                              one script per table (Tables 1-5, S1-S31)
|   `-- figures/                             one script per figure (Figures 1-8, S1-S8, graphical abstract)
|-- outputs/                                 created when the scripts run
|-- requirements.txt
|-- CITATION.cff
`-- LICENSE
```

## Quick start

```bash
git clone https://github.com/[username]/sdg3-nested-geography.git
cd sdg3-nested-geography
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/make_all.py                              # everything (about 2-3 minutes)

# or one item at a time (the first call runs and caches the analysis):
python scripts/tables/table_04_determinants.py
python scripts/figures/figure_04_maps.py
```

Outputs are written to `outputs/`: `tables/` (CSV), `tables_docx/` (one Word file per table), `figures/`
(PNG, 600 dpi), `docx/` (All_Tables, All_Figures, Supplementary_Material) and `results.json` (headline numbers
quoted in the text).

## Reproducibility

* Random seeds are fixed: imputation (`random_state` 100-119), bootstrap (`default_rng(2026)`), permutation
  tests (`seed 12345`), gap statistic (`default_rng(7)`), k-means (`random_state 0`).
* Missing values are multiply imputed (m = 20, chained equations with posterior draws); estimates are pooled with
  Rubin's rules.
* Mediation intervals use 5,000 bias-corrected bootstrap resamples of countries (250 per imputation).
* Maps use Natural Earth boundaries bundled with geopandas < 1.0. Map lines do not necessarily depict accepted
  national boundaries.

## Script to manuscript map

### Tables

| Script | Manuscript item |
|---|---|
| `scripts/tables/table_01_data_model.py` | Table 1. Data model: constructs, indicators, treatment and sources (48 countries, most recent available values) |
| `scripts/tables/table_02_pipeline_modules.py` | Table 2. Pipeline modules, design decisions and built-in checks |
| `scripts/tables/table_03_nested_inequality.py` | Table 3. Nested inequality in SDG 3 indicators: population-weighted Gini and Theil indices and the share of inequality lying between regions |
| `scripts/tables/table_04_determinants.py` | Table 4. Determinants of SDG3-PI: standardised OLS coefficients (robust standard errors in parentheses) |
| `scripts/tables/table_05_mediation.py` | Table 5. Serial–parallel mediation of environmental risk through poverty and health-system pressure (standardised estimates) |
| `scripts/tables/table_S01_workbook_mapping.py` | Table S1. Workbook columns mapped to the constructs of the conceptual framework |
| `scripts/tables/table_S02_data_quality.py` | Table S2. Data-quality checks and actions taken |
| `scripts/tables/table_S03_source_appraisal.py` | Table S3. Appraisal of data sources and decisions |
| `scripts/tables/table_S04_index_indicators.py` | Table S4. SDG3-PI indicators: properties and log-transformation decision |
| `scripts/tables/table_S05_goalposts.py` | Table S5. Goalposts used to rescale each indicator to 0–100 and resulting scores |
| `scripts/tables/table_S06_weights.py` | Table S6. Weights within SDG3-PI dimensions |
| `scripts/tables/table_S07_kenya_example.py` | Table S7. Worked example of the SDG3-PI computation: Kenya |
| `scripts/tables/table_S08_country_scores.py` | Table S8. SDG3-PI and dimension scores by country (0 = worst observed, 100 = 2030 target) |
| `scripts/tables/table_S09_index_robustness.py` | Table S9. Robustness of SDG3-PI to aggregation choices |
| `scripts/tables/table_S10_pca_loadings.py` | Table S10. Principal-component loadings of composite constructs |
| `scripts/tables/table_S11_validation.py` | Table S11. Validation checks for constructs and alternative measures |
| `scripts/tables/table_S12_climate_components.py` | Table S12. Climate-vulnerability components and composites |
| `scripts/tables/table_S13_descriptives.py` | Table S13. Descriptive statistics of model variables (n = 48) |
| `scripts/tables/table_S14_correlations.py` | Table S14. Correlation matrix of model variables |
| `scripts/tables/table_S15_gaps.py` | Table S15. Absolute and relative gaps between best and worst performers |
| `scripts/tables/table_S16_afe_afw.py` | Table S16. SDG3-PI and dimensions in Africa Eastern & Southern (AFE) versus Western & Central (AFW) |
| `scripts/tables/table_S17_au_regions.py` | Table S17. Mean scores by African Union region (robustness grouping) |
| `scripts/tables/table_S18_morans_i.py` | Table S18. Global spatial autocorrelation (Moran's I) |
| `scripts/tables/table_S19_cluster_number.py` | Table S19. Choosing the number of clusters |
| `scripts/tables/table_S20_cluster_profiles.py` | Table S20. Cluster profiles (means) and member countries |
| `scripts/tables/table_S21_dimension_models.py` | Table S21. Model (2) estimated for each SDG3-PI dimension |
| `scripts/tables/table_S22_supplementary_specifications.py` | Table S22. Supplementary specifications of the SDG3-PI model |
| `scripts/tables/table_S23_diagnostics.py` | Table S23. Regression diagnostics for model (2) |
| `scripts/tables/table_S24_spatial_models.py` | Table S24. Spatial lag and spatial error models (maximum likelihood) for model (2) |
| `scripts/tables/table_S25_mediation_effects.py` | Table S25. All path coefficients and indirect, direct and total effects of the mediation system |
| `scripts/tables/table_S26_moderated_mediation.py` | Table S26. Cultural moderation of the mediation pathways (conditional indirect effects at the 10th, 50th and 90th percentiles) |
| `scripts/tables/table_S27_exposure_juncture.py` | Table S27. Exposure juncture: environmental deprivation regressed on each cultural construct, ln GDP per capita and governance |
| `scripts/tables/table_S28_mediation_robustness.py` | Table S28. Robustness of the mediation results to alternative climate and deprivation measures |
| `scripts/tables/table_S29_sensitivity.py` | Table S29. Sensitivity of the indirect effects to unmeasured mediator–outcome confounding |
| `scripts/tables/table_S30_health_belief_model.py` | Table S30. Health Belief Model extension: health-belief proxies, service uptake and mortality |
| `scripts/tables/table_S31_income_deviants.py` | Table S31. Countries performing furthest above and below the level predicted by income |

### Figures

| Script | Manuscript item | Output |
|---|---|---|
| `scripts/figures/figure_01_system_architecture.py` | Fig. 1 | `outputs/figures/Figure_1.png` |
| `scripts/figures/figure_02_conceptual_framework.py` | Fig. 2 | `outputs/figures/Figure_2.png` |
| `scripts/figures/figure_03_provenance_robustness.py` | Fig. 3 | `outputs/figures/Figure_3.png` |
| `scripts/figures/figure_04_maps.py` | Fig. 4 | `outputs/figures/Figure_4.png` |
| `scripts/figures/figure_05_nested_inequality.py` | Fig. 5 | `outputs/figures/Figure_5.png` |
| `scripts/figures/figure_06_spatial_structure.py` | Fig. 6 | `outputs/figures/Figure_6.png` |
| `scripts/figures/figure_07_mediation_paths.py` | Fig. 7 | `outputs/figures/Figure_7.png` |
| `scripts/figures/figure_08_income_deviants.py` | Fig. 8 | `outputs/figures/Figure_8.png` |
| `scripts/figures/figure_S01_country_profiles.py` | Fig. S1 | `outputs/figures/Figure_S1.png` |
| `scripts/figures/figure_S02_climate_maps.py` | Fig. S2 | `outputs/figures/Figure_S2.png` |
| `scripts/figures/figure_S03_afe_afw.py` | Fig. S3 | `outputs/figures/Figure_S3.png` |
| `scripts/figures/figure_S04_cluster_profiles.py` | Fig. S4 | `outputs/figures/Figure_S4.png` |
| `scripts/figures/figure_S05_conditional_effects.py` | Fig. S5 | `outputs/figures/Figure_S5.png` |
| `scripts/figures/figure_S06_exposure_juncture.py` | Fig. S6 | `outputs/figures/Figure_S6.png` |
| `scripts/figures/figure_S07_health_belief_model.py` | Fig. S7 | `outputs/figures/Figure_S7.png` |
| `scripts/figures/figure_S08_coefficients.py` | Fig. S8 | `outputs/figures/Figure_S8.png` |
| `scripts/figures/graphical_abstract.py` | Graphical abstract | `outputs/figures/Graphical_Abstract.png` |

## Data

All indicators come from public sources (World Bank, WHO, UNICEF, UNAIDS, IHME, WHO/UNICEF JMP, ND-GAIN, OECD
SIGI, Afrobarometer, EPR, V-Dem, HIEF, Wellcome Global Monitor, DHS and others); see `data/README.md`, Table 1
and Table S3. The data remain under the licences of their producers.

## Citation

Please cite the article (details to be added on publication) and this repository (`CITATION.cff`).

## Licence

Code: MIT licence (see `LICENSE`).
