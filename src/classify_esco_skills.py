
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR / "data" / "processed"
    / "esco_skill_candidates.csv"
)

OUTPUT_PATH = (
    BASE_DIR / "data" / "processed"
    / "esco_skill_review.csv"
)

CATEGORY_RULES = {
    "Programming Languages": {
        "computer programming",
        "web programming",
    },
    "Databases": {
        "database management systems",
    },
    "Software Engineering": {
        "programming computer systems",
        "designing ict systems or applications",
    },
}


def suggest_category(value):
    if pd.isna(value):
        return ""

    parents = {
        parent.strip().lower()
        for parent in str(value).split("|")
    }

    for category, keywords in CATEGORY_RULES.items():
        if parents & keywords:
            return category

    return ""


def main():
    df = pd.read_csv(INPUT_PATH)

    review = df[
        ["conceptUri", "preferredLabel", "altLabels", "skillType",
         "broaderConceptPT"]
    ].copy()

    # Suggestions are not final approvals
    review["include"] = "review"

    review["category"] = review[
        "broaderConceptPT"
    ].apply(suggest_category)

    review["canonical_name"] = ""
    review["notes"] = ""

    print("\nSuggested category counts:")
    print(review["category"].value_counts(dropna=False))

    print("\nFirst 15 suggestions:")
    print(
        review[["preferredLabel", "category"]]
        .head(15)
        .to_string(index=False)
    )

    # Do not overwrite any existing manual decisions
    if OUTPUT_PATH.exists():
        print(
            "Review file already exists. "
            "Delete or move it only if you want to regenerate it."
        )
        return

    review.to_csv(OUTPUT_PATH, index=False)

    print("Total candidates:", len(review))
    print("\nSuggested category counts:")
    print(review["category"].value_counts(dropna=False))

    print("\nSaved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
