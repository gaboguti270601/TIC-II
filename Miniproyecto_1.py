import RPi.GPIO as GPIO
import time
import random

# Definir los pines de los botones
boton1_pin = 2
boton2_pin = 3
boton3_pin = 4

# Definir los pines de las luces
luz1_pin = 5
luz2_pin = 6
luz3_pin = 7

# Definir el pin del buzzer
buzzer_pin = 8

# Configurar los pines de los botones como entradas
GPIO.setup(boton1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configurar los pines de las luces como salidas
GPIO.setup(luz1_pin, GPIO.OUT)
GPIO.setup(luz2_pin, GPIO.OUT)
GPIO.setup(luz3_pin, GPIO.OUT)

# Configurar el pin del buzzer como salida
GPIO.setup(buzzer_pin, GPIO.OUT)

# Definir los sonidos del buzzer
sonido1 = [200, 0.1]
sonido2 = [400, 0.1]
sonido3 = [600, 0.1]

# Crear una lista de luces y sonidos
luces = [luz1_pin, luz2_pin, luz3_pin]
sonidos = [sonido1, sonido2, sonido3]

# Función para reproducir un sonido en el buzzer
def reproducir_sonido(frecuencia, duracion):
    if frecuencia > 0:
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(duracion)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.05)

# Función para iluminar una luz y reproducir un sonido
def iluminar_luz(luz, sonido):
    GPIO.output(luz, GPIO.HIGH)
    reproducir_sonido(sonido[0], sonido[1])
    GPIO.output(luz, GPIO.LOW)
    time.sleep(0.5)

# Función para reproducir una secuencia aleatoria de luces y sonidos
def reproducir_secuencia(secuencia):
    for i in range(len(secuencia)):
        iluminar_luz(luces[secuencia[i]], sonidos[secuencia[i]])

# Función para leer el botón presionado
def leer_boton():
    boton1 = not GPIO.input(boton1_pin)
    boton2 = not GPIO.input(boton2_pin)
    boton3 = not GPIO.input(boton3_pin)

    if boton1:
        return 0
    elif boton2:
        return 1
    elif boton3:
        return 2

# Función principal del juego
def jugar():
    secuencia = []
    intento = []

    while True:
        secuencia.append(random.randint(0, 2))
        reproducir_secuencia(secuencia)

        for i in range(len(secuencia)):
            boton_presionado = False

            while not boton_presionado:
                boton = leer_boton()
                if boton is not None:
                    iluminar_luz(luces[boton], sonidos[boton])
                    intento.append(boton)
                    boton_presionado = True
                if intento[i] != secuencia[i]:
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    return False

        time.sleep(0.5)
        intento = []

# Configurar el modo de la biblioteca RPi.GPIO
GPIO.setmode(GPIO.BCM)

# Ejecutar la función principal del juego
jugar()

# Limpiar los pines de la Raspberry Pi
GPIO.cleanup()