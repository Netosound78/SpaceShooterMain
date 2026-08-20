import os
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        bullet_path = os.path.join(ASSET_DIR, "Player1Shot.png")
        self.image = pygame.image.load(bullet_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (28, 12))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 12

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos=(120, HEIGHT // 2), controls=None, image_name="PlayerShip.png"):
        super().__init__()

        player_path = os.path.join(ASSET_DIR, image_name)
        self.image = pygame.image.load(player_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 6
        self.health = 100
        self.last_shot = 0
        self.shot_delay = 250

        self.controls = controls or {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
        }

    def update(self):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[self.controls["up"]]:
            dy -= self.speed
        if keys[self.controls["down"]]:
            dy += self.speed
        if keys[self.controls["left"]]:
            dx -= self.speed
        if keys[self.controls["right"]]:
            dx += self.speed

        self.rect.x += dx
        self.rect.y += dy

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