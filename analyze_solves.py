explicacion = '''
Este script analiza los csvs generados en Cubeast
plot de averages al final, con la tendencia
puedes medir diferentes pasos
'''

import pandas as pd
import os
import numpy as np

def read_csv_file(file_path):
    """
    Reads a CSV file and returns its content as a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# read all files from a directory and return only one dataframe with all data
def read_csv_files_from_directory(directory):
    """
    Reads all CSV files from a directory and concatenates them into a single DataFrame.
    """
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = read_csv_file(file_path)
            if df is not None:
                all_data.append(df)
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()
# df_test = read_csv_file(os.path.join(os.getcwd(), "Rubik", "inputs", "solve_lite.csv"))
# df_test = read_csv_file('D:\\Documentos\\Coding\\Python\\Rubik\\inputs\\solve_lite.csv')
# df = read_csv_file('D:\\Documentos\\Coding\\Python\\Rubik\\inputs\\solves full hasta 2025-07-29.csv')
df_1 = read_csv_file('D:\\Documentos\\Coding\\Python\\Rubik\\inputs\\acum\\solves 2025-08-03.csv')
df_2 = read_csv_files_from_directory('D:\\Documentos\\Coding\\Python\\Rubik\\inputs\\acum')
df = df_2.copy()

# Parámetro de tiempo máximo permitido (en milisegundos)
MAX_TIME = 25000  # 30 segundos
trim_percent = 0.05  # 5% de recorte

# Filtrar el DataFrame original
df_original = df.copy()
df = df[(df["dnf"] == False) & (df["time"] <= MAX_TIME)].copy()
len(df)
# tomar solo una de las sesiones, campo "session_name"
session_name = 'gan12'
if session_name:
    df = df[df["session_name"] == session_name]

len(df)
# take only last X rows
last_rows = 1000
last_rows = None
if last_rows:
    df = df.iloc[-last_rows:]

numbers = [5, 12, 50, 100, 250, 500]

# Convertir la columna de fecha a datetime y ordenar cronológicamente
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date").reset_index(drop=True)

# Excluir DNFs para los promedios, pero conservamos las filas en el df final
def compute_ao(series, count, trim_percent=0.0):
    """
    Calcula un average of N (aoN) recortando un porcentaje si es necesario.
    Excluye mejor y peor para ao5 y ao12 (i.e., trim_percent = 0.4 equivale a quitar 40% en total).
    """
    if len(series) < count:
        return np.nan
    recent = series[-count:]
    if trim_percent > 0:
        k = int(len(recent) * trim_percent)
        recent = sorted(recent)[k:-k or None]  # evita cortar todo
    elif count in (5, 12):
        recent = sorted(recent)[1:-1]  # quitar mejor y peor
    return np.mean(recent) if len(recent) >= 1 else np.nan

def add_average_column(df, column_name, n, trim_percent=0.0, new_col_name=None):
    """
    Añade una columna al DataFrame con el average (tipo WCA) de los últimos n valores
    de `column_name`, aplicando trimming si se indica.

    - Para n=5 o n=12, se descarta automáticamente el mejor y el peor.
    - Para otros valores, se descarta trim_percent superior e inferior (por ejemplo 0.05).

    Params:
        df (pd.DataFrame): el DataFrame.
        column_name (str): nombre de la columna con los tiempos.
        n (int): tamaño del average (aoN).
        trim_percent (float): porcentaje a recortar para medias grandes.
        new_col_name (str or None): nombre de la nueva columna (por defecto: 'ao{n}')
    """
    if new_col_name is None:
        new_col_name = f"{column_name}_ao{n}"

    values = df[column_name].tolist()
    averages = []

    for i in range(len(values)):
        if i + 1 < n:
            averages.append(np.nan)
            continue

        window = values[i+1-n:i+1]

        if n in (5, 12):
            trimmed = sorted(window)[1:-1]  # quitar el mejor y el peor
        elif trim_percent > 0:
            k = int(len(window) * trim_percent)
            trimmed = sorted(window)[k:len(window)-k or None]
        else:
            trimmed = window

        avg = np.mean(trimmed) if trimmed else np.nan
        averages.append(avg)

    df[new_col_name] = averages


def get_ao_columns(df, row_name, trim_percent=0.05, numbers=[5, 12, 50, 100]):
    """
    Devuelve las columnas de promedios de N (aoN) para el DataFrame dado.
    """
    for n in numbers:
        if n == 5 or n == 12:
            trim_percent_param = 0
        else:
            trim_percent_param = trim_percent
        add_average_column(df, row_name, n, trim_percent=trim_percent_param)

def rename_columns(df, old_col, new_col):
    """
    Renombra una columna en el DataFrame.
    """
    if old_col in df.columns:
        df.rename(columns={old_col: new_col}, inplace=True)
    else:
        print(f"Column '{old_col}' not found in DataFrame")

rename_columns(df, 'step_0_execution_time', 'cross')
rename_columns(df, 'step_1_recognition_time', 'f2l_1_pensar')
rename_columns(df, 'step_1_execution_time', 'f2l_1_ex')
rename_columns(df, 'step_2_execution_time', 'f2l_2_ex')
rename_columns(df, 'step_3_execution_time', 'f2l_3_ex')
rename_columns(df, 'step_4_execution_time', 'f2l_4_ex')
rename_columns(df, 'step_2_recognition_time', 'f2l_2_pensar')
rename_columns(df, 'step_3_recognition_time', 'f2l_3_pensar')
rename_columns(df, 'step_4_recognition_time', 'f2l_4_pensar')
rename_columns(df, 'step_5_recognition_time', 'oll_pensar')
rename_columns(df, 'step_5_execution_time', 'oll_ex')
rename_columns(df, 'step_6_recognition_time', 'pll_pensar')
rename_columns(df, 'step_6_execution_time', 'pll_ex')

time_columns = [
    'time',
    'slice_turns',
    'total_execution_time',
    'cross',
    'f2l_1_pensar',
    'f2l_1_ex',
    'f2l_2_ex',
    'f2l_3_ex',
    'f2l_4_ex',
    'f2l_2_pensar',
    'f2l_3_pensar',
    'f2l_4_pensar',
    'oll_pensar',
    'oll_ex',
    'pll_pensar',
    'pll_ex',
]


for time_column in time_columns:
    get_ao_columns(df, time_column, trim_percent=0.05, numbers=numbers)
    # print progress
    print(f"Processed {time_column} for averages of {numbers}")

new_columns = {}
for n in numbers:
    new_columns[f'pensar_ao{n}'] = df[f"time_ao{n}"] - df[f"total_execution_time_ao{n}"]
    new_columns[f'pct_pensar_ao{n}'] = df[f"total_execution_time_ao{n}"] / df[f"time_ao{n}"]
    new_columns[f'total_f2l_1_ao{n}'] = df[f'f2l_1_pensar_ao{n}'] + df[f'f2l_1_ex_ao{n}']
    new_columns[f'total_f2l_2_ao{n}'] = df[f'f2l_2_pensar_ao{n}'] + df[f'f2l_2_ex_ao{n}']
    new_columns[f'total_f2l_3_ao{n}'] = df[f'f2l_3_pensar_ao{n}'] + df[f'f2l_3_ex_ao{n}']
    new_columns[f'total_f2l_4_ao{n}'] = df[f'f2l_4_pensar_ao{n}'] + df[f'f2l_4_ex_ao{n}']
    new_columns[f'total_oll_ao{n}'] = df[f'oll_pensar_ao{n}'] + df[f'oll_ex_ao{n}']
    new_columns[f'total_pll_ao{n}'] = df[f'pll_pensar_ao{n}'] + df[f'pll_ex_ao{n}']

df = pd.concat([df, pd.DataFrame(new_columns)], axis=1)

import matplotlib.pyplot as plt

def plot_ao(df, ao_column, step=0, col2=None):
    """
    Plotea la evolución de un average of N (aoN) en el DataFrame dado.
    """
    if step == 0:
        step = len(df) // 200  # muestreo por defecto
    plt.figure(figsize=(12, 6))
    plt.plot(
        df.index[::step],
        df[ao_column][::step],
        marker='o',
        linestyle='-',
        color='blue',
        label=ao_column
    )
    if col2:
        plt.plot(
            df.index[::step],
            df[col2][::step],
            marker='o',
            linestyle='-',
            color='red',
            label=col2
        )
    plt.title(f"Evolución del {ao_column} (muestreo cada {step})")
    plt.xlabel("Número de resolución")
    plt.ylabel("Tiempo (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_columns(df, columns, step=0):
    """
    Plotea la evolución de varias columnas en el DataFrame dado.
    """
    if step == 0:
        step = len(df) // 200  # muestreo por defecto
    plt.figure(figsize=(12, 6))
    for col in columns:
        plt.plot(
            df.index[::step],
            df[col][::step],
            marker='o',
            linestyle='-',
            label=col
        )
    plt.title(f"Evolución de las columnas (muestreo cada {step})")
    plt.xlabel("Número de resolución")
    plt.ylabel("Tiempo (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


plot_ao(df, 'time_ao250', step=10)
plot_ao(df, 'inspection_time_ao250', step=10, col2='total_execution_time_ao250')
plot_ao(df, 'pct_inspection_ao250')
plot_ao(df, 'f2l_1_pensar_ao250')
plot_ao(df, 'total_oll_ao250')
plot_ao(df, 'total_pll_ao250')

plot_columns(df, [
    "total_f2l_1_ao500",
    "total_f2l_2_ao500",
    "total_f2l_3_ao500",
    "total_f2l_4_ao500",
    "total_oll_ao500",
    "total_pll_ao500",
])

# quiero saber el % de solves sub X segundos, para X de 10 a 20
def percentage_below_threshold(df, column, threshold):
    """
    Calcula el porcentaje de valores en una columna que están por debajo de un umbral dado.
    """
    count_below = df[df[column] < threshold*1000].shape[0]
    total_count = df.shape[0]
    return round((count_below / total_count) * 100, 2) if total_count > 0 else 0

# Calcular el porcentaje de solves por debajo de diferentes thresholds
thresholds = range(10, 21)  # de 10 a 20 segundos
percentages = {}
for threshold in thresholds:
    percentages[threshold] = percentage_below_threshold(df, 'time', threshold)
# Imprimir los resultados
print("Porcentaje de solves por debajo de diferentes thresholds:")
for threshold, percentage in percentages.items():
    print(f"{threshold} segundos: {percentage:.2f}%")

# repetir la operacion dividiendo df de 1000 en 1000
def percentage_below_threshold_divided(df, column, threshold, chunk_size=1000):
    """
    Calcula el porcentaje de valores en una columna que están por debajo de un umbral dado,
    dividiendo el DataFrame en chunks de tamaño `chunk_size`.
    """
    percentages = []
    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start + chunk_size]
        count_below = chunk[chunk[column] < threshold * 1000].shape[0]
        total_count = chunk.shape[0]
        percentages.append(round((count_below / total_count) * 100, 2) if total_count > 0 else 0)
    return percentages
# Calcular el porcentaje de solves por debajo de diferentes thresholds en chunks de 1000
chunk_percentages = {}
for threshold in thresholds:
    chunk_percentages[threshold] = percentage_below_threshold_divided(df, 'time', threshold)
# Imprimir los resultados por chunks
print("Porcentaje de solves por debajo de diferentes thresholds (dividido en chunks):")
for threshold, percentage_list in chunk_percentages.items():
    print(f"{threshold} segundos: {percentage_list}")

# plot chunk_percentages de manera visual
def plot_chunk_percentages(chunk_percentages, title="Porcentaje de solves por debajo de thresholds (chunks)"):
    """
    Plotea el porcentaje de solves por debajo de diferentes thresholds en chunks.
    """
    plt.figure(figsize=(10, 6))
    for threshold, percentages in chunk_percentages.items():
        plt.plot(percentages, marker='o', label=f"{threshold} segundos")
    plt.title(title)
    plt.xlabel("Chunk index")
    plt.ylabel("Porcentaje (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_chunk_percentages(chunk_percentages)


# calcular una lista con el tiempo mejor cada 10 resolves
def best_time_per_n_resolves(df, n=10):
    """
    Calcula el mejor tiempo cada n resolves.
    """
    best_times = []
    for i in range(0, len(df), n):
        chunk = df.iloc[i:i + n]
        if not chunk.empty:
            best_time = chunk['time'].min()
            best_times.append(best_time)
        else:
            best_times.append(np.nan)
    return best_times

# Calcular los mejores tiempos cada 10 resolves
best_times = best_time_per_n_resolves(df, n=5)
# plot
def plot_best_times(best_times, title="Mejor tiempo cada 10 resolves"):
    """
    Plotea los mejores tiempos cada n resolves.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(best_times, marker='o', linestyle='-', color='green', label='Mejor tiempo')
    plt.title(title)
    plt.xlabel("Chunk de 10 resolves")
    plt.ylabel("Tiempo (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    # añadir linea de regresion
    z = np.polyfit(range(len(best_times)), best_times, 1)
    p = np.poly1d(z)

    plt.show()

# plot_best_times(best_times)
# añadir linea de regresion al anterior plot

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Lista de números
datos = best_times

# Eje x como índices de los datos
x = np.arange(len(datos)).reshape(-1, 1)
y = np.array(datos)

# Modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(x, y)

# Predicción de la recta
y_pred = modelo.predict(x)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, label='Datos', marker='o')
plt.plot(x, y_pred, label='Regresión lineal', color='red', linestyle='--')
plt.xlabel('Índice')
plt.ylabel('Valor')
plt.title('Gráfico de líneas con regresión lineal')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



