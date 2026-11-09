
import pandas as pd
import os

# Load order items dataset
input_path = "data/raw/olist_order_items_dataset.csv"

items = pd.read_csv(input_path)

print("Original dataset shape:", items.shape)

# Remove exact duplicate rows
items = items.drop_duplicates()

# Convert shipping limit date
items["shipping_limit_date"] = pd.to_datetime(
    items["shipping_limit_date"],
    errors="coerce"
)

# Check invalid prices and freight values
print("\nInvalid price values:",
      (items["price"] < 0).sum())

print("Invalid freight values:",
      (items["freight_value"] < 0).sum())

# Keep valid non-negative price and freight records
items = items[
    (items["price"] >= 0) &
    (items["freight_value"] >= 0)
].copy()

# Calculate total item cost
items["total_item_cost"] = (
    items["price"] + items["freight_value"]
)

# Create processed folder
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/order_items_cleaned.csv"

items.to_csv(output_path, index=False)

print("\nORDER ITEMS CLEANING COMPLETED!")

print("Cleaned dataset shape:", items.shape)

print("\nMissing values:")
print(items.isnull().sum())

print("\nFirst 5 records:")
print(items.head())

print("\nTotal product sales value:",
      round(items["price"].sum(), 2))

print("\nSaved successfully at:", output_path)
