import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = BASE_DIR / "data" / "raw" / "job_postings.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "cleaned_job.csv"

# Load the dataset
df = pd.read_csv(RAW_PATH, low_memory=False)

print("Original Dataset shape:", df.shape)

selected_columns = [
    "job_id",
    "company_id",
    "title",
    "description",
    "location",
    "formatted_experience_level",
    "formatted_work_type",
    "job_posting_url"
]

df = df[selected_columns].copy()

# Remove records without a job description
df = df.dropna(subset=["description"])

# Handle missing values
df["formatted_experience_level"] = df["formatted_experience_level"].fillna("Not Specified")
df["company_id"] = df["company_id"].astype("Int64")  # Use Int64 to allow for NaN values

# Remove extra whitespaces in text fields
text_columns = ["title", 
                "description", 
                "location"]

for col in text_columns:
    df[col] = ( df[col].str.replace(r"\s+", " ", regex=True)  # Replace multiple spaces with a single space
                .str.strip()  # Remove leading and trailing spaces
              )

# Remove duplicate job IDs
df = df.drop_duplicates(subset=["job_id"])

# Save the cleaned dataset
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
df.to_csv(OUTPUT_PATH, index=False)

print("Cleaned Dataset shape:", df.shape)
print("Cleaned dataset saved successfully")

