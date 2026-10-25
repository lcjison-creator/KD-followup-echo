KD FOLLOW-UP ECHOCARDIOGRAPHY - JAHA FIGURES AND TABLES, LOCAL ONE-CLICK REPRODUCTION (v3, October 25, 2026)

v3 regroups the figures into five composite main figures (more panels per figure, fewer supplemental figures). The numbers are
unchanged; Figure 1B (timing of the post-discharge echocardiograms) is new, and the primary-versus-all-data comparison is now a
supplemental table. Every figure passes an automatic layout check before it is saved (no overlapping text, no legend on data).

WHAT THE NOTEBOOK PRODUCES
- Main Figures 1-5 (PDF vector, TIFF 600 dpi LZW, PNG 600 dpi; at most 7.0 x 9.0 in) and main Tables 1-2 (CSV).
- The supplemental figure and 16 supplemental tables (18 CSV files; Tables S2 and S13 have two parts).
- Figure legends and table notes: Figure_legends_and_table_notes_main.txt, Tables_preview_main.txt and
  Supplement_legends_and_notes.json (supplemental legends and notes, keyed by content).
- Descriptive_numbers_v3.json (timing of the 1st-4th post-discharge echocardiograms, quoted in the Results) and
  Figure_sizes_v3.csv (saved size of each figure).
- MANIFEST_sha256.csv of all outputs.
All outputs go to output_kd_jaha_figures_tables_v3/ next to the notebook.

PANELS OF THE MAIN FIGURES
  Figure 1  A study flow; B timing of the 1st-4th echocardiograms after discharge
  Figure 2  A aneurysm and B any involvement by window after discharge; C cumulative incidence of a new aneurysm
  Figure 3  A robustness of the first-visit yield (all alternative analyses); B measurement-noise model; C category at detection
            and at the last report of the aneurysms found at the first visit
  Figure 4  A, B status by day of illness (all children; uncomplicated course); C window of first documentation;
            D course of in-hospital aneurysms by size
  Figure 5  A risk-factor count; B exact in-hospital Z; C age; D risk-based selection; E new aneurysm by risk-factor count;
            F new aneurysm after in-hospital dilation only

FOLDER LAYOUT (keep it as in the repository; the notebook must sit next to inputs/)
code/06_figures_and_tables/
  KD_JAHA_figures_tables_v3.ipynb          <- open this and Run All
  README_how_to_run.txt                     <- this file
  requirements.txt                          <- Python packages
  INPUT_MANIFEST_sha256.csv                 <- SHA-256 of every input; checked by the first code cell
  EXPECTED_OUTPUTS_sha256.csv               <- reference hashes of the tables, legends and notes; checked by the last cell
  inputs/
    locked/                                 <- locked aggregate results (no patient-level data)
      v4/Results_locked_v4.txt
      v4_1/Results_locked_v4_1.txt
      v4_1/Table2_sequential_yield.csv, Table3a_..., Table4a_..., Table4b_..., Table6_..., Table7_...,
           TableM1a_..., TableM1b_... (2), TableM2b_... (3), TableM3a_... (2), TableM3b_..., TableM3c_... (2),
           TableM4a_..., TableS2_..., TableS3_..., TableS4_...             (21 locked CSV tables)
      v4_1/key_numbers_clean.json           <- key_numbers.json of v4.1 with the report excerpts removed
      v4_1/key_numbers_v4_1_modules.json
      v5/Results_locked_v5.txt
      v5/TableV5_1_validation_vs_v4.csv, TableV5_2_P1_sensitivity.csv
      v5/TableV5_4_P1_events.csv            <- research ID column removed
      v5/key_numbers_v5.json
      coronary_v1/Results_locked_coronary_v1.txt
    frozen_patient_level/                   <- research IDs only, no free text; not in the public repository (see DATA PROTECTION)
      cohort_C1_primary.csv                 <- derivation cohort C1 (v4.1), one row per child
      KD_master_index_v1_reduced.parquet    <- 4 columns of the Kit master index (ID, index year, discharge date, C1 flag)
      KD_echo_reports_AHA_v1.parquet        <- per-report AHA categories 2018-2026 (Kit v1)
      KD_echo_reports_combined_v5.parquet   <- per-report combined categories, validation period (Kit v1.1 addendum)
      KD_echo_measure_2025_2026_dates.parquet  <- examination dates of the 2025-2026 structured export (export window only)
      KD_JAHA_covariates_v1.parquet         <- derived covariates per index admission (age, sex, IVIG, laboratory values)
    methods_checks/z_equation_source_check_v3_output_2026-10-25.txt
    comparison/comparison_extraction_v2.csv
  output_kd_jaha_figures_tables_v3/         <- created by the notebook

SOFTWARE
- Python 3.10 or later with the packages in requirements.txt:
    pip install -r requirements.txt
  (or with conda: conda install numpy pandas scipy matplotlib pyarrow pillow jupyter)
- Tested with Python 3.11 in two environments, with identical tables, legends and figure pixels:
    pandas 2.2.3, numpy 1.26.4, scipy 1.13.1, matplotlib 3.8.4, pyarrow 16.1.0
    pandas 3.0.2, numpy 2.4.4, scipy 1.17.1, matplotlib 3.10.9
  If Jupyter reports "cannot import name 'backend2gui'", the IPython and ipykernel versions do not match; install
  ipython==8.27.0 and ipykernel==6.29.5 (or update both to their latest versions).
- Font: Arial (installed on Windows and macOS). Without Arial the notebook falls back to Liberation Sans, which has the same
  metrics, so the layout does not change.

