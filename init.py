from pywinauto.application import Application
import pyautogui
import time
import pyautogui
import os
from pywinauto import findwindows
from screeninfo import get_monitors
from PIL import Image
import easyocr
import cv2
import numpy as np
import json
import pandas as pd


def scroll_down(number):
    i = 0
    while i < number:
        pyautogui.scroll(-1)
        i = i + 1

def open_every_rank():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    move_to_rank(current_directory, 1)
    pyautogui.click()
    time.sleep(0.25)

    move_to_rank(current_directory, 2)
    pyautogui.click()
    time.sleep(0.25)

    move_to_rank(current_directory, 3)
    pyautogui.click()
    time.sleep(0.25)

    move_to_rank(current_directory, 4)
    pyautogui.click()
    time.sleep(0.25)

def get_leader_info():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    cursor_x, cursor_y = pyautogui.position()
    cursor_y = cursor_y - 125
    pyautogui.moveTo(cursor_x, cursor_y)
    time.sleep(0.25)
    extract_profile_info_from_screen(current_directory)

def get_row_info(pending_number, spacing):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    #Move vertical and get
    scroll_down(spacing)
    cursor_x, cursor_y = pyautogui.position()
    time.sleep(0.25)
    extract_profile_info_from_screen(current_directory)

    pending_number = pending_number -1

    if pending_number >= 1:
        move_to_the_right(cursor_x, cursor_y)
        time.sleep(0.25)
        extract_profile_info_from_screen(current_directory)
        pending_number = pending_number -1

    pyautogui.moveTo(cursor_x, cursor_y)
    time.sleep(0.25)

    return pending_number

def get_row_info_with_move(pending_number):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    #Move vertical and get
    cursor_x, cursor_y = pyautogui.position()
    cursor_y = cursor_y + 125
    pyautogui.moveTo(cursor_x, cursor_y)
    time.sleep(0.25)
    extract_profile_info_from_screen(current_directory)

    pending_number = pending_number -1
    if pending_number > 1:
        move_to_the_right(cursor_x, cursor_y)
        time.sleep(0.25)
        extract_profile_info_from_screen(current_directory)
        pending_number = pending_number -1

    pyautogui.moveTo(cursor_x, cursor_y)
    time.sleep(0.25)

    return pending_number

def tune_image_for_OCR(image):
    screenshot_np = np.array(image)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)

    # Reescalado de la imagen
    scaled = cv2.resize(gray, (gray.shape[1]*2, gray.shape[0]*2), interpolation=cv2.INTER_LINEAR)

    kernel = np.ones((2,2), np.uint8)
    # adaptive_thresh = cv2.adaptiveThreshold(scaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # # Aplicar transformaciones morfológicas
    # dilated = cv2.dilate(adaptive_thresh, kernel, iterations = 1)
    eroded = cv2.erode(scaled, kernel, iterations = 1)
    return eroded

def extract_members_by_rank():
    cursor_x, cursor_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    screenshot = pyautogui.screenshot(region=(cursor_x - 20 , cursor_y - 20, screen_width - cursor_x, screen_height - cursor_y))

    modified_screenshot = tune_image_for_OCR(screenshot)
    reader = easyocr.Reader(['en'])
    resultados_ocr = reader.readtext(modified_screenshot)
    r4number = 0
    r3number = 0
    r2number = 0
    r1number = 0

    for i, result in enumerate(resultados_ocr):
        texto = result[1]
        if 'Rango 4' in texto:
            r4number = int(resultados_ocr[i + 1][1].replace('/8', ''))
        if 'Rango 3' in texto:
            r3number = int(resultados_ocr[i + 1][1])
        if 'Rango 2' in texto:
            r2number = int(resultados_ocr[i + 1][1])
        if 'Rango 1' in texto:
            r1number = int(resultados_ocr[i + 1][1])

    return r1number, r2number, r3number, r4number

def move_to_the_right(x, y):
    pyautogui.moveTo(x + 550, y, 1)
    time.sleep(0.25)

def move_to_rank(current_directory, rank):
    find_and_click_button(os.path.join(current_directory, 'buttons', 'R' + str(rank)+'.png'), 0.99, click = False)

def can_cast_int(s):
    try:
        int(s)  # Intenta convertir el string a int
        return True  # Si tiene éxito, retorna True
    except ValueError:  # Si surge un error de valor
        return False

def extract_profile_info_from_screen(current_directory):
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(0.25)
    found = find_and_click_button(os.path.join(current_directory, 'buttons', 'Inf.png'))
    
    if found is True:
        time.sleep(0.50)
        screenshot = pyautogui.screenshot()
        modified_screenshot = tune_image_for_OCR(screenshot)
        time.sleep(1)
        pyautogui.press('esc')
        reader = easyocr.Reader(['es'])
        resultados_ocr = reader.readtext(modified_screenshot)
        
        register = {
        }
        for i, result in enumerate(resultados_ocr):
            texto = result[1] 
            if "Poder" in texto:
                if i + 1 < len(resultados_ocr):
                    register['Power'] = int((resultados_ocr[i + 1][1]).replace(" ", ""))
                    register['Id'] = int(resultados_ocr[i + 2][1])
            if "Méritos" in texto:
                if i + 1 < len(resultados_ocr):
                    merits = (resultados_ocr[i + 1][1]).replace(" ", "")
                    if not merits or not can_cast_int(merits) or int(merits) < 1000:
                        register['Merits'] = 0
                    else:
                        register['Merits'] = int(merits)
                    break
        
        outputPath = os.path.join(current_directory, 'outputs', str(register['Id']) +'.json')
        with open(outputPath, 'w') as json_file:
            json.dump(register, json_file, ensure_ascii=False, indent=4) 

