"""关卡难度曲线"""


class DifficultyManager:
    """难度管理器 - 控制游戏难度递增"""

    def __init__(self):
        self.level = 1
        self.score = 0
        self.speed_multiplier = 1.0
        self.obstacle_frequency = 150

    def update(self, delta_score=1):
        """更新难度"""
        self.score += delta_score

        new_level = (self.score // 15) + 1
        if new_level > self.level:
            self.level_up(new_level)

    def level_up(self, new_level):
        """升级"""
        self.level = new_level
        self.speed_multiplier = 1.0 + (self.level - 1) * 0.08
        self.obstacle_frequency = max(80, 150 - (self.level - 1) * 8)

    def get_speed(self, base_speed):
        """获取当前速度"""
        return base_speed * self.speed_multiplier

    def get_spawn_interval(self):
        """获取障碍物生成间隔"""
        return self.obstacle_frequency

    def reset(self):
        """重置难度"""
        self.level = 1
        self.score = 0
        self.speed_multiplier = 1.0
        self.obstacle_frequency = 150
