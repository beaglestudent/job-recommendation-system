import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "data" / "processed" / "jobs_with_skills.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "skill_evaluation.csv"

# Load dataset
df = pd.read_csv(INPUT_PATH, low_memory=False)

# Separate jobs by6 extraction result
with_skills = df[df["skill_count"]>0]
without_skills = df[df["skill_count"]==0]

# Sample from both groups
sample_with = with_skills.sample(n=25, random_state=42)
sample_without = without_skills.sample(n=25, random_state=42)

# Combine and Shuffle samples
evaluation = pd.concat(
    [sample_with, sample_without],
    ignore_index = True
).sample(frac=1, random_state=42)

# Select columns for manual evaluation
evaluation = evaluation[
   [ "job_id",
    "title",
    "description",
    "technical_skills"]
].copy()

# Add a column for manually verfied skills
evaluation["actual_skills"] = ""

# Save evaluation dataset
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok = True)
evaluation.to_csv(OUTPUT_PATH, index = False)

print("Evaluation sample created:", len(evaluation))
print("Saved to:", OUTPUT_PATH)