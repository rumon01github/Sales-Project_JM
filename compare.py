import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("superstore.csv")

# --- By Region ---
region = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)
region["Margin_%"] = (region["Total_Profit"] / region["Total_Sales"]) * 100
print("Performance by REGION:")
print(region.round(2))

# --- By Category ---
category = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)
category["Margin_%"] = (category["Total_Profit"] / category["Total_Sales"]) * 100
print("\nPerformance by CATEGORY:")
print(category.round(2))

# --- Bar chart: profit by region ---
plt.figure(figsize=(9, 5))
plt.bar(region.index, region["Total_Profit"], color="seagreen")
plt.title("Total Profit by Region")
plt.ylabel("Profit ($)")
plt.tight_layout()
plt.savefig("profit_by_region.png")
print("\nSaved profit_by_region.png")
plt.show()

# --- Bar chart: profit by category ---
plt.figure(figsize=(9, 5))
plt.bar(category.index, category["Total_Profit"], color="mediumpurple")
plt.title("Total Profit by Category")
plt.ylabel("Profit ($)")
plt.tight_layout()
plt.savefig("profit_by_category.png")
print("Saved profit_by_category.png")
plt.show()