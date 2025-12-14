import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your SQLite database
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
conn.execute("PRAGMA journal_mode = WAL;")
cursor = conn.cursor()

query = """
select
    res.average
from
(
    SELECT
        T1.personId
        , printf('%04d-%02d-%02d', T2.year, T2.month, T2.day) AS competition_date
        , min(average) as average
    FROM
        results AS T1
    JOIN
        competitions AS T2 ON T1.competitionId = T2.id
    where
        T1.eventId = '333'
        and T1.average > 0
    group by
        personId
        , competition_date
) res
JOIN
(
    SELECT
        T1.personId
        , MIN(printf('%04d-%02d-%02d', T2.year, T2.month, T2.day)) AS first_competition_date
    FROM
        results AS T1
    JOIN
        competitions AS T2 ON T1.competitionId = T2.id
    where
        T1.eventId = '333'
        and T1.average > 0
    GROUP BY
        T1.personId
) first_date
on
    res.personId = first_date.personId
    and res.competition_date = first_date.first_competition_date
"""

cursor.execute(query)
df = pd.read_sql_query(query, conn)
df['average_seconds'] = df['average'] / 100.0


### PLOT
print(f"Found {len(df)} first averages")
print("Stats (in seconds):")
print(df['average_seconds'].describe())

plt.figure(figsize=(12, 6))

max_time = 100

df[df['average_seconds'] <= max_time]['average_seconds'].hist(bins=100, edgecolor='black', alpha=0.7)

plt.title('Average Times at First 3x3x3 Competition')
plt.xlabel('Average Time (Seconds)')
plt.ylabel('Frecuency (Number of competitiors)')
plt.gca().ticklabel_format(style='plain', axis='y')
plt.grid(axis='y', alpha=0.5)
# red column to indicate mean
plt.axvline(df['average_seconds'].mean(), color='red', linestyle='dashed', linewidth=1)
# indicate on legend what the red line is
plt.legend(['Mean: {:.2f} seconds'.format(df['average_seconds'].mean())])
plt.show()
