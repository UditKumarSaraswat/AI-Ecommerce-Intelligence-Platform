
import pandas as pd
import os

# Load geolocation dataset
geo = pd.read_csv(
    "data/raw/olist_geolocation_dataset.csv"
)

print("Original dataset shape:", geo.shape)

# Remove exact duplicate records
geo = geo.drop_duplicates()

# Standardize city names
geo["geolocation_city"] = (
    geo["geolocation_city"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Standardize state codes
geo["geolocation_state"] = (
    geo["geolocation_state"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# Remove invalid coordinates
geo = geo[
    geo["geolocation_lat"].between(-90, 90) &
    geo["geolocation_lng"].between(-180, 180)
].copy()

# Save cleaned dataset
os.makedirs("data/processed", exist_ok=True)

output_path = "data/processed/geolocation_cleaned.csv"

geo.to_csv(output_path, index=False)

print("\nGEOLOCATION CLEANING COMPLETED!")

print("Cleaned dataset shape:", geo.shape)

print("\nMissing values:")
print(geo.isnull().sum())

print("\nFirst 5 records:")
print(geo.head())

print("\nSaved successfully at:", output_path)
