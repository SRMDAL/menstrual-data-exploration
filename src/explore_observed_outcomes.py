from pathlib import Path
import pandas as pd

# Locate the project folder.
project_dir = Path(__file__).resolve().parent.parent

# Locate and load the main dataset.
data_path = project_dir / "data" / "cleaned_studyu_data.csv"
main_df = pd.read_csv(data_path)

# Keep only rows that were not imputed.
observed_df = main_df[main_df["imputed"] == False]

# Check how many observed rows belong to each actual phase.
print("\n--- Observed rows by phase ---")
print(observed_df["actual_phase"].value_counts(dropna=False))



# Check how many actual values are available for each outcome.
outcome_columns = [
    "pain",
    "tablets",
    "mood",
    "symptoms_count"
]

print("\n--- Available outcome values by phase ---")

print(observed_df.groupby("actual_phase")[outcome_columns].count())



# Calculate the average of each outcome in each phase.
print("\n--- Average outcome values by phase ---")

print(observed_df.groupby("actual_phase")[outcome_columns].mean())



# Calculate the median of each outcome in each phase.
print("\n--- Median outcome values by phase ---")

print(observed_df.groupby("actual_phase")[outcome_columns].median())



# Count zero and non-zero observations for each outcome.
print("\n--- Zero and non-zero observations ---")

for column in outcome_columns:
    print(f"\n{column}")

    print(
        observed_df.groupby("actual_phase")[column]
        .apply(lambda values: (values == 0).sum())
    )
