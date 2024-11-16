import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a 'Agg' para evitar el uso de tkinter
import matplotlib.pyplot as plt
import numpy as np

# Traigo la información desde donde lo tengo guardado en el PC
df = pd.read_csv(r"C:\Users\migue\Downloads\MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR__B_SICA_Y_MEDIA_POR_DEPARTAMENTO_20241023.csv")

# Elimino las columnas que no me interesan
df = df.drop(columns=['APROBACIÓN_PRIMARIA', 'COBERTURA_NETA_TRANSICIÓN', 'COBERTURA_NETA_PRIMARIA', 
                      'REPROBACIÓN_TRANSICIÓN', 'REPROBACIÓN_PRIMARIA', 'REPITENCIA_TRANSICIÓN', 
                      'REPITENCIA_PRIMARIA'])

# Elimino las filas que no tengan datos en alguna columna
df = df.dropna()

# Usamos el DataFrame para agrupar la información y poderla graficar
mean_cobertura = df.groupby('DEPARTAMENTO')['COBERTURA_NETA_SECUNDARIA'].mean().reset_index()
num_departamentos = len(mean_cobertura)
colors = plt.get_cmap('tab10')(np.linspace(0, 1, num_departamentos))

# Se le da un estilo a la gráfica
plt.figure(figsize=(45, 15))  
plt.bar(mean_cobertura['DEPARTAMENTO'], mean_cobertura['COBERTURA_NETA_SECUNDARIA'], 
        color=colors)

plt.title('Cobertura Neta Secundaria por Departamento')  
plt.xlabel('Departamento')  
plt.ylabel('Cobertura')  
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

# Guarda la gráfica en un archivo en lugar de mostrarla directamente
plt.savefig("cobertura_neta_secundaria.png")
