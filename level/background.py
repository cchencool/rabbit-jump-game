# 背景管理
"""多主题背景和视差滚动"""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUNDS, GRASS_GREEN


class Background:
    """背景类 - 支持多主题"""

    def __init__(self, theme="grass"):
        self.theme = theme
        self.color = BACKGROUNDS.get(theme, GRASS_GREEN)

        # 视差滚动元素
        self.scroll_offset = 0
        self.clouds = self._generate_clouds()
        self.hills = self._generate_hills()

    def _generate_clouds(self):
        """生成云朵"""
        clouds = []
        for i in range(5):
            x = i * 200
            y = 50 + (i % 3) * 30
            clouds.append({"x": x, "y": y})
        return clouds

    def _generate_hills(self):
        """生成山丘"""
        hills = []
        for i in range(3):
            x = i * 300
            hills.append({"x": x, "height": 100 + i * 20})
        return hills

    def update(self, speed=1):
        """更新背景滚动"""
        self.scroll_offset -= speed
        if self.scroll_offset <= -SCREEN_WIDTH:
            self.scroll_offset = 0

        # 更新云朵
        for cloud in self.clouds:
            cloud["x"] -= speed * 0.5
            if cloud["x"] < -100:
                cloud["x"] = SCREEN_WIDTH + 100

        # 更新山丘
        for hill in self.hills:
            hill["x"] -= speed * 0.3
            if hill["x"] < -300:
                hill["x"] = SCREEN_WIDTH

    def draw(self, screen):
        """绘制背景"""
        # 填充背景色
        screen.fill(self.color)

        # 绘制云朵
        for cloud in self.clouds:
            pygame.draw.ellipse(
                screen,
                (255, 255, 255),
                (cloud["x"], cloud["y"], 80, 40)
            )

        # 绘制山丘
        for hill in self.hills:
            pygame.draw.polygon(
                screen,
                self._get_hill_color(),
                [
                    (hill["x"], SCREEN_HEIGHT - 80),
                    (hill["x"] + 150, SCREEN_HEIGHT - 80 - hill["height"]),
                    (hill["x"] + 300, SCREEN_HEIGHT - 80)
                ]
            )

        # 绘制地面
        pygame.draw.rect(
            screen,
            (101, 67, 33),
            (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        )

    def _get_hill_color(self):
        """获取山丘颜色"""
        colors = {
            "grass": (76, 153, 76),
            "ocean": (255, 255, 200),
            "ice": (200, 230, 255),
            "city": (100, 100, 100)
        }
        return colors.get(self.theme, (76, 153, 76))

    def set_theme(self, theme):
        """设置背景主题"""
        self.theme = theme
        self.color = BACKGROUNDS.get(theme, GRASS_GREEN)
