"""
Các class hiệu ứng visual cho Zombie Head Smash Game
"""

import pygame
import random
import math
import constants as const

# --- Particle Effects Classes ---
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, velocity_x, velocity_y, lifetime=1000):
        super().__init__()
        self.image = pygame.Surface(const.PARTICLE_SIZE, pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (2, 2), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = const.PARTICLE_GRAVITY
        self.lifetime = lifetime
        self.age = 0
        self.original_color = color

    def update(self):
        self.age += 16  # Assume 60 FPS
        if self.age >= self.lifetime:
            self.kill()
            return

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.velocity_y += self.gravity

        # Fade out effect
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        faded_color = (*self.original_color, int(alpha))
        self.image = pygame.Surface(const.PARTICLE_SIZE, pygame.SRCALPHA)
        temp_color = self.original_color + (int(alpha),) if len(self.original_color) == 3 else self.original_color
        pygame.draw.circle(self.image, temp_color, (2, 2), 2)

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, font, lifetime=1500):
        super().__init__()
        self.font = font
        self.original_color = color
        self.text = text
        self.lifetime = lifetime
        self.age = 0
        self.start_y = y
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.age += 16
        if self.age >= self.lifetime:
            self.kill()
            return

        # Float upward and fade
        progress = self.age / self.lifetime
        self.rect.y = self.start_y - (progress * 50)  # Float up 50 pixels
        
        # Fade out
        alpha = max(0, 255 * (1 - progress))
        faded_color = (*self.original_color, int(alpha))
        self.image = self.font.render(self.text, True, self.original_color)
        # Apply alpha to surface
        temp_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        temp_surface.blit(self.image, (0, 0))
        temp_surface.set_alpha(alpha)
        self.image = temp_surface

class ScreenShake:
    def __init__(self):
        self.shake_amount = 0
        self.shake_duration = 0
        self.shake_timer = 0

    def add_shake(self, amount, duration):
        self.shake_amount = max(self.shake_amount, amount)
        self.shake_duration = max(self.shake_duration, duration)
        self.shake_timer = 0

    def update(self):
        if self.shake_timer < self.shake_duration:
            self.shake_timer += 16  # 60 FPS
            return True
        else:
            self.shake_amount = 0
            return False

    def get_offset(self):
        if self.shake_amount > 0:
            return (random.randint(-self.shake_amount, self.shake_amount),
                   random.randint(-self.shake_amount, self.shake_amount))
        return (0, 0)

class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, color=const.YELLOW):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.color = color
        self.radius = 5
        self.max_radius = const.EXPLOSION_MAX_RADIUS
        self.growth_rate = const.EXPLOSION_GROWTH_RATE
        self.alpha = 255
        self.fade_rate = const.EXPLOSION_FADE_RATE
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.image.fill((0, 0, 0, 0))
        
        # Draw expanding circles
        for i in range(3):
            current_radius = max(0, self.radius - i * 15)
            if current_radius > 0:
                circle_alpha = max(0, self.alpha - i * 50)
                color_with_alpha = (*self.color, circle_alpha)
                center = (self.max_radius, self.max_radius)
                pygame.draw.circle(self.image, color_with_alpha, center, int(current_radius), 3)
        
        self.radius += self.growth_rate
        self.alpha -= self.fade_rate
        
        if self.alpha <= 0 or self.radius >= self.max_radius:
            self.kill()

class RainbowText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font, lifetime=2000):
        super().__init__()
        self.text = text
        self.font = font
        self.lifetime = lifetime
        self.age = 0
        self.start_y = y
        self.color_index = 0
        self.image = self.font.render(text, True, const.RAINBOW_COLORS[0])
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.age += 16
        if self.age >= self.lifetime:
            self.kill()
            return

        # Animate rainbow colors
        self.color_index = (self.color_index + 0.2) % len(const.RAINBOW_COLORS)
        current_color = const.RAINBOW_COLORS[int(self.color_index)]
        
        # Float upward and scale
        progress = self.age / self.lifetime
        self.rect.y = self.start_y - (progress * 80)
        scale = 1.0 + math.sin(progress * math.pi) * 0.5
        
        # Create scaled text
        text_surface = self.font.render(self.text, True, current_color)
        if scale != 1.0:
            new_width = int(text_surface.get_width() * scale)
            new_height = int(text_surface.get_height() * scale)
            if new_width > 0 and new_height > 0:
                text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
        
        # Apply fade
        alpha = int(255 * (1 - progress))
        text_surface.set_alpha(alpha)
        self.image = text_surface
        self.rect = self.image.get_rect(center=self.rect.center)

class StarEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = random.uniform(const.STAR_SIZE_MIN, const.STAR_SIZE_MAX)
        self.max_size = self.size * 3
        self.growth_rate = random.uniform(0.1, 0.3)
        self.rotation = 0
        self.rotation_speed = random.uniform(const.STAR_ROTATION_SPEED_MIN, const.STAR_ROTATION_SPEED_MAX)
        self.color = random.choice(const.RAINBOW_COLORS)
        self.alpha = 255
        self.fade_rate = random.uniform(3, 8)
        self.lifetime = random.randint(1000, 2000)
        self.age = 0
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-4, -1)
        
        self.image = pygame.Surface((int(self.max_size * 2), int(self.max_size * 2)), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.age += 16
        if self.age >= self.lifetime:
            self.kill()
            return

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (int(self.x), int(self.y))

        # Update star properties
        self.size = min(self.max_size, self.size + self.growth_rate)
        self.rotation += self.rotation_speed
        self.alpha = max(0, self.alpha - self.fade_rate)

        # Draw rotating star
        self.image.fill((0, 0, 0, 0))
        self.draw_star()

    def draw_star(self):
        points = []
        num_points = 5
        center = (self.image.get_width() // 2, self.image.get_height() // 2)
        
        for i in range(num_points * 2):
            angle = math.radians(self.rotation + i * 36)
            if i % 2 == 0:
                radius = self.size
            else:
                radius = self.size * 0.4
            
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        if len(points) >= 3:
            color_with_alpha = (*self.color, int(self.alpha))
            pygame.draw.polygon(self.image, color_with_alpha, points)

class WaveEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, color=const.ELECTRIC_BLUE):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.color = color
        self.radius = 0
        self.max_radius = const.WAVE_MAX_RADIUS
        self.wave_speed = const.WAVE_SPEED
        self.wave_count = const.WAVE_COUNT
        self.alpha = 255
        self.fade_rate = const.WAVE_FADE_RATE
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.image.fill((0, 0, 0, 0))
        center = (self.max_radius, self.max_radius)
        
        # Draw multiple expanding waves
        for i in range(self.wave_count):
            wave_radius = (self.radius - i * 30) % self.max_radius
            if wave_radius > 0:
                wave_alpha = max(0, self.alpha - i * 60)
                color_with_alpha = (*self.color, wave_alpha)
                if wave_radius < self.max_radius - 5:
                    pygame.draw.circle(self.image, color_with_alpha, center, int(wave_radius), 2)
        
        self.radius += self.wave_speed
        self.alpha -= self.fade_rate
        
        if self.alpha <= 0:
            self.kill()

def create_blood_particles(x, y, combo=1):
    """Tạo hiệu ứng máu khi tiêu diệt zombie"""
    particles = pygame.sprite.Group()
    particle_count = const.BLOOD_PARTICLE_COUNT_BASE + combo * const.BLOOD_PARTICLE_COUNT_COMBO_BONUS
    particle_count = min(particle_count, const.BLOOD_PARTICLE_COUNT_MAX)
    
    for _ in range(particle_count):
        velocity_x = random.uniform(-12, 12)
        velocity_y = random.uniform(-15, -2)
        color = random.choice([const.BLOOD_RED, const.RED, (180, 0, 0), (120, 0, 0)])
        lifetime = random.randint(1000, 1800)
        particle = Particle(x, y, color, velocity_x, velocity_y, lifetime)
        particles.add(particle)
    
    return particles
