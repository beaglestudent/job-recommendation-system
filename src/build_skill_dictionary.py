import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR / "data" / "external" / "digitalSkillsCollection_en.csv"
)

OUTPUT_PATH = (
    BASE_DIR / "data" / "processed" / "esco_skill_candidates.csv"
)

SELECTED_CATEGORIES = {
    "software and application development and analysis",
    "database and network design and administration",
    "managing, gathering and storing digital data",
    "programming computer systems",
    "designing ict systems or applications",
    "computer programming",
    "database management systems",
    "use databases"
}

def is_relevant_category(value):
    if pd.isna(value):
        return False

    categories = {
        category.strip().lower()
        for category in str(value).split("|")
    }

    return bool(categories & SELECTED_CATEGORIES)

def main():
    df = pd.read_csv(INPUT_PATH)

    filtered = df[
        df["broaderConceptPT"].apply(is_relevant_category)
    ].copy()

    # Keep useful metadata for review
    selected_columns = [
        "conceptUri",
        "preferredLabel",
        "altLabels",
        "description",
        "skillType",
        "broaderConceptPT"
    ]

    filtered = filtered[selected_columns]

    # Remove duplicate ESCO concepts
    filtered = filtered.drop_duplicates(
        subset = ["conceptUri"]
    )

    # Sort for easier manual review
    filtered = filtered.sort_values(
        by = "preferredLabel",
        key = lambda col: col.str.lower()
    )

    # Save candidates without modifying source data
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    filtered.to_csv(OUTPUT_PATH, index=False)

    print("Total ESCO digital skills:", len(df))
    print("Filtered skill candidates:", len(filtered))
    print("Unique skill labels:", filtered["preferredLabel"].nunique())

    print("\nFirst 20 candidates:")
    print(
        filtered[["preferredLabel", "broaderConceptPT"]].head(20).to_string(index=False)
    )

    print("\nSaved to:", OUTPUT_PATH)

    # Create a separate file for reviewing skills
    review = filtered[
        ["conceptUri","preferredLabel","altLabels","skillType"]
    ].copy()

    # columns for manual review
    review["include"] = ""
    review["category"] = ""
    review["canonical_name"] = ""
    review["notes"] = ""

    review_path = (
        BASE_DIR / "data" / "processed" / "esco_skill_review.csv"
    )

    review.to_csv(review_path,index=False)

    print("Review file saved to:", review_path)
    

if __name__ == "__main__":
    main()