"""
Generate a synthetic retail sales dataset (India-based) for the
Retail Sales Analysis project. Includes deliberate data quality issues
(duplicates, missing discounts, inconsistent category casing) so the
cleaning step in eda_analysis.py is genuine.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N_ORDERS = 2000

# ---------------- Reference data ----------------
region_state_city = {
    "North": [("Uttar Pradesh", "Lucknow"), ("Uttar Pradesh", "Ghaziabad"),
              ("Delhi", "New Delhi"), ("Punjab", "Ludhiana"), ("Haryana", "Gurugram")],
    "South": [("Karnataka", "Bengaluru"), ("Tamil Nadu", "Chennai"),
              ("Telangana", "Hyderabad"), ("Kerala", "Kochi")],
    "East":  [("West Bengal", "Kolkata"), ("Odisha", "Bhubaneswar"), ("Bihar", "Patna")],
    "West":  [("Maharashtra", "Mumbai"), ("Maharashtra", "Pune"),
              ("Gujarat", "Ahmedabad"), ("Rajasthan", "Jaipur")],
}
regions = list(region_state_city.keys())
# West and South are stronger markets, East is weaker
region_weights = [0.27, 0.30, 0.13, 0.30]

categories = {
    "Electronics": {
        "sub": ["Mobile Phones", "Laptops", "Headphones", "Smart Watches", "Tablets"],
        "price_range": (1500, 55000),
        "base_margin": 0.10,     # thin margins, prone to negative profit with discounts
        "qty_range": (1, 3),
    },
    "Furniture": {
        "sub": ["Office Chairs", "Study Tables", "Bookcases", "Sofas", "Bed Frames"],
        "price_range": (2500, 35000),
        "base_margin": 0.18,
        "qty_range": (1, 2),
    },
    "Clothing": {
        "sub": ["Men's Wear", "Women's Wear", "Kids Wear", "Footwear", "Winter Wear"],
        "price_range": (300, 4500),
        "base_margin": 0.35,
        "qty_range": (1, 5),
    },
    "Office Supplies": {
        "sub": ["Stationery", "Printers", "Paper Products", "Storage & Organizers"],
        "price_range": (50, 8000),
        "base_margin": 0.28,
        "qty_range": (1, 8),
    },
    "Groceries": {
        "sub": ["Snacks", "Beverages", "Staples", "Personal Care"],
        "price_range": (40, 1200),
        "base_margin": 0.22,
        "qty_range": (1, 10),
    },
}
category_names = list(categories.keys())
# Electronics & Clothing sell more units overall
category_weights = [0.27, 0.13, 0.24, 0.16, 0.20]

segments = ["Consumer", "Corporate", "Home Office"]
segment_weights = [0.55, 0.30, 0.15]

product_adjectives = ["Pro", "Max", "Plus", "Lite", "Classic", "Ultra", "Smart", "Eco", "Premium", "Basic"]
brands = ["Nova", "Zenith", "Orbit", "Vertex", "Pulse", "Crest", "Aura", "Apex", "Nimbus", "Atlas"]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
total_days = (end_date - start_date).days

# Festive season boost (Oct-Dec) and monsoon dip (Jul-Aug)
def date_weight(d):
    month = d.month
    if month in (10, 11, 12):
        return 2.2
    if month in (7, 8):
        return 0.6
    return 1.0

# Build weighted date pool
all_dates = [start_date + timedelta(days=i) for i in range(total_days + 1)]
date_w = np.array([date_weight(d) for d in all_dates], dtype=float)
date_w = date_w / date_w.sum()

rows = []
for i in range(1, N_ORDERS + 1):
    order_id = f"ORD-{i:05d}"
    order_date = np.random.choice(all_dates, p=date_w)
    ship_date = order_date + timedelta(days=int(np.random.randint(1, 7)))

    region = np.random.choice(regions, p=region_weights)
    state, city = region_state_city[region][np.random.randint(len(region_state_city[region]))]

    category = np.random.choice(category_names, p=category_weights)
    cat_info = categories[category]
    sub_category = np.random.choice(cat_info["sub"])
    product_name = f"{np.random.choice(brands)} {sub_category} {np.random.choice(product_adjectives)}"

    unit_price = np.random.uniform(*cat_info["price_range"])
    quantity = np.random.randint(cat_info["qty_range"][0], cat_info["qty_range"][1] + 1)
    sales = round(unit_price * quantity, 2)

    # Discount: most orders 0-20%, some up to 40%
    discount = round(np.random.choice(
        [0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40],
        p=[0.30, 0.20, 0.18, 0.14, 0.10, 0.05, 0.03]
    ), 2)

    base_margin = cat_info["base_margin"]
    # Profit shrinks (and can go negative) as discount eats into thin margins
    profit = round(sales * (base_margin - discount) + np.random.normal(0, sales * 0.03), 2)

    segment = np.random.choice(segments, p=segment_weights)
    customer_id = f"CUST-{np.random.randint(1, 401):04d}"

    rows.append([
        order_id, order_date.strftime("%Y-%m-%d"), ship_date.strftime("%Y-%m-%d"),
        customer_id, segment, region, state, city,
        category, sub_category, product_name,
        sales, quantity, discount, profit
    ])

df = pd.DataFrame(rows, columns=[
    "Order_ID", "Order_Date", "Ship_Date", "Customer_ID", "Segment",
    "Region", "State", "City", "Category", "Sub_Category", "Product_Name",
    "Sales", "Quantity", "Discount", "Profit"
])

# ---------------- Inject realistic data quality issues ----------------

# 1. Inconsistent category casing for ~3% of rows
inconsistent_idx = df.sample(frac=0.03, random_state=1).index
df.loc[inconsistent_idx, "Category"] = df.loc[inconsistent_idx, "Category"].str.lower()

# 2. Missing Discount values for ~2% of rows
missing_idx = df.sample(frac=0.02, random_state=2).index
df.loc[missing_idx, "Discount"] = np.nan

# 3. Duplicate rows (~15 duplicates)
dupes = df.sample(n=15, random_state=3)
df = pd.concat([df, dupes], ignore_index=True)

# Shuffle rows so duplicates/issues aren't clustered
df = df.sample(frac=1, random_state=4).reset_index(drop=True)

df.to_csv(r"C:\Users\ADMIN\Downloads\retail_sales_project\data\retail_sales_data.csv", index=False)
print(f"Generated dataset with {len(df)} rows (including {len(dupes)} intentional duplicates)")
print(df.head())
