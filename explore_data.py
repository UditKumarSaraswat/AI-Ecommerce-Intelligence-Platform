
import pandas as pd

orders = pd.read_csv("data/raw/olist_orders_dataset.csv")

print("DATASET SHAPE:")
print(orders.shape)

print("\nCOLUMN NAMES:")
print(orders.columns.tolist())

print("\nORDER STATUS COUNT:")
print(orders["order_status"].value_counts())

print("\nDUPLICATE ORDER IDs:")
print(orders["order_id"].duplicated().sum())

print("\nORDER DATE RANGE:")
print(orders["order_purchase_timestamp"].min())
print(orders["order_purchase_timestamp"].max())
