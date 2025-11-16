explicacion = '''
Read a CSV file, convert to pandas DataFrame
Some columns are not needed, so we will drop them and save the cleaned DataFrame to a new CSV file.
'''

import pandas as pd
import os
import numpy as np

input_path = 'D:\\Documentos\\Coding\\Python\\cube\\csv\\solve_lite.csv'
input_path = 'D:\\Documentos\\Coding\\Python\\Rubik - no git\\inputs\\acum\\solves 2025-08-03.csv'
input_path = 'D:\\Documentos\\Coding\\Python\\Rubik - no git\\inputs\\acum\\solves 2025-08-12.csv'
input_path = 'D:\\Documentos\\Coding\\Python\\Rubik - no git\\inputs\\acum\\solves full hasta 2025-07-29.csv'
input_path = 'D:\\Documentos\\Coding\\Python\\Rubik - no git\\inputs\\2025-08-13 to 2025-11-16.csv'
df = pd.read_csv(input_path)
# for c in df.columns:
#     # calculate the size in bytes of each column
#     byte_size = df[c].memory_usage(deep=True)
#     if byte_size != 348:
#         print(f"{df[c].memory_usage(deep=True)}  -  {c}")

# drop column named solution and each that contains "_recorded_moves"
expressions_to_drop = ["solution", "_recorded_moves", "_skipped", "_name", "_has_turns", "_moves"]
columns_to_drop = [c for c in df.columns if any(expr in c for expr in expressions_to_drop)]
# columns_to_drop = [c for c in df.columns if c == "solution" or "_recorded_moves" in c or "_skipped" in c or "_name" in c or "_has_turns" in c]
columns_to_drop.append("ruleset")
columns_to_drop.append("one_turn_away_two_second_penalty")
columns_to_drop.append("inspection_two_second_penalty")
columns_to_drop.append("device_color_scheme")
columns_to_drop.append("scramble")
columns_to_drop.append("scramble_provider")
columns_to_drop.append("description")
columns_to_drop.remove("session_name")
df_cleaned = df.drop(columns=columns_to_drop)

# compare the size in bytes of the cleaned dataframe
cleaned_size = df_cleaned.memory_usage(deep=True).sum()
# original size
original_size = df.memory_usage(deep=True).sum()
# print the size reduction in %
reduction_percent = (original_size - cleaned_size) / original_size * 100
print(f"{original_size} bytes to {cleaned_size} bytes, reduction: {reduction_percent:.2f}%")

# save cleaned dataframe to new csv file
output_path = f"{input_path[:-4]}_cleaned.csv"
df_cleaned.to_csv(output_path, index=False)


