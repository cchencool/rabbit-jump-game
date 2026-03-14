# 玩家角色类
"""兔子角色、物理和动画"""

import pygame
from settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_GRAVITY,
    PLAYER_JUMP_FORCE,
    PLAYER_SPEED,
    GROUND_Y,
)


class Player(pygame.sprite.Sprite):
    """玩家角色类 - 兔子"""

    def __init__(self, x=100, color=(255, 100, 100)):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_Y - PLAYER_HEIGHT

        # 物理属性
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = True

        # 动画
        self.frame = 0
        self.animation_timer = 0

    def jump(self):
        """跳跃"""
        if self.on_ground:
            self.velocity_y = PLAYER_JUMP_FORCE
            self.is_jumping = True
            self.on_ground = False

    def update(self):
        """更新玩家状态"""
        # 应用重力
        self.velocity_y += PLAYER_GRAVITY
        self.rect.y += self.velocity_y

        # 地面检测
        if self.rect.y >= GROUND_Y - PLAYER_HEIGHT:
            self.rect.y = GROUND_Y - PLAYER_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False
            self.on_ground = True

    def draw(self, screen):
        """绘制玩家"""
        screen.blit(self.image, self.rect)

    def set_costume(self, color):
        """更换服装颜色"""
        self.image.fill(color)


class PlayerTwo(Player):
    """第二个玩家角色"""

    def __init__(self, x=200, color=(100, 100, 255)):
        super().__init__(x, color)
