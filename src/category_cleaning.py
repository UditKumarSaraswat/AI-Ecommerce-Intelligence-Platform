
import pandas as pd
import os

# Load category translation dataset
categories = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)

print("Original dataset shape:", categories.shape)

# Remove duplicate category names
categories = categories.drop_duplicates(
    subset="product_category_name"
)

# Clean Portuguese category names
categories["product_category_name"] = (
    categories["product_category_name"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Clean English category names
categories["product_category_name_english"] = (
    categories["product_category_name_english"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Save cleaned dataset
os.makedirs("data/processed", exist_ok=True)

output_path = "data/processed/categories_cleaned.csv"

categories.to_csv(output_path, index=False)

print("\nCATEGORY CLEANING COMPLETED!")

print("Cleaned dataset shape:", categories.shape)

print("\nMissing values:")
print(categories.isnull().sum())

print("\nFirst 5 records:")
print(categories.head())

print("\nSaved successfully at:", output_path)
