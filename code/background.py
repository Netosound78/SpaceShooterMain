import os
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT

class Background:
    def __init__(self):
        bg_path = os.path.join(ASSET_DIR, "Blue Nebula 1 - 1024x1024.png")
        self.image = pygame.image.load(bg_path).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

    def draw(self, window):
        window.blit(self.image, (0, 0))