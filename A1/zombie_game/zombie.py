"""
Class Zombie cho Zombie Head Smash Game
"""

import pygame
import random
import math
import constants as const

class Zombie(pygame.sprite.Sprite):
    def __init__(self, image, speed_multiplier=1.0):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.spawn_time = pygame.time.get_ticks()
        
        # Nếu speed_multiplier = 0, zombie sẽ không tự biến mất (mode Classic)
        if speed_multiplier == 0:
            self.lifetime = float('inf')  # Vô hạn - không tự biến mất
        else:
            self.lifetime = random.randint(
                int(1500 / speed_multiplier), 
                int(3000 / speed_multiplier)
            )  # Thời gian tồn tại (ms), phụ thuộc vào độ khó
        
        self.speed_multiplier = speed_multiplier
        self.popping_up = True
        self.pop_animation_start = pygame.time.get_ticks()
        self.pop_animation_duration = const.ZOMBIE_POP_ANIMATION_DURATION
        self.hit = False
        self.splat_time = 0
        self.splat_duration = const.ZOMBIE_SPLAT_DURATION
        
        # Enhanced animation properties
        self.wiggle_amount = 0
        self.wiggle_speed = 0.1
        self.glow_intensity = 0
        self.scale_factor = 1.0
        self.rotation_angle = 0
        self.bounce_offset = 0
        self.warning_time = const.ZOMBIE_WARNING_TIME  # Thời gian cảnh báo trước khi biến mất (ms)

    def set_position(self, x, y):
        """Đặt vị trí zombie"""
        self.rect.center = (x, y)

    def update(self):
        """Cập nhật trạng thái zombie"""
        current_time = pygame.time.get_ticks()

        # Hiệu ứng xuất hiện (pop-up animation) với bouncing
        if self.popping_up:
            elapsed = current_time - self.pop_animation_start
            if elapsed < self.pop_animation_duration:
                # Elastic ease-out animation
                progress = elapsed / self.pop_animation_duration
                if progress < 0.5:
                    scale_factor = 2 * progress * progress
                else:
                    scale_factor = 1 - 2 * (progress - 1) * (progress - 1) * 0.3
                
                # Bounce effect
                self.bounce_offset = math.sin(progress * math.pi * 3) * 5 * (1 - progress)
                
                current_width = int(self.original_image.get_width() * scale_factor)
                current_height = int(self.original_image.get_height() * scale_factor)
                if current_width > 0 and current_height > 0:
                    scaled_image = pygame.transform.scale(self.original_image, (current_width, current_height))
                    self.image = scaled_image
                    original_center = self.rect.center
                    self.rect = self.image.get_rect(center=(original_center[0], original_center[1] + self.bounce_offset))
            else:
                self.popping_up = False
                self.image = self.original_image
                self.rect = self.image.get_rect(center=(self.rect.center[0], self.rect.center[1] - self.bounce_offset))
                self.bounce_offset = 0

        # Hiệu ứng wiggle khi zombie sắp biến mất
        if not self.hit and self.speed_multiplier > 0:
            time_remaining = self.lifetime - (current_time - self.spawn_time)
            if time_remaining <= self.warning_time and time_remaining > 0:
                # Tăng dần cường độ wiggle
                warning_progress = 1 - (time_remaining / self.warning_time)
                self.wiggle_amount = math.sin(current_time * 0.02) * 3 * warning_progress
                self.glow_intensity = int(100 * warning_progress)
                
                # Tạo hiệu ứng glow bằng cách vẽ outline
                if not self.popping_up:
                    glow_surface = pygame.Surface((self.original_image.get_width() + 6, 
                                                 self.original_image.get_height() + 6), pygame.SRCALPHA)
                    for i in range(3):
                        glow_color = (*const.BLOOD_RED, self.glow_intensity - i * 20)
                        enlarged = pygame.transform.scale(self.original_image, 
                                                        (self.original_image.get_width() + i * 2,
                                                         self.original_image.get_height() + i * 2))
                        glow_surface.blit(enlarged, (3 - i, 3 - i))
                    
                    glow_surface.blit(self.original_image, (3, 3))
                    self.image = glow_surface
                    
                    # Apply wiggle offset
                    original_center = self.rect.center
                    self.rect = self.image.get_rect(center=(original_center[0] + self.wiggle_amount, original_center[1]))

        # Nếu đã bị đập, hiển thị splat và biến mất sau một thời gian
        if self.hit:
            if current_time - self.splat_time > self.splat_duration:
                self.kill()

        # Zombie tự động biến mất nếu không bị đập (trừ mode Classic)
        elif not self.hit and self.speed_multiplier > 0 and current_time - self.spawn_time > self.lifetime:
            self.kill()
    
    def is_alive(self):
        """Kiểm tra zombie còn sống không"""
        return not self.hit and (self.speed_multiplier == 0 or 
                                pygame.time.get_ticks() - self.spawn_time < self.lifetime)
    
    def hit_zombie(self):
        """Đánh trúng zombie"""
        if not self.hit:
            self.hit = True
            self.splat_time = pygame.time.get_ticks()
            return True
        return False
    
    def should_disappear(self):
        """Kiểm tra zombie có nên biến mất không"""
        if self.hit:
            return pygame.time.get_ticks() - self.splat_time > self.splat_duration
        elif self.speed_multiplier > 0:
            return pygame.time.get_ticks() - self.spawn_time > self.lifetime
        return False
