
import pandas as pd
import os

# Load customers dataset
input_path = "data/raw/olist_customers_dataset.csv"

customers = pd.read_csv(input_path)

print("Original dataset shape:", customers.shape)

# Remove duplicate customer IDs
customers = customers.drop_duplicates(
    subset="customer_id"
)

# Clean city names
customers["customer_city"] = (
    customers["customer_city"]
    .str.strip()
    .str.lower()
)

# Standardize state codes
customers["customer_state"] = (
    customers["customer_state"]
    .str.strip()
    .str.upper()
)

# Keep ZIP code prefixes as five-character strings
customers["customer_zip_code_prefix"] = (
    customers["customer_zip_code_prefix"]
    .astype("string")
    .str.zfill(5)
)

# Create processed folder
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/customers_cleaned.csv"

customers.to_csv(output_path, index=False)

print("\nCUSTOMER CLEANING COMPLETED!")

print("Cleaned dataset shape:", customers.shape)

print("\nDuplicate customer IDs:",
      customers["customer_id"].duplicated().sum())

print("\nMissing values:")
print(customers.isnull().sum())

print("\nFirst 5 records:")
print(customers.head())

print("\nSaved successfully at:", output_path)
