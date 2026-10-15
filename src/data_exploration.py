# Path to the job postings dataset

import pandas as pd
from pathlib import Path

# Locate the project's root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the job postings dataset
DATA_PATH = BASE_DIR / "data" / "raw" / "job_postings.csv"

#Load the dataset

df = pd.read_csv(DATA_PATH, low_memory=False)

#Display basic information

print("Dataset shape:", df.shape)

print("\nColumn names:", df.columns)
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head(5)) 

print("\nMissing values per column:")
print(df.isnull().sum())


# Calculate the percentage of missing values
missing_percentage = df.isnull().mean() * 100

# Sort column by missing percentage
missing_percentage = missing_percentage.sort_values(ascending=False)

print("\n Missing Values Percentage (%):")
print(missing_percentage.round(2))  # Round to 2 decimal places 

# Count duplicated job IDs
duplicated_ids = df["job_id"].duplicated().sum()

print("\nNumber of duplicated job IDs:", duplicated_ids)

# count exact duplicates rows
duplicated_rows = df.duplicated().sum()

print("Duplicated Rows:", duplicated_rows)

