
from pathlib import Path
import pandas as pd


# Load the dataset.
project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "cleaned_studyu_data.csv"
df = pd.read_csv(data_path)


# Count rows for each participant.
for code, group in df.groupby("invite_code"):
    total = len(group)
    imputed = (group["imputed"] == True).sum()
    not_imputed = (group["imputed"] == False).sum()

    print(code, "Total:", total,
          "Imputed:", imputed,
          "Not imputed:", not_imputed)


# Compare study-day values.
valid_days = df.dropna(
    subset=["days_since_start", "inferred_day_of_study"]
)

differences = (
    valid_days["days_since_start"]
    - valid_days["inferred_day_of_study"]
)

mismatches = valid_days[differences != 0]

print("\nStudy-day comparison")
print("Rows compared:", len(valid_days))
print("Rows with differences:", len(mismatches))

print("\nDifference values:")
print(differences.value_counts().sort_index())


print("\nDifferences by participant:")
print(mismatches["invite_code"].value_counts().to_string())


# Compare phase values.
valid_phases = df.dropna(
    subset=["actual_phase", "inferred_phase"]
)

mismatches = valid_phases[
    valid_phases["actual_phase"] != valid_phases["inferred_phase"]
]

print("\nPhase comparison")
print("Rows compared:", len(valid_phases))
print("Rows with disagreements:", len(mismatches))

print("\nDetails of phase disagreements:")
print(
    mismatches[
        ["invite_code", "measurement_date", "actual_phase", "inferred_phase"]
    ].to_string(index=False)
)

print("\nPhase disagreements by participant:")
print(mismatches["invite_code"].value_counts().to_string())



# Inspect larger study-day differences.
large_differences = valid_days[differences >= 6]

print("\nLarger study-day differences:")
print(
    large_differences[
        [
            "invite_code",
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
        ]
    ].to_string(index=False)
)




# Inspect the timelines of participants with larger differences.
for code in ["ID06", "ID12", "ID13"]:
    group = df[df["invite_code"] == code]

    print("\nParticipant:", code)

    early_rows = group[group["inferred_day_of_study"] <= 10].sort_values("inferred_day_of_study")

    print(
        early_rows[
            [
                "measurement_date",
                "days_since_start",
                "inferred_day_of_study",
                "imputed",
                "actual_phase",
                "inferred_phase",
            ]
        ].to_string(index=False)
    )



# Inspect the rows around each phase disagreement.
print("\nContext around phase disagreements:")

for index in mismatches.index:
    code = mismatches.loc[index, "invite_code"]

    group = df[df["invite_code"] == code].copy()
    group = group.sort_values("inferred_day_of_study")

    position = group.index.get_loc(index)

    start = max(0, position - 2)
    end = min(len(group), position + 3)

    nearby_rows = group.iloc[start:end]

    print("\nParticipant:", code)
    print(
        nearby_rows[
            [
                "measurement_date",
                "days_since_start",
                "inferred_day_of_study",
                "imputed",
                "actual_phase",
                "inferred_phase",
            ]
        ].to_string(index=False)
    )



# Inspect study-day differences for ID03.
group = df[df["invite_code"] == "ID03"]

print("\nStudy-day values for ID03:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
        ]
    ].to_string(index=False)
)



# Inspect study-day differences for ID03.
group = df[df["invite_code"] == "ID03"]

print("\nStudy-day values for ID03:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
        ]
    ].to_string(index=False)
)



# Inspect non-imputed study-day values for ID03.
group = df[df["invite_code"] == "ID03"]

group = group[group["imputed"] == False].copy()

group = group.sort_values("inferred_day_of_study")

group["day_difference"] = (
    group["days_since_start"] - group["inferred_day_of_study"]
)

print("\nStudy-day values for ID03:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
            "day_difference",
        ]
    ].to_string(index=False)
)



# Inspect non-imputed study-day values for ID04.
group = df[df["invite_code"] == "ID04"]

group = group[group["imputed"] == False].copy()

group = group.sort_values("inferred_day_of_study")

group["day_difference"] = (
    group["days_since_start"] - group["inferred_day_of_study"]
)

print("\nStudy-day values for ID04:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
            "day_difference",
        ]
    ].to_string(index=False)
)



# Inspect non-imputed study-day values for ID14.
group = df[df["invite_code"] == "ID14"]

group = group[group["imputed"] == False].copy()

group = group.sort_values("inferred_day_of_study")

group["day_difference"] = (
    group["days_since_start"] - group["inferred_day_of_study"]
)

print("\nStudy-day values for ID14:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
            "day_difference",
        ]
    ].to_string(index=False)
)



# Inspect non-imputed study-day values for ID15.
group = df[df["invite_code"] == "ID15"]

group = group[group["imputed"] == False].copy()

group = group.sort_values("inferred_day_of_study")

group["day_difference"] = (
    group["days_since_start"] - group["inferred_day_of_study"]
)

print("\nStudy-day values for ID15:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
            "day_difference",
        ]
    ].to_string(index=False)
)



# Inspect non-imputed study-day values for ID02.
group = df[df["invite_code"] == "ID02"]

group = group[group["imputed"] == False].copy()

group = group.sort_values("inferred_day_of_study")

group["day_difference"] = (
    group["days_since_start"] - group["inferred_day_of_study"]
)

