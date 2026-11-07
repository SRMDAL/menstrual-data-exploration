from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Locate the project folder.
project_dir = Path(__file__).resolve().parent.parent

# Locate and load the main dataset.
data_path = project_dir / "data" / "cleaned_studyu_data.csv"
main_df = pd.read_csv(data_path)

# Keep only rows that were not imputed.
observed_df = main_df[main_df["imputed"] == False]

# Calculate the average of each outcome in each phase.
outcome_columns = [
    "pain",
    "tablets",
    "mood",
    "symptoms_count"
]

phase_averages = observed_df.groupby("actual_phase")[outcome_columns].mean()

print(phase_averages)


# Draw a bar chart of the average outcomes.
phase_averages.plot(kind="bar")

# Add a title and axis labels.
plt.title("Average outcome values by phase")
plt.xlabel("Study phase")
plt.ylabel("Average value")

# Keep the phase labels horizontal.
plt.xticks(rotation=0)

# Adjust the layout and display the chart.
plt.tight_layout()
plt.show()



# Count zero observations for each outcome in each phase.
zero_counts = observed_df.groupby("actual_phase")[outcome_columns].apply(
    lambda group: (group == 0).sum()
)

# Count non-zero observations for each outcome in each phase.
non_zero_counts = observed_df.groupby("actual_phase")[outcome_columns].apply(
    lambda group: (group > 0).sum()
)

print("\n--- Zero observations ---")
print(zero_counts)

print("\n--- Non-zero observations ---")
print(non_zero_counts)



# Draw a bar chart of zero observations.
zero_counts.plot(kind="bar")

plt.title("Zero observations by phase")
plt.xlabel("Study phase")
plt.ylabel("Number of zero values")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()



# Draw a bar chart of non-zero observations.
non_zero_counts.plot(kind="bar")

plt.title("Non-zero observations by phase")
plt.xlabel("Study phase")
plt.ylabel("Number of non-zero values")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()
