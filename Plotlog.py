import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Leer el archivo de log y crear un DataFrame de pandas
df = pd.read_csv('log.txt', delimiter=' - ', names=['timestamp', 'description'])

# Convertir la columna de timestamp a formato de fecha y hora
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extraer las variables sensadas (temperatura y humedad)
df['temperature'] = df['description'].str.extract(r'Temp: ([0-9.]+)')
df['humidity'] = df['description'].str.extract(r'Humidity: ([0-9]+)')

# Convertir las columnas de temperatura y humedad a valores numéricos
df['temperature'] = pd.to_numeric(df['temperature'])
df['humidity'] = pd.to_numeric(df['humidity'])

# Graficar la temperatura
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['temperature'], color='red')
plt.xlabel('Tiempo')
plt.ylabel('Temperatura (°C)')
plt.title('Gráfico de Temperatura')
plt.grid(True)
plt.show()

# Graficar la humedad
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['humidity'], color='blue')
plt.xlabel('Tiempo')
plt.ylabel('Humedad (%)')
plt.title('Gráfico de Humedad')
plt.grid(True)
plt.show()

# Calcular los valores mínimo, máximo y promedio de temperatura y humedad
temperature_min = df['temperature'].min()
temperature_max = df['temperature'].max()
temperature_avg = df['temperature'].mean()

humidity_min = df['humidity'].min()
humidity_max = df['humidity'].max()
humidity_avg = df['humidity'].mean()

# Obtener los tiempos de inicio y término
start_time = df['timestamp'].min()
end_time = df['timestamp'].max()

# Imprimir la tabla resumen
print('Tabla Resumen:')
print('----------------------------------------------------')
print('Variable    Mínimo    Máximo    Promedio')
print('----------------------------------------------------')
print(f'Temperatura  {temperature_min:.1f}°C    {temperature_max:.1f}°C    {temperature_avg:.1f}°C')
print(f'Humedad      {humidity_min}%      {humidity_max}%      {humidity_avg:.1f}%')
print('----------------------------------------------------')
print('Tiempo de inicio:', start_time)
print('Tiempo de término:', end_time)
