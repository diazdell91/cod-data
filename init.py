import pyautogui
import time
import os
import easyocr
import cv2
import numpy as np
import json
import pandas as pd
import random
import tkinter as tk
import shutil
from tkinter import simpledialog


def get_random_speed():
    numero = random.uniform(0.1, 0.4)
    return round(numero, 2)

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

    timeSpeed = get_random_speed()
    pyautogui.moveTo(cursor_x, cursor_y, duration = timeSpeed)
    time.sleep(0.25)

    return pending_number

def get_row_info_with_move(pending_number):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    cursor_x, cursor_y = pyautogui.position()
    cursor_y = cursor_y + 125
    timeSpeed = get_random_speed()
    pyautogui.moveTo(cursor_x, cursor_y, duration = timeSpeed)
    time.sleep(0.25)
    extract_profile_info_from_screen(current_directory)

    pending_number = pending_number - 1
    if pending_number >= 1:
        move_to_the_right(cursor_x, cursor_y)
        time.sleep(0.25)
        extract_profile_info_from_screen(current_directory)
        pending_number = pending_number -1

    timeSpeed = get_random_speed()
    pyautogui.moveTo(cursor_x, cursor_y, duration = timeSpeed)
    time.sleep(0.25)

    return pending_number

def tune_image_for_OCR(image):
    screenshot_np = np.array(image)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    scaled = cv2.resize(gray, (gray.shape[1]*2, gray.shape[0]*2), interpolation=cv2.INTER_LINEAR)
    kernel = np.ones((2,2), np.uint8)
    eroded = cv2.erode(scaled, kernel, iterations = 1)

    return eroded

def get_user_data():
    root = tk.Tk()
    root.withdraw() 

    alliance_name = simpledialog.askstring("Input", "Type the Guild Name:", parent=root)
    r1 = simpledialog.askinteger("Input", "Type the r1's number:", parent=root)
    r2 = simpledialog.askinteger("Input", "Type the r2's number:", parent=root)
    r3 = simpledialog.askinteger("Input", "Type the r3's number:", parent=root)
    r4 = simpledialog.askinteger("Input", "Type the r4's number:", parent=root)

    return alliance_name, r1, r2, r3, r4

def move_to_the_right(x, y):
    timeSpeed = get_random_speed()
    pyautogui.moveTo(x + 550, y, duration = timeSpeed)
    time.sleep(0.25)

def move_to_rank(current_directory, rank):
    find_and_click_button(os.path.join(current_directory, 'buttons', 'R' + str(rank)+'.png'), 0.99, click = False)

def can_cast_int(s):
    try:
        int(s) 
        return True  
    except ValueError:  
        return False

def extract_profile_info_from_screen(current_directory):
    time.sleep(0.50)
    pyautogui.click()
    time.sleep(0.25)
    found = find_and_click_button(os.path.join(current_directory, 'buttons', 'Inf.png'))
    time.sleep(0.25)

    if found is True:
        time.sleep(0.25)
        screenshot0 = pyautogui.screenshot(region=(665, 674, 784 - 665, 712 - 674))
        time.sleep(0.25)
        modified_screenshot0 = tune_image_for_OCR(screenshot0)
        found2 = find_and_click_button(os.path.join(current_directory, 'buttons', 'MoreInfo.png'))
        time.sleep(0.5)
        if found2 is True:
            screenshot = pyautogui.screenshot(region=(847, 546, 1210, 587))
            screenshot2 = pyautogui.screenshot(region=(542, 546, 305, 648))
            modified_screenshot = tune_image_for_OCR(screenshot)
            modified_screenshot2 = tune_image_for_OCR(screenshot2)
            time.sleep(0.5)
            pyautogui.press('esc')
            pyautogui.press('esc')
            reader = easyocr.Reader(['es'])
            resultados_ocr = reader.readtext(modified_screenshot)
            resultados_ocr2 = reader.readtext(modified_screenshot2)
            resultados_ocr0 = reader.readtext(modified_screenshot0)
            
            register = {
            }
            for i, result in enumerate(resultados_ocr0):
                register['Id'] = int(resultados_ocr0[i][1])
            

            found = False
            name = ""
            for i, result in enumerate(resultados_ocr2):
                texto2 = result[1] 
                if "Poder" in texto2:
                    found = False
                    register['Name'] = name
                    try:
                        register['CurrentPower'] = int(resultados_ocr2[i+1][1].replace(" ", ""))
                    except ValueError:
                        register['CurrentPower'] = "Error"
                if "Méritos" in texto2:
                    try:
                        merits = int(resultados_ocr2[i + 1][1].replace(" ", ""))
                        if  int(merits) < 1000:
                            register['Merits'] = 0
                        else:
                            register['Merits'] = int(merits)
                    except ValueError:
                        register['Merits'] = "Error"

                if found:
                    name  = name + str(texto2)
                if "Lord" in texto2:
                    found = True
                
            for i, result in enumerate(resultados_ocr):
                texto = result[1] 
                if "Máximo poder histórico" in texto:
                    if i + 1 < len(resultados_ocr):
                        register['MaxPower'] = int(resultados_ocr[i + 1][1].replace(" ", ""))
                if "Unidades eliminadas" in texto:
                    if i + 1 < len(resultados_ocr):
                        register['KilledUnits'] = int(resultados_ocr[i + 1][1].replace(" ", ""))
                if "Unidades muertas" in texto:
                    if i + 1 < len(resultados_ocr):
                        register['DeathUnits'] = int(resultados_ocr[i + 1][1].replace(" ", ""))
                if "Unidades curadas" in texto:
                    if i + 1 < len(resultados_ocr):
                        register['HealedUnits'] = int(resultados_ocr[i + 1][1].replace(" ", ""))
                        
            outputPath = os.path.join(current_directory, 'outputs', str(register['Id']) +'.json')
            with open(outputPath, 'w') as json_file:
                json.dump(register, json_file, ensure_ascii=False, indent=4) 

