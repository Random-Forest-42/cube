import sqlite3

DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

table_name_1 = 'results_extended'

query_todojunto = f'''
create table todojunto as

select

    t1.*

    , t2.person_competition_number

    , t3.first_competition_date

    , julianday(t1.competition_date) - julianday(t3.first_competition_date) AS days_since_first_competition

from

    {table_name_1} as t1

left join

(

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

) t2

on

    t1.personId = t2.personId

    and t1.competitionId = t2.competitionId



left join

(

    select

        personId,

        MIN(competition_date) AS first_competition_date

    from

        {table_name_1}

    group by

        personId

) t3

on

    t1.personId = t3.personId
'''
cursor.execute(query_todojunto)

conn.commit()
