import pyautogui
import time
import os
import random
import tkinter as tk
from tkinter import simpledialog
import uuid
import numpy as np
import cv2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_speed():
    numero = random.uniform(0.1, 0.4)
    return round(numero, 2)

def tune_image_for_OCR(image):
    screenshot_np = np.array(image)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    scaled = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2), interpolation=cv2.INTER_LINEAR)
    kernel = np.ones((2, 2), np.uint8)
    eroded = cv2.erode(scaled, kernel, iterations=1)
    return eroded

def get_user_data():
    root = tk.Tk()
    root.withdraw()
    alliance_name = simpledialog.askstring("Input", "Type the Guild Name:", parent=root)
    return alliance_name

def extract_profile_info_from_screen(current_directory, alliance_name):
    folder_name = str(uuid.uuid4())
    
    for attempt in range(3):
        time.sleep(0.5)
        found = find_button(os.path.join(current_directory, 'buttons', 'Inf.png'), 0.8)
        if not found:
            logging.warning('Inf.png button not found.')
            continue

        time.sleep(0.5)
        screenshot0 = pyautogui.screenshot(region=(665, 674, 784 - 665, 712 - 674))
        save_screenshot(screenshot0, current_directory, "1", folder_name, alliance_name)
        
        found2 = find_button(os.path.join(current_directory, 'buttons', 'MoreInfo.png'), 0.7)
        time.sleep(0.5)
        
        if not found2:
            found2 = find_button(os.path.join(current_directory, 'buttons', 'MoreInfo2.png'), 0.7)
        
        if found2:
            screenshot1 = pyautogui.screenshot(region=(140, 650, 250, 600))
            time.sleep(0.1)
            screenshot2 = pyautogui.screenshot(region=(542, 546, 305, 848))
            save_screenshot(screenshot1, current_directory, "2", folder_name, alliance_name)
            time.sleep(0.13)
            save_screenshot(screenshot2, current_directory, "3", folder_name, alliance_name)
            time.sleep(1)
            
            pyautogui.press('esc')
            time.sleep(1)
            pyautogui.press('esc')
            time.sleep(1)
            return True
        else:
            logging.warning('MoreInfo button not found.')

    return False

def find_button(image_path, confidenceValue=0.7, click=True):
    try:
        button_location = pyautogui.locateOnScreen(image_path, confidence=confidenceValue)
        if button_location:
            time.sleep(0.3)
            button_center = pyautogui.center(button_location)
            time.sleep(0.4)
            duration = get_random_speed()
            pyautogui.moveTo(button_center.x, button_center.y, duration=duration)
            time.sleep(0.3)
            if click:
                pyautogui.click(button_center.x, button_center.y)
            return button_center
        else:
            return None
    except Exception as e:
        logging.warning(f'Error finding button MoreInfo: {e}')
        return None

def save_screenshot(screenshot, current_directory, image_number, folder_name, alliance_name):
    folder_path = os.path.join(current_directory, 'outputs', alliance_name, str(folder_name))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, f'{image_number}.png')
    screenshot.save(file_path)

def process_ranks(current_directory, alliance_name):
    player_button_path = os.path.join(current_directory, 'buttons', '1.png')
    initial_position = find_button(player_button_path, 0.90, click=False)

    if initial_position is None:
        logging.error("Error: Could not find starting position of first player.")
        return

    rank_positions = [
        (initial_position.x, initial_position.y),
        (initial_position.x, initial_position.y + 100),
        (initial_position.x, initial_position.y + 200),
        (initial_position.x, initial_position.y + 300)
    ]
    
    rank_count = 0

    while rank_count < 210:
        logging.info(f"Processing rank {rank_count + 1}")
        
        for i in range(4):
            rank_position = rank_positions[i]
            pyautogui.moveTo(rank_position, duration=get_random_speed())
            time.sleep(0.5)
            pyautogui.click()
            success = extract_profile_info_from_screen(current_directory, alliance_name)
            if not success:
                logging.error("Failed to extract profile info. Continuing process.")
            time.sleep(0.5)
            rank_count += 1
            if rank_count >= 210:
                break

        # Scroll after processing 4 players
        logging.info("Returning to initial position")
        pyautogui.moveTo(rank_positions[3], duration=get_random_speed())
        time.sleep(0.5)
        logging.info("Scrolling")
        pyautogui.scroll(-400)  # Desplazar 400 píxeles en el eje vertical
        time.sleep(1.5)

def main():
    time.sleep(2)
    current_directory = os.path.dirname(os.path.realpath(__file__))
    alliance_name = get_user_data()
    time.sleep(2)
    process_ranks(current_directory, alliance_name)
    logging.info("Process completed.")

if __name__ == "__main__":
    main()
