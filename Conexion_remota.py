import paramiko
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Configuramos de la conexión SSH.
hostname = '192.168.18.25'
username = 'raspi'
password = 'raspi'

# Ruta del archivo a copiarse.
ruta_origen = '/home/raspi/Documents/log.txt'

# Ruta donde se copiara el archivo.
ruta_destino = 'C:/Users/gabog/Desktop/log.txt'

# Definimos la funcion que copia el log.txt por SSH al pc de destino.
def copiar_archivo(ruta_origen, ruta_destino):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    sftp = ssh.open_sftp()
    sftp.get(ruta_origen, ruta_destino)
    sftp.close()
    ssh.close()

# Ejecutamos la funcion para copiar el archivo.
copiar_archivo(ruta_origen, ruta_destino)

#Leemos el archivo de log.txt y creamos una tabla para ingresar los datos.
df = pd.read_csv('log.txt', delimiter=' - ', names=['Tiempo', 'descripción'])

# Convertimos la columna de tiempo a formato de fecha y hora.
df['Tiempo'] = pd.to_datetime(df['Tiempo'])

# Extraemos las variables de temperatura y humedad de la tabla.
df['Temperatura'] = df['descripción'].str.extract(r'Temperatura: ([0-9.]+)')
df['Humedad'] = df['descripción'].str.extract(r'Humedad: ([0-9]+)')

# Convertimos las columnas de temperatura y humedad a números.
df['Temperatura'] = pd.to_numeric(df['Temperatura'])
df['Humedad'] = pd.to_numeric(df['Humedad'])

# Calculamos los valores mínimo, máximo y promedio de temperatura y humedad.
temperatura_min = df['Temperatura'].min()
temperatura_max = df['Temperatura'].max()
temperatura_prom = df['Temperatura'].mean()

humedad_min = df['Humedad'].min()
humedad_max = df['Humedad'].max()
humedad_prom = df['Humedad'].mean()

# Obtenemos los tiempos de inicio y final.
tiempo_inicio = df['Tiempo'].min()
tiempo_final = df['Tiempo'].max()

# Imprimimos la tabla.
print('Tabla Resumen:')
print('----------------------------------------------------')
print('Variable    Mínimo    Máximo    Promedio')
print('----------------------------------------------------')
print(f'Temperatura  {temperatura_min:.1f}°C    {temperatura_max:.1f}°C    {temperatura_prom:.1f}°C')
print(f'Humedad      {humedad_min}%      {humedad_max}%      {humedad_prom:.1f}%')
print('----------------------------------------------------')
print('Tiempo de inicio:', tiempo_inicio)
print('Tiempo de término:', tiempo_final)

# Creamos una figura con subplots.
fig, axes = plt.subplots(2, 1, figsize=(6, 5))

# Graficamos la temperatura.
axes[0].plot(df['Tiempo'], df['Temperatura'], color='red')
axes[0].set_xlabel('Tiempo')
axes[0].set_ylabel('Temperatura (°C)')
axes[0].set_title('Gráfico de Temperatura')
axes[0].grid(True)

# Graficamos la humedad.
axes[1].plot(df['Tiempo'], df['Humedad'], color='blue')
axes[1].set_xlabel('Tiempo')
axes[1].set_ylabel('Humedad (%)')
axes[1].set_title('Gráfico de Humedad')
axes[1].grid(True)

# Ajustar el espaciado entre subplots.
plt.tight_layout()

# Mostrar los subplots.
plt.show()
