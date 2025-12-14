import sqlite3
# import pandas as pd

# Connect to your SQLite database
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

table_name_1 = 'results_extended'

delete_query = f'drop table if exists {table_name_1}'
cursor.execute(delete_query)

query = f'''
create table {table_name_1} as
select
    r.eventId
    , r.best
    , r.average
    , r.personId
    , r.competitionId
    , r.pos
    , printf('%04d-%02d-%02d', comp.year, comp.month, comp.day) as competition_date
    , p.name AS person_name
    , p.countryId AS person_countryId
from
    Results r
left join
    Competitions AS comp
on
    r.competitionId = comp.id
left join
    (select * from Persons where subid = 1) AS p
on
    r.personId = p.id
'''

cursor.execute(query)

query = f'drop INDEX if exists idx_person_comp;'
cursor.execute(query)
query = f'CREATE INDEX idx_person_comp ON {table_name_1} (personId, competitionId);'
cursor.execute(query)
query = f'drop INDEX if exists idx_person;'
cursor.execute(query)
query = f'CREATE INDEX idx_person ON {table_name_1} (personId);'
cursor.execute(query)
query = f'drop INDEX if exists idx_country;'
cursor.execute(query)
query = f'CREATE INDEX idx_country ON {table_name_1} (person_countryId);'
cursor.execute(query)

delete_query = f'drop table if exists t_person_competition_number'
cursor.execute(delete_query)
query = f'''
create table t_person_competition_number as
    select
        personId
        , competitionId
        , ROW_NUMBER() OVER (
            PARTITION BY personId
            ORDER BY competition_date ASC
        ) as person_competition_number
        , competition_date
    from
    (
        select
            personId
            , competitionId
            , min(competition_date) as competition_date
        from
            {table_name_1}
        group by
            personId
            , competitionId
    ) a
'''
cursor.execute(query)
query = f'drop INDEX if exists idx_person_comp_2;'
cursor.execute(query)
query = f'CREATE INDEX idx_person_comp_2 ON t_person_competition_number (personId, competitionId);'
cursor.execute(query)

delete_query = f'drop table if exists t_person_first_competition'
cursor.execute(delete_query)
query = f'''
create table t_person_first_competition as
    select
        personId,
        MIN(competition_date) AS first_competition_date
    from
        {table_name_1}
    group by
        personId
'''
cursor.execute(query)
query = f'drop index if exists idx_person_2;'
cursor.execute(query)
query = f'CREATE unique INDEX idx_person_2 ON t_person_first_competition (personId);'
cursor.execute(query)

table_name_2 = f'{table_name_1}_with_rank'
delete_query = f'drop table if exists {table_name_2}'
cursor.execute(delete_query)
query = f'''
create table {table_name_2} as
select
    t1.*
    , t2.person_competition_number
    , t3.first_competition_date
    , julianday(t1.competition_date) - julianday(t3.first_competition_date) AS days_since_first_competition
from
    {table_name_1} as t1
left join
    t_person_competition_number t2
on
    t1.personId = t2.personId
    and t1.competitionId = t2.competitionId
left join
    t_person_first_competition t3
on
    t1.personId = t3.personId

'''
cursor.execute(query)

c_query = f'select count(1) from {table_name_1}'
cursor.execute(c_query)
results = cursor.fetchall()
print(results)
c_query = f'select count(1) from {table_name_2}'
cursor.execute(c_query)
results = cursor.fetchall()
print(results)


query = f'drop INDEX if exists idx_person_comp_t2;'
cursor.execute(query)
query = f'CREATE INDEX idx_person_comp_t2 ON {table_name_2} (personId, competitionId);'
cursor.execute(query)
query = f'drop INDEX if exists idx_person_t2;'
cursor.execute(query)
query = f'CREATE INDEX idx_person_t2 ON {table_name_2} (personId);'
cursor.execute(query)
query = f'drop INDEX if exists idx_country_t2;'
cursor.execute(query)
query = f'CREATE INDEX idx_country_t2 ON {table_name_2} (person_countryId);'
cursor.execute(query)

conn.commit()

