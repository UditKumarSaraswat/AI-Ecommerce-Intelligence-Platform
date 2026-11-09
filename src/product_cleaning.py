
import pandas as pd
import os

# Load products dataset
products = pd.read_csv(
    "data/raw/olist_products_dataset.csv"
)

print("Original dataset shape:", products.shape)

# Remove duplicate product IDs
products = products.drop_duplicates(
    subset="product_id"
)

# Clean category names
products["product_category_name"] = (
    products["product_category_name"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Check missing values
print("\nMissing values:")
print(products.isnull().sum())

# Create processed folder
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/products_cleaned.csv"

products.to_csv(output_path, index=False)

print("\nPRODUCT CLEANING COMPLETED!")
print("Cleaned dataset shape:", products.shape)

print("\nFirst 5 records:")
print(products.head())

print("\nSaved successfully at:", output_path)
