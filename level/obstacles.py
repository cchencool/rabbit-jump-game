"""障碍物生成和管理"""

import pygame
import random
from settings import SCREEN_WIDTH, GROUND_Y


class Obstacle(pygame.sprite.Sprite):
    """障碍物基类"""

    def __init__(self, x=None, width=30, height=40, speed=4, obstacle_type="rock"):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.obstacle_type = obstacle_type
        self._draw_obstacle(width, height)
        self.rect = self.image.get_rect()

        self.rect.x = x if x is not None else SCREEN_WIDTH
        self.rect.y = GROUND_Y - height

        self.hitbox = pygame.Rect(self.rect.x + 4, self.rect.y + 4, width - 8, height - 4)

        self.speed = speed

    def _draw_obstacle(self, width, height):
        """绘制障碍物"""
        self.image.fill((0, 0, 0, 0))

        if self.obstacle_type == "rock":
            self._draw_rock(width, height)
        elif self.obstacle_type == "cactus":
            self._draw_cactus(width, height)
        elif self.obstacle_type == "box":
            self._draw_box(width, height)
        elif self.obstacle_type == "barrel":
            self._draw_barrel(width, height)
        else:
            self._draw_rock(width, height)

    def _draw_rock(self, width, height):
        """绘制石头"""
        points = [
            (width // 2, 0),
            (width, height // 3),
            (width - 5, height),
            (5, height),
            (0, height // 3),
        ]
        pygame.draw.polygon(self.image, (120, 120, 120), points)
        pygame.draw.polygon(self.image, (140, 140, 140), [(width // 2, 5), (width - 10, height // 3), (width // 2 + 5, height - 10), (10, height - 10), (5, height // 3)])

    def _draw_cactus(self, width, height):
        """绘制仙人掌"""
        pygame.draw.rect(self.image, (34, 120, 34), (width // 2 - 8, 0, 16, height), border_radius=8)
        pygame.draw.rect(self.image, (34, 120, 34), (0, height // 4, width // 3, 8), border_radius=4)
        pygame.draw.rect(self.image, (34, 120, 34), (0, height // 4, 8, height // 3), border_radius=4)
        pygame.draw.rect(self.image, (34, 120, 34), (width - width // 3, height // 3, width // 3, 8), border_radius=4)
        pygame.draw.rect(self.image, (34, 120, 34), (width - 8, height // 3, 8, height // 4), border_radius=4)

    def _draw_box(self, width, height):
        """绘制木箱"""
        pygame.draw.rect(self.image, (160, 120, 60), (0, 0, width, height), border_radius=4)
        pygame.draw.rect(self.image, (140, 100, 40), (2, 2, width - 4, height - 4), border_radius=3)
        pygame.draw.line(self.image, (120, 80, 30), (0, 0), (width, height), 3)
        pygame.draw.line(self.image, (120, 80, 30), (width, 0), (0, height), 3)

    def _draw_barrel(self, width, height):
        """绘制木桶"""
        pygame.draw.ellipse(self.image, (140, 90, 40), (0, 0, width, height))
        pygame.draw.ellipse(self.image, (120, 70, 30), (3, 3, width - 6, height - 6))
        pygame.draw.line(self.image, (100, 60, 20), (0, height // 3), (width, height // 3), 3)
        pygame.draw.line(self.image, (100, 60, 20), (0, height * 2 // 3), (width, height * 2 // 3), 3)

    def update(self):
        """更新障碍物位置"""
        self.rect.x -= self.speed
        self.hitbox.x = self.rect.x + 4
        self.hitbox.y = self.rect.y + 4

    def draw(self, screen):
        """绘制障碍物"""
        screen.blit(self.image, self.rect)


class Heart:
    """爱心血包"""

    def __init__(self, x=None, y=None, speed=3):
        self.size = 24
        self.rect = pygame.Rect(x if x is not None else SCREEN_WIDTH, y if y is not None else GROUND_Y - 150, self.size, self.size)
        self.hitbox = pygame.Rect(self.rect.x + 4, self.rect.y + 4, self.size - 8, self.size - 8)
        self.speed = speed
        self.bob_offset = 0
        self.bob_timer = 0

    def update(self):
        """更新位置"""
        self.rect.x -= self.speed
        self.hitbox.x = self.rect.x + 4
        self.hitbox.y = self.rect.y + 4

        self.bob_timer += 1
        self.bob_offset = int(pygame.math.Vector2(0, 1).rotate(self.bob_timer * 6).y * 5)

    def draw(self, screen):
        """绘制爱心"""
        cx = self.rect.x + self.size // 2
        cy = self.rect.y + self.size // 2 + self.bob_offset

        pygame.draw.circle(screen, (255, 80, 80), (cx - 6, cy - 4), 7)
        pygame.draw.circle(screen, (255, 80, 80), (cx + 6, cy - 4), 7)
        pygame.draw.polygon(screen, (255, 80, 80), [
            (cx - 12, cy - 2),
            (cx, cy + 12),
            (cx + 12, cy - 2),
        ])

        pygame.draw.circle(screen, (255, 150, 150), (cx - 6, cy - 5), 3)
        pygame.draw.circle(screen, (255, 150, 150), (cx + 6, cy - 5), 3)


class Apple:
    """小苹果 - 拾取加分"""

    def __init__(self, x=None, y=None, speed=3):
        self.size = 20
        self.rect = pygame.Rect(x if x is not None else SCREEN_WIDTH, y if y is not None else GROUND_Y - 150, self.size, self.size)
        self.hitbox = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.size - 4, self.size - 4)
        self.speed = speed
        self.bob_offset = 0
        self.bob_timer = 0

    def update(self):
        """更新位置"""
        self.rect.x -= self.speed
        self.hitbox.x = self.rect.x + 2
        self.hitbox.y = self.rect.y + 2

        self.bob_timer += 1
        self.bob_offset = int(pygame.math.Vector2(0, 1).rotate(self.bob_timer * 8).y * 4)

    def draw(self, screen):
        """绘制苹果"""
        cx = self.rect.x + self.size // 2
        cy = self.rect.y + self.size // 2 + self.bob_offset

        pygame.draw.circle(screen, (220, 50, 50), (cx, cy), 8)
        pygame.draw.circle(screen, (255, 80, 80), (cx - 2, cy - 2), 3)
        pygame.draw.line(screen, (50, 120, 50), (cx, cy - 8), (cx + 2, cy - 12), 2)


class Coin:
    """小金币 - 拾取后10秒无敌"""

    def __init__(self, x=None, y=None, speed=3):
        self.size = 22
        self.rect = pygame.Rect(x if x is not None else SCREEN_WIDTH, y if y is not None else GROUND_Y - 150, self.size, self.size)
        self.hitbox = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.size - 4, self.size - 4)
        self.speed = speed
        self.bob_offset = 0
        self.bob_timer = 0
        self.spin_angle = 0

    def update(self):
        """更新位置"""
        self.rect.x -= self.speed
        self.hitbox.x = self.rect.x + 2
        self.hitbox.y = self.rect.y + 2

        self.bob_timer += 1
        self.bob_offset = int(pygame.math.Vector2(0, 1).rotate(self.bob_timer * 6).y * 5)
        self.spin_angle += 3

    def draw(self, screen):
        """绘制金币"""
        cx = self.rect.x + self.size // 2
        cy = self.rect.y + self.size // 2 + self.bob_offset

        spin_scale = abs(pygame.math.Vector2(1, 0).rotate(self.spin_angle).x)
        width = max(4, int(10 * spin_scale))

        pygame.draw.ellipse(screen, (255, 215, 0), (cx - width, cy - 9, width * 2, 18))
        pygame.draw.ellipse(screen, (255, 240, 100), (cx - width + 2, cy - 7, width * 2 - 4, 14))


class ObstacleManager:
    """障碍物管理器"""

    def __init__(self):
        self.obstacles = []
        self.hearts = []
        self.apples = []
        self.coins = []
        self.spawn_timer = 0
        self.spawn_interval = 120
        self.heart_timer = 0
        self.heart_interval = 600
        self.apple_timer = 0
        self.apple_interval = 180
        self.coin_timer = 0
        self.coin_interval = 900
        self.speed = 4
        self.obstacle_types = ["rock", "cactus", "box", "barrel"]

    def update(self, player_rect):
        """更新所有障碍物"""
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_obstacle()

    def update_hearts(self):
        """更新所有爱心"""
        self.heart_timer += 1
        if self.heart_timer >= self.heart_interval:
            self.heart_timer = 0
            self.spawn_heart()

        for heart in self.hearts[:]:
            heart.update()
            if heart.rect.right < 0:
                self.hearts.remove(heart)

    def spawn_heart(self):
        """生成爱心血包"""
        y = random.randint(GROUND_Y - 250, GROUND_Y - 120)
        heart = Heart(y=y, speed=self.speed * 0.8)
        self.hearts.append(heart)

    def update_apples(self):
        """更新所有苹果"""
        self.apple_timer += 1
        if self.apple_timer >= self.apple_interval:
            self.apple_timer = 0
            self.spawn_apple()

        for apple in self.apples[:]:
            apple.update()
            if apple.rect.right < 0:
                self.apples.remove(apple)

    def spawn_apple(self):
        """生成小苹果"""
        y = random.randint(GROUND_Y - 250, GROUND_Y - 100)
        apple = Apple(y=y, speed=self.speed * 0.8)
        self.apples.append(apple)

    def update_coins(self):
        """更新所有金币"""
        self.coin_timer += 1
        if self.coin_timer >= self.coin_interval:
            self.coin_timer = 0
            self.spawn_coin()

        for coin in self.coins[:]:
            coin.update()
            if coin.rect.right < 0:
                self.coins.remove(coin)

    def spawn_coin(self):
        """生成小金币"""
        y = random.randint(GROUND_Y - 250, GROUND_Y - 120)
        coin = Coin(y=y, speed=self.speed * 0.8)
        self.coins.append(coin)

    def spawn_obstacle(self):
        """生成新障碍物"""
        height = random.randint(40, 80)
        width = random.randint(30, 50)
        obstacle_type = random.choice(self.obstacle_types)
        obstacle = Obstacle(width=width, height=height, speed=self.speed, obstacle_type=obstacle_type)
        self.obstacles.append(obstacle)

    def increase_speed(self, increment=0.5):
        """增加障碍物速度"""
        self.speed += increment
        for obstacle in self.obstacles:
            obstacle.speed = self.speed

    def reset(self):
        """重置管理器"""
        self.obstacles = []
        self.hearts = []
        self.apples = []
        self.coins = []
        self.spawn_timer = 0
        self.heart_timer = 0
        self.apple_timer = 0
        self.coin_timer = 0
        self.speed = 4

    def draw(self, screen):
        """绘制所有障碍物和道具"""
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for heart in self.hearts:
            heart.draw(screen)
        for apple in self.apples:
            apple.draw(screen)
        for coin in self.coins:
            coin.draw(screen)
