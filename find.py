import pyautogui
import cv2
import numpy as np
import time

def find_and_click_button(button_image_path, confidence=0.8, click=True):
    pyautogui.click()
    screenshot = pyautogui.screenshot()
    screen_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    button = cv2.imread(button_image_path, cv2.IMREAD_GRAYSCALE)
    
    # Aplicar preprocesamiento si es necesario, por ejemplo, ajuste de contraste
    # button = cv2.equalizeHist(button)

    res = cv2.matchTemplate(screen_gray, button, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= confidence:
        button_height, button_width = button.shape
        center_x = max_loc[0] + button_width // 2
        center_y = max_loc[1] + button_height // 2

        print(f"Button found with confidence {max_val}. Clicking at ({center_x}, {center_y})")
        time.sleep(3)
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        time.sleep(0.40)
        if click:
            print("Clicking")
            pyautogui.click(clicks=1)
        else:
            print(f"Button found with confidence {max_val}")
        return True
    else:
        print(f"Button not found with confidence {confidence}. Max value was {max_val}")
        return False

# Ejemplo de uso:
button_image_path = "buttons/Inf.png"  # Reemplaza con la ruta a tu imagen del botón
found = find_and_click_button(button_image_path, confidence=0.3, click=True)

if found:
    print("Button found and clicked")
else:
    print("Button not found")
