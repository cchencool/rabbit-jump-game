"""游戏主循环、状态机和核心管理"""

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, GROUND_Y
from level.background import Background
from level.obstacles import ObstacleManager
from level.difficulty import DifficultyManager
from player.player import Player
from player.controller import KeyboardController, HybridController
from player.costumes import CostumeManager, COSTUMES


class GameState:
    """游戏状态枚举"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Game:
    """游戏主类"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rabbit Jump Game")
        self.clock = pygame.time.Clock()

        self.state = GameState.MENU
        self.running = True

        self.player = None
        self.player_two = None
        self.controller = None
        self.obstacle_manager = ObstacleManager()
        self.difficulty = DifficultyManager()
        self.background = Background("grass")
        self.costume_manager = CostumeManager()

        self.two_player_mode = False
        self.use_joycon = False

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 72)

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.GAME_OVER:
                        self.reset_game()

                if event.key == pygame.K_RETURN:
                    if self.state == GameState.MENU:
                        self.start_game()
                    elif self.state == GameState.GAME_OVER:
                        self.reset_game()

                if self.state == GameState.MENU:
                    if event.key == pygame.K_RIGHT:
                        self.costume_manager.cycle_next()
                    elif event.key == pygame.K_LEFT:
                        self.costume_manager.cycle_prev()
                    elif event.key == pygame.K_t:
                        self.two_player_mode = not self.two_player_mode
                    elif event.key == pygame.K_j:
                        self.use_joycon = not self.use_joycon

                if self.state == GameState.PLAYING and event.key == pygame.K_c:
                    if self.player:
                        self.costume_manager.cycle_next()
                        self.player.set_costume(self.costume_manager.get_color())

    def start_game(self):
        """开始游戏"""
        color = self.costume_manager.get_color()
        self.player = Player(x=150, color=color)

        if self.use_joycon and pygame.joystick.get_count() > 0:
            self.controller = HybridController(0)
            self.controller.connect()
            print("Using Joycon controller")
        else:
            self.controller = KeyboardController()
            print("Using keyboard controller")

        if self.two_player_mode:
            self.player_two = Player(x=280, color=(100, 100, 255))

        self.obstacle_manager.reset()
        self.difficulty.reset()
        self.background = Background("grass")
        self.state = GameState.PLAYING

    def reset_game(self):
        """重置游戏"""
        self.state = GameState.MENU
        self.player = None
        self.player_two = None
        self.obstacle_manager.reset()
        self.difficulty.reset()

    def update(self):
        """更新游戏逻辑"""
        if self.state == GameState.PLAYING:
            self.background.update(speed=2)

            if self.player:
                self.controller.update()
                if self.controller.check_jump():
                    self.player.jump()
                self.player.update()

            if self.player_two:
                if self.player.is_jumping and self.player_two.on_ground:
                    self.player_two.jump()
                self.player_two.update()

            self.difficulty.update(self.obstacle_manager.spawn_timer // 10)
            self.obstacle_manager.update(self.player.rect if self.player else None)

            if self.check_collision():
                self.state = GameState.GAME_OVER

    def check_collision(self):
        """检测玩家与障碍物的碰撞"""
        players = [p for p in [self.player, self.player_two] if p]
        for obstacle in self.obstacle_manager.obstacles:
            for player in players:
                if player.rect.colliderect(obstacle.rect):
                    return True
        return False

    def draw(self):
        """绘制游戏画面"""
        if self.state == GameState.PLAYING:
            self.background.draw(self.screen)
        else:
            self.screen.fill(WHITE)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_paused()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        """绘制菜单"""
        title = self.title_font.render("Rabbit Jump Game", True, (50, 50, 50))
        start = self.font.render("Press ENTER to Start", True, (80, 80, 80))

        costume_name = COSTUMES[self.costume_manager.current]["name"]
        costume_info = self.small_font.render(f"Costume: {costume_name} (LEFT/RIGHT to change)", True, (100, 100, 100))

        two_player_info = self.small_font.render(f"2P Mode: {'ON' if self.two_player_mode else 'OFF'} (Press T to toggle)", True, (100, 100, 100))

        joycon_mode_info = self.small_font.render(f"Joycon Mode: {'ON' if self.use_joycon else 'OFF'} (Press J to toggle)", True, (100, 100, 100))

        controls = self.small_font.render("Controls: SPACE/Up/W to jump, C to change costume", True, (120, 120, 120))
        joycon_status = self.small_font.render(f"Joycon: {'Ready (Press J to toggle)' if pygame.joystick.get_count() > 0 else 'Not detected'}", True, (130, 130, 130))

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))
        self.screen.blit(costume_info, (SCREEN_WIDTH // 2 - costume_info.get_width() // 2, 250))
        self.screen.blit(two_player_info, (SCREEN_WIDTH // 2 - two_player_info.get_width() // 2, 310))
        self.screen.blit(joycon_mode_info, (SCREEN_WIDTH // 2 - joycon_mode_info.get_width() // 2, 360))
        self.screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, 430))
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 520))
        self.screen.blit(joycon_status, (SCREEN_WIDTH // 2 - joycon_status.get_width() // 2, 570))

        preview_x = SCREEN_WIDTH // 2 - 32
        preview_y = 620
        preview_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        from player.player import draw_rabbit
        draw_rabbit(
            preview_surface,
            0, 0,
            64, 64,
            self.costume_manager.get_color(),
            0, False, False,
        )
        self.screen.blit(preview_surface, (preview_x, preview_y))

    def draw_game(self):
        """绘制游戏画面"""
        self.obstacle_manager.draw(self.screen)

        if self.player:
            self.player.draw(self.screen)
        if self.player_two:
            self.player_two.draw(self.screen)

        self.draw_ui()

    def draw_ui(self):
        """绘制游戏 UI"""
        score_text = self.font.render(f"Score: {self.difficulty.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (20, 20))

        level_text = self.small_font.render(f"Level: {self.difficulty.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (20, 70))

        if self.player_two:
            p2_text = self.small_font.render("2P", True, (100, 100, 255))
            self.screen.blit(p2_text, (SCREEN_WIDTH - 60, 20))

    def draw_paused(self):
        """绘制暂停画面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        paused = self.font.render("PAUSED", True, (255, 255, 255))
        hint = self.small_font.render("Press ESC to resume", True, (200, 200, 200))
        self.screen.blit(paused, (SCREEN_WIDTH // 2 - paused.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

    def draw_game_over(self):
        """绘制游戏结束画面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        game_over = self.font.render("GAME OVER", True, (255, 255, 255))
        score = self.small_font.render(f"Final Score: {self.difficulty.score}", True, (200, 200, 200))
        restart = self.small_font.render("Press ENTER to Restart", True, (200, 200, 200))

        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    def run(self):
        """游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
