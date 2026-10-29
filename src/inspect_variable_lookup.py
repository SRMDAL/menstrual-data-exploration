
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
keywords = ["phase", "menstru", "pain", "cycle"]

for keyword in keywords:
    matches = lookup_df[
        lookup_df["column_name"].str.contains(keyword, case=False, na=False)
        | lookup_df["question_en"].str.contains(keyword, case=False, na=False)
        | lookup_df["label_en"].str.contains(keyword, case=False, na=False)
    ]

    print(f"\n--- Keyword: {keyword} ---")
    print(matches[["column_name", "question_en", "label_en"]].to_string(index=False))

