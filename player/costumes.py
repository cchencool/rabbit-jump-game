# 换装系统
"""服装管理和切换"""

import pygame

# 服装颜色定义
COSTUMES = {
    "default": {"color": (255, 100, 100), "name": "Default"},
    "blue": {"color": (100, 100, 255), "name": "Blue"},
    "green": {"color": (100, 255, 100), "name": "Green"},
    "yellow": {"color": (255, 255, 100), "name": "Yellow"},
    "purple": {"color": (180, 100, 255), "name": "Purple"},
    "orange": {"color": (255, 150, 50), "name": "Orange"},
    "pink": {"color": (255, 150, 200), "name": "Pink"},
    "black": {"color": (50, 50, 50), "name": "Black"},
    "white": {"color": (240, 240, 240), "name": "White"},
    "gold": {"color": (255, 215, 0), "name": "Gold"},
}

# 风格分类
STYLES = {
    "casual": ["default", "blue", "green", "yellow"],
    "vivid": ["orange", "pink", "purple"],
    "elegant": ["black", "white", "gold"],
}


class CostumeManager:
    """服装管理器"""

    def __init__(self):
        self.unlocked = list(COSTUMES.keys())
        self.current = "pink"

    def set_costume(self, costume_id):
        """设置当前服装"""
        if costume_id in self.unlocked:
            self.current = costume_id
            return True
        return False

    def get_color(self):
        """获取当前颜色"""
        return COSTUMES[self.current]["color"]

    def get_costume_names(self):
        """获取所有服装名称"""
        return [COSTUMES[k]["name"] for k in self.unlocked]

    def cycle_next(self):
        """循环到下一个服装"""
        keys = list(self.unlocked)
        current_index = keys.index(self.current)
        next_index = (current_index + 1) % len(keys)
        self.current = keys[next_index]

    def cycle_prev(self):
        """循环到上一个服装"""
        keys = list(self.unlocked)
        current_index = keys.index(self.current)
        prev_index = (current_index - 1) % len(keys)
        self.current = keys[prev_index]
