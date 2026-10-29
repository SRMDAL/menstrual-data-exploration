from pathlib import Path
import pandas as pd


# Load the dataset.
project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "cleaned_studyu_data.csv"
df = pd.read_csv(data_path)

# Count non-imputed rows per group.
counts = df[df["imputed"] == False].groupby("invite_code").size()

# Select the group with the most non-imputed rows.
example_code = counts.idxmax()

print(f"Selected invite code: {example_code}")
print(f"Non-imputed rows: {counts.max()}")


# Select the rows for the chosen invite code.
group = df[df["invite_code"] == example_code]

# Choose columns related to the timeline.
timeline_columns = [
    "measurement_date",
    "days_since_start",
    "imputed",
    "actual_phase",
    "inferred_day_of_study",
    "inferred_phase",
    "menstruating",
    "inferred_menstruating",
]

# Display the first 15 rows.
print("\nTimeline for the selected group:")
print(group[timeline_columns].head(15).to_string(index=False))




# Compare study-day values only where both are available.
valid_days = group.dropna(
    subset=["days_since_start", "inferred_day_of_study"]
)

day_mismatch = valid_days[
    valid_days["days_since_start"] != valid_days["inferred_day_of_study"]
]

print("\nRows where available study-day values differ:")
print(
    day_mismatch[
        ["measurement_date", "days_since_start", "inferred_day_of_study"]
    ].to_string(index=False)
)
print(f"Number of mismatches: {len(day_mismatch)}")

# Compare phase values only where both are available.
valid_phases = group.dropna(subset=["actual_phase", "inferred_phase"])

phase_mismatch = valid_phases[
    valid_phases["actual_phase"] != valid_phases["inferred_phase"]
]

print("\nRows where available phase values differ:")
print(
    phase_mismatch[
        ["measurement_date", "actual_phase", "inferred_phase"]
    ].to_string(index=False)
)
print(f"Number of mismatches: {len(phase_mismatch)}")



# Select rows marked as imputed.
imputed_group = group[group["imputed"] == True]

# Display timeline information for the imputed rows.
print("\nImputed rows for the selected group:")
print(
    imputed_group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
            "actual_phase",
            "inferred_phase",
            "menstruating",
            "inferred_menstruating",
        ]
    ].to_string(index=False)
)

print(f"\nNumber of imputed rows: {len(imputed_group)}")



# Check the inferred study-day values for the selected group.
study_days = group["inferred_day_of_study"]

print("\nInferred study-day summary:")
print(f"Number of rows: {len(study_days)}")
print(f"Number of unique study days: {study_days.nunique()}")
print(f"Minimum study day: {study_days.min()}")
print(f"Maximum study day: {study_days.max()}")

# Check for repeated inferred study days.
duplicate_days = study_days[study_days.duplicated()]

print(f"Repeated study-day values: {len(duplicate_days)}")
print(duplicate_days.to_list())



# Check whether any inferred study-day numbers are missing.
expected_days = set(range(60))
observed_days = set(study_days.dropna().astype(int))
missing_days = expected_days - observed_days

print(f"Missing inferred study days: {sorted(missing_days)}")
print(f"Number of missing study days: {len(missing_days)}")



# Summarize the phase assignments across the inferred study days.
phase_summary = group.groupby(
    ["inferred_phase", "actual_phase"],
    dropna=False
).size().reset_index(name="row_count")

print("\nActual versus inferred phase counts:")
print(phase_summary.to_string(index=False))




# Display rows around the phase disagreement.
if not phase_mismatch.empty:
    mismatch_index = phase_mismatch.index[0]

    start_index = max(mismatch_index - 2, group.index.min())
    end_index = min(mismatch_index + 2, group.index.max())

    print("\nRows around the phase disagreement:")
    print(
        group.loc[start_index:end_index, [
            "measurement_date",
            "inferred_day_of_study",
            "imputed",
            "actual_phase",
            "inferred_phase",
            "menstruating",
            "inferred_menstruating",
        ]].to_string(index=False)
    )
else:
    print("\nNo phase disagreements were found.")