# Calcular los mejores tiempos cada 10 resolves
best_times = best_time_per_n_resolves(df, n=40)
datos = best_times

# Eje x como índices de los datos
x = np.arange(len(datos)).reshape(-1, 1)
y = np.array(datos)

# Modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(x, y)

# Predicción de la recta
y_pred = modelo.predict(x)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, label='Datos', marker='o')
plt.plot(x, y_pred, label='Regresión lineal', color='red', linestyle='--')
plt.xlabel('Índice')
plt.ylabel('Valor')
plt.title('Gráfico de líneas con regresión lineal')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#### Ratios optimos
cross_ratio = 0.12
cross_1_ratio = 0.245
f2l_and_cross_ratio = 0.62
f2l_ratio = f2l_and_cross_ratio - cross_ratio
oll_ratio = 0.165
pll_ratio = 0.215

# last value of total_execution_time_ao500
last_times = {
    "total": df['time_ao500'].iloc[-1],
    "cross": df['cross_ao500'].iloc[-1],
    "cross_1": df['cross_ao500'].iloc[-1] + df['total_f2l_1_ao500'].iloc[-1],
    "f2l": df['total_f2l_1_ao500'].iloc[-1] + df['total_f2l_2_ao500'].iloc[-1] + df['total_f2l_3_ao500'].iloc[-1] + df['total_f2l_4_ao500'].iloc[-1],
    "oll": df['total_oll_ao500'].iloc[-1],
    "pll": df['total_pll_ao500'].iloc[-1],
}

# print time de cada paso por el inverso de su ratio optimo
for key, value in last_times.items():
    if key == 'total':
        continue  # no necesitamos el total para los ratios
    optimal_ratio = locals()[f"{key}_ratio"]
    print(f"{key}: {value / optimal_ratio:.3f} segundos (Óptimo: {optimal_ratio:.3f})")

# Calcular los ratios
ratios = {key: value / last_times['total'] for key, value in last_times.items()}
del ratios['total']  # eliminar el ratio total, ya que no es necesario
# comparar con los ratios optimos
print("Ratios actuales:")
for key, value in ratios.items():
    print(f"{key}: {value:.3f} (Óptimo: {locals()[f'{key}_ratio']:.3f})")
# Comparar con los ratios óptimos
print("\nComparación con los ratios óptimos:")
for key, value in ratios.items():
    optimal_value = locals()[f"{key}_ratio"]
    if value < optimal_value:
        print(f"{key}: {value:.3f} (Mejor que óptimo: {optimal_value:.3f})")
    elif value > optimal_value:
        print(f"{key}: {value:.3f} (Peor que óptimo: {optimal_value:.3f})")
    else:
        print(f"{key}: {value:.3f} (Igual que óptimo: {optimal_value:.3f})")

