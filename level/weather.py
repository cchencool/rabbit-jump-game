"""天气系统 - 随机天气变化"""

import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class WeatherType:
    """天气类型"""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    OVERCAST = "overcast"
    FOGGY = "foggy"
    RAINY = "rainy"
    SNOWY = "snowy"
    PETAL = "petal"


class WeatherSystem:
    """天气系统"""

    def __init__(self):
        self.current_weather = WeatherType.SUNNY
        self.timer = 0
        self.duration = random.randint(1800, 3600)
        self.particles = []
        self._init_particles()

    def _init_particles(self):
        """初始化粒子"""
        self.particles = []
        if self.current_weather == WeatherType.RAINY:
            for _ in range(100):
                self.particles.append({
                    "x": random.randint(0, SCREEN_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT),
                    "speed": random.randint(8, 15),
                    "length": random.randint(10, 20),
                })
        elif self.current_weather == WeatherType.SNOWY:
            for _ in range(60):
                self.particles.append({
                    "x": random.randint(0, SCREEN_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT),
                    "speed": random.uniform(1, 3),
                    "size": random.randint(2, 5),
                    "drift": random.uniform(-0.5, 0.5),
                })
        elif self.current_weather == WeatherType.PETAL:
            for _ in range(40):
                self.particles.append({
                    "x": random.randint(0, SCREEN_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT),
                    "speed": random.uniform(1, 2),
                    "size": random.randint(4, 8),
                    "drift": random.uniform(-1, 1),
                    "rotation": random.randint(0, 360),
                    "color": random.choice([(255, 180, 200), (255, 150, 180), (255, 200, 220)]),
                })

    def update(self):
        """更新天气"""
        self.timer += 1
        if self.timer >= self.duration:
            self.timer = 0
            self.switch_weather()

        self._update_particles()

    def switch_weather(self):
        """随机切换天气"""
        self.current_weather = random.choice([
            WeatherType.SUNNY,
            WeatherType.CLOUDY,
            WeatherType.OVERCAST,
            WeatherType.FOGGY,
            WeatherType.RAINY,
            WeatherType.SNOWY,
            WeatherType.PETAL,
        ])
        self.duration = random.randint(1800, 3600)
        self._init_particles()

    def _update_particles(self):
        """更新粒子位置"""
        if self.current_weather == WeatherType.RAINY:
            for p in self.particles:
                p["y"] += p["speed"]
                p["x"] -= 2
                if p["y"] > SCREEN_HEIGHT:
                    p["y"] = -p["length"]
                    p["x"] = random.randint(0, SCREEN_WIDTH)
        elif self.current_weather == WeatherType.SNOWY:
            for p in self.particles:
                p["y"] += p["speed"]
                p["x"] += p["drift"] + math.sin(p["y"] * 0.02) * 0.5
                if p["y"] > SCREEN_HEIGHT:
                    p["y"] = -p["size"]
                    p["x"] = random.randint(0, SCREEN_WIDTH)
        elif self.current_weather == WeatherType.PETAL:
            for p in self.particles:
                p["y"] += p["speed"]
                p["x"] += p["drift"] + math.sin(p["y"] * 0.01) * 1
                p["rotation"] += 2
                if p["y"] > SCREEN_HEIGHT:
                    p["y"] = -p["size"]
                    p["x"] = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        """绘制天气效果"""
        if self.current_weather == WeatherType.SUNNY:
            self._draw_sunny(screen)
        elif self.current_weather == WeatherType.CLOUDY:
            self._draw_cloudy(screen)
        elif self.current_weather == WeatherType.OVERCAST:
            self._draw_overcast(screen)
        elif self.current_weather == WeatherType.FOGGY:
            self._draw_foggy(screen)
        elif self.current_weather == WeatherType.RAINY:
            self._draw_rainy(screen)
        elif self.current_weather == WeatherType.SNOWY:
            self._draw_snowy(screen)
        elif self.current_weather == WeatherType.PETAL:
            self._draw_petal(screen)

    def _draw_sunny(self, screen):
        """晴天 - 明亮阳光"""
        pass

    def _draw_cloudy(self, screen):
        """多云 - 轻微变暗"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(30)
        screen.blit(overlay, (0, 0))

    def _draw_overcast(self, screen):
        """阴天 - 明显变暗"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(60)
        screen.blit(overlay, (0, 0))

    def _draw_foggy(self, screen):
        """大雾 - 白色雾效"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((200, 200, 200))
        overlay.set_alpha(100)
        screen.blit(overlay, (0, 0))

    def _draw_rainy(self, screen):
        """雨天"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(50)
        screen.blit(overlay, (0, 0))

        for p in self.particles:
            pygame.draw.line(screen, (150, 180, 220), (p["x"], p["y"]), (p["x"] - 2, p["y"] + p["length"]), 2)

    def _draw_snowy(self, screen):
        """下雪"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(40)
        screen.blit(overlay, (0, 0))

        for p in self.particles:
            pygame.draw.circle(screen, (255, 255, 255), (int(p["x"]), int(p["y"])), p["size"])

    def _draw_petal(self, screen):
        """飘花瓣"""
        for p in self.particles:
            petal_surface = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(petal_surface, p["color"], (0, 0, p["size"] * 2, p["size"]))
            rotated = pygame.transform.rotate(petal_surface, p["rotation"])
            new_rect = rotated.get_rect(center=(p["x"], p["y"]))
            screen.blit(rotated, new_rect)
