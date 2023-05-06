from gpiozero import LED, Button, Buzzer
from time import sleep
from random import randint

# Definir los pines de los LEDs y botones
led_pins = [4, 17, 18]
button_pins = [27, 22, 23]
buzzer_pin = 24

# Crear los objetos LED, Button y Buzzer
leds = [LED(pin) for pin in led_pins]
buttons = [Button(pin) for pin in button_pins]
buzzer = Buzzer(buzzer_pin)

# Diccionario que asocia cada LED con un sonido particular
sounds = {
    4: (262, 0.5),   # C4
    17: (294, 0.5),  # D4
    18: (330, 0.5)   # E4
}

# Función para reproducir un sonido a través del Buzzer
def play_sound(pin):
    if pin in sounds:
        frequency, duration = sounds[pin]
        buzzer.beep(frequency=frequency, duration=duration)

# Función para generar una nueva secuencia aleatoria
def generate_sequence(length):
    return [randint(0, len(led_pins)-1) for _ in range(length)]

# Función para reproducir una secuencia de LEDs y sonidos
def play_sequence(sequence):
    for i in sequence:
        leds[i].on()
        play_sound(led_pins[i])
        sleep(0.5)
        leds[i].off()
        sleep(0.5)

# Función para obtener la secuencia ingresada por el usuario
def get_input(length):
    input_sequence = []
    while len(input_sequence) < length:
        for i in range(len(buttons)):
            if buttons[i].is_pressed:
                input_sequence.append(i)
                play_sound(led_pins[i])
                while buttons[i].is_pressed:
                    pass
    return input_sequence

# Función para verificar si la secuencia ingresada es correcta
def check_input(input_sequence, sequence):
    return input_sequence == sequence

# Función para reiniciar el juego
def restart_game():
    buzzer.beep(frequency=262, duration=1)
    sleep(1)
    global level, sequence
    level = 1
    sequence = generate_sequence(level)

# Configurar el nivel inicial y la secuencia
level = 1
sequence = generate_sequence(level)

# Bucle principal del juego
while True:
    print("Nivel:", level)
    sleep(1)
    play_sequence(sequence)
    user_sequence = get_input(level)
    if check_input(user_sequence, sequence):
        print("¡Correcto!")
        level += 1
        if level > 5:
            print("¡Ganaste!")
            break
        sequence = generate_sequence(level)
    else:
        print("¡Game Over!")
        restart_game()
