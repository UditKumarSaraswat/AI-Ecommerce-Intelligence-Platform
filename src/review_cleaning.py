
import pandas as pd
import os

# Load reviews dataset
reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

print("Original dataset shape:", reviews.shape)

# Remove exact duplicate rows
reviews = reviews.drop_duplicates()

# Clean review comments
reviews["review_comment_title"] = (
    reviews["review_comment_title"]
    .fillna("")
    .astype(str)
    .str.strip()
)

reviews["review_comment_message"] = (
    reviews["review_comment_message"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Convert review dates
date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in date_columns:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )

# Check review scores
print("\nReview score distribution:")
print(reviews["review_score"].value_counts().sort_index())

# Keep valid review scores (1 to 5)
reviews = reviews[
    reviews["review_score"].between(1, 5)
].copy()

# Create processed folder
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/reviews_cleaned.csv"

reviews.to_csv(output_path, index=False)

print("\nREVIEW CLEANING COMPLETED!")

print("Cleaned dataset shape:", reviews.shape)

print("\nMissing values:")
print(reviews.isnull().sum())

print("\nAverage review score:",
      round(reviews["review_score"].mean(), 2))

print("\nSaved successfully at:", output_path)
