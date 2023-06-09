import paramiko
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Configuración de la conexión SSH
hostname = '192.168.18.25'
username = 'raspi'
password = 'raspi'

# Ruta del archivo de log en la Raspberry Pi
remote_path = '/home/raspi/log.txt'

# Ruta local de destino en tu computadora
local_path = 'C:/Users/gabog/Desktop/log.txt'

def copiar_archivo(remote_path, local_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    sftp = ssh.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()
    ssh.close()
copiar_archivo(remote_path, local_path)
#Leer el archivo de log y crear un DataFrame de pandas
df = pd.read_csv('log.txt', delimiter=' - ', names=['timestamp', 'description'])

# Convertir la columna de timestamp a formato de fecha y hora
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extraer las variables sensadas (temperatura y humedad)
df['temperature'] = df['description'].str.extract(r'Temp: ([0-9.]+)')
df['humidity'] = df['description'].str.extract(r'Humidity: ([0-9]+)')

# Convertir las columnas de temperatura y humedad a valores numéricos
df['temperature'] = pd.to_numeric(df['temperature'])
df['humidity'] = pd.to_numeric(df['humidity'])


# Crear una figura con subplots
fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# Graficar la temperatura en el primer subplot
axes[0].plot(df['timestamp'], df['temperature'], color='red')
axes[0].set_xlabel('Tiempo')
axes[0].set_ylabel('Temperatura (°C)')
axes[0].set_title('Gráfico de Temperatura')
axes[0].grid(True)

# Graficar la humedad en el segundo subplot
axes[1].plot(df['timestamp'], df['humidity'], color='blue')
axes[1].set_xlabel('Tiempo')
axes[1].set_ylabel('Humedad (%)')
axes[1].set_title('Gráfico de Humedad')
axes[1].grid(True)

# Ajustar el espaciado entre subplots
plt.tight_layout()

# Mostrar los subplots
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
