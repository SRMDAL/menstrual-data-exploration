from pathlib import Path
import pandas as pd

# Locate the project folder.
project_dir = Path(__file__).resolve().parent.parent

# Locate and load the baseline survey file.
baseline_path = project_dir / "data" / "final_upsurvey_data_labeled_mpisapp.csv"
baseline_df = pd.read_csv(baseline_path)


# Locate and load the main study data.
main_data_path = project_dir / "data" / "cleaned_studyu_data.csv"
main_df = pd.read_csv(main_data_path)


print("\n--- Possible menstrual history columns ---")

for column in baseline_df.columns:
    if "cycle" in column.lower() or "menstru" in column.lower() or "period" in column.lower():
        print(column)



print("\n--- ID27 menstrual history ---")

id27 = baseline_df[baseline_df["unique_id"] == "ID27"]

print(id27[[
    "Cycle Length",
    "Period Duration",
    "Days with Menstrual Pain per Cycle"
]])



print("\n--- ID27 inferred menstrual timeline ---")

id27_main = main_df[main_df["unique_id"] == "ID27"]

print(id27_main[[
    "inferred_day_of_study",
    "inferred_phase",
    "inferred_menstruating",
    "menstruation_day",
    "imputed",
    "pain_imputed"
]].to_string(index=False))
