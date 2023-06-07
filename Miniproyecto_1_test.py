import time
import board
import adafruit_dht
import logging

# Configurar la configuración del logging
logging.basicConfig(
    filename='log.txt',  # Nombre y ubicación del archivo de logging
    level=logging.INFO,  # Nivel de registro mínimo
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de registro
)

# Initialize the dht device with the data pin connected to pin 16 (GPIO 23) of the Raspberry Pi:
dhtDevice = adafruit_dht.DHT11(board.D18)

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

    except RuntimeError as error:
        # Registrar el mensaje de error en el archivo de log
        logging.error("{} - {}".format(timestamp, error.args[0]))

    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
