import time
import board
import adafruit_dht
import logging
import paramiko

# Configurar la configuración del logging
logging.basicConfig(
    filename='log.txt',  # Nombre y ubicación del archivo de logging
    level=logging.INFO,  # Nivel de registro mínimo
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de registro
)

# Configuración de la conexión SSH
hostname = '<dirección_ip_raspberry>'
username = 'pi'
password = '<contraseña_raspberry>'

# Ruta del archivo de log en la Raspberry Pi
remote_path = 'ruta/al/archivo/log.txt'

# Ruta local de destino en tu computadora
local_path = 'ruta/local/de/destino/log.txt'

# Intervalo de tiempo entre transferencias (en segundos)
transfer_interval = 60  # Cambia esto según tus necesidades

# Initialize the dht device with the data pin connected to pin 16 (GPIO 23) of the Raspberry Pi:
dhtDevice = adafruit_dht.DHT11(board.D18)

# Crear una instancia de cliente SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Conexión SSH
ssh_client.connect(hostname, username=username, password=password)

while True:
    try:
        # Obtener la marca de tiempo actual
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Leer los valores del sensor
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # Crear la descripción del evento con los valores leídos
        event_description = "Temp: {:.1f} C    Humidity: {}%".format(temperature_c, humidity)

        # Registrar el evento en el archivo de log
        logging.info("{} - {}".format(timestamp, event_description))

        # Crear cliente SFTP
        sftp_client = ssh_client.open_sftp()

        # Transferir el archivo de log
        sftp_client.get(remote_path, local_path)

        # Cerrar el cliente SFTP
        sftp_client.close()

    except RuntimeError as error:
        # Registrar el mensaje de error en el archivo de log
        logging.error("{} - {}".format(timestamp, error.args[0]))

    except paramiko.AuthenticationException:
        print("Error de autenticación al conectar por SSH.")
        break

    except paramiko.SSHException as e:
        print("Error en la conexión SSH:", str(e))

    except Exception as e:
        print("Error durante la transferencia del archivo:", str(e))

    time.sleep(2.0)

    # Cerrar la conexión SSH y salir del bucle si se presiona Ctrl+C
    except KeyboardInterrupt:
        ssh_client.close()
        break
