# 障碍物类
"""障碍物生成和管理"""

import pygame
import random
from settings import SCREEN_WIDTH, GROUND_Y


class Obstacle(pygame.sprite.Sprite):
    """障碍物基类"""

    def __init__(self, x=None, width=30, height=40, speed=4, color=(139, 69, 19)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # 如果没有指定 X 位置，从屏幕右侧生成
        self.rect.x = x if x is not None else SCREEN_WIDTH
        self.rect.y = GROUND_Y - height

        self.speed = speed

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
        self.spawn_interval = 120  # 帧数，约 2 秒
        self.speed = 4

    def update(self, player_rect):
        """更新所有障碍物"""
        # 更新现有障碍物
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)

        # 生成新障碍物
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_obstacle()

    def spawn_obstacle(self):
        """生成新障碍物"""
        # 随机高度和宽度
        height = random.randint(30, 60)
        width = random.randint(20, 40)
        obstacle = Obstacle(width=width, height=height, speed=self.speed)
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
