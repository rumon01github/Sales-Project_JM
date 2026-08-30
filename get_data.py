import pandas as pd

# Live no-login copy of the classic Superstore dataset
url = "https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv"

print("Downloading Superstore data...")
df = pd.read_csv(url, encoding="latin-1")

# Save locally so we never download again
df.to_csv("superstore.csv", index=False)

print("Done. Saved to superstore.csv")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))
print("\nColumn names:")
print(list(df.columns))
print("\nFirst few rows:")
print(df.head())