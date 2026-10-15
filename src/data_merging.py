import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

JOBS_PATH = BASE_DIR / "data" / "processed" / "cleaned_job.csv"
COMPANIES_PATH = BASE_DIR / "data" / "raw" / "companies.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "jobs_final.csv"

# Load the datasets
jobs = pd.read_csv(JOBS_PATH, low_memory=False)
companies = pd.read_csv(COMPANIES_PATH, low_memory=False)

print("Jobs shape:", jobs.shape)    
print("Companies shape:", companies.shape)  

# Select company information
companies = companies[["company_id", "name"]].copy()

# Rename the column for clarity
companies = companies.rename(columns={"name": "company_name"})

# Ensure company IDs use compatible data types
jobs["company_id"] = pd.to_numeric(jobs["company_id"], errors='coerce').astype('Int64')

companies["company_id"] = pd.to_numeric(companies["company_id"], errors='coerce').astype('Int64')

# Merge the datasets with the company instruction
merged = jobs.merge(companies, 
                    on="company_id", 
                    how="left")

# Handle the missing company names
merged["company_name"] = merged["company_name"].fillna("Unknown Company")

# Load job skills dataset
SKILLS_PATH = BASE_DIR / "data" / "raw" / "job_skills.csv"
skills_df = pd.read_csv(SKILLS_PATH, low_memory=False)

# Remove duplicate job_cateogory relationships
skills_df = skills_df.drop_duplicates(subset=["job_id", "skill_abr"])

# Group categories belonging to the same job
skills_grouped = skills_df.groupby("job_id")["skill_abr"].apply(lambda values: ", ".join(sorted(values.dropna()))).reset_index()

# Merge with job dataset
merged = merged.merge(skills_grouped, 
                      on="job_id", 
                      how="left",
                      validate = "one_to_one")

# Handle jobs without skill category records
merged["skill_categories"] = merged["skill_abr"].fillna("Not Specified")
merged = merged.drop(columns=["skill_abr"], errors="ignore")

# Verify merge results
print("\nMerged Dataset shape:", merged.shape )

print("Missing company names:", (merged["company_name"] == "Unknown Company").sum())

# Ensure no miss any job
assert len(merged) == len(jobs), "Mismatch in number of jobs after merging"
assert merged["job_id"].is_unique, "Duplicate job IDs found after merging"
assert 'skill_categories' in merged.columns, "Skill categories column missing after merging"

# Save the final merged dataset
merged.to_csv(OUTPUT_PATH, index=False)

print("\nFinal merged dataset saved successfully")

# Checking 
print("\nFinal dataset columns:", merged.columns.tolist())
print("\nSample skills categories:")
print(
    merged[["title","company_name", "skill_categories"]].head(10).to_string(index=False)
)