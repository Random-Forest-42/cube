import sqlite3
import pandas as pd

# Connect to your SQLite database
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

min_case_when_sql = ''
for i in range(6, 26):
    min_case_when_sql += f",\n    min(case when average < {i} * 100 then days_since_first_competition else null end) as days_sub_{i}"

query = f"""
select
    personId
    {min_case_when_sql}
from
    results_extended_with_rank
where
    eventId = '333'
    and average > 0
    and average < 2500
group by
    personId
"""

cursor.execute(query)
df = pd.read_sql_query(query, conn)
df.iloc[0]['days_sub_11']

import math
import matplotlib.pyplot as plt
import seaborn as sns

cols = [f"days_sub_{i}" for i in range(7, 16)]
n = len(cols)
cols_per_row = 3
rows = math.ceil(n / cols_per_row)

fig, axes = plt.subplots(rows, cols_per_row, figsize=(cols_per_row * 4, rows * 3))
axes = axes.flatten()

for ax, col in zip(axes, cols):
    s = df[col].dropna()
    if s.empty:
        ax.set_visible(False)
        continue
    # Set custom xlim for left-heavy distributions
    if col in ["days_sub_15", "days_sub_14", "days_sub_13"]:
        # Set a tighter xlim based on the 95th percentile
        right = s.quantile(0.95)
        left = s.min()
        sns.histplot(s, bins=30, kde=True, ax=ax, color="#4c72b0")
        ax.set_xlim(left, right)
    else:
        sns.histplot(s, bins=30, kde=True, ax=ax, color="#4c72b0")
    ax.axvline(s.median(), color="red", linestyle="--", linewidth=1)
    p20 = s.quantile(0.2)
    ax.axvline(p20, color="green", linestyle=":", linewidth=1)
    p10 = s.quantile(0.1)
    ax.axvline(p10, color="orange", linestyle=":", linewidth=1)
    ax.set_title(col)
    ax.set_xlabel("Days")
    ax.set_ylabel("Count")
    ax.text(0.98, 0.95, f"n={s.size}\nmean={s.mean():.1f}\nmed={s.median():.1f}\np20={p20:.1f}\np10={p10:.1f}",
            transform=ax.transAxes, ha="right", va="top", fontsize=8)

# hide any extra axes
for ax in axes[len(cols):]:
    ax.set_visible(False)

plt.tight_layout()
plt.show()
