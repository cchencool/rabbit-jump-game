"""兔子角色、物理和动画"""

import pygame
from settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_GRAVITY,
    PLAYER_JUMP_FORCE,
    PLAYER_SPEED,
    GROUND_Y,
)


def draw_rabbit(surface, x, y, width, height, color, frame, is_jumping, is_running, practice_mode=False):
    """绘制栩栩如生的像素风兔子"""
    pixel_size = 4
    body_color = color
    belly_color = tuple(min(c + 40, 255) for c in color)
    eye_color = (30, 30, 30)
    nose_color = (255, 150, 150)
    inner_ear_color = tuple(max(c - 60, 0) for c in color)

    cx = x + width // 2
    cy = y + height // 2

    bounce_offset = 0
    if is_running and not is_jumping:
        bounce_offset = abs(pygame.time.get_ticks() % 200 - 100) // 25

    ear_wiggle = 0
    if is_jumping:
        ear_wiggle = -8

    body_rects = [
        (cx - 16, cy - 8 + bounce_offset, 32, 24),
    ]

    ear_data = [
        (cx - 12, cy - 28 + bounce_offset + ear_wiggle, 8, 24),
        (cx + 4, cy - 28 + bounce_offset + ear_wiggle, 8, 24),
    ]

    inner_ear_data = [
        (cx - 10, cy - 24 + bounce_offset + ear_wiggle, 4, 16),
        (cx + 6, cy - 24 + bounce_offset + ear_wiggle, 4, 16),
    ]

    head_rect = (cx - 14, cy - 16 + bounce_offset, 28, 20)

    eye_data = [
        (cx - 8, cy - 10 + bounce_offset, 5, 6),
        (cx + 4, cy - 10 + bounce_offset, 5, 6),
    ]

    eye_shine_data = [
        (cx - 6, cy - 10 + bounce_offset, 2, 2),
        (cx + 6, cy - 10 + bounce_offset, 2, 2),
    ]

    nose_rect = (cx - 2, cy - 4 + bounce_offset, 4, 3)

    mouth_points = [
        (cx - 4, cy + 2 + bounce_offset),
        (cx, cy + 5 + bounce_offset),
        (cx + 4, cy + 2 + bounce_offset),
    ]

    belly_rect = (cx - 10, cy + 2 + bounce_offset, 20, 14)

    leg_offset = 0
    if is_running and not is_jumping:
        leg_offset = (pygame.time.get_ticks() % 300) // 150 * 4

    front_legs = [
        (cx - 12, cy + 14 + bounce_offset, 8, 12 + leg_offset),
        (cx + 4, cy + 14 + bounce_offset, 8, 12 - leg_offset),
    ]

    back_legs = [
        (cx - 18, cy + 12 + bounce_offset, 10, 14 - leg_offset),
        (cx + 8, cy + 12 + bounce_offset, 10, 14 + leg_offset),
    ]

    tail_circle = (cx + 18, cy + 4 + bounce_offset, 6)

    for rect in body_rects:
        pygame.draw.rect(surface, body_color, rect, border_radius=8)

    for ear in ear_data:
        pygame.draw.ellipse(surface, body_color, ear)

    for inner_ear in inner_ear_data:
        pygame.draw.ellipse(surface, inner_ear_color, inner_ear)

    pygame.draw.ellipse(surface, body_color, head_rect)

    for eye in eye_data:
        pygame.draw.ellipse(surface, eye_color, eye)

    for shine in eye_shine_data:
        pygame.draw.ellipse(surface, (255, 255, 255), shine)

    pygame.draw.ellipse(surface, nose_color, nose_rect)

    if len(mouth_points) >= 3:
        pygame.draw.lines(surface, eye_color, False, mouth_points, 2)

    pygame.draw.ellipse(surface, belly_color, belly_rect)

    for leg in front_legs:
        pygame.draw.rect(surface, body_color, leg, border_radius=4)

    for leg in back_legs:
        pygame.draw.rect(surface, body_color, leg, border_radius=4)

    pygame.draw.circle(surface, (240, 240, 240), (tail_circle[0], tail_circle[1]), tail_circle[2])

    if practice_mode:
        hand_y = cy + 10 + bounce_offset
        for side in [-1, 1]:
            hx = cx + side * 16
            pygame.draw.circle(surface, (255, 80, 80), (hx - 3, hand_y - 2), 4)
            pygame.draw.circle(surface, (255, 80, 80), (hx + 3, hand_y - 2), 4)
            pygame.draw.polygon(surface, (255, 80, 80), [
                (hx - 6, hand_y),
                (hx, hand_y + 7),
                (hx + 6, hand_y),
            ])


class Player(pygame.sprite.Sprite):
    """玩家角色类 - 兔子"""

    def __init__(self, x=100, color=(255, 100, 100)):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_Y - PLAYER_HEIGHT

        self.hitbox = pygame.Rect(x + 12, GROUND_Y - PLAYER_HEIGHT + 8, 40, 48)

        self.color = color
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = True
        self.is_running = True
        self.jump_count = 0
        self.max_jumps = 2

        self.frame = 0
        self.animation_timer = 0

        self.hp = 3
        self.max_hp = 3
        self.invincible_timer = 0
        self.invincible_duration = 60

        self.shield_timer = 0
        self.shield_duration = 600

        self.practice_mode = False

    def take_damage(self):
        """受到伤害"""
        if self.shield_timer > 0:
            return
        if self.invincible_timer > 0:
            return
        self.hp -= 1
        self.invincible_timer = self.invincible_duration

    def heal(self):
        """恢复血量"""
        if self.hp < self.max_hp:
            self.hp += 1

    def update_invincibility(self):
        """更新无敌状态"""
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.shield_timer > 0:
            self.shield_timer -= 1

    def jump(self):
        """跳跃（支持二级跳）"""
        if self.jump_count < self.max_jumps:
            if self.on_ground:
                self.velocity_y = PLAYER_JUMP_FORCE
            else:
                self.velocity_y = PLAYER_JUMP_FORCE * 0.85
            self.is_jumping = True
            self.on_ground = False
            self.jump_count += 1

    def update(self):
        """更新玩家状态"""
        self.velocity_y += PLAYER_GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= GROUND_Y - PLAYER_HEIGHT:
            self.rect.y = GROUND_Y - PLAYER_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False
            self.on_ground = True
            self.jump_count = 0

        self.hitbox.x = self.rect.x + 12
        self.hitbox.y = self.rect.y + 8

        self.update_invincibility()

        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % 4

    def draw(self, screen):
        """绘制玩家"""
        if self.invincible_timer > 0 and (self.invincible_timer // 4) % 2 == 0:
            return
        self.image.fill((0, 0, 0, 0))
        draw_rabbit(
            self.image,
            0, 0,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            self.color,
            self.frame,
            self.is_jumping,
            self.is_running,
            self.practice_mode,
        )
        screen.blit(self.image, self.rect)

        if self.shield_timer > 0:
            shield_alpha = int(100 + 50 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() % 360).x)
            shield_surface = pygame.Surface((PLAYER_WIDTH + 20, PLAYER_HEIGHT + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(shield_surface, (255, 215, 0, shield_alpha), (0, 0, PLAYER_WIDTH + 20, PLAYER_HEIGHT + 20), 3)
            screen.blit(shield_surface, (self.rect.x - 10, self.rect.y - 10))

    def set_costume(self, color):
        """更换服装颜色"""
        self.color = color


class PlayerTwo(Player):
    """第二个玩家角色"""

    def __init__(self, x=200, color=(100, 100, 255)):
        super().__init__(x, color)