def find_and_click_button(image_path, confidenceValue = 0.8, click = True):
    # Usa esa ruta en pyautogui con el área de búsqueda definida
    button_location = pyautogui.locateOnScreen(image_path, confidence=confidenceValue)

    if button_location:
        # Calcula el punto central del botón
        button_center = pyautogui.center(button_location)
        # Haz clic en el punto central del botón
        if click:
            pyautogui.click(button_center)
        else:
            pyautogui.moveTo(button_center.x, button_center.y, duration=1)
        return True
    else:
        return False

def navigateToAlliance(current_directory):
    window_handle = findwindows.find_windows(title_re=".*[cC]all [oO]f [dD]ragons.*")[0]
    app = Application().connect(handle=window_handle)

    window = app.top_window()
    time.sleep(1)
    window.set_focus()
    window.click()
    time.sleep(1)

    # Abre el menú del gremio
    pyautogui.press('o')
    time.sleep(1)
    

    # Search and click config button
    find_and_click_button(os.path.join(current_directory, 'buttons', 'Conf.png'))

    time.sleep(1)
    # Search and click searchButton
    find_and_click_button(os.path.join(current_directory, 'buttons', 'ClanSearch.png'))

    time.sleep(1)
    # Search and click SearchVAR
    find_and_click_button(os.path.join(current_directory, 'buttons', 'SearchVar.png'))

    pyautogui.press('#')
    pyautogui.press('A')
    pyautogui.press('S')
    pyautogui.press('C')

    # Search and click SearchIntro
    find_and_click_button(os.path.join(current_directory, 'buttons', 'SearchIntro.png'))

    # Search and click ViewButton
    find_and_click_button(os.path.join(current_directory, 'buttons', 'ViewButton.png'))

    time.sleep(1)
    # Search and click MembersButton
    find_and_click_button(os.path.join(current_directory, 'buttons', 'Members.png'))

def exportExcel():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    current_directory = os.path.join(current_directory, 'outputs')
    data_list = []

    for file in os.listdir(current_directory):
        if file.endswith('.json'):
            ruta_completa = os.path.join(current_directory, file)
            with open(ruta_completa, 'r') as f:
                data = json.load(f)
                input = {
                    "Power": data["Power"],
                    "Id": data["Id"],
                    "Merits": data["Merits"]
                }
                data_list.append(input)

    df = pd.DataFrame(data_list)
    file_name = 'data.xlsx'
    df.to_excel(file_name, index=False)


def main():
    # current_directory = os.path.dirname(os.path.realpath(__file__))
    # # navigateToAlliance(current_directory)
    # time.sleep(0.5)
    # move_to_rank(current_directory, 4)
    # time.sleep(0.5)
    # pyautogui.click()

    # r1, r2, r3, r4 = extract_members_by_rank()

    # manualMoveR4 = False
    # manualMoveR3 = False
    # manualMoveR2 = False
    # if r1 < 5:
    #     manualMoveR2 = True

    # if (r1 + r2) < 5:
    #     manualMoveR3 = True

    # open_every_rank()
    
    # get_leader_info()
    # move_to_rank(current_directory, 4)
    # time.sleep(0.25)

    # spacing = 2 
    # while(r4 > 0):
    #     r4 = get_row_info(r4, spacing)
    #     if(spacing == 2):
    #         spacing = 3
    #     else:
    #         spacing = 2
    
    # scroll_down(spacing - 1)
    # time.sleep(0.5)
    # move_to_rank(current_directory, 3)
    # time.sleep(1)

    # spacing = 2 
    # while(r3 > 0):
    #     r3 = get_row_info(r3, spacing)
    #     if(spacing == 2):
    #         spacing = 3
    #     else:
    #         spacing = 2

    # scroll_down(spacing - 1)
    # time.sleep(0.5)
    # move_to_rank(current_directory, 2)
    # time.sleep(1)

    # spacing = 2 
    # while(r2 > 0):
    #     r2 = get_row_info(r2, spacing)
    #     if(spacing == 2):
    #         spacing = 3
    #     else:
    #         spacing = 2
    
    # scroll_down(spacing - 1)
    # time.sleep(0.5)
    # move_to_rank(current_directory, 2)
    # time.sleep(1)

    # spacing = 2 
    # while(r1 > 0):
    #     if r1 > 6:
    #         r1 = get_row_info(r1, spacing)
    #         if(spacing == 2):
    #             spacing = 3
    #         else:
    #             spacing = 2
    #     else:
    #         r1 = get_row_info_with_move(r1)
    
    exportExcel()

if __name__ == "__main__":
    main()