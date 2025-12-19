import sqlite3
import pandas as pd

# Connect to your SQLite database
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

eventId = '333'
min_case_when_sql = ''
min_seconds = 6
max_seconds = 20
for i in range(min_seconds, max_seconds):
    min_case_when_sql += f",\n    min(case when best >= {i} * 100 then worldRank else null end) as rank_{i}"

query = f"""
select
    count(1) as total_cubers
    {min_case_when_sql}
from
    RanksAverage
where
    eventId = '{eventId}'
"""

cursor.execute(query)
df = pd.read_sql_query(query, conn)
total_cubers = df.iloc[0]['total_cubers']
df.iloc[0]['rank_8']

percents = {}
for i in range(min_seconds, max_seconds):
    rank = df.iloc[0][f'rank_{i}']
    percents[i] = (rank / total_cubers) * 100
    print(f"Minimum rank to be sub {i}: {rank} ({percents[i]:.2f}%)")

# plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(list(percents.keys()), list(percents.values()), marker='o')
plt.title(f'Percentage of Cubers by Best Average in {eventId}')
plt.xlabel('Sub X')
plt.ylabel('Percentage (%)')
# Show only every 2 seconds on X axis, but keep all points plotted
# step = 2
# plt.xticks(list(range(min_seconds, max_seconds, step)))
plt.grid()
plt.show()
