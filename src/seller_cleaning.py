
import pandas as pd
import os

# Load sellers dataset
sellers = pd.read_csv(
    "data/raw/olist_sellers_dataset.csv"
)

print("Original dataset shape:", sellers.shape)

# Remove duplicate seller IDs
sellers = sellers.drop_duplicates(
    subset="seller_id"
)

# Clean city names
sellers["seller_city"] = (
    sellers["seller_city"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Standardize state codes
sellers["seller_state"] = (
    sellers["seller_state"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# Format ZIP code prefixes
sellers["seller_zip_code_prefix"] = (
    sellers["seller_zip_code_prefix"]
    .astype("string")
    .str.zfill(5)
)

# Create processed folder
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/sellers_cleaned.csv"

sellers.to_csv(output_path, index=False)

print("\nSELLER CLEANING COMPLETED!")

print("Cleaned dataset shape:", sellers.shape)

print("\nDuplicate seller IDs:",
      sellers["seller_id"].duplicated().sum())

print("\nMissing values:")
print(sellers.isnull().sum())

print("\nFirst 5 records:")
print(sellers.head())

print("\nSaved successfully at:", output_path)
