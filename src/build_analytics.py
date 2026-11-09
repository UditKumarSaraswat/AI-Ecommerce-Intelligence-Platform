
import pandas as pd
import os

# Load cleaned datasets
orders = pd.read_csv("data/processed/orders_cleaned.csv")
customers = pd.read_csv("data/processed/customers_cleaned.csv")
items = pd.read_csv("data/processed/order_items_cleaned.csv")
products = pd.read_csv("data/processed/products_cleaned.csv")
payments = pd.read_csv("data/processed/payments_cleaned.csv")
reviews = pd.read_csv("data/processed/reviews_cleaned.csv")
sellers = pd.read_csv("data/processed/sellers_cleaned.csv")
categories = pd.read_csv("data/processed/categories_cleaned.csv")

print("ALL DATASETS LOADED SUCCESSFULLY!")

# 1. Prepare product-level sales details
sales_detail = (
    orders
    .merge(items, on="order_id", how="inner")
    .merge(customers, on="customer_id", how="left")
    .merge(products, on="product_id", how="left")
    .merge(sellers, on="seller_id", how="left")
    .merge(categories, on="product_category_name", how="left")
)

# 2. Aggregate payments at order level
payment_summary = (
    payments.groupby("order_id", as_index=False)
    .agg(
        total_payment=("payment_value", "sum"),
        payment_installments=("payment_installments", "max")
    )
)

# 3. Aggregate reviews at order level
review_summary = (
    reviews.groupby("order_id", as_index=False)
    .agg(
        average_review_score=("review_score", "mean"),
        review_count=("review_id", "nunique")
    )
)

# 4. Prepare order-level summary
order_summary = (
    orders
    .merge(customers, on="customer_id", how="left")
    .merge(payment_summary, on="order_id", how="left")
    .merge(review_summary, on="order_id", how="left")
)

# 5. Create processed folder
os.makedirs("data/processed", exist_ok=True)

# 6. Save integrated datasets
sales_detail.to_csv(
    "data/processed/sales_detail.csv",
    index=False
)

order_summary.to_csv(
    "data/processed/order_summary.csv",
    index=False
)

# 7. Calculate business KPIs
total_orders = order_summary["order_id"].nunique()

total_revenue = sales_detail["price"].sum()

average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

average_review = reviews["review_score"].mean()

delivered_orders = (
    order_summary["order_status"] == "delivered"
).sum()

delivery_rate = (
    delivered_orders / total_orders * 100
    if total_orders else 0
)

print("\nDATA INTEGRATION COMPLETED!")

print("\nSALES DETAIL SHAPE:", sales_detail.shape)
print("ORDER SUMMARY SHAPE:", order_summary.shape)

print("\nBUSINESS KPIs")
print("--------------------------")
print("Total Orders:", total_orders)
print("Product Revenue: R$", round(total_revenue, 2))
print("Average Order Value: R$", round(average_order_value, 2))
print("Average Review Score:", round(average_review, 2))
print("Delivered Orders:", delivered_orders)
print("Delivery Rate:", round(delivery_rate, 2), "%")

print("\nFILES SAVED SUCCESSFULLY!")
