import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import os, sys

# --- CONFIG ---
CSV_PATH = '4x4.csv'  # Change to your file path
CSV_PATH = '4x4.csv'  # Change to your file path
file_name = '4x4.csv'
CSV_PATH = os.path.join('D:\\', 'Documentos', 'Coding', 'Python', 'cube', 'cstimer', 'input', file_name)
# df_2 = read_csv_files_from_directory('D:\\Documentos\\Coding\\Python\\cube\\csv\\acum')
# --- LOAD DATA ---
# Read CSV with ; separator, skip first row if it's a comment
df = pd.read_csv(CSV_PATH, sep=';', comment='/', engine='python')

# --- CLEAN DATA ---
# Remove DNFs
df = df[~df['Time'].str.startswith('DNF')].copy()

# last X days
days_limit = 200
cutoff_date = datetime.now() - pd.Timedelta(days=days_limit)
df = df[pd.to_datetime(df['Date']) >= cutoff_date]

# Function to convert time string to seconds
def time_to_seconds(t):
    # Handles formats like '1:23.45'
    try:
        if len(t.split(':')) == 1:
            return float(t)
        else:
            m, s = t.split(':')
            return int(m) * 60 + float(s)
    except Exception:
        return np.nan

df['Seconds'] = df['Time'].apply(time_to_seconds)
df['Date'] = pd.to_datetime(df['Date'])

# Remove rows with invalid times
df = df.dropna(subset=['Seconds'])

# Sort by date
df = df.sort_values('Date').reset_index(drop=True)

# --- STATISTICS ---
total_solves = len(df)
best_time = df['Seconds'].min()
best_time_str = df.loc[df['Seconds'].idxmin(), 'Time']
mean_time = df['Seconds'].mean()
median_time = df['Seconds'].median()
first_date = df['Date'].min()
last_date = df['Date'].max()
days_span = (last_date - first_date).days + 1

# Progress rate: improvement per month
if days_span > 1:
    time_diff = df.iloc[0]['Seconds'] - df.iloc[-1]['Seconds']
    months = days_span / 30.44
    progress_per_month = time_diff / months
else:
    progress_per_month = np.nan

# --- PRINT STATS ---
print(f"Total solves: {total_solves}")
print(f"Best time: {best_time_str} ({best_time:.2f} seconds)")
print(f"Mean time: {mean_time:.2f} seconds ({int(mean_time//60)}:{mean_time%60:.2f})")
print(f"Median time: {median_time:.2f} seconds ({int(median_time//60)}:{median_time%60:.2f})")
print(f"Date range: {first_date.date()} to {last_date.date()} ({days_span} days)")
print(f"Progress rate: {progress_per_month:.2f} seconds/month")

# --- PLOTS ---
sns.set(style="darkgrid")

# 1. Progress over time
plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Seconds'], marker='o', linestyle='-', alpha=0.7)
plt.title('4x4 Progress Over Time')
plt.xlabel('Date')
plt.ylabel('Time (seconds)')
plt.gca().invert_yaxis()  # Lower times are better
plt.tight_layout()
plt.show()

# 2. Histogram of times
plt.figure(figsize=(8,4))
plt.hist(df['Seconds'], bins=30, color='skyblue', edgecolor='k')
plt.title('Distribution of Solve Times')
plt.xlabel('Time (seconds)')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# 3. Rolling average (e.g., 20 solves). X axis are solves, not date
window = 20
df['RollingMean'] = df['Seconds'].rolling(window).mean()
plt.figure(figsize=(12,5))
plt.plot(df.index, df['Seconds'], alpha=0.3, label='Single')
plt.plot(df.index, df['RollingMean'], color='red', label=f'Rolling Mean ({window})')
plt.title('Rolling Average Progress')
plt.xlabel('Solves')
plt.ylabel('Time (seconds)')
plt.gca().invert_yaxis()
plt.legend()
plt.tight_layout()
plt.show()

# 4. Boxplot by month (optional)
df['Month'] = df['Date'].dt.to_period('M')
plt.figure(figsize=(12,5))
sns.boxplot(x='Month', y='Seconds', data=df)
plt.title('Monthly Solve Time Distribution')
plt.xlabel('Month')
plt.ylabel('Time (seconds)')
plt.gca().invert_yaxis()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()