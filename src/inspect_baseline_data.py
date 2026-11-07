from pathlib import Path
import pandas as pd

# Locate the project folder.
project_dir = Path(__file__).resolve().parent.parent

# Locate and load the baseline survey file.
baseline_path = project_dir / "data" / "final_upsurvey_data_labeled_mpisapp.csv"
baseline_df = pd.read_csv(baseline_path)


main_data_path = project_dir / "data" / "cleaned_studyu_data.csv"
main_df = pd.read_csv(main_data_path)

# Check the dataset dimensions.
print("Dataset dimensions:")
print(baseline_df.shape)

# Display all column names.
print("\nColumn names:")
for column in baseline_df.columns:
    print(column)

# Check participant identifiers.
print("\nParticipant identifiers:")
print(baseline_df["unique_id"].value_counts())

# Check whether participant identifiers are missing.
print("\nMissing participant identifiers:")
print(baseline_df["unique_id"].isna().sum())



# Inspect baseline variables related to pain, medication, and symptoms.

baseline_columns = [
    "Worst Pain Severity (0-10)",
    "Average Pain Severity (0-10)",
    "Days with Menstrual Pain per Cycle",
    "Average Daily Pain Tablets Taken",
    "Cramps",
    "Back pain in the lower area",
    "Nausea, vomiting or diarrhea",
    "Painful urination",
    "Painful bowel movements",
    "Bloated stomach",
    "Painful sexual intercourse",
    "Fatigue or concentration difficulties",
    "Fainting",
    "Headaches",
    "None of the above"
]

for column in baseline_columns:

    print(f"\n--- {column} ---")

    print("Missing values:")
    print(baseline_df[column].isna().sum())

    print("Value counts:")
    print(baseline_df[column].value_counts(dropna=False).sort_index())



# Compare ID02's baseline pain information with the main dataset.

participant_id = "ID02"

# Find ID02's baseline survey record.
baseline_record = baseline_df[
    baseline_df["unique_id"] == participant_id
]

print("\n--- ID02: Baseline pain information ---")

print(
    baseline_record[
        [
            "Worst Pain Severity (0-10)",
            "Average Pain Severity (0-10)",
            "Days with Menstrual Pain per Cycle"
        ]
    ].to_string(index=False)
)

# Find ID02's rows in the main dataset.
participant_data = main_df[
    main_df["unique_id"] == participant_id
]

# Display the pain values and imputation status.
print("\n--- ID02: Pain values in the main dataset ---")

print(
    participant_data[
        [
            "inferred_day_of_study",
            "actual_phase",
            "inferred_phase",
            "imputed",
            "pain",
            "pain_imputed",
            "pain_sensitivity"
        ]
    ].to_string(index=False)
)



# Compare baseline pain scores with imputed pain values.

print("\n--- Baseline pain and imputed pain comparison ---")

for participant_id in baseline_df["unique_id"]:

    # Find the participant's baseline information.
    baseline_record = baseline_df[
        baseline_df["unique_id"] == participant_id
    ]

    average_pain = baseline_record["Average Pain Severity (0-10)"].iloc[0]
    worst_pain = baseline_record["Worst Pain Severity (0-10)"].iloc[0]

    # Find the participant's data in the main dataset.
    participant_data = main_df[
        main_df["unique_id"] == participant_id
    ]

    # Keep only imputed rows.
    imputed_data = participant_data[
        participant_data["imputed"] == True
    ]

    # Count the imputed pain values.
    pain_values = imputed_data["pain_imputed"]
    pain_counts = pain_values.value_counts()

    # Print the results.
    print("\nParticipant:", participant_id)
    print("Baseline average pain:", average_pain)
    print("Baseline worst pain:", worst_pain)
    print("Imputed pain values:")
    print(pain_counts.sort_index())



# Keep only imputed rows.
imputed_rows = main_df[main_df["imputed"] == True]

# Show columns related to menstruation.
for column in imputed_rows.columns:
    if "menstru" in column.lower():
        print(column)



# Keep only imputed rows.
imputed_rows = main_df[main_df["imputed"] == True]

# Count pain values for each inferred menstruation status.
for status in imputed_rows["inferred_menstruating"].unique():

    print("\nInferred menstruating:", status)

    status_rows = imputed_rows[
        imputed_rows["inferred_menstruating"] == status
    ]

    print(status_rows["pain_imputed"].value_counts().sort_index())



# Keep imputed rows where menstruation was inferred.
imputed_menstruation_rows = imputed_rows[
    imputed_rows["inferred_menstruating"] == True
]

# Get the available menstruation days.
menstruation_days = imputed_menstruation_rows["menstruation_day"].dropna().unique()

# Check pain values for each menstruation day.
for day in sorted(menstruation_days):

    print("\nMenstruation day:", day)

    day_rows = imputed_menstruation_rows[
        imputed_menstruation_rows["menstruation_day"] == day
    ]

    print(day_rows["pain_imputed"].value_counts().sort_index())



# Calculate average imputed pain for each menstruation day.
for day in sorted(menstruation_days):

    day_rows = imputed_menstruation_rows[
        imputed_menstruation_rows["menstruation_day"] == day
    ]

    average_pain = day_rows["pain_imputed"].mean()
    number_of_rows = len(day_rows)

    print("Day:", day)
    print("Average pain:", round(average_pain, 2))
    print("Number of rows:", number_of_rows)
    print()



# Keep only rows with actual pain measurements.
observed_rows = main_df[main_df["imputed"] == False]

# Keep rows where menstruation was recorded as True.
observed_menstruation_rows = observed_rows[
    observed_rows["menstruating"] == True
]

