from gpiozero import LED, Button, Buzzer
from time import sleep
import random

led_pins = [4, 17, 18]
button_pins = [27, 22, 23]
buzzer_pin = 24

leds = [LED(pin) for pin in led_pins]
buttons = [Button(pin) for pin in button_pins]
buzzer = Buzzer(buzzer_pin)

sequence = []
level = 1
speeds = [1, 0.75, 0.5]  # Velocidades para cada nivel

# Asociar cada LED con un sonido
sounds = {leds[0]: (262, 0.5), leds[1]: (330, 0.5), leds[2]: (392, 0.5)}

# Función para reproducir un sonido en el buzzer
def play_sound(frequency, duration):
    buzzer.frequency = frequency
    buzzer.on()
    sleep(duration)
    buzzer.off()

# Función para generar una nueva secuencia aleatoria
def generate_sequence():
    return [random.choice(leds) for _ in range(level)]

# Función para reproducir una secuencia
def play_sequence():
    for led in sequence:
        led.on()
        play_sound(*sounds[led])
        led.off()
        sleep(speeds[level-1])

# Función para esperar que el usuario repita la secuencia
def get_input():
    input_sequence = []
    for _ in range(level):
        while True:
            for i, button in enumerate(buttons):
                if button.is_pressed:
                    input_sequence.append(leds[i])
                    play_sound(*sounds[leds[i]])
                    sleep(0.5)
                    break
            else:
                continue
            break
    return input_sequence

# Función para verificar si la secuencia ingresada por el usuario es correcta
def check_input(input_sequence):
    return input_sequence == sequence

# Función para reiniciar el juego
def restart_game():
    play_sound(262, 1)
    sleep(1)
    global level, sequence
    level = 1
    sequence = []

# Bucle principal del juego
while True:
    print("Nivel:", level)
    sleep(1)

    # Generar y reproducir una nueva secuencia
    sequence = generate_sequence()
    play_sequence()

    # Esperar que el usuario repita la secuencia
    input_sequence = get_input()

    # Verificar si la secuencia ingresada es correcta
    if check_input(input_sequence):
        level += 1
        if level > len(speeds):
            print("¡Ganaste!")
            restart_game()
        else:
            print("¡Correcto! Siguiente nivel.")
    else:
        print("¡Incorrecto! Inténtalo de nuevo.")
        play_sound(110, 2)
        restart_game()

    sleep(1)
