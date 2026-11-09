
import pandas as pd
import os

data_path = "data/raw"

files = os.listdir(data_path)

print("DATASET FILES:")
for file in files:
    print(file)

print("\nCHECKING ORDERS DATASET")

orders = pd.read_csv(
    os.path.join(data_path, "olist_orders_dataset.csv")
)

print("\nFirst 5 records:")
print(orders.head())

print("\nDataset information:")
print(orders.info())

print("\nMissing values:")
print(orders.isnull().sum())

print("\nTotal orders:", len(orders))

print("\nDATASET LOADED SUCCESSFULLY!")
