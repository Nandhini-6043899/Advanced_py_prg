"""
Data Visualization Dashboard using Matplotlib.
Line charts (trends), bar charts (comparisons) and pie charts (share) on one dashboard.
Saves dashboard.png and shows the window when a display is available.
"""
import matplotlib
import os
if not os.environ.get("DISPLAY") and os.name != "nt" and "darwin" not in os.sys.platform:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales_2025 = [120, 135, 150, 145, 170, 185, 175, 190, 210, 230, 260, 300]
sales_2026 = [140, 150, 170, 168, 195, 210, 205, 225, 245, 270, 0, 0]
sales_2026 = [v if v else np.nan for v in sales_2026]

products = ["Laptop", "Phone", "Tablet", "Headphones", "Monitor"]
revenue = [480, 390, 210, 95, 160]
regions = ["North", "South", "East", "West"]
q1 = [85, 70, 60, 90]
q2 = [95, 78, 72, 88]
costs = [30, 25, 20, 15, 10]
cost_labels = ["Salaries", "Marketing", "Logistics", "Rent", "Other"]

colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2"]

fig, axs = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle("Sales Performance Dashboard", fontsize=20, fontweight="bold")

# 1. Line chart - monthly trend, two years
ax = axs[0, 0]
ax.plot(months, sales_2025, marker="o", color=colors[0], label="2025")
ax.plot(months, sales_2026, marker="s", color=colors[1], label="2026")
ax.set_title("Monthly Sales Trend (Rs lakh)")
ax.grid(alpha=0.3)
ax.legend()
ax.tick_params(axis="x", rotation=45)

# 2. Line chart - cumulative sales with fill
ax = axs[0, 1]
cum = np.cumsum(sales_2025)
ax.plot(months, cum, color=colors[2], linewidth=2)
ax.fill_between(months, cum, alpha=0.25, color=colors[2])
ax.set_title("Cumulative Sales 2025")
ax.grid(alpha=0.3)
ax.tick_params(axis="x", rotation=45)

# 3. Bar chart - revenue by product
ax = axs[0, 2]
bars = ax.bar(products, revenue, color=colors)
ax.bar_label(bars, padding=2)
ax.set_title("Revenue by Product")
ax.tick_params(axis="x", rotation=30)

# 4. Grouped bar chart - region by quarter
ax = axs[1, 0]
x = np.arange(len(regions))
w = 0.38
ax.bar(x - w / 2, q1, w, label="Q1", color=colors[0])
ax.bar(x + w / 2, q2, w, label="Q2", color=colors[1])
ax.set_xticks(x, regions)
ax.set_title("Regional Sales: Q1 vs Q2")
ax.legend()

# 5. Pie chart - product share
ax = axs[1, 1]
ax.pie(revenue, labels=products, autopct="%1.1f%%", startangle=90, colors=colors,
       explode=[0.06 if r == max(revenue) else 0 for r in revenue])
ax.set_title("Revenue Share by Product")

# 6. Donut chart - cost breakdown
ax = axs[1, 2]
ax.pie(costs, labels=cost_labels, autopct="%1.0f%%", startangle=140, colors=colors,
       wedgeprops={"width": 0.45})
ax.set_title("Cost Breakdown")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("dashboard.png", dpi=150)
print("Saved dashboard.png")
if matplotlib.get_backend().lower() != "agg":
    plt.show()
