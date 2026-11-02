
# Data Quality Findings

## 1. Dataset overview

I started by inspecting `cleaned_studyu_data.csv` to understand its structure and check for anything that might affect further analysis.

The dataset contains 2,160 rows and 42 columns, with 36 `invite_code` values and 60 rows per group.

The `imputed` column shows that 1,856 rows are marked as imputed and 304 are not. According to the dataset description, missing trial data were imputed using an adapted Baseline Observation Carried Forward (BOCF) method, using information from participants' baseline surveys.

Imputed rows often have missing values in fields such as `measurement_date`, `days_since_start`, `actual_phase`, and `menstruating`. However, some inferred fields, such as `inferred_day_of_study` and `inferred_phase`, still have values.

The baseline survey variable associated with question 7 has 304 non-missing values and 1,856 missing values, matching the counts of non-imputed and imputed rows. I haven't confirmed why these counts match.

I also noticed that `id` and `unique_id` are not always the same. In the first row, for example, `id` is `ID06`, while `unique_id` is `ID01`. The `is_survey1` field is True on dated rows and missing on imputed rows in the initial inspection, but I haven't looked into its meaning yet.

## 2. Investigating ID02's timeline

I used `inspect_timeline.py` to examine the participant with the most non-imputed rows. The script selected `ID02`, which has 60 rows: 48 non-imputed and 12 imputed.

The `inferred_day_of_study` values cover every integer from 0 to 59 exactly once, with no repeated or missing study-day values.

### Study-day difference

I compared `days_since_start` with `inferred_day_of_study` wherever both values were available. I found 13 rows where `days_since_start` was one greater than `inferred_day_of_study`.

The affected dates were:

- 2025-02-14
- 2025-02-20
- 2025-02-28
- 2025-03-01
- 2025-03-02
- 2025-03-03
- 2025-03-05
- 2025-03-09
- 2025-03-12
- 2025-03-20
- 2025-04-01
- 2025-04-02
- 2025-04-06

I haven't found an explanation for this one-day difference yet.

### Phase difference

I also compared `actual_phase` and `inferred_phase`. There was one disagreement for ID02, on 2025-02-09:

- `actual_phase`: B
- `inferred_phase`: A1
- `inferred_day_of_study`: 3
- `imputed`: False

The previous day had A1 in both phase fields, and the following day had B in both. The disagreement occurs at a phase transition, but I haven't confirmed the rules used to assign these fields.

### Imputed rows

The 12 imputed rows for ID02 have no `measurement_date` or `actual_phase` value, but they still contain inferred timeline information.

Ten rows have inferred phase B, and two have inferred phase A2. The inferred menstruation status is False for 10 rows and True for two.

## 3. Checking the validation file

I inspected `study_flow_validation.csv` to see how its information compares with the main dataset.

The file contains 36 rows and 17 columns. For ID02, the validation record reports:

- `valid`: True
- `pattern`: A1-B-A2
- `num_measurements`: 48
- `num_measurements_A1`: 3
- `num_measurements_B`: 20
- `num_measurements_A2`: 25
- `len_A1`: 4
- `len_B`: 29
- `len_A2`: 27
- `num_phases`: 3

The phase-specific measurement counts add up to 48, matching the number of non-imputed rows. The phase lengths add up to 60, matching the total number of rows.

The phase lengths also match the counts obtained by grouping ID02's rows by `inferred_phase`. The last measurement date in the validation record is 2025-04-06, matching the last dated observation in the main dataset.

I haven't confirmed the exact criteria behind `valid=True`, so I can't say precisely what the validation flag guarantees.

## 4. Checking the variable lookup

I inspected `variable_lookup.csv`, which contains 70 rows and 8 columns. It includes baseline survey questions about menstrual pain, symptoms, medication, cycle characteristics, physical activity, and general health.

I searched the English column names, questions, and labels for `phase`, `menstru`, `pain`, and `cycle`. The search for `phase` returned no matches. The other searches found menstrual-health-related variables, but they didn't explain how the trial's phase and study-day fields were assigned.

## 5. What I still need to investigate

I tried opening the two GitHub repositories listed in the dataset record:

- [MPIS study-data evaluation](https://github.com/valeriatisch/mpis-study-data-evaluation)
- [MPIS study-report app](https://github.com/valeriatisch/mpis-study-report-app)

Both returned 404 pages, so I couldn't inspect their source code.

The study protocol describes the cycle-adaptive trial design, but I haven't found enough information to explain the differences between the timeline and phase fields.

For now, I've left the original data unchanged. My next step is to check whether the same patterns occur in other participants and look for more information about how these fields were defined.

## 6. Checking imputation across phases

I wanted to see whether imputed rows were distributed equally across the three inferred phases. I counted the imputed and non-imputed rows in A1, A2, and B.

A1 had 197 imputed rows out of 334 (59.0%), A2 had 759 out of 798 (95.1%), and B had 900 out of 1,028 (87.5%).

I noticed that A2 had a much higher percentage of imputed rows than A1. B also had a high percentage.

Since 17 participants had no non-imputed rows at all, I repeated the calculation using only the other 19 participants.

The percentages were lower, but the pattern was the same: A1 had 37.4% imputed rows, A2 had 89.3%, and B had 77.1%.

So, excluding participants whose entire timelines were imputed did not change the overall pattern. I still don't know why the percentages differ between phases.

## 7. Checking imputation for individual participants

I also counted the imputed and non-imputed rows for each participant in each inferred phase.

The results showed that participants don't all have the same amount of non-imputed data in each phase. For example, ID01–ID04 had non-imputed rows in all three phases, while ID15 had non-imputed rows only in B. ID17 had no A2 phase in its inferred timeline.

Some participants had no non-imputed rows in A2, B, or both. This is worth looking into because it means that the amount of measured data available for each participant differs between phases.

I haven't calculated the imputation percentages for each participant yet.

## 8. Next step

Next, I want to calculate the imputation percentage for each participant in each phase. This should help me see whether the high percentages in A2 and B are common across participants or mainly due to a few of them.

After that, I'll decide whether there are any other data-quality issues I need to investigate before moving on to exploring pain, symptoms, and the other variables.

## Sources

- MPIS Study Data, Zenodo: https://zenodo.org/records/21538147
- MPIS study protocol, medRxiv: https://www.medrxiv.org/content/10.1101/2025.09.20.25336223v1
- Evaluation repository listed in the dataset record: https://github.com/valeriatisch/mpis-study-data-evaluation
- Study-report app repository listed in the dataset record: https://github.com/valeriatisch/mpis-study-report-app
