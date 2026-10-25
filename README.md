# Echocardiography After an Uncomplicated In-Hospital Course of Kawasaki Disease

Code and aggregate results for the manuscript *Echocardiography After an Uncomplicated In-Hospital Course of Kawasaki Disease:
Yield of Successive Post-Discharge Examinations* (Changjian Li, Yong Zhang, Dan Hu). The citation and archive DOI will be
added on publication.

Retrospective cohort study at Wuhan Children's Hospital, Wuhan, China: derivation cohort of index admissions 2018–2024 (2021
excluded) and temporal validation cohort from March 8, 2025. Ethics approval: Ethics Committee of Wuhan Children's Hospital,
2024R034-E02.

## Contents

| Folder | What it holds |
|---|---|
| `code/01_coronary_classification` | Per-report American Heart Association coronary category from the echocardiography report text, and the reconstruction of the laboratory Z-score equation (`KD_coronary_AHA_v1.ipynb`). |
| `code/02_derivation` | Derivation analysis: v4 (locked September 30, 2026) and v4.1, which adds the modules on selection, measurement noise, risk-based strategies and management (plan written October 1, 2026, before their outcomes were examined). |
| `code/03_temporal_validation` | Temporal validation (`KD_echo_surveillance_v5_validation.ipynb`) and its plan (`V5_VALIDATION_PLAN.txt`, locked October 14, 2026, before any validation outcome was computed; SHA-256 `8d6b811b2d42ac80cdc4438b7adbeb9623e39ff962899e710c72c0c6f482065f`). |
| `code/04_methods_checks` | Which published Z-score equation reproduces the reported Z values; observed timing of follow-up visits. |
| `code/05_published_cohorts` | Check of the counts extracted from published cohorts against the article text (the article PDFs are not included). |
| `code/06_figures_and_tables` | One-click notebook that rebuilds every figure and table of the article (Figures 1–5, Tables 1–2, Figure S1, Tables S1–S16) from the locked aggregate results in `inputs/locked/` and the frozen research-ID tables (not included, see below). Every number that also appears in the locked results is asserted during the run. See `README_how_to_run.txt`. |
| `results/display_items` | The figures (PDF, PNG), tables (CSV), legends and table notes produced by that notebook. |
| `results/methods_checks`, `results/published_cohorts` | Outputs of the scripts in `code/04` and `code/05`. |

The locked result files (`Results_locked_v4.txt`, `Results_locked_v4_1.txt`, `Results_locked_v5.txt`,
`Results_locked_coronary_v1.txt`) and the aggregate tables written with them are in `code/06_figures_and_tables/inputs/locked/`.
The notebooks are stored without outputs.

## Data availability

The patient-level data are pseudonymized (research identifiers only) and are not public. They are available from the
corresponding authors on reasonable request with approval of the Ethics Committee of Wuhan Children's Hospital. The notebooks in
`code/01`–`code/03` read the hospital data exports and the study's internal frozen tables, which are not included; they are
provided so that every analytic step can be read. With the frozen tables listed in
`code/06_figures_and_tables/inputs/frozen_patient_level/README.md`, the figures and tables can be rebuilt exactly; without
them, the first code cell of the notebook lists the missing files.

## Software

Python 3.11 with numpy, pandas, scipy, matplotlib, pyarrow, pillow and Jupyter (`code/06_figures_and_tables/requirements.txt`).
The figure and table notebook was tested with pandas 2.2.3 (numpy 1.26.4, matplotlib 3.8.4) and pandas 3.0.2 (numpy 2.4.4,
matplotlib 3.10.9); both runs gave identical tables, legends and figure pixels.

## License

Code: MIT License (`LICENSE`). Aggregate results, figures and tables: Creative Commons Attribution 4.0 International (CC BY 4.0).
