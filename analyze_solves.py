explicacion = '''
Este script analiza los csvs generados en Cubeast
plot de averages al final, con la tendencia
puedes medir diferentes pasos
'''
import pandas as pd
import os
import numpy as np

import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns

### FLAGS para hacer algunos pasos o no

flag_histograms = True
flag_scatterplots = True

def read_csv_files_from_directory(directory):
    """
    Reads all CSV files from a directory and concatenates them into a single DataFrame.
    """
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            if df is not None:
                all_data.append(df)
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

df_2 = read_csv_files_from_directory('D:\\Documentos\\Coding\\Python\\cube\\csv\\acum')
df = df_2.copy()

# Parámetro de tiempo máximo permitido (en milisegundos)
MAX_TIME = 20000
MAX_TIME = 30000
trim_percent = 0.05  # 5% de recorte

# Filtrar el DataFrame original
df_original = df.copy()
df = df[(df["dnf"] == False) & (df["time"] <= MAX_TIME)].copy()
print(f"Filtered out {len(df_original) - len(df)} rows due to DNF or time > {MAX_TIME} ms.")
# tomar solo una de las sesiones, campo "session_name"
session_name = 'slow solves'
session_name = None
session_name = 'gan12'
if session_name:
    df = df[df["session_name"] == session_name]

# take only solutions with step_0_slice_turns > 0. this is to avoid weird solution. TODO: mejorar para no perder x-cross
df = df[df["step_0_slice_turns"] > 0]

# calculate a column with number of steps skipped, ex step_0_slice_turns = 0, step_1_slice_turns = 0
df['steps_skipped'] = 0
for i in range(7):
    df['steps_skipped'] += (df[f'step_{i}_slice_turns'] == 0).astype(int)

# take out solutions with 2 or more steps skipped, to avoid weird solutions
# print the number of rows before and after
print(f"Rows before filtering steps skipped: {len(df)}")
df = df[df['steps_skipped'] < 2]
print(f"Rows after filtering steps skipped: {len(df)}")

# take only last X rows
last_rows = None
last_rows = 5000
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

# for col in  df.columns:
#     print(col)
rename_columns(df, 'step_0_execution_time', 'cross')
rename_columns(df, 'step_1_recognition_time', 'f2l_1_think')
rename_columns(df, 'step_1_execution_time', 'f2l_1_ex')
rename_columns(df, 'step_2_execution_time', 'f2l_2_ex')
rename_columns(df, 'step_3_execution_time', 'f2l_3_ex')
rename_columns(df, 'step_4_execution_time', 'f2l_4_ex')
rename_columns(df, 'step_2_recognition_time', 'f2l_2_think')
rename_columns(df, 'step_3_recognition_time', 'f2l_3_think')
rename_columns(df, 'step_4_recognition_time', 'f2l_4_think')
rename_columns(df, 'step_5_recognition_time', 'oll_think')
rename_columns(df, 'step_5_execution_time', 'oll_ex')
rename_columns(df, 'step_6_recognition_time', 'pll_think')
rename_columns(df, 'step_6_execution_time', 'pll_ex')

rename_columns(df, 'step_0_slice_turns', 'cross_move_count')
rename_columns(df, 'step_1_slice_turns', 'f2l_1_move_count')
rename_columns(df, 'step_2_slice_turns', 'f2l_2_move_count')
rename_columns(df, 'step_3_slice_turns', 'f2l_3_move_count')
rename_columns(df, 'step_4_slice_turns', 'f2l_4_move_count')
rename_columns(df, 'step_5_slice_turns', 'oll_move_count')
rename_columns(df, 'step_6_slice_turns', 'pll_move_count')

columns_to_calculate_ao = [
    'time',
    'slice_turns',
    'total_execution_time',
    'cross',
    'f2l_1_think',
    'f2l_1_ex',
    'f2l_2_ex',
    'f2l_3_ex',
    'f2l_4_ex',
    'f2l_2_think',
    'f2l_3_think',
    'f2l_4_think',
    'oll_think',
    'oll_ex',
    'pll_think',
    'pll_ex',
    'cross_move_count',
    'f2l_1_move_count',
    'f2l_2_move_count',
    'f2l_3_move_count',
    'f2l_4_move_count',
    'oll_move_count',
    'pll_move_count',
]