HOW TO RUN
1. Unzip the package anywhere; keep the folder layout above (do not move the notebook out of the folder).
2. Open KD_JAHA_figures_tables_v3.ipynb in Jupyter Lab, Jupyter Notebook or VS Code.
3. Run All. A full run takes about 1 to 3 minutes.
4. Find the results in output_kd_jaha_figures_tables_v3/. The last cell should print
   "24 of 24 tables, legends and notes identical to the reference run".

CHECKS BUILT INTO THE RUN
- Input check (first code cell): every file listed in INPUT_MANIFEST_sha256.csv must be present and unchanged; otherwise the
  run stops and lists the missing or changed files.
- Lock check: the SHA-256 of Results_locked_v4.txt, Results_locked_v4_1.txt and Results_locked_v5.txt must match their locks.
- Number check: every number that also appears in the locked results is asserted while the figures and tables are built; the
  run stops at the first mismatch. Table 1, Figure 1B, Figure 3C and the validation curve of Figure 2C are descriptive additions
  computed from the same frozen data.
- Layout check (before each figure is saved): the run stops if two pieces of text overlap or touch, if a legend covers a line,
  marker, whisker, bar, confidence band or text, if a label inside a panel lies on a line or whisker, if anything falls outside
  the figure, or if the saved figure would be wider than 7.0 in or taller than 9.0 in.
- Output check (last cell): the CSV, TXT and JSON outputs are compared with the reference run. Figure files and
  Figure_sizes_v3.csv are not compared, because the local font and software versions change their bytes but not their content.

FILE NAMES AND SUPPLEMENTAL NUMBERS (as in KD_JAHA_supplemental_material_v2.pdf)
  Figure 1   Figure1_study_flow_and_follow_up
  Figure 2   Figure2_successive_postdischarge_echocardiograms
  Figure 3   Figure3_robustness_and_course_of_first_visit_aneurysms
  Figure 4   Figure4_timing_of_findings_and_course_of_aneurysms
  Figure 5   Figure5_risk_factors_and_selective_echocardiography
  Table 1    Table1_characteristics_uncomplicated_course.csv
  Table 2    Table2_aneurysm_at_first_postdischarge_echo.csv
  Figure S1  FigureS_published_cohorts
  Table S1   TableS_definitions.csv
  Table S2   TableS_z_coefficients.csv (part A) and TableS_z_equations.csv (part B)
  Table S3   TableS_accuracy.csv
  Table S4   TableS_wording.csv
  Table S5   TableS_sensitivity.csv
  Table S6   TableS_plan_b.csv (primary analysis versus all available data)
  Table S7   TableS_selection.csv
  Table S8   TableS_noise.csv
  Table S9   TableS_validation.csv
  Table S10  TableS_validation_events.csv
  Table S11  TableS_management.csv
  Table S12  TableS_z_gradient.csv
  Table S13  TableS_infants.csv (part A) and TableS_infants_firth.csv (part B)
  Table S14  TableS_timing.csv
  Table S15  TableS_strategies.csv
  Table S16  TableS_published.csv
  The supplemental numbers follow the order of first citation in manuscript v2; if the text changes, the numbers may change, but the
  file names do not.

WHERE THE INPUTS COME FROM (audit trail)
1. Hospital exports (Scientific Research Data Platform of Wuhan Children's Hospital): the three Kawasaki disease 30-day re-export
   workbooks (data end September 28, 2026) and the 2025-2026 structured echocardiography export (echo_measure_2025_2026.xlsx).
2. KD_coronary_AHA_v1.ipynb: per-report AHA categories and the Z-equation reconstruction -> Results_locked_coronary_v1.txt.
3. KD Research Kit v1 (KD_master_index_v1, KD_echo_reports_AHA_v1) and its v1.1 addendum (2025-2026 structured table,
   KD_echo_reports_combined_v5).
4. KD_echo_surveillance_v4.ipynb and KD_echo_surveillance_v4_1.ipynb -> Results_locked_v4/v4_1, their CSV tables and
   cohort_C1_primary.csv.
5. KD_echo_surveillance_v5_validation.ipynb -> Results_locked_v5 and its CSV tables (validation plan V5_VALIDATION_PLAN.txt,
   locked October 14, 2026).
6. z_equation_source_check_v3_2026-10-25.py -> the Z-equation check output; build_comparison_v2.py -> comparison_extraction_v2.csv.
7. KD_JAHA_covariates_v1.parquet was frozen from the hospital exports by the cloud version of this notebook
   (KD_JAHA_display_items_v2/v3.ipynb, section 7), with the covariate definitions of the locked v4/v4.1 analysis; the notebook checks
   that it reproduces the locked Table 4b counts.
The input check accepts a file only if its SHA-256 matches INPUT_MANIFEST_sha256.csv. key_numbers_clean.json,
KD_master_index_v1_reduced.parquet, KD_echo_measure_2025_2026_dates.parquet, KD_JAHA_covariates_v1.parquet and the copy of
TableV5_4 were made for this release.

DATA PROTECTION
- inputs/frozen_patient_level/ holds patient-level data under research identifiers (no names, hospital numbers or free text).
  It is not part of the public repository; the files are available from the corresponding authors on reasonable request with
  approval of the Ethics Committee of Wuhan Children's Hospital (2024R034-E02).
- No report, discharge or outpatient text is included. The report excerpts stored in the original v4.1 key_numbers.json were
  removed (key_numbers_clean.json), and the research ID column was removed from the copy of TableV5_4.
- The public repository holds the notebook, requirements.txt, this README and inputs/locked, inputs/methods_checks and
  inputs/comparison.
