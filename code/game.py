import os
import pygame

from code.const import WIDTH, HEIGHT, FPS, WHITE, RED, GREEN, ASSET_DIR
from code.background import Background
from code.player import Player
from code.enemy import Enemy
from code.menu import Menu
from code.explosion import Explosion


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()

        self.background = Background()

        self.font_ui = pygame.font.SysFont("arial", 24, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 32, bold=True)
        self.font_big = pygame.font.SysFont("arial", 48, bold=True)

        self.score_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "highscore.txt"
        )

    def play_music(self, filename, volume=0.5, loop=-1):
        music_path = os.path.join(ASSET_DIR, filename)
        if os.path.exists(music_path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()

    def load_high_score(self):
        if os.path.exists(self.score_file):
            with open(self.score_file, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if content.isdigit():
                    return int(content)
        return 0

    def save_high_score(self, score):
        high_score = self.load_high_score()
        if score > high_score:
            with open(self.score_file, "w", encoding="utf-8") as file:
                file.write(str(score))

    def calculate_level(self, score):
        if score >= 2000:
            return 3
        elif score >= 1000:
            return 2
        return 1

    def draw_ui(self, score, level, p1_health, p2_health=None):
        score_text = self.font_ui.render(f"Score: {score}", True, WHITE)
        level_text = self.font_ui.render(f"Level: {level}", True, WHITE)
        p1_text = self.font_ui.render(f"P1 Health: {p1_health}", True, WHITE)

        self.window.blit(score_text, (20, 20))
        self.window.blit(level_text, (20, 50))
        self.window.blit(p1_text, (20, 80))

        pygame.draw.rect(self.window, RED, (20, 115, 200, 18))
        pygame.draw.rect(self.window, GREEN, (20, 115, max(0, p1_health * 2), 18))

        if p2_health is not None:
            p2_text = self.font_ui.render(f"P2 Health: {p2_health}", True, WHITE)
            self.window.blit(p2_text, (20, 145))

            pygame.draw.rect(self.window, RED, (20, 180, 200, 18))
            pygame.draw.rect(self.window, GREEN, (20, 180, max(0, p2_health * 2), 18))

    def create_enemies(self, amount=6):
        enemies = pygame.sprite.Group()
        for _ in range(amount):
            enemies.add(Enemy())
        return enemies

    def update_enemy_difficulty(self, enemies, level):
        for enemy in enemies:
            if hasattr(enemy, "base_speed"):
                enemy.speed = enemy.base_speed + (level - 1) * 2
            else:
                enemy.speed += 0

    def score_screen(self):
        high_score = self.load_high_score()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        return "menu"

            self.window.fill((10, 10, 20))

            title = self.font_big.render("HIGH SCORE", True, WHITE)
            score_text = self.font_medium.render(f"Best Score: {high_score}", True, GREEN)
            info_text = self.font_ui.render("Pressione ENTER ou ESC para voltar", True, WHITE)

            self.window.blit(title, (WIDTH // 2 - title.get_width() // 2, 170))
            self.window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 250))
            self.window.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, 330))

            pygame.display.flip()
            self.clock.tick(FPS)

    def game_over_screen(self, score):
        self.stop_music()
        self.save_high_score(score)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

            self.window.fill((10, 10, 20))

            title = self.font_big.render("GAME OVER", True, RED)
            score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
            restart_text = self.font_ui.render("Pressione R para reiniciar", True, WHITE)
            menu_text = self.font_ui.render("Pressione ESC para voltar ao menu", True, WHITE)

            self.window.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))
            self.window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 240))
            self.window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 320))
            self.window.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 360))

            pygame.display.flip()
            self.clock.tick(FPS)

    def play(self, players_count=1):
        self.background = Background()

        score = 0
        level = self.calculate_level(score)
        self.background.set_level(level)

        player1 = Player(
            start_pos=(120, HEIGHT // 2 - 60),
            controls={
                "up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
            },
            image_name="PlayerShip.png"
        )

        players = pygame.sprite.Group()
        players.add(player1)
        player_list = [player1]

        if players_count == 2:
            player2 = Player(
                start_pos=(120, HEIGHT // 2 + 60),
                controls={
                    "up": pygame.K_UP,
                    "down": pygame.K_DOWN,
                    "left": pygame.K_LEFT,
                    "right": pygame.K_RIGHT,
                },
                image_name="PlayerShip.png"
            )
            players.add(player2)
            player_list.append(player2)

        bullets = pygame.sprite.Group()
        enemies = self.create_enemies(6)
        explosions = pygame.sprite.Group()

        self.play_music("Level1.mp3", volume=0.4)

        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop_music()
                        return "menu"

                    if event.key == pygame.K_SPACE and player1.can_shoot():
                        bullets.add(player1.shoot())

                    if players_count == 2:
                        if event.key == pygame.K_RCTRL and player_list[1].can_shoot():
                            bullets.add(player_list[1].shoot())

            players.update()
            bullets.update()
            enemies.update()
            explosions.update()

            hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
            for _, enemy_list in hits.items():
                for enemy in enemy_list:
                    score += 10
                    explosions.add(Explosion(enemy.rect.center))
                    enemy.respawn()

            for player in player_list:
                player_hits = pygame.sprite.spritecollide(player, enemies, False)
                for enemy in player_hits:
                    player.health -= 1
                    explosions.add(Explosion(player.rect.center))
                    enemy.respawn()

            level = self.calculate_level(score)
            self.background.set_level(level)
            self.background.update()
            self.update_enemy_difficulty(enemies, level)

            if any(player.health <= 0 for player in player_list):
                return self.game_over_screen(score)

            self.background.draw(self.window)
            players.draw(self.window)
            bullets.draw(self.window)
            enemies.draw(self.window)
            explosions.draw(self.window)

            if players_count == 1:
                self.draw_ui(score, level, player_list[0].health)
            else:
                self.draw_ui(score, level, player_list[0].health, player_list[1].health)

            pygame.display.flip()

        self.stop_music()
        return "menu"

    def run(self):
        running = True

        while running:
            menu = Menu(self.window)
            menu_result = menu.run(self.clock)

            if menu_result == "quit":
                running = False

            elif menu_result == "start_1p":
                result = self.play(players_count=1)

                if result == "quit":
                    running = False
                elif result == "restart":
                    continue
                elif result == "menu":
                    continue

            elif menu_result == "start_2p":
                result = self.play(players_count=2)

                if result == "quit":
                    running = False
                elif result == "restart":
                    continue
                elif result == "menu":
                    continue

            elif menu_result == "score":
                result = self.score_screen()

                if result == "quit":
                    running = False

        self.stop_music()
        pygame.quit()