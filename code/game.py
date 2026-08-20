import pygame
from code.const import WIDTH, HEIGHT, FPS, WHITE, RED, GREEN
from code.background import Background
from code.player import Player
from code.enemy import Enemy
from code.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()

        self.background = Background()

        self.font_ui = pygame.font.SysFont("arial", 24, bold=True)
        self.font_big = pygame.font.SysFont("arial", 48, bold=True)

    def draw_ui(self, score, health):
        score_text = self.font_ui.render(f"Score: {score}", True, WHITE)
        health_text = self.font_ui.render(f"Health: {health}", True, WHITE)

        self.window.blit(score_text, (20, 20))
        self.window.blit(health_text, (20, 50))

        pygame.draw.rect(self.window, RED, (20, 80, 200, 20))
        pygame.draw.rect(self.window, GREEN, (20, 80, max(0, health * 2), 20))

    def game_over_screen(self, score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_ESCAPE:
                        return "quit"

            self.window.fill((10, 10, 20))

            game_over = self.font_big.render("GAME OVER", True, RED)
            score_text = self.font_ui.render(f"Final Score: {score}", True, WHITE)
            restart_text = self.font_ui.render("Pressione R para reiniciar", True, WHITE)
            quit_text = self.font_ui.render("Pressione ESC para sair", True, WHITE)

            self.window.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, 180))
            self.window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 260))
            self.window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 320))
            self.window.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 360))

            pygame.display.flip()
            self.clock.tick(60)

    def play(self):
        player = Player()

        player_group = pygame.sprite.Group()
        player_group.add(player)

        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()

        for _ in range(6):
            enemies.add(Enemy())

        score = 0
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.can_shoot():
                        bullets.add(player.shoot())

            player_group.update()
            bullets.update()
            enemies.update()

            hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
            for bullet, enemy_list in hits.items():
                for enemy in enemy_list:
                    score += 10
                    enemy.respawn()

            player_hits = pygame.sprite.spritecollide(player, enemies, False)
            for enemy in player_hits:
                player.health -= 1
                enemy.respawn()

            if player.health <= 0:
                return self.game_over_screen(score)

            self.background.draw(self.window)
            player_group.draw(self.window)
            bullets.draw(self.window)
            enemies.draw(self.window)
            self.draw_ui(score, player.health)

            pygame.display.flip()

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_result = menu.run(self.clock)

            if menu_result == "quit":
                break

            if menu_result == "start":
                result = self.play()

                if result == "quit":
                    break

                if result == "restart":
                    continue

        pygame.quit()