# Get the available menstruation days.
observed_days = observed_menstruation_rows["menstruation_day"].dropna().unique()

# Calculate average pain for each day.
for day in sorted(observed_days):

    day_rows = observed_menstruation_rows[
        observed_menstruation_rows["menstruation_day"] == day
    ]

    average_pain = day_rows["pain"].mean()
    number_of_rows = len(day_rows)

    print("Day:", day)
    print("Average observed pain:", round(average_pain, 2))
    print("Number of rows:", number_of_rows)
    print()



# Check how many participants contributed data on each menstruation day.

print("--- Imputed data ---")

for day in sorted(menstruation_days):

    day_rows = imputed_menstruation_rows[
        imputed_menstruation_rows["menstruation_day"] == day
    ]

    participant_count = day_rows["unique_id"].nunique()

    print("Day:", day)
    print("Number of participants:", participant_count)
    print()


print("--- Observed data ---")

for day in sorted(observed_days):

    day_rows = observed_menstruation_rows[
        observed_menstruation_rows["menstruation_day"] == day
    ]

    participant_count = day_rows["unique_id"].nunique()

    print("Day:", day)
    print("Number of participants:", participant_count)
    print()



# Select participant ID26.
participant_rows = main_df[
    main_df["unique_id"] == "ID26"
]

# Keep rows where menstruation was recorded or inferred.
participant_rows = participant_rows[
    (participant_rows["menstruating"] == True)
    | (participant_rows["inferred_menstruating"] == True)
]

# Show the relevant columns.
print(
    participant_rows[
        [
            "unique_id",
            "imputed",
            "menstruating",
            "inferred_menstruating",
            "menstruation_day",
            "pain",
            "pain_imputed"
        ]
    ].to_string(index=False)
)



# Select all rows for participant ID26.
participant_rows = main_df[
    main_df["unique_id"] == "ID26"
]

# Show the timeline information.
print(
    participant_rows[
        [
            "inferred_day_of_study",
            "measurement_date",
            "imputed",
            "inferred_phase",
            "inferred_menstruating",
            "menstruation_day",
            "pain",
            "pain_imputed"
        ]
    ].to_string(index=False)
)



# Select participant ID27.
participant_rows = main_df[
    main_df["unique_id"] == "ID27"
]

# Keep rows where inferred menstruation is True.
menstruation_rows = participant_rows[
    participant_rows["inferred_menstruating"] == True
]

# Show the inferred menstruation days and pain values.
print(
    menstruation_rows[
        [
            "inferred_day_of_study",
            "inferred_phase",
            "menstruation_day",
            "pain_imputed"
        ]
    ].to_string(index=False)
)



# Select participant ID02.
participant_rows = main_df[
    main_df["unique_id"] == "ID02"
]

# Keep rows where menstruation was recorded or inferred.
menstruation_rows = participant_rows[
    (participant_rows["menstruating"] == True)
    | (participant_rows["inferred_menstruating"] == True)
]

# Show the relevant columns.
print(
    menstruation_rows[
        [
            "inferred_day_of_study",
            "imputed",
            "menstruating",
            "inferred_menstruating",
            "menstruation_day",
            "pain",
            "pain_imputed"
        ]
    ].to_string(index=False)
)



# Select participant ID02.
participant_rows = main_df[
    main_df["unique_id"] == "ID02"
]

# Sort the participant's rows by study day.
participant_rows = participant_rows.sort_values(
    "inferred_day_of_study"
)

# Keep only imputed rows.
imputed_rows = participant_rows[
    participant_rows["imputed"] == True
]

# Display the imputed rows and relevant columns.
print("\n--- ID02: All imputed rows ---")

print(
    imputed_rows[
        [
            "inferred_day_of_study",
            "inferred_phase",
            "inferred_menstruating",
            "menstruation_day",
            "pain",
            "pain_imputed"
        ]
    ].to_string(index=False)
)


# Get the study-day numbers of the imputed rows.
imputed_days = imputed_rows["inferred_day_of_study"].tolist()

# Create a list of the days immediately before and after each imputed day.
neighbor_days = []

for day in imputed_days:
    neighbor_days.append(day - 1)
    neighbor_days.append(day + 1)

# Select the neighboring days from the participant's data.
neighbor_rows = participant_rows[
    participant_rows["inferred_day_of_study"].isin(neighbor_days)
]

# Display the neighboring observations.
print("\n--- ID02: Days surrounding imputed rows ---")

print(
    neighbor_rows[
        [
            "inferred_day_of_study",
            "imputed",
            "inferred_phase",
            "inferred_menstruating",
            "menstruation_day",
            "pain",
            "pain_imputed"
        ]
    ].to_string(index=False)
)


# Keep only observed rows among the neighboring days.
observed_neighbor_rows = neighbor_rows[
    neighbor_rows["imputed"] == False
]

# Display the observed neighboring rows.
print("\n--- ID02: Observed neighboring rows ---")

print(
    observed_neighbor_rows[
        [
            "inferred_day_of_study",
            "inferred_phase",
            "inferred_menstruating",
            "menstruation_day",
            "pain"
        ]
    ].to_string(index=False)
)



# Find ID02's baseline information.
baseline_record = baseline_df[
    baseline_df["unique_id"] == "ID02"
]

# Display selected baseline pain and medication information.
print("\n--- ID02: Baseline pain information ---")

print(
    baseline_record[
        [
            "Days with Menstrual Pain per Cycle",
            "Worst Pain Severity (0-10)",
            "Average Pain Severity (0-10)",
            "Days Using Pain Medication per Cycle",
            "Average Daily Pain Tablets Taken"
        ]
    ].to_string(index=False)
)
