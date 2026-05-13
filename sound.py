"""音效管理器 - 生成和播放游戏音效"""

import pygame
import math
import struct


class SoundManager:
    """音效管理器"""

    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self._generate_sounds()

    def _generate_sounds(self):
        """生成所有音效"""
        sample_rate = 22050

        self.sounds["jump"] = self._create_tone(
            sample_rate, 0.15, 400, 800, "sine"
        )

        self.sounds["apple"] = self._create_chime(
            sample_rate, 0.2, [800, 1000, 1200]
        )

        self.sounds["heart"] = self._create_tone(
            sample_rate, 0.25, 500, 700, "sine"
        )

        self.sounds["coin"] = self._create_chime(
            sample_rate, 0.3, [1200, 1500, 1800, 2000]
        )

        self.sounds["damage"] = self._create_thud(sample_rate, 0.15)

        self.sounds["game_over"] = self._create_tone(
            sample_rate, 0.5, 400, 100, "sine"
        )

    def _create_tone(self, sample_rate, duration, start_freq, end_freq, wave_type="sine"):
        """创建单音调音效"""
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            progress = i / num_samples
            freq = start_freq + (end_freq - start_freq) * progress
            phase = 2 * math.pi * freq * t

            if wave_type == "sine":
                value = math.sin(phase)
            elif wave_type == "sawtooth":
                value = 2 * (phase / (2 * math.pi) % 1) - 1
            else:
                value = math.sin(phase)

            envelope = math.exp(-t * 8)
            value = int(value * envelope * 32767)
            samples.append(value)

        sound_bytes = struct.pack(f"{len(samples)}h", *samples)
        sound = pygame.mixer.Sound(buffer=sound_bytes)
        return sound

    def _create_chime(self, sample_rate, duration, frequencies):
        """创建和弦音效"""
        num_samples = int(sample_rate * duration)
        samples = [0.0] * num_samples

        for i, freq in enumerate(frequencies):
            delay = i * 0.05
            delay_samples = int(delay * sample_rate)
            tone_samples = int(sample_rate * (duration - delay))
            if tone_samples <= 0:
                continue

            for j in range(tone_samples):
                t = j / sample_rate
                value = math.sin(2 * math.pi * freq * t)
                envelope = math.exp(-t * 10)
                value = value * envelope
                idx = delay_samples + j
                if idx < num_samples:
                    samples[idx] += value

        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            samples = [s / max_val * 0.8 for s in samples]

        int_samples = [int(s * 32767) for s in samples]
        sound_bytes = struct.pack(f"{len(int_samples)}h", *int_samples)
        sound = pygame.mixer.Sound(buffer=sound_bytes)
        return sound

    def _create_thud(self, sample_rate, duration):
        """创建'咚'的撞击音效"""
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            freq = 80 + 40 * math.exp(-t * 30)
            phase = 2 * math.pi * freq * t

            value = math.sin(phase)
            noise = (math.sin(phase * 3.7) * 0.3 + math.sin(phase * 7.1) * 0.15)
            value = value + noise

            envelope = math.exp(-t * 25)
            value = int(value * envelope * 32767 * 0.8)
            samples.append(value)

        sound_bytes = struct.pack(f"{len(samples)}h", *samples)
        sound = pygame.mixer.Sound(buffer=sound_bytes)
        return sound

    def play(self, sound_name):
        """播放音效"""
        if not self.enabled:
            return
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def toggle(self):
        """切换音效开关"""
        self.enabled = not self.enabled
        return self.enabled
