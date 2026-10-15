import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SKILLS_PATH = BASE_DIR / "data" / "raw" / "job_skills.csv"

# Load the skill dataset
skills_df = pd.read_csv(SKILLS_PATH, low_memory=False)

print("\nColumn names:",)
print(skills_df.columns.tolist())

print("\nFirst 10 records:")
print(skills_df.head(10).to_string(index=False))

# Check duplicate
print("\nDuplicate records:", skills_df.duplicated().sum())

# Count distinct jobs
print("\nUnique job IDs:", skills_df["job_id"].nunique())

# Examine skill categories
if "skill_abr" in skills_df.columns:
    print("\nSkill categories distribution:")
    print(skills_df["skill_abr"].value_counts())

    print("\nNumber of distinct skill categories:")
    print(skills_df["skill_abr"].nunique())

print("\nAll skill categories:")
print(sorted(skills_df["skill_abr"].dropna().unique()))

print("\nTop 15 most common categories:")
print(skills_df["skill_abr"].value_counts().head(15))