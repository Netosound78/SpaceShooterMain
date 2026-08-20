import pygame
from code.const import YELLOW, RED

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.frames = []
        self.index = 0
        self.counter = 0
        self.animation_speed = 2

        sizes = [20, 30, 42, 56, 72, 90]

        for size in sizes:
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 220, 0, 180), (size, size), size)
            pygame.draw.circle(surf, (255, 120, 0, 160), (size, size), int(size * 0.7))
            pygame.draw.circle(surf, (255, 40, 0, 140), (size, size), int(size * 0.4))
            self.frames.append(surf)

        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=center)

    def update(self):
        self.counter += 1

        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.frames):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(center=center)