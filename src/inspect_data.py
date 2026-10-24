from pathlib import Path
import pandas as pd


# Find the project folder and the CSV file.
project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "cleaned_studyu_data.csv"

# Read the CSV file.
df = pd.read_csv(data_path)

# Show the dataset size.
print("\nDataset dimensions:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Count the distinct invite codes.
number_of_groups = df["invite_code"].nunique()
print(f"Number of distinct invite codes: {number_of_groups}")

# Display the first 3 rows.
print("\nFirst 3 rows:")
print(df.head(3).to_string(index=False))

# Display the last 3 rows.
print("\nLast 3 rows:")
print(df.tail(3).to_string(index=False))

# Display all column names.
print("\nColumn names:")
for column in df.columns:
    print(column)

# Show the column names and data types.
print("\nColumn names and data types:")
print(df.dtypes.to_string())

# Count missing values in each column.
print("\nMissing values per column:")
missing_values = df.isna().sum()
print(missing_values.to_string())

# Check how the rows are marked in the imputed column.
if "imputed" in df.columns:
    print("\nImputed column counts:")
    imputed_counts = df["imputed"].value_counts(dropna=False)
    print(imputed_counts.to_string())

    # Count rows in each invite-code group.
    per_code = df.groupby("invite_code").agg(
        total_rows=("imputed", "size"),
        imputed_rows=("imputed", "sum"),
    )

    per_code["not_imputed_rows"] = (
        per_code["total_rows"] - per_code["imputed_rows"]
    )

    # Summarize the group sizes.
    print("\nSummary by invite-code group:")
    print(f"Number of groups: {len(per_code)}")

    min_rows = per_code["total_rows"].min()
    max_rows = per_code["total_rows"].max()
    print(f"Rows per group (minimum, maximum): {min_rows}, {max_rows}")

    min_imputed = per_code["imputed_rows"].min()
    median_imputed = per_code["imputed_rows"].median()
    max_imputed = per_code["imputed_rows"].max()
    print(
        "Imputed rows per group (minimum, median, maximum): "
        f"{min_imputed}, {median_imputed}, {max_imputed}"
    )

    min_not_imputed = per_code["not_imputed_rows"].min()
    median_not_imputed = per_code["not_imputed_rows"].median()
    max_not_imputed = per_code["not_imputed_rows"].max()
    print(
        "Not-imputed rows per group (minimum, median, maximum): "
        f"{min_not_imputed}, {median_not_imputed}, {max_not_imputed}"
    )

    # Count groups with no rows of either type.
    no_imputed_groups = (per_code["imputed_rows"] == 0).sum()
    no_not_imputed_groups = (per_code["not_imputed_rows"] == 0).sum()
    print(f"Groups with zero imputed rows: {no_imputed_groups}")
    print(f"Groups with zero not-imputed rows: {no_not_imputed_groups}")

    # Count how many groups have each number of not-imputed rows.
    print("\nDistribution of not-imputed rows per group:")
    distribution = per_code["not_imputed_rows"].value_counts().sort_index()
    print(distribution.to_string())

    # Choose the group with the most rows marked as not imputed.
    example_code = per_code["not_imputed_rows"].idxmax()
    example_group = df[df["invite_code"] == example_code]

    # Choose the columns to inspect.
    columns_to_inspect = [
        "imputed",
        "measurement_date",
        "pain",
        "tablets",
        "mood",
        "pain_imputed",
        "tablets_imputed",
        "mood_imputed",
    ]

    # Separate rows marked as imputed and not imputed.
    not_imputed_rows = example_group[example_group["imputed"] == False]
    imputed_rows = example_group[example_group["imputed"] == True]

    # Display five example rows of each type.
    print("\nExample rows marked as not imputed:")
    print(not_imputed_rows[columns_to_inspect].head(5).to_string(index=False))

    print("\nExample rows marked as imputed:")
    print(imputed_rows[columns_to_inspect].head(5).to_string(index=False))


# Inspect the question 7 responses.
column_name = "survey1_question7_response"

print("\nQuestion 7: first two non-missing values:")
print(df[column_name].dropna().head(2).to_string(index=False))

print("\nQuestion 7: response counts, including missing values:")
print(df[column_name].value_counts(dropna=False).to_string())

# Compare question 7 responses with the imputed flag.
print("\nQuestion 7 missingness by imputed status:")

question7_missing = df["survey1_question7_response"].isna()

comparison = pd.crosstab(
    df["imputed"],
    question7_missing,
    margins=True,
)

print(comparison.to_string())
