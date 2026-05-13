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
        self.previous_weather = None
        self.timer = 0
        self.duration = random.randint(1200, 2400)
        self.particles = []
        self.fog_particles = []
        self.cloud_particles = []
        self.transition_alpha = 255
        self.is_transitioning = False
        self.transition_timer = 0
        self.transition_duration = 60
        self._init_particles()
        self._init_fog_particles()
        self._init_cloud_particles()

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

    def _init_fog_particles(self):
        """初始化雾气粒子"""
        self.fog_particles = []
        for _ in range(15):
            self.fog_particles.append({
                "x": random.randint(-200, SCREEN_WIDTH + 200),
                "y": random.randint(0, SCREEN_HEIGHT),
                "size": random.randint(150, 300),
                "speed": random.uniform(0.3, 1.0),
                "alpha": random.randint(30, 80),
            })

    def _init_cloud_particles(self):
        """初始化云层粒子"""
        self.cloud_particles = []
        for _ in range(20):
            self.cloud_particles.append({
                "x": random.randint(-300, SCREEN_WIDTH + 300),
                "y": random.randint(20, 250),
                "width": random.randint(200, 400),
                "height": random.randint(60, 120),
                "speed": random.uniform(0.2, 0.8),
                "alpha": random.randint(150, 220),
                "layer": random.randint(0, 2),
            })

    def update(self):
        """更新天气"""
        self.timer += 1
        if self.timer >= self.duration:
            self.timer = 0
            self.switch_weather()

        self._update_particles()
        self._update_fog_particles()
        self._update_cloud_particles()
        self._update_transition()

    def _update_transition(self):
        """更新过渡效果"""
        if self.is_transitioning:
            self.transition_timer += 1
            progress = self.transition_timer / self.transition_duration
            if progress < 0.5:
                self.transition_alpha = int(255 * (progress * 2))
            else:
                self.transition_alpha = int(255 * (1 - (progress - 0.5) * 2))
            if self.transition_timer >= self.transition_duration:
                self.is_transitioning = False
                self.transition_alpha = 255

    def switch_weather(self):
        """随机切换天气"""
        self.previous_weather = self.current_weather
        self.current_weather = random.choice([
            WeatherType.SUNNY,
            WeatherType.CLOUDY,
            WeatherType.OVERCAST,
            WeatherType.FOGGY,
            WeatherType.RAINY,
            WeatherType.SNOWY,
            WeatherType.PETAL,
        ])
        self.duration = random.randint(1200, 2400)
        self._init_particles()
        self.is_transitioning = True
        self.transition_timer = 0

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

    def _update_fog_particles(self):
        """更新雾气粒子"""
        for fog in self.fog_particles:
            fog["x"] += fog["speed"]
            if fog["x"] > SCREEN_WIDTH + fog["size"]:
                fog["x"] = -fog["size"]
                fog["y"] = random.randint(0, SCREEN_HEIGHT)

    def _update_cloud_particles(self):
        """更新云层粒子"""
        for cloud in self.cloud_particles:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > SCREEN_WIDTH + cloud["width"]:
                cloud["x"] = -cloud["width"]
                cloud["y"] = random.randint(20, 250)

    def draw(self, screen):
        """绘制天气效果"""
        if self.is_transitioning:
            if self.previous_weather:
                self._draw_weather_effect(screen, self.previous_weather, 255 - self.transition_alpha)
            self._draw_weather_effect(screen, self.current_weather, self.transition_alpha)
        else:
            self._draw_weather_effect(screen, self.current_weather, 255)

    def _draw_weather_effect(self, screen, weather, alpha):
        """绘制特定天气效果"""
        if weather == WeatherType.SUNNY:
            self._draw_sunny(screen, alpha)
        elif weather == WeatherType.CLOUDY:
            self._draw_cloudy(screen, alpha)
        elif weather == WeatherType.OVERCAST:
            self._draw_overcast(screen, alpha)
        elif weather == WeatherType.FOGGY:
            self._draw_foggy(screen, alpha)
        elif weather == WeatherType.RAINY:
            self._draw_rainy(screen, alpha)
        elif weather == WeatherType.SNOWY:
            self._draw_snowy(screen, alpha)
        elif weather == WeatherType.PETAL:
            self._draw_petal(screen, alpha)

    def _draw_sunny(self, screen, alpha=255):
        """晴天 - 明亮阳光"""
        pass

    def _draw_cloudy(self, screen, alpha=255):
        """多云 - 轻微变暗"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(30 * alpha / 255))
        screen.blit(overlay, (0, 0))

    def _draw_overcast(self, screen, alpha=255):
        """阴天 - 浓云蔽日，多层厚云遮挡阳光"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(80 * alpha / 255))
        screen.blit(overlay, (0, 0))

        for cloud in sorted(self.cloud_particles, key=lambda c: c["layer"]):
            cloud_alpha = int(cloud["alpha"] * alpha / 255)
            cloud_surface = pygame.Surface((cloud["width"], cloud["height"]), pygame.SRCALPHA)
            cx, cy = cloud["width"] // 2, cloud["height"] // 2
            pygame.draw.ellipse(cloud_surface, (100, 100, 110, cloud_alpha), (0, 0, cloud["width"], cloud["height"]))
            pygame.draw.ellipse(cloud_surface, (120, 120, 130, cloud_alpha), (cloud["width"] // 4, -cloud["height"] // 3, cloud["width"] // 2, cloud["height"] // 2))
            pygame.draw.ellipse(cloud_surface, (90, 90, 100, cloud_alpha), (cloud["width"] // 3, cloud["height"] // 4, cloud["width"] // 3, cloud["height"] // 2))
            screen.blit(cloud_surface, (cloud["x"], cloud["y"]))

    def _draw_foggy(self, screen, alpha=255):
        """大雾 - 动态雾气效果"""
        for fog in self.fog_particles:
            fog_alpha = int(fog["alpha"] * alpha / 255)
            fog_surface = pygame.Surface((fog["size"], fog["size"]), pygame.SRCALPHA)
            pygame.draw.circle(fog_surface, (220, 220, 220, fog_alpha), (fog["size"] // 2, fog["size"] // 2), fog["size"] // 2)
            screen.blit(fog_surface, (fog["x"] - fog["size"] // 2, fog["y"] - fog["size"] // 2))

    def _draw_rainy(self, screen, alpha=255):
        """雨天"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(50 * alpha / 255))
        screen.blit(overlay, (0, 0))

        for p in self.particles:
            pygame.draw.line(screen, (150, 180, 220), (p["x"], p["y"]), (p["x"] - 2, p["y"] + p["length"]), 2)

    def _draw_snowy(self, screen, alpha=255):
        """下雪"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(40 * alpha / 255))
        screen.blit(overlay, (0, 0))

        for p in self.particles:
            pygame.draw.circle(screen, (255, 255, 255), (int(p["x"]), int(p["y"])), p["size"])

    def _draw_petal(self, screen, alpha=255):
        """飘花瓣"""
        for p in self.particles:
            petal_surface = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(petal_surface, p["color"], (0, 0, p["size"] * 2, p["size"]))
            rotated = pygame.transform.rotate(petal_surface, p["rotation"])
            new_rect = rotated.get_rect(center=(p["x"], p["y"]))
            screen.blit(rotated, new_rect)