print("\nStudy-day values for ID02:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
            "day_difference",
        ]
    ].to_string(index=False)
)



# Inspect non-imputed study-day values for ID17.
group = df[df["invite_code"] == "ID17"]

group = group[group["imputed"] == False].copy()

group = group.sort_values("inferred_day_of_study")

group["day_difference"] = (
    group["days_since_start"] - group["inferred_day_of_study"]
)

print("\nStudy-day values for ID17:")
print(
    group[
        [
            "measurement_date",
            "days_since_start",
            "inferred_day_of_study",
            "day_difference",
        ]
    ].to_string(index=False)
)



# Compare calendar-day gaps with changes in study-day values for ID02.
group = df[df["invite_code"] == "ID02"]

group = group[group["imputed"] == False].copy()

group["measurement_date"] = pd.to_datetime(group["measurement_date"])

group = group.sort_values("measurement_date")

group["date_gap"] = group["measurement_date"].diff().dt.days

group["days_since_start_change"] = group["days_since_start"].diff()

group["inferred_day_change"] = group["inferred_day_of_study"].diff()

print("\nCalendar gaps and study-day changes for ID02:")
print(
    group[
        [
            "measurement_date",
            "date_gap",
            "days_since_start_change",
            "inferred_day_change",
        ]
    ].to_string(index=False)
)



# Compare calendar gaps and study-day changes across all participants.

group = df[df["imputed"] == False].copy()

group["measurement_date"] = pd.to_datetime(group["measurement_date"])

group = group.sort_values(["invite_code", "measurement_date"])

group["date_gap"] = group.groupby("invite_code")["measurement_date"].diff().dt.days

group["days_since_start_change"] = group.groupby("invite_code")["days_since_start"].diff()

group["inferred_day_change"] = group.groupby("invite_code")["inferred_day_of_study"].diff()

print("\nTimeline comparison across participants:")
print(
    group[
        [
            "invite_code",
            "measurement_date",
            "date_gap",
            "days_since_start_change",
            "inferred_day_change",
        ]
    ].to_string(index=False)
)



# Check inferred study-day coverage for each participant.

for participant in df["invite_code"].unique():
    group = df[df["invite_code"] == participant]

    day_count = group["inferred_day_of_study"].nunique()
    missing_days = group["inferred_day_of_study"].isna().sum()
    duplicate_days = group["inferred_day_of_study"].duplicated().sum()
    missing_phases = group["inferred_phase"].isna().sum()

    print(
        participant,
        "Unique days:", day_count,
        "Missing days:", missing_days,
        "Duplicate days:", duplicate_days,
        "Missing phases:", missing_phases
    )



# Verify that every participant has exactly days 0 to 59.

for participant in df["invite_code"].unique():
    group = df[df["invite_code"] == participant]

    days = sorted(group["inferred_day_of_study"].tolist())

    if days == list(range(60)):
        print(participant, "Complete sequence: 0–59")
    else:
        print(participant, "Unexpected sequence:", days)



# Compare imputed and non-imputed rows across inferred phases.

phase_counts = df.groupby(
    ["inferred_phase", "imputed"]
).size()

print("\nImputation counts by inferred phase:")
print(phase_counts)



# Calculate the percentage of imputed rows in each inferred phase.

phase_percentages = df.groupby("inferred_phase")["imputed"].mean() * 100

print("\nImputed rows by inferred phase (%):")
print(phase_percentages.round(1))



# Compare imputed and non-imputed rows by participant and phase.

participant_phase_counts = df.groupby(
    ["invite_code", "inferred_phase", "imputed"]
).size()

print("\nImputation counts by participant and phase:")
print(participant_phase_counts)



# Display the grouped counts as a table.

participant_phase_table = participant_phase_counts.unstack(
    level="imputed",
    fill_value=0
)

print("\nImputation counts by participant and phase:")
print(participant_phase_table.to_string())



# Count rows in each inferred phase for ID17.

id17 = df[df["invite_code"] == "ID17"]

print("\nInferred phase counts for ID17:")
print(id17["inferred_phase"].value_counts())



# Keep participants who have at least one non-imputed row.
# Create an empty list.
participants_with_data = []

for participant_id in df["invite_code"].unique():

    participant_rows = df[df["invite_code"] == participant_id]

    non_imputed_rows = participant_rows[participant_rows["imputed"] == False]

    if len(non_imputed_rows) > 0:
        participants_with_data.append(participant_id)

# Print the number of participants.
print("\nParticipants with non-imputed data:")
print(len(participants_with_data))


# Keep only participants who have at least one non-imputed row.

participants_to_keep = participants_with_data

# Check which rows belong to the participants we want to keep.
rows_to_keep = df["invite_code"].isin(participants_to_keep)

# Keep only those rows in a new DataFrame.
df_with_data = df[rows_to_keep]


# Group rows by phase and imputation status.
phase_counts = df_with_data.groupby(["inferred_phase", "imputed"]).size()

print("\nImputation counts among participants with non-imputed data:")
print(phase_counts)



# Group the data by participant, phase, and imputation status.
participant_phase_counts = df_with_data.groupby(
    ["invite_code", "inferred_phase", "imputed"]
).size()

# Print the results.
print("\nImputation counts by participant and phase (19 participants):")
print(participant_phase_counts.to_string())
