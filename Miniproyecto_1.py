import time
import board
import adafruit_dht
import logging

# Initialize the dht device with the data pin connected to pin 16 (GPIO 23) of the Raspberry Pi:
dhtDevice = adafruit_dht.DHT11(board.D18)

# Configurar la configuración del logging
logging.basicConfig(
    filename='log.txt', # Nombre y ubicación del archivo de logging
    level=logging.INFO, # Nivel de registro mínimo
    format='%(asctime)s - %(levelname)s - %(message)s' # Formato de registro
)
while True:
    try:
        # Print the values via the serial interface
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
    except RuntimeError as error:
        # Errors happen quite often, DHT's are hard to read, just move on
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    time.sleep(2.0)
# Registrar eventos de ejemplo
logging.debug('Este es un mensaje de depuración')
logging.info('Este es un mensaje informativo')
logging.warning('Este es un mensaje de advertencia')
logging.error('Este es un mensaje de error')
logging.critical('Este es un mensaje crítico')
