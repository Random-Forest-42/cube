import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

event_1 = '333'
event_2 = '444'

query = f'''
select
    best_ev1
    , best_ev2
from
    (
        select
            personId
            , best as best_ev1
        from
            RanksAverage
        where
            eventId = '{event_1}'
            and best > 0
    ) ev_1
    inner join
    (
        select
            personId
            , best as best_ev2
        from
            RanksAverage
        where
            eventId = '{event_2}'
            and best > 0
    ) ev_2
    on ev_1.personId = ev_2.personId

'''

cursor.execute(query)
df = pd.read_sql_query(query, conn)
print(len(df))
# scatterplot of best_ev1 vs best_ev2

def scatter_with_regression(x, y):
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y)
    ## add regression line
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, color='red')
    plt.xlabel('Best Event 1')
    plt.ylabel('Best Event 2')
    plt.title('Comparison of Best Times')
    plt.show()

scatter_with_regression(df['best_ev1'], df['best_ev2'])

# filter some times
min_time_ev_1 = 2000
min_time_ev_2 = 5000

filtered_df = df[(df['best_ev1'] < min_time_ev_1) & (df['best_ev2'] < min_time_ev_2)]

# create filter based on %, not fixed values
percentile_ev1 = 90
percentile_ev2 = 90

min_time_ev_1 = df['best_ev1'].quantile(percentile_ev1 / 100)
min_time_ev_2 = df['best_ev2'].quantile(percentile_ev2 / 100)

filtered_df = df[(df['best_ev1'] < min_time_ev_1) & (df['best_ev2'] < min_time_ev_2)]

print(f"Filtered down to {len(filtered_df)} cubers")
scatter_with_regression(filtered_df['best_ev1'], filtered_df['best_ev2'])


import matplotlib.pyplot as plt
import pandas as pd

# Ejemplo con matplotlib
plt.hexbin(filtered_df['best_ev1'], filtered_df['best_ev2'], gridsize=50, cmap='inferno')
plt.colorbar(label='Number of cubers')
plt.show()
plt.hexbin(df['best_ev1'], df['best_ev2'], gridsize=50, cmap='magma')
plt.colorbar(label='Number of cubers')
plt.show()

import seaborn as sns
sns.histplot(df, x="best_ev1", y="best_ev2", bins=50, pthresh=.1, cmap="mako")
sns.histplot(filtered_df, x="best_ev1", y="best_ev2", bins=50, pthresh=.1, cmap="mako")

sns.kdeplot(data=df, x="best_ev1", y="best_ev2", fill=True, thresh=0, levels=30, cmap="viridis")
sns.kdeplot(data=filtered_df, x="best_ev1", y="best_ev2", fill=True, thresh=0, levels=30, cmap="viridis")