import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("superstore.csv")

# Turn the text date into a real date Python understands
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")

# Group by month and add up the sales in each month
monthly = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
monthly.index = monthly.index.to_timestamp()   # make the dates plottable

print("First few months of sales:")
print(monthly.head())

# Compare the first year's total sales to the last year's (growth)
df["Year"] = df["Order Date"].dt.year
yearly = df.groupby("Year")["Sales"].sum()
print("\nSales by year:")
print(yearly)

first_year = yearly.iloc[0]
last_year = yearly.iloc[-1]
growth = ((last_year - first_year) / first_year) * 100
print(f"\nGrowth from {yearly.index[0]} to {yearly.index[-1]}: {growth:.1f}%")

# --- The line chart ---
plt.figure(figsize=(11, 5))
plt.plot(monthly.index, monthly.values, color="steelblue")
plt.title("Monthly Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Sales ($)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("sales_trend.png")   # save FIRST
print("Chart saved as sales_trend.png")   # confirm it happened

plt.show()   # then show the pop-up