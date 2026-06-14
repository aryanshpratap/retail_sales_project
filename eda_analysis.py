"""
Retail Sales Analysis - Exploratory Data Analysis
Performs data cleaning, aggregation, and generates visualizations
for the synthetic retail sales dataset.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

RAW_PATH = r"C:\Users\ADMIN\Downloads\retail_sales_project\data\retail_sales_data.csv"
CLEAN_PATH = r"C:\Users\ADMIN\Downloads\retail_sales_project\data\cleaned_retail_sales_data.csv"
CHART_DIR = r"C:\Users\ADMIN\Downloads\retail_sales_project\charts"

# ============================================================
# 1. LOAD & INSPECT
# ============================================================
df = pd.read_csv(RAW_PATH)
print("=" * 60)
print("RAW DATA OVERVIEW")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"\nUnique Category values (before cleaning): {df['Category'].unique()}")

# ============================================================
# 2. DATA CLEANING
# ============================================================
# Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
print(f"\nRemoved {before - len(df)} duplicate rows")

# Standardize Category casing (title case)
df["Category"] = df["Category"].str.title()

# Fill missing Discount with 0 (assume no discount applied if not recorded)
missing_discount = df["Discount"].isnull().sum()
df["Discount"] = df["Discount"].fillna(0)
print(f"Filled {missing_discount} missing Discount values with 0")

# Convert dates
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])

# Derived columns
df["Year"] = df["Order_Date"].dt.year
df["Month"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.strftime("%b %Y")
df["Profit_Margin_%"] = (df["Profit"] / df["Sales"] * 100).round(2)

print(f"\nCleaned shape: {df.shape}")
df.to_csv(CLEAN_PATH, index=False)
print(f"Saved cleaned dataset to {CLEAN_PATH}")

# ============================================================
# 3. KEY METRICS
# ============================================================
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
overall_margin = total_profit / total_sales * 100
total_orders = df["Order_ID"].nunique()
avg_order_value = total_sales / total_orders

print("\n" + "=" * 60)
print("KEY METRICS")
print("=" * 60)
print(f"Total Sales:        Rs. {total_sales:,.2f}")
print(f"Total Profit:       Rs. {total_profit:,.2f}")
print(f"Overall Margin:     {overall_margin:.2f}%")
print(f"Total Orders:       {total_orders:,}")
print(f"Avg Order Value:    Rs. {avg_order_value:,.2f}")

# ============================================================
# 4. CATEGORY-LEVEL ANALYSIS
# ============================================================
cat_summary = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order_ID", "count")
).reset_index()
cat_summary["Profit_Margin_%"] = (cat_summary["Total_Profit"] / cat_summary["Total_Sales"] * 100).round(2)
cat_summary = cat_summary.sort_values("Total_Sales", ascending=False)

print("\n" + "=" * 60)
print("SALES & PROFIT BY CATEGORY")
print("=" * 60)
print(cat_summary.to_string(index=False))

# ============================================================
# 5. REGION-LEVEL ANALYSIS
# ============================================================
region_summary = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).reset_index().sort_values("Total_Sales", ascending=False)

print("\n" + "=" * 60)
print("SALES & PROFIT BY REGION")
print("=" * 60)
print(region_summary.to_string(index=False))

# ============================================================
# 6. MONTHLY TREND
# ============================================================
monthly = df.groupby(["Year", "Month"]).agg(
    Total_Sales=("Sales", "sum")
).reset_index()
monthly["Label"] = pd.to_datetime(monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str) + "-01")
monthly = monthly.sort_values("Label")

# ============================================================
# 7. TOP PRODUCTS
# ============================================================
top_products = df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()

print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY SALES")
print("=" * 60)
print(top_products.to_string(index=False))

# ============================================================
# 8. DISCOUNT vs PROFIT
# ============================================================
discount_corr = df[["Discount", "Profit_Margin_%"]].corr().iloc[0, 1]
print(f"\nCorrelation between Discount and Profit Margin: {discount_corr:.2f}")

# ============================================================
# VISUALIZATIONS
# ============================================================

# 1. Total Sales by Category
plt.figure(figsize=(8, 5))
sns.barplot(data=cat_summary, x="Total_Sales", y="Category", hue="Category", palette="viridis", legend=False)
plt.title("Total Sales by Category")
plt.xlabel("Total Sales (Rs.)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/01_sales_by_category.png", dpi=120)
plt.close()

# 2. Profit Margin by Category
plt.figure(figsize=(8, 5))
colors = ["#2a9d8f" if x >= 0 else "#e76f51" for x in cat_summary.sort_values("Profit_Margin_%")["Profit_Margin_%"]]
sns.barplot(data=cat_summary.sort_values("Profit_Margin_%"), x="Profit_Margin_%", y="Category",
            hue="Category", palette=colors, legend=False)
plt.title("Profit Margin (%) by Category")
plt.xlabel("Profit Margin (%)")
plt.ylabel("")
plt.axvline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/02_profit_margin_by_category.png", dpi=120)
plt.close()

# 3. Monthly Sales Trend
plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly, x="Label", y="Total_Sales", marker="o", color="#264653")
plt.title("Monthly Sales Trend (2023-2024)")
plt.xlabel("Month")
plt.ylabel("Total Sales (Rs.)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/03_monthly_sales_trend.png", dpi=120)
plt.close()

# 4. Sales by Region
plt.figure(figsize=(7, 5))
sns.barplot(data=region_summary, x="Region", y="Total_Sales", hue="Region", palette="crest", legend=False)
plt.title("Total Sales by Region")
plt.ylabel("Total Sales (Rs.)")
plt.xlabel("")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/04_sales_by_region.png", dpi=120)
plt.close()

# 5. Profit distribution by Category (boxplot)
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Category", y="Profit", hue="Category", palette="Set2", legend=False)
plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
plt.title("Profit Distribution by Category")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/05_profit_distribution_by_category.png", dpi=120)
plt.close()

# 6. Discount vs Profit Margin scatter
plt.figure(figsize=(7, 5))
sns.scatterplot(data=df, x="Discount", y="Profit_Margin_%", hue="Category", alpha=0.5, palette="tab10")
plt.title("Discount vs Profit Margin")
plt.xlabel("Discount")
plt.ylabel("Profit Margin (%)")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/06_discount_vs_profit_margin.png", dpi=120)
plt.close()

# 7. Top 10 Products by Sales
plt.figure(figsize=(9, 5))
sns.barplot(data=top_products, x="Sales", y="Product_Name", hue="Product_Name", palette="mako", legend=False)
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales (Rs.)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/07_top10_products.png", dpi=120)
plt.close()

print("\nAll charts saved to:", CHART_DIR)
print("\nDone.")
