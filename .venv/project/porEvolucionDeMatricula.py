import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a 'Agg' para evitar el uso de tkinter
import matplotlib.pyplot as plt
import numpy as np

# Cargar el archivo de matrículas
df_matricula = pd.read_csv(r"C:\Users\migue\Downloads\MEN_MATRICULA_EN_EDUCACION_EN_PREESCOLAR__B_SICA_Y_MEDIA_HASTA_2023_20241022.csv")

# Limpiar los nombres de las columnas para eliminar espacios adicionales
df_matricula.columns = df_matricula.columns.str.strip()

# Asegurar que 'TOTAL_MATRICULA' sea leído como un número
df_matricula['TOTAL_MATRICULA'] = pd.to_numeric(df_matricula['TOTAL_MATRICULA'], errors='coerce')

# Eliminar las filas que tienen valores NaN en 'TOTAL_MATRICULA'
df_matricula = df_matricula.dropna(subset=['TOTAL_MATRICULA'])

# Agrupar por ANNO_INF y DEPARTAMENTO para sumar correctamente las matrículas
matricula_agrupada = df_matricula.groupby(['ANNO_INF', 'DEPARTAMENTO'])['TOTAL_MATRICULA'].sum().reset_index()

# Crear un gráfico para ver la suma total de matrículas por año
evolucion_matricula = matricula_agrupada.groupby('ANNO_INF')['TOTAL_MATRICULA'].sum().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(evolucion_matricula['ANNO_INF'], evolucion_matricula['TOTAL_MATRICULA'], marker='o')

# Configuración del gráfico
plt.title('Evolución de la Matrícula a lo Largo de los Años (Ajustada)')
plt.xlabel('Año')
plt.ylabel('Total de Matrículas')
plt.grid(True)

# Guardar el gráfico en un archivo
plt.savefig("evolucion_matricula_ajustada.png")

# Mostrar los totales por grado para verificar la agregación general
matriculas_por_grado = df_matricula.groupby('GRADO')['TOTAL_MATRICULA'].sum().reset_index()
print(matriculas_por_grado)

# Agrupar y mostrar un resumen de la matrícula por departamento para ver tendencias generales
matriculas_por_departamento = df_matricula.groupby('DEPARTAMENTO')['TOTAL_MATRICULA'].sum().reset_index()
print(matriculas_por_departamento)