# warning: performance issue if we do it one by one
# for col in columns_to_calculate_ao:
#     get_ao_columns(df, col, trim_percent=0.05, numbers=numbers)
#     # print progress
#     print(f"Processed {col} for averages of {numbers}")

ao_columns_dict = {}
for col in columns_to_calculate_ao:
    for n in numbers:
        # Calcula la columna average
        averages = []
        values = df[col].tolist()
        trim_percent_param = 0 if n in (5, 12) else 0.05
        for i in range(len(values)):
            if i + 1 < n:
                averages.append(np.nan)
                continue
            window = values[i+1-n:i+1]
            if n in (5, 12):
                trimmed = sorted(window)[1:-1]
            elif trim_percent_param > 0:
                k = int(len(window) * trim_percent_param)
                trimmed = sorted(window)[k:len(window)-k or None]
            else:
                trimmed = window
            avg = np.mean(trimmed) if trimmed else np.nan
            averages.append(avg)
        ao_columns_dict[f"{col}_ao{n}"] = averages

# 2. Haz un solo concat al final
df = pd.concat([df, pd.DataFrame(ao_columns_dict)], axis=1)

new_columns = {}
for n in numbers:
    new_columns[f'think_ao{n}'] = df[f"time_ao{n}"] - df[f"total_execution_time_ao{n}"]
    new_columns[f'pct_think_ao{n}'] = 1 - (df[f"total_execution_time_ao{n}"] / df[f"time_ao{n}"])
    new_columns[f'total_f2l_1_ao{n}'] = df[f'f2l_1_think_ao{n}'] + df[f'f2l_1_ex_ao{n}']
    new_columns[f'total_f2l_2_ao{n}'] = df[f'f2l_2_think_ao{n}'] + df[f'f2l_2_ex_ao{n}']
    new_columns[f'total_f2l_3_ao{n}'] = df[f'f2l_3_think_ao{n}'] + df[f'f2l_3_ex_ao{n}']
    new_columns[f'total_f2l_4_ao{n}'] = df[f'f2l_4_think_ao{n}'] + df[f'f2l_4_ex_ao{n}']
    new_columns[f'total_oll_ao{n}'] = df[f'oll_think_ao{n}'] + df[f'oll_ex_ao{n}']
    new_columns[f'total_pll_ao{n}'] = df[f'pll_think_ao{n}'] + df[f'pll_ex_ao{n}']
    new_columns[f'total_f2l_1'] = df[f'f2l_1_think'] + df[f'f2l_1_ex']
    new_columns[f'total_f2l_2'] = df[f'f2l_2_think'] + df[f'f2l_2_ex']
    new_columns[f'total_f2l_3'] = df[f'f2l_3_think'] + df[f'f2l_3_ex']
    new_columns[f'total_f2l_4'] = df[f'f2l_4_think'] + df[f'f2l_4_ex']
    new_columns[f'total_oll'] = df[f'oll_think'] + df[f'oll_ex']
    new_columns[f'total_pll'] = df[f'pll_think'] + df[f'pll_ex']
    new_columns[f'total_think'] = df[f'time'] - df[f'total_execution_time']
    new_columns[f'cross_1'] = df[f'cross'] + df[f'f2l_1_think'] + df[f'f2l_1_ex']

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
plot_ao(df, 'think_ao250', step=10, col2='total_execution_time_ao250')
plot_ao(df, 'pct_think_ao250')
plot_ao(df, 'f2l_1_think_ao250')
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
last_layer_plus_last_slot_ratio = oll_ratio + pll_ratio + (f2l_ratio / 4)

