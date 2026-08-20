import os
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT, WHITE, YELLOW, GREEN

class Menu:
    def __init__(self, window):
        self.window = window

        menu_path = os.path.join(ASSET_DIR, "Menu.png")
        self.image = pygame.image.load(menu_path).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.font_title = pygame.font.SysFont("arial", 52, bold=True)
        self.font_text = pygame.font.SysFont("arial", 28)
        self.options = [
            "New Game - 1 Player",
            "New Game - 2 Players",
            "Score",
            "Quit"
        ]
        self.selected = 0
        self.music_started = False

    def play_music(self):
        if not self.music_started:
            music_path = os.path.join(ASSET_DIR, "Menu.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
            self.music_started = True

    def run(self, clock):
        self.play_music()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)

                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)

                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()

                        if self.selected == 0:
                            return "start_1p"
                        elif self.selected == 1:
                            return "start_2p"
                        elif self.selected == 2:
                            return "score"
                        elif self.selected == 3:
                            return "quit"

                    elif event.key == pygame.K_ESCAPE:
                        return "quit"

            self.window.blit(self.image, (0, 0))

            title = self.font_title.render("SPACE SHOOTER", True, WHITE)
            self.window.blit(title, (WIDTH // 2 - title.get_width() // 2, 90))

            for i, option in enumerate(self.options):
                color = GREEN if i == self.selected else YELLOW
                text = self.font_text.render(option, True, color)
                self.window.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 50))

            pygame.display.flip()
            clock.tick(60)
