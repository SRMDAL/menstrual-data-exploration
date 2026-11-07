# Data Quality Findings

## 1. Dataset overview

I started by looking at `cleaned_studyu_data.csv` to understand the data and check for possible issues.

The dataset has 2,160 rows and 42 columns. There are 36 `invite_code` values, with 60 rows for each one.

The `imputed` column shows that 1,856 rows are imputed and 304 are not. According to the dataset description, missing trial data were filled in using an adapted Baseline Observation Carried Forward (BOCF) method and information from the baseline surveys.

Many imputed rows have missing values in columns like `measurement_date`, `days_since_start`, `actual_phase`, and `menstruating`. However, columns like `inferred_day_of_study` and `inferred_phase` still have values.

I also noticed that the baseline survey variable for question 7 has 304 non-missing values and 1,856 missing values. These numbers are the same as the counts of non-imputed and imputed rows. I don't know why yet.

Another thing I noticed is that `id` and `unique_id` are not always the same. For example, in the first row, `id` is `ID06`, but `unique_id` is `ID01`.

I also noticed that `is_survey1` is True on dated rows and missing on imputed rows. I haven't checked what this column means yet.

## 2. Looking at ID02's timeline

I used `inspect_timeline.py` to look at the participant with the most non-imputed rows. It selected ID02, which has 48 non-imputed rows and 12 imputed rows.

The `inferred_day_of_study` column contains all values from 0 to 59, with no duplicates or missing days.

### Study-day difference

I compared `days_since_start` with `inferred_day_of_study` wherever both values were available.

For ID02, there were 13 rows where `days_since_start` was one day higher than `inferred_day_of_study`.

These were the dates:

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

I don't know why the two columns have different values on these dates.

### Phase difference

I also compared `actual_phase` and `inferred_phase`.

There was one difference, on 2025-02-09:

- `actual_phase`: B
- `inferred_phase`: A1
- `inferred_day_of_study`: 3
- `imputed`: False

The day before had A1 in both columns, and the next day had B in both. So this difference happens when the phase changes. I haven't found out why the two columns disagree.

### Imputed rows

The 12 imputed rows for ID02 don't have `measurement_date` or `actual_phase`, but they still have inferred timeline information.

Ten of these rows have inferred phase B, and two have A2. The inferred menstruation status is False in 10 rows and True in two.

## 3. Checking the validation file

I looked at `study_flow_validation.csv` to compare it with the main dataset.

It has 36 rows and 17 columns. For ID02, the validation file shows:

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

The measurement counts add up to 48, which is the number of non-imputed rows. The phase lengths add up to 60, which is the total number of rows.

The phase lengths also match what I got when I grouped ID02's rows by `inferred_phase`.

The last measurement date in the validation file is 2025-04-06, the same as the last dated row in the main dataset.

I still don't know exactly what `valid=True` means or what it checks.

## 4. Checking the variable lookup

I looked at `variable_lookup.csv`. It has 70 rows and 8 columns.

It contains baseline survey questions about menstrual pain, symptoms, medication, cycle length, physical activity, and general health.

I searched the English column names, questions, and labels for `phase`, `menstru`, `pain`, and `cycle`.

The search for `phase` didn't return anything. The other searches found some related variables, but nothing that explains how the phase and study-day columns were assigned.

## 5. Checking the documentation

I tried opening the two GitHub repositories listed in the dataset record:

