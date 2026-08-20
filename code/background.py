import os
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT


class Background:
    def __init__(self):
        self.level = 1
        self.images = []
        self.index = 0
        self.change_interval = 5000
        self.last_change = pygame.time.get_ticks()

        self.load_level_images(self.level)

    def load_level_images(self, level):
        self.level = level
        self.images = []
        self.index = 0
        self.last_change = pygame.time.get_ticks()

        if level == 1:
            prefix = "Blue Nebula"
        elif level == 2:
            prefix = "Green Nebula"
        else:
            prefix = "Purple Nebula"

        for i in range(1, 9):
            filename = f"{prefix} {i} - 1024x1024.png"
            path = os.path.join(ASSET_DIR, filename)

            if os.path.exists(path):
                image = pygame.image.load(path).convert()
                image = pygame.transform.scale(image, (WIDTH, HEIGHT))
                self.images.append(image)

        if not self.images:
            raise FileNotFoundError(f"Nenhum background encontrado para o level {level} com prefixo {prefix}.")

        self.image = self.images[self.index]

    def set_level(self, level):
        if level != self.level:
            self.load_level_images(level)

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_change >= self.change_interval:
            self.last_change = now
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def draw(self, window):
        window.blit(self.image, (0, 0))