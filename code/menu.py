import os
import pygame
from code.const import ASSET_DIR, WIDTH, HEIGHT, WHITE, YELLOW

class Menu:
    def __init__(self, window):
        self.window = window

        menu_path = os.path.join(ASSET_DIR, "Menu.png")
        self.image = pygame.image.load(menu_path).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.font_title = pygame.font.SysFont("arial", 52, bold=True)
        self.font_text = pygame.font.SysFont("arial", 28)

        self.music_started = False

    def play_music(self):
        if not self.music_started:
            music_path = os.path.join(ASSET_DIR, "Menu.mp3")
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
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return "start"

                    if event.key == pygame.K_ESCAPE:
                        return "quit"

            self.window.blit(self.image, (0, 0))

            title = self.font_title.render("SPACE SHOOTER", True, WHITE)
            start = self.font_text.render("ENTER = Start", True, YELLOW)
            exit_game = self.font_text.render("ESC = Sair", True, YELLOW)

            self.window.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
            self.window.blit(start, (WIDTH // 2 - start.get_width() // 2, 360))
            self.window.blit(exit_game, (WIDTH // 2 - exit_game.get_width() // 2, 400))

            pygame.display.flip()
            clock.tick(60)
