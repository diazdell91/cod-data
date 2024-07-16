import pyautogui
import time

# Instrucciones para el usuario
print("Move your mouse to the desired position and wait for 5 seconds...")

# Esperar 5 segundos para que el usuario mueva el mouse a la posición deseada
time.sleep(5)

# Obtener la posición actual del mouse
x, y = pyautogui.position()

print(f"The current mouse position is: ({x}, {y})")
