import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
table_name = 'results_extended_with_rank'

image_name_suffix = 'practice_vs_time'

def plot(df:pd.DataFrame, category_name:str):
    ### PLOT
    print(f"Found {len(df)} first averages")
    print("Stats (in seconds):")
    print(df['average_seconds'].describe())

    plt.figure(figsize=(12, 6))

    max_time = df['average_seconds'].mean() * 2

    df[df['average_seconds'] <= max_time]['average_seconds'].hist(bins=100, edgecolor='black', alpha=0.7)

    plt.title(f'Average Times at {category_name} on 3x3x3')
    plt.xlabel('Average Time (Seconds)')
    plt.ylabel('Frecuency (Number of rounds)')
    plt.gca().ticklabel_format(style='plain', axis='y')
    plt.grid(axis='y', alpha=0.5)
    mean_value = df['average_seconds'].mean()
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
    under_10_seconds = len(df[df['average_seconds'] <= 10])
    total_competitors = len(df)
    # obtain mode value as the bin mode, not the values mode
    counts, bin_edges = np.histogram(df['average_seconds'], bins=100)
    max_count_index = np.argmax(counts)
    mode_value = (bin_edges[max_count_index] + bin_edges[max_count_index + 1]) / 2
    # mode_value = df['average_seconds'].mode()[0]
    plt.axvline(mode_value, color='green', linestyle='dashed', linewidth=1)
    plt.legend(
        [
            'Mean: {:.2f} seconds'.format(mean_value),
            'Mode: {:.2f} seconds'.format(mode_value),
            'Under 10 seconds: {} ({:.2f}%)'.format(under_10_seconds, (under_10_seconds / total_competitors) * 100),
        ]
    )
    category_name_clean = category_name.replace(" ", "_").replace("-", "to").replace(",", "").replace(">", "morethan").replace("<", "lessthan").replace(":", "")
    plt.savefig(f'D:\\Documentos\\Coding\\Python\\cube\\wca_statistics\\results\\{image_name_suffix}_{category_name_clean}.png')
    plt.show()

query = f'''
select
    average
    , case
        when days_since_first_competition = 0 then '00: first competition'
        when days_since_first_competition < 180 then '01: up to 6 months'
        when days_since_first_competition < 365 then '02: 6-12 months'
        when days_since_first_competition < 365 * 2 then '03: 1-2 years'
        when days_since_first_competition < 365 * 3 then '04: 2-3 years'
        when days_since_first_competition < 365 * 4 then '05: 3-4 years'
        when days_since_first_competition < 365 * 5 then '06: 4-5 years'
        when days_since_first_competition < 365 * 6 then '07: 5-6 years'
        else '08: more than 6 years'
    end as category
from
    {table_name}
where
    eventId = '333'
    and average > 0
'''
cursor.execute(query)
df = pd.read_sql_query(query, conn)
df['average_seconds'] = df['average'] / 100.0

# Call plot for each distinct category value
categories = df['category'].dropna().unique()
# sort categories in str order
categories = sorted(categories)
for category in categories:
    subset = df[df['category'] == category]
    plot(subset, category)