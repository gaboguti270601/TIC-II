from gpiozero import LED, Button, Buzzer
import time
import random

led_pins = [4, 17, 18]
button_pins = [27, 22, 23]
buzzer_pin = 24

leds = [LED(pin) for pin in led_pins]
buttons = [Button(pin) for pin in button_pins]
buzzer = Buzzer(buzzer_pin)

# Asignar sonidos a cada LED
sounds = {
    4: [400, 0.3],
    17: [600, 0.3],
    18: [800, 0.3]
}

def play_sound(pin):
    # Reproducir el sonido correspondiente al pin del LED
    if pin in sounds:
        frequency, duration = sounds[pin]
        buzzer.play(frequency)
        time.sleep(duration)
        buzzer.stop()

def generate_sequence(length):
    # Generar una secuencia aleatoria de encendido de los LEDs
    sequence = []
    for i in range(length):
        led = random.choice(leds)
        sequence.append(led)
        play_sound(led.pin)
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    return sequence

def get_input_sequence(length):
    # Esperar a que el usuario ingrese la secuencia a través de los botones
    input_sequence = []
    while len(input_sequence) < length:
        for button in buttons:
            if button.is_pressed:
                input_sequence.append(button)
                play_sound(button.pin)
                time.sleep(0.5)
                break
    return input_sequence

def play_game():
    level = 1
    while True:
        # Generar y reproducir la secuencia aleatoria
        sequence = generate_sequence(level)
        input_sequence = get_input_sequence(level)
        # Verificar si la secuencia ingresada es correcta
        if sequence == input_sequence:
            print("Correcto!")
            level += 1
            # Incrementar la velocidad de la secuencia
            # para los siguientes niveles
            for i in range(level):
                time.sleep(0.1)
                led = random.choice(leds)
                sequence.append(led)
                play_sound(led.pin)
                led.on()
                time.sleep(0.5)
                led.off()
                time.sleep(0.5)
        else:
            print("Game Over!")
            buzzer.play(1000)
            time.sleep(1)
            buzzer.stop()
            level = 1

# Iniciar el juego
play_game()
