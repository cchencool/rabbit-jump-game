# 输入控制器
"""键盘和手柄输入控制"""

import pygame
from settings import JOYCON_DEADZONE


class InputController:
    """输入控制器基类"""

    def __init__(self):
        self.jump_pressed = False

    def update(self):
        """更新输入状态"""
        raise NotImplementedError

    def check_jump(self):
        """检查是否跳跃"""
        return self.jump_pressed


class KeyboardController(InputController):
    """键盘控制器"""

    def __init__(self, jump_keys=None):
        super().__init__()
        self.jump_keys = jump_keys or [pygame.K_SPACE, pygame.K_UP, pygame.K_w]
        self.prev_jump_state = False

    def update(self):
        """更新键盘状态"""
        keys = pygame.key.get_pressed()
        current_jump = any(keys[key] for key in self.jump_keys)
        self.jump_pressed = current_jump and not self.prev_jump_state
        self.prev_jump_state = current_jump


P1_JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]
P2_JUMP_KEYS = [pygame.K_RETURN, pygame.K_s, pygame.K_DOWN]


class JoyconController(InputController):
    """Joycon 手柄控制器 - 使用 pygame 手柄支持"""

    def __init__(self, player_index=0):
        super().__init__()
        self.player_index = player_index
        self.joystick = None
        self.connected = False

        # 陀螺仪数据
        self.gyro_y = 0
        self.last_gyro_y = 0
        self.jump_threshold = 0.3  # 体感跳跃灵敏度

        # 按钮跳跃（备用）
        self.jump_button = 0  # A 按钮

    def connect(self):
        """连接 Joycon"""
        pygame.joystick.init()
        count = pygame.joystick.get_count()

        if count > self.player_index:
            self.joystick = pygame.joystick.Joystick(self.player_index)
            self.joystick.init()
            self.connected = True
            print(f"Connected Joycon {self.player_index}: {self.joystick.get_name()}")
            print(f"  Axes: {self.joystick.get_numaxes()}, Buttons: {self.joystick.get_numbuttons()}")
            return True

        print(f"No Joycon found for player {self.player_index}")
        return False

    def update(self):
        """更新手柄状态"""
        if not self.connected or not self.joystick:
            self.jump_pressed = False
            return

        self.jump_pressed = False

        # 方法 1: 按钮跳跃（A 按钮）
        try:
            if self.joystick.get_button(self.jump_button):
                self.jump_pressed = True
                return
        except Exception:
            pass

        # 方法 2: 体感跳跃（陀螺仪）
        try:
            if self.joystick.get_numaxes() >= 4:
                # 读取陀螺仪 Y 轴（向上挥动）
                self.gyro_y = self.joystick.get_axis(3)

                # 检测快速向上运动
                gyro_change = self.gyro_y - self.last_gyro_y
                if gyro_change > self.jump_threshold:
                    self.jump_pressed = True

                self.last_gyro_y = self.gyro_y
        except Exception as e:
            print(f"Error reading gyro: {e}")

    def calibrate(self):
        """校准陀螺仪"""
        print("Calibrating Joycon...")
        samples = 50
        gyro_sum = 0

        for _ in range(samples):
            try:
                if self.joystick and self.joystick.get_numaxes() >= 4:
                    gyro_sum += self.joystick.get_axis(3)
            except Exception:
                pass
            pygame.time.wait(10)

        self.last_gyro_y = gyro_sum / samples
        print(f"Calibration complete: baseline={self.last_gyro_y}")

    def disconnect(self):
        """断开连接"""
        if self.joystick:
            self.joystick.quit()
            self.joystick = None
            self.connected = False


class HybridController(InputController):
    """混合控制器 - 支持键盘 + 手柄同时使用"""

    def __init__(self, player_index=0):
        super().__init__()
        self.keyboard = KeyboardController()
        self.joycon = JoyconController(player_index)

    def connect(self):
        """连接手柄（可选）"""
        return self.joycon.connect()

    def update(self):
        """更新两种输入"""
        self.keyboard.update()
        self.joycon.update()

        # 任一输入触发跳跃
        self.jump_pressed = self.keyboard.jump_pressed or self.joycon.jump_pressed

    def disconnect(self):
        """断开手柄"""
        self.joycon.disconnect()
