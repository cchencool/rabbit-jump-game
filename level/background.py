"""多主题背景和视差滚动"""

import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUNDS, GRASS_GREEN


class Background:
    """背景类 - 支持多主题"""

    def __init__(self, theme="grass"):
        self.theme = theme
        self.color = BACKGROUNDS.get(theme, GRASS_GREEN)

        self.scroll_offset = 0
        self.clouds = self._generate_clouds()
        self.hills = self._generate_hills()
        self.flowers = self._generate_flowers()
        self.birds = self._generate_birds()
        self.stars = self._generate_stars()

    def _generate_clouds(self):
        """生成云朵"""
        clouds = []
        for i in range(8):
            x = random.randint(0, SCREEN_WIDTH * 2)
            y = random.randint(30, 200)
            size = random.randint(60, 120)
            clouds.append({"x": x, "y": y, "size": size, "speed": random.uniform(0.3, 0.7)})
        return clouds

    def _generate_hills(self):
        """生成山丘"""
        hills = []
        for i in range(5):
            x = i * 350
            hills.append({"x": x, "height": random.randint(80, 150), "width": random.randint(250, 400)})
        return hills

    def _generate_flowers(self):
        """生成花朵装饰"""
        flowers = []
        for i in range(15):
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT - 120 + random.randint(-10, 10)
            color = random.choice([(255, 100, 100), (255, 200, 100), (255, 150, 200), (200, 100, 255)])
            flowers.append({"x": x, "y": y, "color": color, "size": random.randint(4, 8)})
        return flowers

    def _generate_birds(self):
        """生成飞鸟"""
        birds = []
        for i in range(3):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(50, 150)
            birds.append({"x": x, "y": y, "wing_up": True, "timer": 0})
        return birds

    def _generate_stars(self):
        """生成星星装饰（用于特殊主题）"""
        stars = []
        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(20, 300)
            stars.append({"x": x, "y": y, "twinkle": random.randint(0, 100)})
        return stars

    def update(self, speed=1):
        """更新背景滚动"""
        self.scroll_offset -= speed
        if self.scroll_offset <= -SCREEN_WIDTH:
            self.scroll_offset = 0

        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"]
            if cloud["x"] < -cloud["size"]:
                cloud["x"] = SCREEN_WIDTH + cloud["size"]
                cloud["y"] = random.randint(30, 200)

        for hill in self.hills:
            hill["x"] -= speed * 0.3
            if hill["x"] < -hill["width"]:
                hill["x"] = SCREEN_WIDTH + random.randint(50, 200)

        for flower in self.flowers:
            flower["x"] -= speed * 0.8
            if flower["x"] < -20:
                flower["x"] = SCREEN_WIDTH + random.randint(10, 100)
                flower["y"] = SCREEN_HEIGHT - 120 + random.randint(-10, 10)

        for bird in self.birds:
            bird["x"] -= speed * 1.2
            bird["timer"] += 1
            if bird["timer"] % 20 == 0:
                bird["wing_up"] = not bird["wing_up"]
            if bird["x"] < -50:
                bird["x"] = SCREEN_WIDTH + 50
                bird["y"] = random.randint(50, 150)

        for star in self.stars:
            star["twinkle"] = (star["twinkle"] + 1) % 100

    def draw(self, screen):
        """绘制背景"""
        screen.fill(self.color)

        self._draw_sky_details(screen)

        for star in self.stars:
            alpha = 150 + 100 * (star["twinkle"] / 100)
            star_color = (int(255 * alpha / 255), int(255 * alpha / 255), int(200 * alpha / 255))
            pygame.draw.circle(screen, star_color, (int(star["x"]), int(star["y"])), 2)

        for hill in self.hills:
            pygame.draw.polygon(
                screen,
                self._get_hill_color(),
                [
                    (hill["x"], SCREEN_HEIGHT - 120),
                    (hill["x"] + hill["width"] // 2, SCREEN_HEIGHT - 120 - hill["height"]),
                    (hill["x"] + hill["width"], SCREEN_HEIGHT - 120)
                ]
            )

        for cloud in self.clouds:
            self._draw_cloud(screen, cloud)

        for bird in self.birds:
            self._draw_bird(screen, bird)

        self._draw_ground(screen)

        for flower in self.flowers:
            self._draw_flower(screen, flower)

    def _draw_cloud(self, screen, cloud):
        """绘制云朵"""
        x, y, size = int(cloud["x"]), int(cloud["y"]), cloud["size"]
        pygame.draw.ellipse(screen, (255, 255, 255), (x, y, size, size // 2))
        pygame.draw.ellipse(screen, (255, 255, 255), (x + size // 4, y - size // 6, size // 2, size // 3))
        pygame.draw.ellipse(screen, (255, 255, 255), (x - size // 4, y + size // 8, size // 2, size // 3))

    def _draw_bird(self, screen, bird):
        """绘制飞鸟"""
        x, y = int(bird["x"]), int(bird["y"])
        if bird["wing_up"]:
            pygame.draw.lines(screen, (50, 50, 50), False, [(x - 10, y + 5), (x, y), (x + 10, y + 5)], 2)
        else:
            pygame.draw.lines(screen, (50, 50, 50), False, [(x - 10, y - 5), (x, y), (x + 10, y - 5)], 2)

    def _draw_flower(self, screen, flower):
        """绘制花朵"""
        x, y = int(flower["x"]), int(flower["y"])
        size = flower["size"]
        color = flower["color"]

        pygame.draw.line(screen, (100, 150, 50), (x, y), (x, y + 15), 2)

        for angle in range(0, 360, 60):
            px = x + int(size * math.cos(math.radians(angle)))
            py = y + int(size * math.sin(math.radians(angle)))
            pygame.draw.circle(screen, color, (px, py), size // 2)

        pygame.draw.circle(screen, (255, 255, 100), (x, y), size // 3)

    def _draw_sky_details(self, screen):
        """绘制天空细节（太阳/月亮）"""
        if self.theme == "grass":
            pygame.draw.circle(screen, (255, 220, 100), (SCREEN_WIDTH - 100, 80), 40)
            for i in range(8):
                angle = math.radians(i * 45)
                x1 = SCREEN_WIDTH - 100 + int(50 * math.cos(angle))
                y1 = 80 + int(50 * math.sin(angle))
                x2 = SCREEN_WIDTH - 100 + int(65 * math.cos(angle))
                y2 = 80 + int(65 * math.sin(angle))
                pygame.draw.line(screen, (255, 200, 50), (x1, y1), (x2, y2), 3)
        elif self.theme == "ocean":
            pygame.draw.circle(screen, (200, 220, 255), (SCREEN_WIDTH - 100, 80), 35)
            pygame.draw.circle(screen, (180, 200, 230), (SCREEN_WIDTH - 90, 75), 30)

    def _draw_ground(self, screen):
        """绘制地面"""
        ground_y = SCREEN_HEIGHT - 120

        pygame.draw.rect(screen, (139, 90, 43), (0, ground_y, SCREEN_WIDTH, 120))

        grass_color = (101, 167, 58)
        pygame.draw.rect(screen, grass_color, (0, ground_y, SCREEN_WIDTH, 20))

        for i in range(0, SCREEN_WIDTH, 15):
            offset = (self.scroll_offset * 0.8) % 15
            grass_x = i + offset
            pygame.draw.line(screen, (80, 140, 40), (grass_x, ground_y), (grass_x, ground_y - 10), 2)

    def _get_hill_color(self):
        """获取山丘颜色"""
        colors = {
            "grass": (76, 153, 76),
            "ocean": (100, 180, 150),
            "ice": (180, 210, 230),
            "city": (90, 90, 100)
        }
        return colors.get(self.theme, (76, 153, 76))

    def set_theme(self, theme):
        """设置背景主题"""
        self.theme = theme
        self.color = BACKGROUNDS.get(theme, GRASS_GREEN)
