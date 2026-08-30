import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("superstore.csv")

# The correlation coefficient between Discount and Profit
# Ranges from -1 (move oppositely) to +1 (move together); 0 = no relationship
corr = df["Discount"].corr(df["Profit"])
print(f"Correlation between Discount and Profit: {corr:.3f}")

# Average profit at each discount level - shows the pattern clearly
avg_profit_by_discount = df.groupby("Discount")["Profit"].mean()
print("\nAverage profit at each discount level:")
print(avg_profit_by_discount)

# --- Scatter plot: each dot is one order line ---
plt.figure(figsize=(10, 6))
plt.scatter(df["Discount"], df["Profit"], alpha=0.3, color="darkorange")
plt.axhline(0, color="red", linewidth=1)   # the break-even line (profit = 0)
plt.title(f"Discount vs Profit (correlation = {corr:.3f})")
plt.xlabel("Discount")
plt.ylabel("Profit ($)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("discount_vs_profit.png")
print("\nChart saved as discount_vs_profit.png")
plt.show()