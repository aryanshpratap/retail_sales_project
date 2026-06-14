# Retail Sales Analysis (India) — Data Analyst Project

## Overview
This project analyzes two years (2023-2024) of retail sales transactions across
India to uncover trends in revenue, profitability, regional performance, and
the impact of discounting on margins. It demonstrates an end-to-end data
analyst workflow: data cleaning, exploratory analysis, SQL querying, and
dashboard-ready outputs.

## Dataset
A representative retail transactions dataset (2,000 orders, 15 columns)
covering:
- **Order details:** Order ID, Order Date, Ship Date
- **Customer info:** Customer ID, Segment (Consumer / Corporate / Home Office)
- **Location:** Region, State, City (covering North, South, East, West India)
- **Product info:** Category, Sub-Category, Product Name
- **Metrics:** Sales, Quantity, Discount, Profit

The raw data included realistic data quality issues — duplicate records,
missing discount values, and inconsistent category text casing — which were
identified and resolved during cleaning.

## Tools Used
- **Python (Pandas, NumPy)** — data cleaning and aggregation
- **Seaborn / Matplotlib** — exploratory visualizations
- **SQL (SQLite)** — business-insight queries
- **Power BI / Tableau** — interactive dashboard (see guide below)

## Data Cleaning Steps
1. Removed 15 exact duplicate rows
2. Standardized inconsistent `Category` text casing (e.g., "electronics" → "Electronics")
3. Filled 40 missing `Discount` values with 0
4. Converted date columns to datetime and derived `Year`, `Month`, and `Profit_Margin_%`

Result: a clean dataset of 2,000 unique, analysis-ready records.

## Key Insights

1. **Electronics drives volume but not profit.** Electronics accounts for
   ~64% of total sales (Rs. 3.26 crore) but only a 0.11% profit margin —
   essentially break-even — because of frequent high discounts on
   already thin-margin products.

2. **Clothing and Office Supplies are the most profitable categories**,
   with profit margins of 25.1% and 19.2% respectively, despite
   contributing far less to total revenue.

3. **Discounting strongly erodes margin.** Discount and profit margin show
   a strong negative correlation (-0.69) — orders with discounts above
   30% are frequently loss-making, especially in Electronics.

4. **Seasonality is significant.** Sales spike sharply in October-December
   (festive season), roughly 2-3x the monthly average, while July-August
   (monsoon) sees the lowest sales.

5. **North India leads in revenue** (Rs. 1.48 crore), but the **East region
   has the highest profit margin (6.8%)** despite lower sales volume,
   suggesting more efficient discounting practices there.

6. **Consumer segment dominates**, contributing ~58% of total sales and
   profit, followed by Corporate (28%) and Home Office (14%).

## Visualizations
All charts are in the `charts/` folder:

| File | Description |
|------|-------------|
| `01_sales_by_category.png` | Total sales by product category |
| `02_profit_margin_by_category.png` | Profit margin (%) by category |
| `03_monthly_sales_trend.png` | Monthly sales trend, 2023-2024 |
| `04_sales_by_region.png` | Total sales by region |
| `05_profit_distribution_by_category.png` | Profit distribution (boxplot) by category |
| `06_discount_vs_profit_margin.png` | Discount vs. profit margin relationship |
| `07_top10_products.png` | Top 10 products by sales |

## SQL Analysis
The cleaned dataset is loaded into `retail_sales.db` (SQLite, table `sales`).
See `sql_queries.sql` for all queries, including:
- Revenue and profit margin by category
- Top 5 states by sales
- Monthly revenue trend
- Average discount and profit margin by region
- Top 10 loss-making orders
- Customer segment performance
- Top 5 customers by spend

## Building the Power BI / Tableau Dashboard
Use `data/retail_sales_cleaned.csv` as the data source. Suggested dashboard layout:

**KPI Cards (top row):**
- Total Sales, Total Profit, Overall Profit Margin %, Total Orders

**Visuals:**
- Bar chart: Sales and Profit by Category (dual-axis)
- Line chart: Monthly Sales Trend with a slicer/filter for Year
- Map or bar chart: Sales by State/Region
- Bar chart: Top 10 Products by Sales
- Scatter plot: Discount vs Profit Margin, colored by Category

**Filters/Slicers:**
- Region, Category, Segment, Year

**Steps:**
1. Open Power BI Desktop / Tableau and import `retail_sales_cleaned.csv`
2. Verify data types (Order_Date as Date, Discount/Profit_Margin_% as percentage)
3. Build the visuals above on a single dashboard page
4. Add slicers for Region, Category, Segment, and Year
5. Add KPI cards using the measures listed above
6. Apply a consistent color theme and save/publish

## How to Reproduce
```bash
python generate_data.py     # generates data/retail_sales_data.csv
python eda_analysis.py       # cleans data, prints insights, saves charts
python sql_analysis.py       # loads SQLite DB and runs SQL queries
```

## Project Structure
```
retail_sales_project/
├── data/
│   ├── retail_sales_data.csv       # raw dataset
│   └── retail_sales_cleaned.csv    # cleaned dataset
├── charts/                          # generated visualizations
├── retail_sales.db                  # SQLite database
├── generate_data.py
├── eda_analysis.py
├── sql_analysis.py
├── sql_queries.sql
└── README.md
```
