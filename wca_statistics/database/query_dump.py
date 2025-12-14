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
    --AND r.roundTypeId = 'f'
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

columns, records = run_wca_query(query)

if columns and records:
    print(f"Columnas: {columns}")
    print("-" * 30)
    for record in records:
        # El tiempo 'best' de WCA está en centésimas de segundo, lo convertimos a segundos.
        time_sec = record[1] / 100.0 if record[1] is not None else "N/A"
        print(f"Nombre: {record[0]}, Mejor Tiempo (3x3 Final): {time_sec} s")