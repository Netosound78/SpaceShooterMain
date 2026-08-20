import os
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT


class Background:
    def __init__(self):
        self.images = []
        self.index = 0

        for i in range(1, 9):
            filename = f"Blue Nebula {i} - 1024x1024.png"
            path = os.path.join(ASSET_DIR, filename)

            if os.path.exists(path):
                image = pygame.image.load(path).convert()
                image = pygame.transform.scale(image, (WIDTH, HEIGHT))
                self.images.append(image)

        if not self.images:
            raise FileNotFoundError("Nenhum background Blue Nebula foi encontrado na pasta asset.")

        self.image = self.images[self.index]

        self.change_interval = 10000
        self.last_change = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_change >= self.change_interval:
            self.last_change = now

            self.index = (self.index + 1) % len(self.images)

            self.image = self.images[self.index]

    def draw(self, window):
        window.blit(self.image, (0, 0))