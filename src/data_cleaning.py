
import pandas as pd
import os

# Load original orders dataset
input_path = "data/raw/olist_orders_dataset.csv"

orders = pd.read_csv(input_path)

print("Original dataset shape:", orders.shape)

# Convert date columns into datetime format
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

# Standardize order status
orders["order_status"] = (
    orders["order_status"].str.strip().str.lower()
)

# Remove duplicate order IDs, if any
orders = orders.drop_duplicates(subset="order_id")

# Create useful business analysis columns
orders["purchase_year"] = (
    orders["order_purchase_timestamp"].dt.year
)

orders["purchase_month"] = (
    orders["order_purchase_timestamp"].dt.month
)

orders["purchase_month_name"] = (
    orders["order_purchase_timestamp"].dt.month_name()
)

# Calculate actual delivery time in days
orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Create processed folder if it does not exist
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/orders_cleaned.csv"
orders.to_csv(output_path, index=False)

# Display results
print("\nCLEANING COMPLETED!")
print("Cleaned dataset shape:", orders.shape)

print("\nMissing values after cleaning:")
print(orders.isnull().sum())

print("\nCleaned dataset preview:")
print(orders.head())

print("\nSaved successfully at:", output_path)
