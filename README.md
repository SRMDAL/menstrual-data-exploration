# Menstrual Data Exploration

A small data exploration project using the Menstrual Pain Intervention Among Students (MPIS) dataset.

The goal is to understand the structure of the dataset, examine missing and imputed data, and explore the recorded outcomes across the study phases.

Detailed findings are documented in [Data Quality Findings](notes/data_quality_findings.md).

## Dataset

The project uses the MPIS Study Data Zenodo dataset:

- **Source:** [Zenodo – MPIS Study Data](https://zenodo.org/records/21538147)
- **Version:** 1.0
- **Published:** January 3, 2026
- **License:** CC BY 4.0

The dataset contains 60-day trial records from 36 participants. It includes self-reported pain, painkiller use, mood, symptoms, and other study information.

The dataset is not included in this repository. Download it separately and place the cleaned CSV file in the `data/` folder as `cleaned_studyu_data.csv`.

## What I explored

- Dataset structure, columns, and missing values.
- Imputed and non-imputed records.
- Differences between recorded and inferred timelines.
- Baseline menstrual history.
- Pain, painkiller use, mood, and symptom counts across study phases.
- Descriptive statistics and visualisations of average, zero, and non-zero outcome values using non-imputed records.

## Tools

- Python
- pandas
- Matplotlib

## Running the scripts

Create and activate a Python virtual environment, then install the required packages:

    python -m pip install pandas matplotlib

Place the dataset in the `data/` folder and run the scripts from the project root. For example:

    python src/inspect_data.py
    python src/explore_observed_outcomes.py
    python src/plot_observed_outcomes.py

## Limitations

- The dataset contains a large number of imputed records.
- The number of non-imputed observations differs across study phases.
- Some participants have no non-imputed records.
- The exact process used to generate all inferred timeline values could not be established from the available documentation.
- The outcome comparisons are descriptive. They do not establish that the intervention caused any observed differences.

This project is an exploratory analysis of the available dataset, not an evaluation of the intervention's effectiveness.