# last value of total_execution_time_ao500
last_times = {
    "total": df['time_ao500'].iloc[-1],
    "cross": df['cross_ao500'].iloc[-1],
    "cross_1": df['cross_ao500'].iloc[-1] + df['total_f2l_1_ao500'].iloc[-1],
    "f2l": df['total_f2l_1_ao500'].iloc[-1] + df['total_f2l_2_ao500'].iloc[-1] + df['total_f2l_3_ao500'].iloc[-1] + df['total_f2l_4_ao500'].iloc[-1],
    "oll": df['total_oll_ao500'].iloc[-1],
    "pll": df['total_pll_ao500'].iloc[-1],
    "last_layer_plus_last_slot": df['total_oll_ao500'].iloc[-1] + df['total_pll_ao500'].iloc[-1] + df['total_f2l_4_ao500'].iloc[-1],
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

# Comparar con los ratios óptimos
print("\nComparación con los ratios óptimos:")
for key, value in ratios.items():
    # optimal_value = locals()[f"{key}_ratio"]
    optimal_value = locals().get(f"{key}_ratio")
    if optimal_value:
        if value < optimal_value:
            print(f"{key}: {value:.3f} (Mejor que óptimo: {optimal_value:.3f})")
        elif value > optimal_value:
            print(f"{key}: {value:.3f} (Peor que óptimo: {optimal_value:.3f})")
        else:
            print(f"{key}: {value:.3f} (Igual que óptimo: {optimal_value:.3f})")

#### intentamos bajar el tiempo de think en f2l
# plot f2l_think_ao500
plot_columns(df, [
    # "f2l_1_think_ao500",
    "f2l_2_think_ao500",
    "f2l_3_think_ao500",
    "f2l_4_think_ao500",
    "oll_think_ao500",
    "pll_think_ao500",
], step=10)

# plot in 2 different axes, one list of columns and another
axis_1_columns = [
    "f2l_2_think_ao500",
    "f2l_3_think_ao500",
    "f2l_4_think_ao500",
    "oll_think_ao500",
    "pll_think_ao500",
]

axis_2_columns = [
    "time_ao500",
]
def plot_columns_dual_axis(df, axis_1_columns, axis_2_columns, step=0):
    """
    Plotea la evolución de varias columnas en el DataFrame dado en dos ejes Y diferentes.
    """
    if step == 0:
        step = len(df) // 200  # muestreo por defecto

    fig, ax1 = plt.subplots(figsize=(12, 6))

    for col in axis_1_columns:
        ax1.plot(
            df.index[::step],
            df[col][::step],
            marker='o',
            linestyle='-',
            label=col
        )
    ax1.set_xlabel("Número de resolución")
    ax1.set_ylabel("Tiempo (ms) - Eje 1")
    ax1.grid(True)

    ax2 = ax1.twinx()  # crear un segundo eje Y

    for col in axis_2_columns:
        ax2.plot(
            df.index[::step],
            df[col][::step],
            marker='o',
            linestyle='--',
            color='red',
            label=col
        )
    ax2.set_ylabel("Tiempo (ms) - Eje 2")

    # Combinar leyendas de ambos ejes
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

    plt.title(f"Evolución de las columnas (muestreo cada {step})")
    plt.tight_layout()
    plt.show()

plot_columns_dual_axis(df, axis_1_columns, axis_2_columns, step=10)


# step_0_slice_turns,step_0_face_turns,step_0_quarter_turns

move_count_columns = [
    'cross_move_count_ao500',
    'f2l_1_move_count_ao500',
    'f2l_2_move_count_ao500',
    'f2l_3_move_count_ao500',
    'f2l_4_move_count_ao500',
    # 'oll_move_count_ao500',
    # 'pll_move_count_ao500',
]

plot_columns_dual_axis(df, move_count_columns, axis_2_columns, step=10)

############################################################
############################################################
############################################################
######################### HISTOGRAMAS ###################################
############################################################
############################################################
############################################################

# cortar valores extremos para histogramas, en base a si en el nombre de la columna hay "move_count"
max_move_count = 25

df_clipped = df.copy()
for col in df_clipped.columns:
    if 'move_count' in col:
        df_clipped = df_clipped[df_clipped[col] <= max_move_count]

# histograma de algunas columnas
histogram_columns = [
    'time',
    'slice_turns',
    'total_execution_time',
    'total_think',
    'cross',
    'f2l_1_think',
    'f2l_1_ex',
    'f2l_2_ex',
    'f2l_3_ex',
    'f2l_4_ex',
    'f2l_2_think',
    'f2l_3_think',
    'f2l_4_think',
    'oll_think',
    'oll_ex',
    'pll_think',
    'pll_ex',
    "total_f2l_1",
    "total_f2l_2",
    "total_f2l_3",
    "total_f2l_4",
    "total_oll",
    "total_pll",
    'cross_1'
]

# añadir todos los graficos en un solo plot con subplots
fig, axs = plt.subplots(len(histogram_columns), figsize=(10, 5 * len(histogram_columns)))
for i, col in enumerate(histogram_columns):
    axs[i].hist(df_clipped[col], bins=50, edgecolor='black', alpha=0.7)
    axs[i].set_title(f'Histograma de {col}')
    # añadir linea puntos con mediana y media
    mean_value = df_clipped[col].mean()
    median_value = df_clipped[col].median()
    axs[i].axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Media: {mean_value:.2f}')
    axs[i].axvline(median_value, color='blue', linestyle='dashed', linewidth=1, label=f'Mediana: {median_value:.2f}')
    axs[i].set_xlabel('Valor')
    axs[i].set_ylabel('Frecuencia')
    axs[i].grid(axis='y', alpha=0.5)
    axs[i].legend()

move_count_hist_columns = [
    'cross_move_count',
    'f2l_1_move_count',
    'f2l_2_move_count',
    'f2l_3_move_count',
    'f2l_4_move_count',
    'oll_move_count',
    'pll_move_count',
    'slice_turns'
]

think_columns = [
    'f2l_1_think',
    'f2l_2_think',
    'f2l_3_think',
    'f2l_4_think',
    'oll_think',
    'pll_think',
    'total_think',
]

total_columns = [
    "total_f2l_1",
    "total_f2l_2",
    "total_f2l_3",
    "total_f2l_4",
    "total_oll",
    "total_pll",
    'cross_1',
    'time',
    'turns_per_second',
    'total_execution_time',
    'total_think',
]

def hist_grid(df, columns, title=None):
    cols_per_row = 4
    n = len(columns)
    rows = math.ceil(n / cols_per_row)
    fig, axes = plt.subplots(rows, cols_per_row, figsize=(cols_per_row * 4, rows * 3))
    axes = axes.flatten()
    for i, col in enumerate(columns):
        sns.histplot(df[col], bins=50, ax=axes[i], kde=True)
        axes[i].set_title(f'Histograma de {col}')
        axes[i].set_xlabel('Valor')
        axes[i].set_ylabel('Frecuencia')
        axes[i].grid(axis='y', alpha=0.5)
        # añadir linea puntos con mediana y media
        mean_value = df[col].mean()
        median_value = df[col].median()
        axes[i].axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Media: {mean_value:.2f}')
        axes[i].axvline(median_value, color='blue', linestyle='dashed', linewidth=1, label=f'Mediana: {median_value:.2f}')
        axes[i].legend()
    if title:
        plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.show()

# funcion que dado dos dataframes y un listado de columnas, muestre la diferencia de medianas, en absouluto y porcentual
def compare_median_differences(df1, df2, columns, label1='DF1', label2='DF2'):
    """
    Compara las diferencias de medianas entre dos DataFrames para un listado de columnas.
    """
    print(f"Diferencias de medianas entre {label1} y {label2}:")
    col_info = {}
    for col in columns:
        median1 = df1[col].median()
        median2 = df2[col].median()
        difference = median1 - median2
        percent_difference = (difference / median1 * 100) if median1 != 0 else 0
        col_info[col] = {
            'median1': median1,
            'median2': median2,
            'difference': difference,
            'percent_difference': percent_difference
        }
        print(f"{col}: {label1} mediana = {median1:.2f}, {label2} mediana = {median2:.2f}, diferencia = {difference:.2f}, diferencia porcentual = {percent_difference:.2f}%")
    # plot para visualizar las diferencias en porcentaje de medianas
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(columns, [col_info[col]['percent_difference'] for col in columns])
    ax.set_xlabel('Diferencia porcentual de Medianas')
    ax.set_title(f'Diferencias de Medianas entre {label1} y {label2}')
    plt.show()

def heatmap_correlation(df, columns):
    corr = df[columns].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .8})
    plt.title("Heatmap de Correlación")
    plt.show()