def find_and_click_button(image_path, confidenceValue = 0.8, click = True):
    button_location = pyautogui.locateOnScreen(image_path, confidence=confidenceValue)

    if button_location:
        button_center = pyautogui.center(button_location)
        if click:
            pyautogui.click(button_center)
        else:
            duration = get_random_speed()
            pyautogui.moveTo(button_center.x, button_center.y, duration=duration)
        return True
    else:
        return False
def exportExcel(alliance_name):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    current_directory = os.path.join(current_directory, 'outputs')
    data_list = []

    for file in os.listdir(current_directory):
        if file.endswith('.json'):
            ruta_completa = os.path.join(current_directory, file)
            with open(ruta_completa, 'r') as f:
                data = json.load(f)
                input = {
                    "Name": data["Name"],
                    "Id": data["Id"],
                    "CurrentPower": data["CurrentPower"],
                    "MaxPower": data["MaxPower"],
                    "Merits": data["Merits"],
                    "KilledUnits":data["KilledUnits"],
                    "DeathUnits":data["DeathUnits"],
                    "HealedUnits":data["HealedUnits"]
                }
                data_list.append(input)

    df = pd.DataFrame(data_list)
    file_name = alliance_name + '.xlsx'
    df.to_excel(file_name, index=False)
def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    outputs_path = os.path.join(current_directory, 'outputs')
    clear_folder(outputs_path)
    move_to_rank(current_directory, 4)
    time.sleep(0.5)
    pyautogui.click()
    alliance_name, r1, r2, r3, r4 = get_user_data()
    time.sleep(2.5)
    open_every_rank()
    
    get_leader_info() 
    move_to_rank(current_directory, 4)
    time.sleep(0.25)

    spacing = 2 
    while(r4 > 0):
        r4 = get_row_info(r4, spacing)
        if(spacing == 2):
            spacing = 3
        else:
            spacing = 2
    
    scroll_down(spacing - 1)
    time.sleep(0.5)
    move_to_rank(current_directory, 3)
    time.sleep(1)

    spacing = 2 
    while(r3 > 0):
        r3 = get_row_info(r3, spacing)
        if(spacing == 2):
            spacing = 3
        else:
            spacing = 2

    scroll_down(spacing - 1)
    time.sleep(0.5)
    move_to_rank(current_directory, 2)
    time.sleep(1)

    spacing = 2 
    while(r2 > 0):
        r2 = get_row_info(r2, spacing)
        if(spacing == 2):
            spacing = 3
        else:
            spacing = 2
    
    scroll_down(spacing - 1)
    time.sleep(0.5)
    move_to_rank(current_directory, 2)
    time.sleep(1)

    spacing = 2 
    while(r1 > 0):
        if r1 > 6:
            r1 = get_row_info(r1, spacing)
            if(spacing == 2):
                spacing = 3
            else:
                spacing = 2
        else:
            r1 = get_row_info_with_move(r1)
    
    exportExcel(alliance_name)

if __name__ == "__main__":
    main()