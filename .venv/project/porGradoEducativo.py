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

# Agrupar la información por GRADO y calcular el total de matrículas por grado
matricula_por_grado = df_matricula.groupby('GRADO')['TOTAL_MATRICULA'].sum().reset_index()

# Filtrar los grados desde Sexto hasta Once
grados_seleccionados = ['Sexto', 'Septimo', 'Octavo', 'Noveno', 'Decimo', 'Once']
matricula_por_grado = matricula_por_grado[matricula_por_grado['GRADO'].isin(grados_seleccionados)]

# Ordenar los datos por el orden natural de los grados seleccionados
matricula_por_grado = matricula_por_grado.set_index('GRADO').loc[grados_seleccionados].reset_index()

# Log en consola del total de matrículas por grado seleccionado
print("Total de matrículas por grado educativo (Sexto a Once):")
print(matricula_por_grado)

# Definir colores para la gráfica
num_grados = len(matricula_por_grado)
colors = plt.get_cmap('tab10')(np.linspace(0, 1, num_grados))

# Crear el gráfico de barras con un frame más grande
plt.figure(figsize=(12, 6))  # Ajustar el tamaño del gráfico
bars = plt.bar(matricula_por_grado['GRADO'], matricula_por_grado['TOTAL_MATRICULA'], color=colors)

# Configuración del gráfico
plt.title(f'Distribución de Matrículas por Grado Educativo (Sexto a Once) \nPeriodo: {rango_tiempo}')
plt.xlabel('Grado')
plt.ylabel('Matrículas en millones de estudiantes')

# Formatear el eje Y para que muestre los valores en millones
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x / 1_000_000)}M'))

# Agregar etiquetas con los valores exactos encima de cada barra
for bar in bars:
    height = bar.get_height()
    if height >= 1_000_000:
        label = f'{int(height / 1_000_000)}M'
    else:
        label = f'{int(height):,}'
    plt.text(bar.get_x() + bar.get_width() / 2, height, label, ha='center', va='bottom')

plt.grid(axis='y', linestyle='--', alpha=0.6)

# Ajustar el espaciado para que no se corten las etiquetas
plt.tight_layout()

# Guardar el gráfico en un archivo
plt.savefig("distribucion_matricula_sexto_once.png")
