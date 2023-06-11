import time
import board
import adafruit_dht
import logging

# Configuración del logging.
logging.basicConfig(
    filename='log.txt',  # Nombre y ubicación del archivo de logging.
    level=logging.INFO,  # Nivel de registro mínimo.
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de registro.
)

# Inicializar el dispositivo dht con el pin de datos conectado al pin GPIO 23 de la Raspberry Pi:
dhtDevice = adafruit_dht.DHT11(board.D18)

while True:
    try:
        # Obtener la marca de tiempo actual.
        Tiempo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Leer los valores del sensor.
        Temperatura_c = dhtDevice.temperature
        Humedad = dhtDevice.humidity

        # Crear descripción del texto.
        texto = "Temperatura: {:.1f} C    Humedad: {}%".format(Temperatura_c, Humedad)

        # Registrar el texto en el archivo de log
        logging.info("{} - {}".format(Tiempo, texto))

    except RuntimeError as error:
        # Registrar el mensaje de error en el archivo de log
        logging.error("{} - {}".format(Tiempo, error.args[0]))

    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
