import os
import random
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        enemy_path = os.path.join(ASSET_DIR, "Enemy1.png")
        self.image = pygame.image.load(enemy_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))

        x = random.randint(WIDTH + 20, WIDTH + 300)
        y = random.randint(40, HEIGHT - 40)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.respawn()

    def respawn(self):
        self.rect.x = random.randint(WIDTH + 50, WIDTH + 300)
        self.rect.y = random.randint(40, HEIGHT - 40)
        self.speed = random.randint(3, 7)