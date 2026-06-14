"""
Retail Sales Analysis - SQL Layer
Loads the cleaned dataset into a SQLite database and runs
business-insight queries.
"""

import sqlite3
import pandas as pd

CLEAN_PATH = r"C:\Users\ADMIN\Downloads\retail_sales_project\data\cleaned_retail_sales_data.csv"
DB_PATH = r"C:\Users\ADMIN\Downloads\retail_sales_project\data\retail_sales.db"

# Load cleaned data into SQLite
df = pd.read_csv(CLEAN_PATH)
conn = sqlite3.connect(DB_PATH)
df.to_sql("sales", conn, if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into 'sales' table in {DB_PATH}")

queries = {
    "1. Total Revenue and Profit by Category": """
        SELECT Category,
               ROUND(SUM(Sales), 2) AS Total_Sales,
               ROUND(SUM(Profit), 2) AS Total_Profit,
               ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin_Pct
        FROM sales
        GROUP BY Category
        ORDER BY Total_Sales DESC;
    """,

    "2. Top 5 States by Total Sales": """
        SELECT State,
               ROUND(SUM(Sales), 2) AS Total_Sales,
               COUNT(*) AS Orders
        FROM sales
        GROUP BY State
        ORDER BY Total_Sales DESC
        LIMIT 5;
    """,

    "3. Monthly Revenue Trend": """
        SELECT Year, Month,
               ROUND(SUM(Sales), 2) AS Total_Sales
        FROM sales
        GROUP BY Year, Month
        ORDER BY Year, Month;
    """,

    "4. Average Discount and Profit Margin by Region": """
        SELECT Region,
               ROUND(AVG(Discount) * 100, 2) AS Avg_Discount_Pct,
               ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin_Pct
        FROM sales
        GROUP BY Region
        ORDER BY Profit_Margin_Pct DESC;
    """,

    "5. Top 10 Loss-Making Orders": """
        SELECT Order_ID, Category, Sub_Category, Sales, Discount, Profit
        FROM sales
        WHERE Profit < 0
        ORDER BY Profit ASC
        LIMIT 10;
    """,

    "6. Customer Segment Performance": """
        SELECT Segment,
               COUNT(*) AS Orders,
               ROUND(SUM(Sales), 2) AS Total_Sales,
               ROUND(AVG(Sales), 2) AS Avg_Order_Value,
               ROUND(SUM(Profit), 2) AS Total_Profit
        FROM sales
        GROUP BY Segment
        ORDER BY Total_Sales DESC;
    """,

    "7. Top 5 Customers by Total Spend": """
        SELECT Customer_ID,
               COUNT(*) AS Orders,
               ROUND(SUM(Sales), 2) AS Total_Spend
        FROM sales
        GROUP BY Customer_ID
        ORDER BY Total_Spend DESC
        LIMIT 5;
    """,
}

print("\n" + "=" * 70)
for title, query in queries.items():
    print(f"\n{title}")
    print("-" * 70)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()
print("\nDone.")