if flag_histograms:
    hist_grid(df_clipped, move_count_hist_columns)

    # df solo con solves sub 13 segundos
    df_sub_13 = df_clipped[df_clipped['time'] < 13000]
    df_sub_15 = df_clipped[df_clipped['time'] < 15000]
    print(len(df_sub_13))
    df_15_20 = df_clipped[(df_clipped['time'] >= 15000) & (df_clipped['time'] < 20000)]
    print(len(df_15_20))

    hist_grid(df_sub_13, move_count_hist_columns, title='movecount sub 13s')
    hist_grid(df_15_20, move_count_hist_columns, title='movecount 15-20s')

    hist_grid(df_sub_13, think_columns, title='think sub 13s')
    hist_grid(df_15_20, think_columns, title='think 15-20s')

    hist_grid(df_sub_13, total_columns, title='totales sub 13s')
    hist_grid(df_15_20, total_columns, title='totales 15-20s')


    compare_median_differences(df_sub_13, df_15_20, move_count_hist_columns, label1='Sub 13s', label2='15-20s')
    compare_median_differences(df_sub_13, df_15_20, think_columns, label1='Sub 13s', label2='15-20s')
    compare_median_differences(df_sub_15, df_15_20, think_columns, label1='Sub 15s', label2='15-20s')

    compare_median_differences(df_sub_13, df_15_20, total_columns, label1='Sub 13s', label2='15-20s')
    heatmap_correlation(df_clipped, histogram_columns)

