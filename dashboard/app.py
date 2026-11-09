
import os
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from google import genai


# Load Gemini API key from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="AI E-Commerce Intelligence",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 AI E-Commerce Intelligence Platform")
st.caption("Interactive Business Analytics Dashboard | Olist Dataset")


@st.cache_data
def load_data():
    sales = pd.read_csv("data/processed/sales_detail.csv")
    orders = pd.read_csv("data/processed/order_summary.csv")

    sales["order_purchase_timestamp"] = pd.to_datetime(
        sales["order_purchase_timestamp"], errors="coerce"
    )

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], errors="coerce"
    )

    return sales, orders


try:
    sales, orders = load_data()

    # Sidebar filters
    st.sidebar.title("Dashboard Filters")

    min_date = sales["order_purchase_timestamp"].min().date()
    max_date = sales["order_purchase_timestamp"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    categories = sorted(
        sales["product_category_name_english"]
        .dropna().unique().tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Select Product Categories",
        categories,
        default=[]
    )

    states = sorted(
        sales["customer_state"]
        .dropna().unique().tolist()
    )

    selected_states = st.sidebar.multiselect(
        "Select Customer States",
        states,
        default=[]
    )

    # Apply date filter
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0] if isinstance(date_range, (tuple, list)) else date_range
        end_date = start_date

    sales_filtered = sales[
        sales["order_purchase_timestamp"].dt.date.between(
            start_date, end_date
        )
    ].copy()

    # Apply category filter
    if selected_categories:
        sales_filtered = sales_filtered[
            sales_filtered["product_category_name_english"].isin(
                selected_categories
            )
        ]

    # Apply state filter
    if selected_states:
        sales_filtered = sales_filtered[
            sales_filtered["customer_state"].isin(selected_states)
        ]

    # Filter orders to match selected sales
    selected_order_ids = sales_filtered["order_id"].unique()

    orders_filtered = orders[
        orders["order_id"].isin(selected_order_ids)
    ].copy()

    # KPI calculations
    revenue = sales_filtered["price"].sum()
    total_orders = orders_filtered["order_id"].nunique()
    sales_orders = sales_filtered["order_id"].nunique()

    aov = revenue / sales_orders if sales_orders else 0

    delivered = (
        orders_filtered["order_status"] == "delivered"
    ).sum()

    delivery_rate = (
        delivered / total_orders * 100 if total_orders else 0
    )

    avg_review = orders_filtered["average_review_score"].mean()

    # KPI cards
    st.subheader("Business Performance")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Product Revenue", f"R$ {revenue:,.2f}")
    col3.metric("Average Order Value", f"R$ {aov:,.2f}")
    col4.metric("Delivery Rate", f"{delivery_rate:.2f}%")
    col5.metric(
        "Average Review",
        f"{avg_review:.2f}/5" if pd.notna(avg_review) else "N/A"
    )

    st.divider()

    # Monthly sales trend
    st.subheader("Monthly Sales Trend")

    if not sales_filtered.empty:
        monthly = (
            sales_filtered.dropna(
                subset=["order_purchase_timestamp"]
            )
            .assign(
                month=lambda df: df[
                    "order_purchase_timestamp"
                ].dt.to_period("M").astype(str)
            )
            .groupby("month", as_index=False)["price"]
            .sum()
        )

        fig1 = px.line(
            monthly,
            x="month",
            y="price",
            markers=True,
            title="Monthly Product Revenue",
            labels={"month": "Month", "price": "Revenue (R$)"}
        )

        st.plotly_chart(fig1, use_container_width=True)

    # Category performance
    st.subheader("Top 10 Product Categories")

    if not sales_filtered.empty:
        sales_filtered["category"] = (
            sales_filtered["product_category_name_english"]
            .fillna("Unknown")
        )

        category_sales = (
            sales_filtered.groupby(
                "category", as_index=False
            )["price"]
            .sum()
            .nlargest(10, "price")
        )

        fig2 = px.bar(
            category_sales,
            x="price",
            y="category",
            orientation="h",
            title="Top Categories by Revenue",
            labels={
                "price": "Revenue (R$)",
                "category": "Product Category"
            }
        )

        fig2.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Order status
    st.subheader("Order Status Analysis")

    if not orders_filtered.empty:
        status_data = (
            orders_filtered["order_status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = ["Order Status", "Count"]

        fig3 = px.pie(
            status_data,
            names="Order Status",
            values="Count",
            hole=0.45,
            title="Order Status Distribution"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Customer reviews
    st.subheader("Customer Satisfaction")

    if not orders_filtered.empty:
        review_data = (
            orders_filtered["average_review_score"]
            .dropna()
            .round()
            .value_counts()
            .sort_index()
            .reset_index()
        )

        review_data.columns = ["Review Score", "Count"]

        if not review_data.empty:
            fig4 = px.bar(
                review_data,
                x="Review Score",
                y="Count",
                title="Customer Review Distribution"
            )

            st.plotly_chart(fig4, use_container_width=True)

    if sales_filtered.empty:
        st.warning("No sales found for the selected filters.")

    st.divider()

    # Gemini AI Business Assistant
    st.subheader("🤖 AI Business Assistant")
    st.write(
        "Ask questions about your e-commerce business. "
        "The AI assistant will analyse the currently selected dashboard data."
    )

    question = st.text_input(
        "Ask your business question:",
        placeholder="Example: Which product categories generate the most revenue?"
    )

    if st.button("Ask Gemini AI", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")

        elif not os.getenv("GEMINI_API_KEY"):
            st.error(
                "Gemini API key not found. Please check your .env file "
                "in the main project folder."
            )

        else:
            # Prepare a compact summary of the filtered data
            category_summary = (
                sales_filtered.assign(
                    category=sales_filtered[
                        "product_category_name_english"
                    ].fillna("Unknown")
                )
                .groupby("category")["price"]
                .sum()
                .nlargest(5)
                .round(2)
                .to_dict()
            )

            state_summary = (
                sales_filtered.groupby("customer_state")["price"]
                .sum()
                .nlargest(5)
                .round(2)
                .to_dict()
            )

            status_summary = (
                orders_filtered["order_status"]
                .value_counts()
                .to_dict()
            )

            context = f"""
            E-COMMERCE BUSINESS DATA SUMMARY

            Selected date range: {start_date} to {end_date}
            Selected categories: {selected_categories or "All categories"}
            Selected states: {selected_states or "All states"}

            Total orders: {total_orders}
            Product revenue: R$ {revenue:,.2f}
            Average order value: R$ {aov:,.2f}
            Delivered orders: {delivered}
            Delivery rate: {delivery_rate:.2f}%
            Average review score: {
                round(avg_review, 2) if pd.notna(avg_review) else "N/A"
            }

            Top 5 categories by revenue: {category_summary}
            Top 5 states by revenue: {state_summary}
            Order status counts: {status_summary}
            """

            prompt = f"""
            You are an experienced e-commerce business data analyst.

            Answer the user's question using ONLY the business data
            provided below.

            Rules:
            1. Give clear, practical business insights.
            2. Use the actual figures from the data.
            3. Do not invent statistics or facts.
            4. If the data does not contain the answer, say so clearly.
            5. Suggest useful business actions where appropriate.
            6. Keep the answer easy to understand.

            BUSINESS DATA:
            {context}

            USER QUESTION:
            {question}
            """

            try:
                with st.spinner("Gemini AI is analysing your business data..."):
                    client = genai.Client(
                        api_key=os.getenv("GEMINI_API_KEY")
                    )

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                st.markdown("### 💡 AI Business Analysis")
                st.write(response.text or "Gemini returned an empty response.")

            except Exception as e:
                st.error(
                    "Gemini could not generate a response. "
                    "Please try again later. Technical details: "
                    f"{str(e)}"
                )

    st.success("Interactive dashboard loaded successfully!")

except FileNotFoundError:
    st.error(
        "Dataset files not found. Run "
        "python -m src.build_analytics first."
    )

except Exception as e:
    st.error(f"Something went wrong: {e}")
