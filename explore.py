import pandas as pd

# Read the file we saved (instant, no download)
df = pd.read_csv("superstore.csv")

# 1. Size
print("Total rows (orders):", len(df))

# 2. The big totals
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
print(f"\nTotal Sales:  ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")

# 3. Overall profit margin = profit divided by sales, as a percentage
margin = (total_profit / total_sales) * 100
print(f"Overall Profit Margin: {margin:.1f}%")

# 4. Averages per order line
print(f"\nAverage Sales per line:    ${df['Sales'].mean():,.2f}")
print(f"Average Profit per line:   ${df['Profit'].mean():,.2f}")
print(f"Average Discount:          {df['Discount'].mean()*100:.1f}%")

# 5. How many order lines actually LOST money?
loss_making = (df["Profit"] < 0).sum()
loss_pct = (loss_making / len(df)) * 100
print(f"\nOrder lines with a LOSS: {loss_making} ({loss_pct:.1f}% of all lines)")