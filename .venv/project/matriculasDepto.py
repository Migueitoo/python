import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a 'Agg' para evitar el uso de tkinter
import matplotlib.pyplot as plt
import numpy as np

# Cargar el archivo de matrículas
df_matricula = pd.read_csv(r"C:\Users\migue\Downloads\MEN_MATRICULA_EN_EDUCACION_EN_PREESCOLAR__B_SICA_Y_MEDIA_HASTA_2023_20241022.csv")

# Limpiar los nombres de las columnas para eliminar espacios adicionales
df_matricula.columns = df_matricula.columns.str.strip()

# Asegurar que 'TOTAL_MATRICULA' sea leído como un número, convirtiendo cualquier valor no numérico a NaN
df_matricula['TOTAL_MATRICULA'] = pd.to_numeric(df_matricula['TOTAL_MATRICULA'], errors='coerce')

# Eliminar las filas que tienen valores NaN en 'TOTAL_MATRICULA' (si las hubiera)
df_matricula = df_matricula.dropna(subset=['TOTAL_MATRICULA'])

# Obtener el rango de años en los datos
min_year = int(df_matricula['ANNO_INF'].min())
max_year = int(df_matricula['ANNO_INF'].max())
rango_tiempo = f"{min_year}-{max_year}"

# Agrupar la información por DEPARTAMENTO y calcular el total de matrículas por departamento
matricula_por_departamento = df_matricula.groupby('DEPARTAMENTO')['TOTAL_MATRICULA'].sum().reset_index()

# Ordenar los datos por el total de matrículas de forma descendente para un mejor análisis visual
matricula_por_departamento = matricula_por_departamento.sort_values(by='TOTAL_MATRICULA', ascending=False)

# Log en consola del total de matrículas por departamento
print("Total de matrículas por departamento:")
print(matricula_por_departamento)

# Definir colores para la gráfica
num_departamentos = len(matricula_por_departamento)
colors = plt.get_cmap('tab20')(np.linspace(0, 1, num_departamentos))

# Crear el gráfico de barras con un frame más grande
plt.figure(figsize=(25, 12))  # Aumentar aún más el tamaño de la figura para más espacio
bars = plt.bar(matricula_por_departamento['DEPARTAMENTO'], matricula_por_departamento['TOTAL_MATRICULA'], color=colors)

# Configuración del gráfico
plt.title(f'Distribución de Matrículas por Departamento \nPeriodo: {rango_tiempo}')
plt.xlabel('Departamento')
plt.ylabel('Matrículas en millones de estudiantes')
plt.xticks(rotation=60, ha='right', fontsize=10)  # Rotar etiquetas y ajustar el tamaño de fuente

# Formatear el eje Y para que muestre los valores en millones
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x / 1_000_000)}M'))

# Agregar etiquetas con los valores exactos encima de cada barra
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height / 1_000_000)}M', ha='center', va='bottom')

plt.grid(axis='y', linestyle='--', alpha=0.6)

# Ajustar el espaciado para que no se corten las etiquetas
plt.tight_layout()

# Guardar el gráfico en un archivo
plt.savefig("distribucion_matricula_departamento.png")
