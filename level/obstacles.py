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

    def draw(self, screen):
        """绘制障碍物"""
        screen.blit(self.image, self.rect)


class ObstacleManager:
    """障碍物管理器"""

    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_interval = 120
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
        self.spawn_timer = 0
        self.speed = 4

    def draw(self, screen):
        """绘制所有障碍物"""
        for obstacle in self.obstacles:
            obstacle.draw(screen)
