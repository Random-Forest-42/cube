import sqlite3
import pandas as pd

DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

query = '''
select
*
from
events
'''
cursor.execute(query)
df = pd.read_sql_query(query, conn)
print(df.iloc[0]['id'])
print(df['id'])



query = '''
select
    personId
    , best
from
    RanksAverage
where
    eventId = '333oh'
    and best > 0
'''
cursor.execute(query)
df = pd.read_sql_query(query, conn)
print(df.iloc[0]['personId'])
print(df.iloc[0]['best'])


