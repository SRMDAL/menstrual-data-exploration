
from pathlib import Path
import pandas as pd


# Locate and load the variable lookup file.
project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "variable_lookup.csv"
lookup_df = pd.read_csv(data_path)

# Inspect the structure of the file.
print("Dataset dimensions:")
print(lookup_df.shape)

print("\nColumn names:")
print(lookup_df.columns.tolist())

print("\nFirst 10 rows:")
print(lookup_df.head(10))




# Search for relevant words in the English labels and questions.
keywords = [
    "phase",
    "menstru",
    "pain",
    "cycle",
    "medication",
    "tablet",
    "symptom",
    "mood"
]

for keyword in keywords:
    matches = lookup_df[
        lookup_df["column_name"].str.contains(keyword, case=False, na=False)
        | lookup_df["question_en"].str.contains(keyword, case=False, na=False)
        | lookup_df["label_en"].str.contains(keyword, case=False, na=False)
    ]

    print(f"\n--- Keyword: {keyword} ---")
    print(matches[["column_name", "question_en", "label_en"]].to_string(index=False))



# Load the main dataset.
main_data_path = project_dir / "data" / "cleaned_studyu_data.csv"
main_df = pd.read_csv(main_data_path)

# Print the main dataset columns related to pain, medication, and symptoms.
print("\nPotential outcome columns in the main dataset:")

for column in main_df.columns:
    column_lower = column.lower()

    if (
        "pain" in column_lower
        or "medication" in column_lower
        or "tablet" in column_lower
        or "symptom" in column_lower
        or "mood" in column_lower
    ):
        print(column)



# Check whether the potential outcome columns are documented in the lookup file.
outcome_columns = [
    "symptoms_count",
    "pain_sensitivity",
    "tablets_sensitivity",
    "symptoms_count_sensitivity",
    "mood_sensitivity",
    "pain_imputed",
    "tablets_imputed",
    "mood_imputed",
    "symptoms_count_imputed",
    "pain_day",
    "pain",
    "tablets",
    "mood"
]

print("\nLookup information for potential outcome columns:")

for column in outcome_columns:
    matches = lookup_df[lookup_df["column_name"] == column]

    print(f"\n--- {column} ---")
    print(matches[["column_name", "question_en", "label_en"]].to_string(index=False))



# Inspect the data types and first few values of the potential outcome columns.
print("\nPotential outcome columns: data types")
print(main_df[outcome_columns].dtypes)

print("\nFirst 10 rows of the potential outcome columns:")
print(main_df[outcome_columns].head(10).to_string(index=False))



# Check missing values in the potential outcome columns.
print("\nMissing values in potential outcome columns:")

print(main_df[outcome_columns].isna().sum())

# Check the unique values in each column.
print("\nUnique values in potential outcome columns:")

for column in outcome_columns:
    print(f"\n--- {column} ---")
    print(main_df[column].value_counts(dropna=False).sort_index().to_string())



# Compare original outcome columns with their corresponding imputed columns.
column_pairs = [
    ("pain", "pain_imputed"),
    ("tablets", "tablets_imputed"),
    ("mood", "mood_imputed"),
    ("symptoms_count", "symptoms_count_imputed")
]

print("\nComparing original and imputed outcome columns:")

for original_column, imputed_column in column_pairs:
    print(f"\n--- {original_column} vs {imputed_column} ---")

    # Check whether the values match in non-imputed rows.
    non_imputed_rows = main_df["imputed"] == False

    matching_values = (
        main_df.loc[non_imputed_rows, original_column]
        == main_df.loc[non_imputed_rows, imputed_column]
    )

    print("Matching values in non-imputed rows:")
    print(matching_values.sum())

    print("Non-matching values in non-imputed rows:")
    print((~matching_values).sum())

    # Check whether the imputed column has missing values in imputed rows.
    imputed_rows = main_df["imputed"] == True

    missing_in_imputed_rows = main_df.loc[
        imputed_rows, imputed_column
    ].isna().sum()

    print("Missing values in the imputed column for imputed rows:")
    print(missing_in_imputed_rows)



# Compare sensitivity columns with their corresponding imputed outcome columns.
sensitivity_pairs = [
    ("pain_sensitivity", "pain_imputed"),
    ("tablets_sensitivity", "tablets_imputed"),
    ("mood_sensitivity", "mood_imputed"),
    ("symptoms_count_sensitivity", "symptoms_count_imputed")
]

print("\nComparing sensitivity and imputed outcome columns:")

for sensitivity_column, imputed_column in sensitivity_pairs:
    print(f"\n--- {sensitivity_column} vs {imputed_column} ---")

    matching_values = (
        main_df[sensitivity_column] == main_df[imputed_column]
    )

    print("Matching values:")
    print(matching_values.sum())

    print("Non-matching values:")
    print((~matching_values).sum())



# Display the first 10 rows where sensitivity and imputed values differ.
for sensitivity_column, imputed_column in sensitivity_pairs:
    print(f"\n--- Mismatches: {sensitivity_column} vs {imputed_column} ---")

    mismatches = main_df[
        main_df[sensitivity_column] != main_df[imputed_column]
    ]

    print(
        mismatches[
            [
                "invite_code",
                "imputed",
                "inferred_phase",
                sensitivity_column,
                imputed_column
            ]
        ].head(10).to_string(index=False)
    )



# Count mismatches separately for imputed and non-imputed rows.
print("\nMismatch counts by imputation status:")

for sensitivity_column, imputed_column in sensitivity_pairs:
    print(f"\n--- {sensitivity_column} vs {imputed_column} ---")

    mismatches = (
        main_df[sensitivity_column] != main_df[imputed_column]
    )

    print("Mismatches in imputed rows:")
    print((mismatches & (main_df["imputed"] == True)).sum())

    print("Mismatches in non-imputed rows:")
    print((mismatches & (main_df["imputed"] == False)).sum())



# Check sensitivity values in rows where the two columns differ.
print("\nSensitivity values in mismatching rows:")

for sensitivity_column, imputed_column in sensitivity_pairs:
    mismatches = (
        main_df[sensitivity_column] != main_df[imputed_column]
    )

    print(f"\n--- {sensitivity_column} ---")

    mismatch_values = main_df.loc[mismatches, sensitivity_column]

    print("Values in the sensitivity column:")
    print(mismatch_values.value_counts(dropna=False).sort_index())



# Check the sensitivity values in all imputed rows.

imputed_rows = main_df["imputed"] == True

for sensitivity_column, imputed_column in sensitivity_pairs:

    sensitivity_values = main_df.loc[
        imputed_rows, sensitivity_column
    ]

    missing_count = sensitivity_values.isna().sum()

    non_zero_count = (
        sensitivity_values.notna()
        & (sensitivity_values != 0)
    ).sum()

    print(f"\n--- {sensitivity_column} ---")
    print("Number of imputed rows:", len(sensitivity_values))
    print("Missing sensitivity values:", missing_count)
    print("Non-zero sensitivity values:", non_zero_count)

    print("Sensitivity value distribution:")
    print(sensitivity_values.value_counts(dropna=False).sort_index())
