# Joycon 手柄控制
"""Switch Joycon 体感控制集成"""

import pygame
import math


class JoyconInput:
    """Joycon 输入控制器 - 支持体感跳跃"""

    def __init__(self, player_index=0):
        self.player_index = player_index
        self.joystick = None
        self.connected = False

        # 陀螺仪数据
        self.gyro = {"x": 0, "y": 0, "z": 0}
        self.last_gyro = {"x": 0, "y": 0, "z": 0}
        self.gyro_threshold = 0.5  # 跳跃阈值

        # 按钮状态
        self.buttons = {"A": False, "B": False, "X": False, "Y": False}

        # 校准数据
        self.gyro_offset = {"x": 0, "y": 0, "z": 0}
        self.calibrated = False

    def connect(self):
        """连接 Joycon 手柄"""
        pygame.joystick.init()
        count = pygame.joystick.get_count()

        if count > self.player_index:
            self.joystick = pygame.joystick.Joystick(self.player_index)
            self.joystick.init()
            self.connected = True
            print(f"Connected Joycon {self.player_index}: {self.joystick.get_name()}")

            # 打印手柄信息
            print(f"  Buttons: {self.joystick.get_numbuttons()}")
            print(f"  Axes: {self.joystick.get_numaxes()}")

            return True
        else:
            print(f"No controller found for player {self.player_index}")
            return False

    def calibrate(self):
        """校准陀螺仪零点"""
        samples = 100
        gyro_sum = {"x": 0, "y": 0, "z": 0}

        print("Calibrating... Please keep controller still.")
        for _ in range(samples):
            self._read_gyro()
            for key in gyro_sum:
                gyro_sum[key] += self.gyro[key]
            pygame.time.wait(1)

        for key in self.gyro_offset:
            self.gyro_offset[key] = gyro_sum[key] / samples

        self.calibrated = True
        print(f"Calibration complete: {self.gyro_offset}")

    def _read_gyro(self):
        """读取陀螺仪数据"""
        if not self.joystick:
            return

        try:
            # Joycon 陀螺仪轴映射（可能需要根据实际设备调整）
            # 通常轴 3,4,5 是陀螺仪
            if self.joystick.get_numaxes() >= 6:
                self.gyro["x"] = self.joystick.get_axis(3)
                self.gyro["y"] = self.joystick.get_axis(4)
                self.gyro["z"] = self.joystick.get_axis(5)
            elif self.joystick.get_numaxes() >= 4:
                # 备用映射
                self.gyro["x"] = self.joystick.get_axis(2)
                self.gyro["y"] = self.joystick.get_axis(3)
        except Exception as e:
            print(f"Error reading gyro: {e}")

    def _apply_calibration(self):
        """应用校准偏移"""
        if self.calibrated:
            for key in self.gyro:
                self.gyro[key] -= self.gyro_offset[key]

    def update(self):
        """更新控制器状态"""
        if not self.connected:
            return

        self.last_gyro = self.gyro.copy()
        self._read_gyro()
        self._apply_calibration()

        # 读取按钮
        if self.joystick:
            for i in range(min(4, self.joystick.get_numbuttons())):
                self.buttons[list(self.buttons.keys())[i]] = self.joystick.get_button(i)

    def detect_jump_motion(self):
        """检测跳跃手势（快速向上挥动）"""
        if not self.connected:
            return False

        # 检测 Y 轴陀螺仪的快速正向变化（向上挥动）
        gyro_change = self.gyro["y"] - self.last_gyro["y"]

        # 也检查加速度计的向上运动
        if gyro_change > self.gyro_threshold:
            print(f"Jump detected! gyro_change={gyro_change}")
            return True

        return False

    def is_jump_pressed(self):
        """检查是否按下跳跃按钮或做跳跃手势"""
        if not self.connected:
            return False

        # A 按钮跳跃
        if self.buttons.get("A", False):
            return True

        # 体感跳跃
        if self.detect_jump_motion():
            return True

        return False

    def get_tilt_angle(self):
        """获取手柄倾斜角度"""
        if not self.connected:
            return 0

        # 根据陀螺仪计算倾斜角度
        return math.degrees(math.atan2(self.gyro["x"], self.gyro["y"]))

    def disconnect(self):
        """断开连接"""
        if self.joystick:
            self.joystick.quit()
            self.joystick = None
            self.connected = False


class DualJoyconInput:
    """双 Joycon 输入 - 支持双人游戏"""

    def __init__(self):
        self.player_one = JoyconInput(0)
        self.player_two = JoyconInput(1)

    def connect_both(self):
        """连接两个 Joycon"""
        one_connected = self.player_one.connect()
        two_connected = self.player_two.connect()

        if one_connected and two_connected:
            print("Both Joycons connected!")
            return True
        elif one_connected:
            print("Only Player 1 Joycon connected")
            return True
        else:
            print("No Joycons connected")
            return False

    def update(self):
        """更新两个控制器"""
        self.player_one.update()
        self.player_two.update()

    def player_one_jump(self):
        """玩家 1 跳跃"""
        return self.player_one.is_jump_pressed()

    def player_two_jump(self):
        """玩家 2 跳跃"""
        return self.player_two.is_jump_pressed()

    def calibrate_both(self):
        """校准两个控制器"""
        self.player_one.calibrate()
        self.player_two.calibrate()