- [MPIS study-data evaluation](https://github.com/valeriatisch/mpis-study-data-evaluation)
- [MPIS study-report app](https://github.com/valeriatisch/mpis-study-report-app)

Both returned 404 pages, so I couldn't look at their code.

I also read the study protocol. It explains how the trial works and mentions that some daily questions were only shown when participants reported cramps or related symptoms.

However, it doesn't explain exactly how missing values were filled in or how the inferred timeline fields were created.

I still haven't found enough information to explain the differences between the timeline and phase columns.

I haven't changed the original data.

## 6. Checking imputation across phases

I wanted to see how many rows were imputed in each phase.

The results were:

- A1: 197 out of 334 (59.0%)
- A2: 759 out of 798 (95.1%)
- B: 900 out of 1,028 (87.5%)

A2 had the highest percentage of imputed rows.

I also noticed that 17 participants had no non-imputed rows at all. So I repeated the calculation using only the other 19 participants.

The percentages were lower, but the pattern was still the same:

- A1: 37.4%
- A2: 89.3%
- B: 77.1%

Removing the participants whose entire timelines were imputed didn't change the overall pattern. I still don't know why A2 and B have so many imputed rows.

## 7. Checking individual participants

I wanted to see how the amount of imputed data differed between participants.

For example, ID01–ID04 had non-imputed rows in all three phases, while ID15 had them only in B. ID17 didn't have an A2 phase in its inferred timeline.

Some participants had no non-imputed rows in A2, B, or both.

I then calculated the imputation percentage for each participant in each phase. I checked the median, minimum, and maximum percentages.

- **A1:** median 33.3%, minimum 0%, maximum 85.7% (19 participants)
- **A2:** median 100%, minimum 7.4%, maximum 100% (18 participants)
- **B:** median 85.2%, minimum 34.5%, maximum 100% (19 participants)

The percentages were also high for individual participants in A2 and B, not just when I counted all the rows together.

ID17 had no A2 phase, which is why there are only 18 participants in that group.

I still don't know why the imputation percentages are so different between phases.

## 8. Checking the sensitivity columns

I compared the four sensitivity columns with their corresponding `_imputed` columns: `pain`, `tablets`, `mood`, and `symptoms_count`.

The values were the same in all non-imputed rows.

All the differences were in imputed rows, and every different sensitivity value was 0.

I then checked all 1,856 imputed rows. All four sensitivity columns had 0 in every row. There were no missing values or other values.

So these columns have the same values as the `_imputed` columns in non-imputed rows, but contain only zeros in imputed rows.

I don't know why they were created this way. They might be used for a sensitivity analysis that leaves out imputed values, but I haven't found anything in the documentation to confirm that.

## 9. Checking baseline menstrual history

I wanted to see how the baseline cycle length and period duration compared with the inferred timelines.

I checked three participants: ID02, ID26, and ID27.

**ID02**

- Reported cycle length: 30 days
- Reported period duration: 7 days
- Inferred period starts: study days 0, 26, and 54
- All 12 imputed pain values were 0.
- Its baseline average pain was 5 and worst pain was 8.

**ID26**

- Reported cycle length: 28 days
- Reported period duration: 6 days
- Inferred period starts: study days 1 and 28
- Both periods had the same imputed pain values: 6, 5, 5, 4, 4, 0.

**ID27**

- Reported cycle length: 24 days
- Reported period duration: 7 days
- Inferred period starts: study days 1, 24, and 47
- All three periods had the same imputed pain values: 8, 7, 7, 7, 6, 0, 0.

For ID26 and ID27, the inferred period durations match the baseline answers. Their imputed pain values also repeat across periods.

These are only three participants, so I can't say if the same patterns happen for everyone.

I still haven't figured out exactly how the imputed values are generated. For now, I'll keep observed and imputed values separate and won't treat imputed values as actual reports from participants.

## 10. Exploring observed outcomes

I wanted to look at the four main outcomes using only non-imputed rows.

There were 304 non-imputed rows:

- A1: 127
- B: 138
- A2: 39

All 304 rows had values for `pain`, `tablets`, `mood`, and `symptoms_count`.

I calculated the average and median for each outcome in each phase.

The average values were:

- **Pain:** A1 = 1.28, B = 0.48, A2 = 0.23
- **Tablets:** A1 = 0.10, B = 0.10, A2 = 0
- **Mood:** A1 = 0.66, B = 0.21, A2 = 0.08
- **Symptoms count:** A1 = 1.16, B = 0.36, A2 = 0.15

The median was 0 for all four outcomes in all three phases.

I also counted how many values were zero. A1 had more non-zero pain, mood, and symptom values than B and A2. For tablets, A1 and B both had 9 non-zero values, while A2 had none.

A2 had much fewer non-imputed rows than the other phases, so I need to keep that in mind when comparing the results.

These are just comparisons between the phases. They don't show that the intervention caused the differences.

I only used non-imputed values for this check.

## Sources

- MPIS Study Data, Zenodo: https://zenodo.org/records/21538147
- MPIS study protocol, medRxiv: https://www.medrxiv.org/content/10.1101/2025.09.20.25336223v1
- Evaluation repository listed in the dataset record: https://github.com/valeriatisch/mpis-study-data-evaluation
- Study-report app repository listed in the dataset record: https://github.com/valeriatisch/mpis-study-report-app