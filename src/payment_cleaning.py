
import pandas as pd
import os

# Load payments dataset
payments = pd.read_csv(
    "data/raw/olist_order_payments_dataset.csv"
)

print("Original dataset shape:", payments.shape)

# Remove exact duplicate rows
payments = payments.drop_duplicates()

# Standardize payment type
payments["payment_type"] = (
    payments["payment_type"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Check invalid payment values
print("\nInvalid payment values:")
print("Negative installments:",
      (payments["payment_installments"] < 0).sum())

print("Negative payment amounts:",
      (payments["payment_value"] < 0).sum())

# Keep valid payment records
payments = payments[
    (payments["payment_installments"] >= 0) &
    (payments["payment_value"] >= 0)
].copy()

# Create processed folder
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
output_path = "data/processed/payments_cleaned.csv"

payments.to_csv(output_path, index=False)

print("\nPAYMENT CLEANING COMPLETED!")

print("Cleaned dataset shape:", payments.shape)

print("\nPayment type distribution:")
print(payments["payment_type"].value_counts())

print("\nTotal payment value:",
      round(payments["payment_value"].sum(), 2))

print("\nFirst 5 records:")
print(payments.head())

print("\nSaved successfully at:", output_path)
