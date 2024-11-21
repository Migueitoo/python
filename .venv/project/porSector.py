import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a 'Agg' para evitar el uso de tkinter
import matplotlib.pyplot as plt
import numpy as np

# Cargar el archivo de matrículas
df_matricula = pd.read_csv(r"C:\Users\migue\Downloads\MEN_MATRICULA_EN_EDUCACION_EN_PREESCOLAR__B_SICA_Y_MEDIA_HASTA_2023_20241022.csv")

df_matricula.columns = df_matricula.columns.str.strip()

# Asegurar que 'TOTAL_MATRICULA' sea leído como un número, convirtiendo cualquier valor no numérico a NaN
df_matricula['TOTAL_MATRICULA'] = pd.to_numeric(df_matricula['TOTAL_MATRICULA'], errors='coerce')

# Eliminar las filas que tienen valores NaN en 'TOTAL_MATRICULA' (si las hubiera)
df_matricula = df_matricula.dropna(subset=['TOTAL_MATRICULA'])

# Renombrar los valores de 'SECTOR' para que sean más claros
df_matricula['SECTOR'] = df_matricula['SECTOR'].replace({'OFICIAL': 'Público', 'NO_OFICIAL': 'Privado'})

# Obtener el rango de años en los datos
min_year = int(df_matricula['ANNO_INF'].min())
max_year = int(df_matricula['ANNO_INF'].max())
rango_tiempo = f"{min_year}-{max_year}"

# Agrupar la información por SECTOR y calcular el total de matrículas por sector
matricula_por_sector = df_matricula.groupby('SECTOR')['TOTAL_MATRICULA'].sum().reset_index()

# Log en consola del total de matrículas por sector
print("Total de matrículas por sector:")
print(matricula_por_sector)

# Definir colores para la gráfica
colors = plt.get_cmap('tab10')(np.linspace(0, 1, len(matricula_por_sector)))

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
bars = plt.bar(matricula_por_sector['SECTOR'], matricula_por_sector['TOTAL_MATRICULA'], color=colors)

# Configuración del gráfico
plt.title(f'Desglose de Matrícula por Sector (Público vs. Privado) \nPeriodo: {rango_tiempo}')
plt.xlabel('Sector')
plt.ylabel('Matrículas en millones de estudiantes')

# Formatear el eje Y para que muestre los valores en millones
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x / 1_000_000)}M'))

# Agregar etiquetas con los valores exactos encima de cada barra
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height / 1_000_000)}M', ha='center', va='bottom')

plt.grid(axis='y', linestyle='--', alpha=0.6)

# Guardar el gráfico en un archivo
plt.savefig("desglose_matricula_sector.png")