colums_to_scatterplot = [c for c in histogram_columns if c not in ['time']]
# scatter vs column time
def scatter_plot_columns(df, columns):
    cols_per_row = 2
    n = len(columns)
    rows = math.ceil(n / cols_per_row)
    fig, axs = plt.subplots(len(columns), 1, figsize=(10, 5 * len(columns)))
    for i, col in enumerate(columns):
        sns.scatterplot(data=df, x='time', y=col, ax=axs[i])
        axs[i].set_title(f'Scatter plot: time vs {col}')
        axs[i].set_xlabel('Time (ms)')
        axs[i].set_ylabel(col)
    plt.tight_layout()
    plt.show()

# No mappable was found to use for colorbar creation. First define a mappable such as an image (with imshow) or a contour set (with contourf).

def hexbin_plot_columns(df, columns, cols_per_row=3, dpi=120):
    n = len(columns)
    rows = math.ceil(n / cols_per_row)

    # Ajustamos el tamaño dinámicamente:
    # 6 pulgadas de ancho por columna y 5 de alto por fila suele ser un buen balance.
    width = cols_per_row * 6
    height = rows * 5

    # Creamos la figura. El DPI alto hace que se vea nítido en pantallas grandes.
    fig, axs = plt.subplots(rows, cols_per_row,
                            figsize=(width, height),
                            dpi=dpi,
                            constrained_layout=True) # constrained_layout es mejor que tight_layout

    # Aplanamos los ejes para iterar fácilmente, incluso si es una sola fila o columna
    if n > 1:
        axs_flat = axs.flatten()
    else:
        axs_flat = [axs]

    for i, col in enumerate(columns):
        ax = axs_flat[i]

        # Filtro de outlier (95%)
        df_clipped_heat = df[df[col] <= df[col].quantile(0.95)]

        hb = ax.hexbin(df_clipped_heat['time'],
                       df_clipped_heat[col],
                       gridsize=50,
                       cmap='inferno',
                       mincnt=1) # mincnt=1 evita pintar el fondo donde no hay datos

        ax.set_title(f'Time vs {col}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel(col)

        # Añadimos la barra de color de forma compacta
        fig.colorbar(hb, ax=ax, label='Count', shrink=0.8)

    # Ocultar ejes sobrantes si n no es múltiplo de cols_per_row
    for j in range(i + 1, len(axs_flat)):
        axs_flat[j].axis('off')

    plt.show()
if flag_scatterplots:
    # scatter_plot_columns(df_clipped, colums_to_scatterplot)
    ## all hexbin in same plot
    hexbin_plot_columns(df_clipped, colums_to_scatterplot)
