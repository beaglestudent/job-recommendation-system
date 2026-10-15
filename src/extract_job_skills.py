import pandas as pd
from pathlib import Path
from collections import Counter

from src.skill_extraction import extract_skills

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "data" / "processed" / "jobs_final.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "jobs_with_skills.csv"

def main():

    # Load the cleaned job dataset
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    print("Total job postings:", len(df))

    # Extract technical skills from job descriptions
    df["technical_skills"] = df["description"].apply(extract_skills)

    # Count the number of skills per job
    df["skill_count"] = df["technical_skills"].apply(len)

    # Analyse skill extraction coverage
    jobs_with_skills = (df["skill_count"] > 0).sum()
    print("\nJobs with at least one detected skills:", jobs_with_skills)

    print(
        "Skill extraction coverage:"
        f"{jobs_with_skills / len(df)*100:.2f}%"
    )

    # Count skill frequencies
    skill_counts = Counter(
        skill
        for skills in df["technical_skills"]
        for skill in skills
    )

    print("\nTop 20 most frequently detected skills:")
    for skill, count in skill_counts.most_common(20):
        print(f"{skill}:{count}")

    # Display sample jobs
    print("\nSample extracted skills:")
    for _, row in df.head(10).iterrows():
        print(f"\nJob:{row['title']}")
        print(f"Skills:{row['technical_skills']}")

    # Convert lists to string for CSV storage
    df["technical_skills"] = df["technical_skills"].apply(
        lambda skills: ",".join(skills)
    )

    # Save the result
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved dataset:",OUTPUT_PATH)
    print("Final dataset shape:", df.shape)

if __name__ == "__main__":
    main()