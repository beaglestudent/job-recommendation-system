import pandas as pd
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent

ESCO_PATH = (
    BASE_DIR / "data" / "external" / "digitalSkillsCollection_en.csv"
)

# Load Esco digital skills
df = pd.read_csv(ESCO_PATH)

print("Dataset shape:", df.shape)

print("\nAvailable columns:")
print(
    df[["preferredLabel", "altLabels"]].head(10).to_string(index=False)
)

print("\nMissing values:")
print(
    df[["preferredLabel", "altLabels"]].isnull().sum()
)

print("\nColumn names:")
for column in df.columns:
    print("-", column)

print("\nSample records with metadata:")
print(df.head(3).to_string(index=False))

category_counts = Counter()

for value in df["broaderConceptPT"].dropna():

    # A skill may belong to multiple categories
    categories = value.split("|")

    for category in categories:
        category = category.strip()

        if category:
            category_counts[category] += 1

print("\nTop 30 broader categories:")

for category, count in category_counts.most_common(30):
    print(f"{category}:{count}")

print("\nTotal distinct broader categories:", len(category_counts))