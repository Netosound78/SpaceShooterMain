import os
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_path = os.path.join(ASSET_DIR, "PlayerShip.png")
        self.image = pygame.image.load(player_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect(center=(120, HEIGHT // 2))
        self.speed = 6
        self.health = 100
        self.last_shot = 0
        self.shot_delay = 250

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def can_shoot(self):
        now = pygame.time.get_ticks()
        return now - self.last_shot >= self.shot_delay

    def shoot(self):
        self.last_shot = pygame.time.get_ticks()
        return Bullet(self.rect.right - 5, self.rect.centery)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        bullet_path = os.path.join(ASSET_DIR, "Enemy1Shot.png")
        self.image = pygame.image.load(bullet_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (28, 12))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()