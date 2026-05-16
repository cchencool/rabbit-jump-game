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

        self.waves = self._generate_waves()
        self.ships = self._generate_ships()
        self.seagulls = self._generate_seagulls()

        self.icebergs = self._generate_icebergs()
        self.penguins = self._generate_penguins()
        self.snowflakes = self._generate_snowflakes()

        self.buildings = self._generate_buildings()
        self.roads = self._generate_roads()
        self.streetlights = self._generate_streetlights()

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

    def _generate_waves(self):
        """生成海浪"""
        waves = []
        for i in range(5):
            waves.append({
                "x": i * 300,
                "y": SCREEN_HEIGHT - 120 + random.randint(0, 20),
                "width": random.randint(200, 350),
                "height": random.randint(15, 30),
                "speed": random.uniform(0.5, 1.0),
                "offset": random.uniform(0, math.pi * 2)
            })
        return waves

    def _generate_ships(self):
        """生成船只"""
        ships = []
        for i in range(2):
            ships.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": SCREEN_HEIGHT - 140 + random.randint(0, 30),
                "size": random.randint(40, 70),
                "speed": random.uniform(0.2, 0.5),
                "bob_offset": 0,
                "bob_timer": 0
            })
        return ships

    def _generate_seagulls(self):
        """生成海鸥"""
        seagulls = []
        for i in range(4):
            seagulls.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(40, 180),
                "wing_up": True,
                "timer": 0,
                "speed": random.uniform(0.8, 1.5)
            })
        return seagulls

    def _generate_icebergs(self):
        """生成冰山"""
        icebergs = []
        for i in range(4):
            icebergs.append({
                "x": i * 400 + random.randint(0, 100),
                "width": random.randint(80, 150),
                "height": random.randint(60, 120),
                "speed": 0.2
            })
        return icebergs

    def _generate_penguins(self):
        """生成企鹅"""
        penguins = []
        for i in range(3):
            penguins.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": SCREEN_HEIGHT - 120,
                "speed": random.uniform(0.3, 0.6),
                "waddle": 0,
                "waddle_timer": 0
            })
        return penguins

    def _generate_snowflakes(self):
        """生成雪花"""
        snowflakes = []
        for i in range(50):
            snowflakes.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "size": random.randint(2, 5),
                "speed": random.uniform(0.5, 2.0),
                "drift": random.uniform(-0.5, 0.5)
            })
        return snowflakes

    def _generate_buildings(self):
        """生成高楼"""
        buildings = []
        x = 0
        while x < SCREEN_WIDTH + 200:
            width = random.randint(60, 120)
            height = random.randint(100, 250)
            buildings.append({
                "x": x,
                "width": width,
                "height": height,
                "color": random.choice([(80, 80, 90), (100, 100, 110), (70, 70, 80), (90, 90, 100)]),
                "windows": self._generate_windows(width, height)
            })
            x += width + random.randint(10, 30)
        return buildings

    def _generate_windows(self, building_width, building_height):
        """生成窗户"""
        windows = []
        window_size = 8
        gap = 15
        cols = (building_width - 20) // gap
        rows = (building_height - 30) // gap
        for row in range(rows):
            for col in range(cols):
                if random.random() > 0.3:
                    windows.append({
                        "x": 10 + col * gap,
                        "y": 20 + row * gap,
                        "lit": random.random() > 0.5
                    })
        return windows

    def _generate_roads(self):
        """生成道路标记"""
        roads = []
        for i in range(0, SCREEN_WIDTH + 100, 40):
            roads.append({"x": i})
        return roads

    def _generate_streetlights(self):
        """生成路灯"""
        streetlights = []
        for i in range(0, SCREEN_WIDTH + 100, 150):
            streetlights.append({"x": i})
        return streetlights

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

        for wave in self.waves:
            wave["x"] -= wave["speed"]
            if wave["x"] < -wave["width"]:
                wave["x"] = SCREEN_WIDTH + random.randint(50, 150)

        for ship in self.ships:
            ship["x"] -= ship["speed"]
            ship["bob_timer"] += 1
            ship["bob_offset"] = math.sin(ship["bob_timer"] * 0.05) * 3
            if ship["x"] < -ship["size"]:
                ship["x"] = SCREEN_WIDTH + ship["size"]
                ship["y"] = SCREEN_HEIGHT - 140 + random.randint(0, 30)

        for seagull in self.seagulls:
            seagull["x"] -= seagull["speed"]
            seagull["timer"] += 1
            if seagull["timer"] % 15 == 0:
                seagull["wing_up"] = not seagull["wing_up"]
            if seagull["x"] < -50:
                seagull["x"] = SCREEN_WIDTH + 50
                seagull["y"] = random.randint(40, 180)

        for iceberg in self.icebergs:
            iceberg["x"] -= iceberg["speed"]
            if iceberg["x"] < -iceberg["width"]:
                iceberg["x"] = SCREEN_WIDTH + random.randint(50, 200)

        for penguin in self.penguins:
            penguin["x"] -= penguin["speed"]
            penguin["waddle_timer"] += 1
            if penguin["waddle_timer"] % 10 == 0:
                penguin["waddle"] = (penguin["waddle"] + 1) % 4
            if penguin["x"] < -30:
                penguin["x"] = SCREEN_WIDTH + 30

        for snowflake in self.snowflakes:
            snowflake["y"] += snowflake["speed"]
            snowflake["x"] += snowflake["drift"]
            if snowflake["y"] > SCREEN_HEIGHT:
                snowflake["y"] = -5
                snowflake["x"] = random.randint(0, SCREEN_WIDTH)

        for road in self.roads:
            road["x"] -= speed * 0.8
            if road["x"] < -40:
                road["x"] = SCREEN_WIDTH + 40

        for streetlight in self.streetlights:
            streetlight["x"] -= speed * 0.8
            if streetlight["x"] < -20:
                streetlight["x"] = SCREEN_WIDTH + 150

    def draw(self, screen):
        """绘制背景"""
        screen.fill(self.color)

        self._draw_sky_details(screen)

        for star in self.stars:
            alpha = 150 + 100 * (star["twinkle"] / 100)
            star_color = (int(255 * alpha / 255), int(255 * alpha / 255), int(200 * alpha / 255))
            pygame.draw.circle(screen, star_color, (int(star["x"]), int(star["y"])), 2)

        if self.theme == "city":
            self._draw_city_background(screen)
        elif self.theme == "ice":
            self._draw_ice_background(screen)
        elif self.theme == "ocean":
            self._draw_ocean_background(screen)
        else:
            self._draw_grass_background(screen)

    def _draw_grass_background(self, screen):
        """绘制草原背景"""
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

    def _draw_ocean_background(self, screen):
        """绘制海洋背景"""
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
            self._draw_cloud(screen, cloud, color=(220, 230, 240))

        for seagull in self.seagulls:
            self._draw_seagull(screen, seagull)

        for ship in self.ships:
            self._draw_ship(screen, ship)

        self._draw_ocean_ground(screen)

        for wave in self.waves:
            self._draw_wave(screen, wave)

    def _draw_ice_background(self, screen):
        """绘制冰川背景"""
        for iceberg in self.icebergs:
            self._draw_iceberg(screen, iceberg)

        for cloud in self.clouds:
            self._draw_cloud(screen, cloud, color=(200, 210, 220))

        for snowflake in self.snowflakes:
            pygame.draw.circle(screen, (255, 255, 255), (int(snowflake["x"]), int(snowflake["y"])), snowflake["size"])

        self._draw_ice_ground(screen)

        for penguin in self.penguins:
            self._draw_penguin(screen, penguin)

    def _draw_city_background(self, screen):
        """绘制城市背景"""
        for building in self.buildings:
            self._draw_building(screen, building)

        for streetlight in self.streetlights:
            self._draw_streetlight(screen, streetlight)

        self._draw_city_ground(screen)

        for road in self.roads:
            self._draw_road_marking(screen, road)

    def _draw_cloud(self, screen, cloud, color=(255, 255, 255)):
        """绘制云朵"""
        x, y, size = int(cloud["x"]), int(cloud["y"]), cloud["size"]
        pygame.draw.ellipse(screen, color, (x, y, size, size // 2))
        pygame.draw.ellipse(screen, color, (x + size // 4, y - size // 6, size // 2, size // 3))
        pygame.draw.ellipse(screen, color, (x - size // 4, y + size // 8, size // 2, size // 3))

    def _draw_bird(self, screen, bird):
        """绘制飞鸟"""
        x, y = int(bird["x"]), int(bird["y"])
        if bird["wing_up"]:
            pygame.draw.lines(screen, (50, 50, 50), False, [(x - 10, y + 5), (x, y), (x + 10, y + 5)], 2)
        else:
            pygame.draw.lines(screen, (50, 50, 50), False, [(x - 10, y - 5), (x, y), (x + 10, y - 5)], 2)

    def _draw_seagull(self, screen, seagull):
        """绘制海鸥"""
        x, y = int(seagull["x"]), int(seagull["y"])
        if seagull["wing_up"]:
            pygame.draw.lines(screen, (255, 255, 255), False, [(x - 12, y + 6), (x, y), (x + 12, y + 6)], 2)
        else:
            pygame.draw.lines(screen, (255, 255, 255), False, [(x - 12, y - 6), (x, y), (x + 12, y - 6)], 2)

    def _draw_ship(self, screen, ship):
        """绘制船只"""
        x = int(ship["x"])
        y = int(ship["y"] + ship["bob_offset"])
        size = ship["size"]

        pygame.draw.polygon(screen, (139, 90, 43), [
            (x - size // 2, y),
            (x + size // 2, y),
            (x + size // 3, y + 15),
            (x - size // 3, y + 15)
        ])

        pygame.draw.line(screen, (100, 70, 30), (x, y), (x, y - 25), 3)

        pygame.draw.polygon(screen, (255, 255, 255), [
            (x, y - 25),
            (x + 15, y - 10),
            (x, y - 10)
        ])

    def _draw_wave(self, screen, wave):
        """绘制海浪"""
        x = int(wave["x"])
        y = int(wave["y"])
        width = wave["width"]
        height = wave["height"]

        points = []
        for i in range(0, width, 5):
            px = x + i
            py = y + math.sin((i + self.scroll_offset) * 0.05) * height // 2
            points.append((px, py))

        if len(points) > 1:
            pygame.draw.lines(screen, (100, 180, 220), False, points, 3)

    def _draw_iceberg(self, screen, iceberg):
        """绘制冰山"""
        x = int(iceberg["x"])
        y = SCREEN_HEIGHT - 120
        width = iceberg["width"]
        height = iceberg["height"]

        pygame.draw.polygon(screen, (200, 230, 255), [
            (x, y),
            (x + width // 2, y - height),
            (x + width, y)
        ])

        pygame.draw.polygon(screen, (220, 240, 255), [
            (x + width // 4, y),
            (x + width // 2, y - height + 20),
            (x + width * 3 // 4, y)
        ])

    def _draw_penguin(self, screen, penguin):
        """绘制企鹅"""
        x = int(penguin["x"])
        y = int(penguin["y"])
        waddle_offset = math.sin(penguin["waddle"] * math.pi / 2) * 3

        pygame.draw.ellipse(screen, (30, 30, 30), (x - 10, y - 30, 20, 30))

        pygame.draw.ellipse(screen, (255, 255, 255), (x - 7, y - 25, 14, 20))

        pygame.draw.circle(screen, (30, 30, 30), (x, y - 32), 8)

        pygame.draw.circle(screen, (255, 255, 255), (x - 3, y - 34), 2)
        pygame.draw.circle(screen, (255, 255, 255), (x + 3, y - 34), 2)

        pygame.draw.circle(screen, (0, 0, 0), (x - 3, y - 34), 1)
        pygame.draw.circle(screen, (0, 0, 0), (x + 3, y - 34), 1)

        pygame.draw.polygon(screen, (255, 165, 0), [
            (x - 3, y - 30),
            (x + 3, y - 30),
            (x, y - 27)
        ])

        pygame.draw.ellipse(screen, (255, 165, 0), (x - 8 + waddle_offset, y - 5, 6, 8))
        pygame.draw.ellipse(screen, (255, 165, 0), (x + 2 - waddle_offset, y - 5, 6, 8))

    def _draw_building(self, screen, building):
        """绘制高楼"""
        x = int(building["x"])
        y = SCREEN_HEIGHT - 120 - building["height"]
        width = building["width"]
        height = building["height"]
        color = building["color"]

        pygame.draw.rect(screen, color, (x, y, width, height))

        for window in building["windows"]:
            wx = x + window["x"]
            wy = y + window["y"]
            if window["lit"]:
                pygame.draw.rect(screen, (255, 255, 150), (wx, wy, 8, 8))
            else:
                pygame.draw.rect(screen, (50, 50, 60), (wx, wy, 8, 8))

    def _draw_streetlight(self, screen, streetlight):
        """绘制路灯"""
        x = int(streetlight["x"])
        y = SCREEN_HEIGHT - 120

        pygame.draw.line(screen, (80, 80, 80), (x, y), (x, y - 60), 4)

        pygame.draw.line(screen, (80, 80, 80), (x - 15, y - 60), (x + 15, y - 60), 3)

        pygame.draw.circle(screen, (255, 255, 200), (x, y - 60), 5)

        light_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(light_surface, (255, 255, 200, 50), (20, 20), 20)
        screen.blit(light_surface, (x - 20, y - 80))

    def _draw_road_marking(self, screen, road):
        """绘制道路标记"""
        x = int(road["x"])
        y = SCREEN_HEIGHT - 110
        pygame.draw.rect(screen, (255, 255, 100), (x, y, 20, 4))

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
        elif self.theme == "ice":
            pygame.draw.circle(screen, (220, 230, 240), (SCREEN_WIDTH - 100, 80), 30)
            for i in range(6):
                angle = math.radians(i * 60)
                x1 = SCREEN_WIDTH - 100 + int(40 * math.cos(angle))
                y1 = 80 + int(40 * math.sin(angle))
                x2 = SCREEN_WIDTH - 100 + int(50 * math.cos(angle))
                y2 = 80 + int(50 * math.sin(angle))
                pygame.draw.line(screen, (200, 220, 240), (x1, y1), (x2, y2), 2)

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

    def _draw_ocean_ground(self, screen):
        """绘制海洋地面"""
        ground_y = SCREEN_HEIGHT - 120

        pygame.draw.rect(screen, (30, 80, 120), (0, ground_y, SCREEN_WIDTH, 120))

        sand_color = (210, 180, 140)
        pygame.draw.rect(screen, sand_color, (0, ground_y, SCREEN_WIDTH, 20))

        for i in range(0, SCREEN_WIDTH, 20):
            offset = (self.scroll_offset * 0.8) % 20
            sand_x = i + offset
            pygame.draw.ellipse(screen, (190, 160, 120), (sand_x, ground_y + 5, 8, 4))

    def _draw_ice_ground(self, screen):
        """绘制冰川地面"""
        ground_y = SCREEN_HEIGHT - 120

        pygame.draw.rect(screen, (150, 180, 200), (0, ground_y, SCREEN_WIDTH, 120))

        ice_color = (200, 220, 240)
        pygame.draw.rect(screen, ice_color, (0, ground_y, SCREEN_WIDTH, 20))

        for i in range(0, SCREEN_WIDTH, 25):
            offset = (self.scroll_offset * 0.8) % 25
            ice_x = i + offset
            pygame.draw.line(screen, (180, 200, 220), (ice_x, ground_y), (ice_x + 10, ground_y - 5), 2)

    def _draw_city_ground(self, screen):
        """绘制城市地面"""
        ground_y = SCREEN_HEIGHT - 120

        pygame.draw.rect(screen, (60, 60, 70), (0, ground_y, SCREEN_WIDTH, 120))

        road_color = (80, 80, 90)
        pygame.draw.rect(screen, road_color, (0, ground_y, SCREEN_WIDTH, 20))

        for i in range(0, SCREEN_WIDTH, 30):
            offset = (self.scroll_offset * 0.8) % 30
            road_x = i + offset
            pygame.draw.rect(screen, (100, 100, 110), (road_x, ground_y + 2, 15, 2))

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

        self.clouds = self._generate_clouds()
        self.hills = self._generate_hills()
        self.flowers = self._generate_flowers()
        self.birds = self._generate_birds()
        self.stars = self._generate_stars()

        self.waves = self._generate_waves()
        self.ships = self._generate_ships()
        self.seagulls = self._generate_seagulls()

        self.icebergs = self._generate_icebergs()
        self.penguins = self._generate_penguins()
        self.snowflakes = self._generate_snowflakes()

        self.buildings = self._generate_buildings()
        self.roads = self._generate_roads()
        self.streetlights = self._generate_streetlights()
