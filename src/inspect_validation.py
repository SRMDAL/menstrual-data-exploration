
from pathlib import Path
import pandas as pd


# Locate and load the validation file.
project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "study_flow_validation.csv"
validation_df = pd.read_csv(data_path)

# Inspect the structure of the file.
print("Dataset dimensions:")
print(validation_df.shape)

print("\nColumn names:")
print(validation_df.columns.tolist())

print("\nFirst 10 rows:")
print(validation_df.head(10))



# Select the validation record for ID02.
id02_validation = validation_df[validation_df["invite_code"] == "ID02"]

print("\nValidation record for ID02:")
print(id02_validation.T)

