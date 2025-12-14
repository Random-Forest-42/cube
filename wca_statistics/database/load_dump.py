import sqlite3
import pandas as pd
import glob
import os

# --- Configuration ---
# The name of the SQLite database file you want to create (or connect to)
DB_FILE = "wca_data.db"
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
# The folder where you unzipped the TSV files
TSV_FOLDER = "path/to/your/WCA_TSV_FILES"
TSV_FOLDER = "D:\\Descargas\\WCA_export346_20251212T000027Z.tsv"

# e.g., "C:/Users/YourName/Downloads/WCA_export_20250101"

# --- Import Process ---
print(f"Connecting to database: {DB_FILE}")
conn = sqlite3.connect(DB_FILE)

# Find all TSV files in the folder
tsv_files = glob.glob(os.path.join(TSV_FOLDER, '*.tsv'))
print(f"Found {len(tsv_files)} TSV files to import.")

for tsv_path in tsv_files:
    # 1. Determine the table name from the filename (e.g., 'Persons.tsv' -> 'Persons')
    table_name = os.path.splitext(os.path.basename(tsv_path))[0]
    table_name = table_name.replace("WCA_export_", "")

    print(f"--- Importing {table_name} ---")

    # 2. Read the TSV file into a Pandas DataFrame
    # Note: WCA files are often tab-separated, have no header, and use specific encoding.
    # The first row of the file IS the column header.
    try:
        df = pd.read_csv(tsv_path, sep='\t', encoding='utf-8')
    except Exception as e:
        print(f"Error reading {table_name}: {e}. Skipping.")
        continue

    # 3. Write the DataFrame directly to the SQLite database
    # if_exists='replace' will create the table if it doesn't exist, or overwrite it if it does.
    # index=False ensures Pandas doesn't create an unnecessary index column.
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Successfully loaded {len(df)} rows into table: {table_name}")

# Close the connection
conn.close()
print("\nDatabase import complete!")