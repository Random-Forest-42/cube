import sqlite3

# 1. Definir la ruta a tu archivo .db
DB_FILE = "wca_data.db"
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"

def run_wca_query(sql_query):
    """Ejecuta una consulta SQL y devuelve los resultados."""
    conn = None
    try:
        # 2. Conexión a la base de datos
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 3. Ejecutar la consulta
        cursor.execute(sql_query)

        # 4. Obtener todos los resultados (o usar fetchone/fetchmany)
        results = cursor.fetchall()

        # Opcional: Obtener los nombres de las columnas
        column_names = [description[0] for description in cursor.description]

        return column_names, results

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return None, None

    finally:
        # 5. Cerrar la conexión
        if conn:
            conn.close()

# --- Ejemplo de Uso ---
query = """
SELECT
    p.name,
    r.best
FROM
    Results r
JOIN
    Persons p ON r.personId = p.id
WHERE
    r.eventId = '333'
    AND r.roundTypeId = 'f'
    and r.average > 0
ORDER BY
    r.best
LIMIT 10;
"""
query = """
SELECT
    *
from
    Persons
WHERE
    id = '2024ALFA08'
"""

query = '''
SELECT
    T1.personId,
    T1.average  -- El tiempo de la media en centésimas de segundo
FROM
    Results AS T1
JOIN
    Rounds AS T2 ON T1.competitionId = T2.competitionId
                AND T1.eventId = T2.eventId
                AND T1.roundTypeId = T2.id
WHERE
    T1.eventId = '333'
    AND T2.roundNumber = 1  -- Filtramos por la primera ronda (Round Number 1)
    AND T1.average > 0      -- Filtramos los DNF (-1) y DNS (0)
ORDER BY
    T1.average;
'''

query = '''
SELECT
    T1.personId,
    T1.competitionId,
    T3.startDate AS competitionDate,
    T1.eventId,
    T1.roundTypeId,
    T1.best,
    T1.average
FROM
    Results AS T1
JOIN
    Competitions AS T3 ON T1.competitionId = T3.id
WHERE
    T1.average > 0
    AND t1.roundTypeId IN ('1', 'r1', '0') -- Filtra los códigos de ronda más probables para la "primera ronda"
    AND T3.startDate = (
        SELECT MIN(T2.startDate)
        FROM Results AS T4
        JOIN Competitions AS T2 ON T4.competitionId = T2.id
        WHERE T4.personId = T1.personId
        -- Puedes añadir una condición aquí para asegurar que el MIN(startDate)
        -- corresponde a una ronda que no sea de exhibición, pero es opcional.
    )
ORDER BY
    T1.personId
'''

columns, records = run_wca_query(query)

if columns and records:
    print(f"Columnas: {columns}")
    print("-" * 30)
    for record in records:
        print(record)
        # El tiempo 'best' de WCA está en centésimas de segundo, lo convertimos a segundos.
        time_sec = record[1] / 100.0 if record[1] is not None else "N/A"
        print(f"Nombre: {record[0]}, Mejor Tiempo (3x3 Final): {time_sec} s")