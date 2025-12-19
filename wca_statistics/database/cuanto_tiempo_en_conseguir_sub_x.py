import sqlite3

# Connect to your SQLite database
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

query = """

select
from


"""

cursor.execute(query)
comp_counts = cursor.fetchall()

# Print the results
print("### 🏆 Competitors who achieved a sub-10s 3x3x3 average")
print(f"Total people tracked: {len(comp_counts)}")
print("-" * 50)
print(f"{'WCA ID': <12} | {'Comps to Sub-15s Result': <25}")
print("-" * 50)

# Print a few examples
for person_id, count in comp_counts[:15]:
    print(f"{person_id: <12} | {count: <25}")

conn.close()