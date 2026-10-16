"""
Sales Data Analysis using NumPy and Pandas.
Generates a reproducible sample dataset (or loads sales_data.csv if present),
cleans it, computes statistics and prints business insights.
"""
import os
import numpy as np
import pandas as pd


def make_dataset(n=500, seed=42):
    rng = np.random.default_rng(seed)
    products = {"Laptop": 55000, "Phone": 25000, "Tablet": 18000, "Headphones": 3000, "Monitor": 12000}
    regions = ["North", "South", "East", "West"]
    names = rng.choice(list(products), n)
    df = pd.DataFrame({
        "OrderID": np.arange(1001, 1001 + n),
        "Date": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "Product": names,
        "Region": rng.choice(regions, n),
        "Quantity": rng.integers(1, 6, n),
    })
    df["UnitPrice"] = df["Product"].map(products) * rng.uniform(0.9, 1.1, n).round(2)
    df["Discount"] = rng.choice([0, 0.05, 0.10, 0.15], n)
    return df.sort_values("Date").reset_index(drop=True)


def load_data(path="sales_data.csv"):
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["Date"])
    df = make_dataset()
    df.to_csv(path, index=False)
    print(f"(Sample dataset created: {path})")
    return df


def clean(df):
    df = df.drop_duplicates("OrderID").dropna(subset=["Product", "Quantity", "UnitPrice"]).copy()
    df["Revenue"] = df["Quantity"] * df["UnitPrice"] * (1 - df["Discount"])
    df["Month"] = df["Date"].dt.to_period("M")
    return df


def analyze(df):
    rev = df["Revenue"].to_numpy()
    print("=" * 60)
    print("SALES DATA ANALYSIS REPORT")
    print("=" * 60)
    print(f"Records: {len(df)}   Period: {df['Date'].min().date()} to {df['Date'].max().date()}\n")

    print("--- NumPy statistics on Revenue ---")
    print(f"Total   : {np.sum(rev):,.2f}")
    print(f"Mean    : {np.mean(rev):,.2f}")
    print(f"Median  : {np.median(rev):,.2f}")
    print(f"Std Dev : {np.std(rev):,.2f}")
    print(f"Min/Max : {np.min(rev):,.2f} / {np.max(rev):,.2f}")
    print(f"25/75th percentile: {np.percentile(rev, 25):,.2f} / {np.percentile(rev, 75):,.2f}")

    # Outliers using IQR
    q1, q3 = np.percentile(rev, [25, 75])
    iqr = q3 - q1
    outliers = df[(df["Revenue"] > q3 + 1.5 * iqr) | (df["Revenue"] < q1 - 1.5 * iqr)]
    print(f"Outlier orders (IQR rule): {len(outliers)}")

    print("\n--- Revenue by Product ---")
    by_prod = df.groupby("Product").agg(Orders=("OrderID", "count"), Units=("Quantity", "sum"),
                                         Revenue=("Revenue", "sum")).sort_values("Revenue", ascending=False)
    print(by_prod.round(2))

    print("\n--- Revenue by Region ---")
    by_reg = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    print(by_reg.round(2))

    print("\n--- Monthly Revenue ---")
    monthly = df.groupby("Month")["Revenue"].sum()
    print(monthly.round(2))

    print("\n--- Product x Region Pivot (Revenue) ---")
    print(pd.pivot_table(df, values="Revenue", index="Product", columns="Region", aggfunc="sum").round(0))

    corr = np.corrcoef(df["Discount"], df["Quantity"])[0, 1]

    print("\n--- INSIGHTS ---")
    print(f"1. Top product: {by_prod.index[0]} contributes {by_prod['Revenue'].iloc[0] / rev.sum():.1%} of revenue.")
    print(f"2. Best region: {by_reg.index[0]}; weakest: {by_reg.index[-1]}.")
    print(f"3. Best month: {monthly.idxmax()} ({monthly.max():,.0f}); worst: {monthly.idxmin()} ({monthly.min():,.0f}).")
    print(f"4. Average order value: {rev.mean():,.0f}.")
    print(f"5. Correlation between discount and quantity: {corr:.2f} "
          f"({'discounts barely drive volume' if abs(corr) < 0.2 else 'discounts influence volume'}).")
    growth = (monthly.iloc[-1] - monthly.iloc[0]) / monthly.iloc[0]
    print(f"6. Revenue change first -> last month: {growth:+.1%}.")


if __name__ == "__main__":
    analyze(clean(load_data()))
