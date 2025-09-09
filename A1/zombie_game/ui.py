"""
UI Components cho Zombie Head Smash Game
"""

import pygame
import math
import constants as const

class Button:
    def __init__(self, x, y, width, height, text, font, action=None, normal_image=None, hover_image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.normal_image = pygame.transform.scale(normal_image, (width, height)) if normal_image else None
        self.hover_image = pygame.transform.scale(hover_image, (width, height)) if hover_image else None
        self.is_hovered = False

    def draw(self, surface):
        """Vẽ button lên surface"""
        current_image = self.hover_image if self.is_hovered and self.hover_image else self.normal_image
        if current_image:
            surface.blit(current_image, self.rect)
        else:  # Fallback to colored rect if no image
            color = const.DARK_GRAY if self.is_hovered else const.LIGHT_GRAY
            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, const.BLACK, self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, const.WHITE if current_image else const.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event, click_sound=None):
        """Xử lý sự kiện cho button"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                if click_sound:
                    click_sound.play()
                if self.action:
                    return self.action()
        return None

class UIRenderer:
    def __init__(self, fonts):
        self.fonts = fonts
    
    def draw_enhanced_ui(self, screen, game_stats):
        """Vẽ UI với hiệu ứng nâng cao"""
        hits = game_stats.get('hits', 0)
        misses = game_stats.get('misses', 0)
        combo = game_stats.get('combo', 0)
        max_combo = game_stats.get('max_combo', 0)
        difficulty_level = game_stats.get('difficulty_level', 'EASY')
        timer_start_time = game_stats.get('timer_start_time', 0)
        game_duration = game_stats.get('game_duration', 60000)
        
        # Display scores with dynamic colors and effects
        hit_color = const.GREEN if combo == 0 else const.SCORE_COLORS[min(combo - 1, len(const.SCORE_COLORS) - 1)]
        
        # Add glow effect to hit text when combo is active
        if combo > 1:
            for i in range(3):
                glow_hits = self.fonts['medium'].render(f"Hits: {hits}", True, hit_color)
                glow_hits.set_alpha(50 - i * 15)
                screen.blit(glow_hits, (10 - i, 10 - i))
        
        hits_text = self.fonts['medium'].render(f"Hits: {hits}", True, hit_color)
        misses_text = self.fonts['medium'].render(f"Misses: {misses}", True, const.RED)
        score_text = self.fonts['medium'].render(f"Score: {hits - misses}", True, const.WHITE)
        mode_text = self.fonts['small'].render(f"Mode: {difficulty_level}", True, const.WHITE)

        screen.blit(hits_text, (10, 10))
        screen.blit(misses_text, (10, 50))
        screen.blit(score_text, (10, 90))
        screen.blit(mode_text, (10, 130))

        # Enhanced combo display with rainbow effect
        if combo > 1:
            combo_color_index = (pygame.time.get_ticks() * 0.01) % len(const.RAINBOW_COLORS)
            combo_color = const.RAINBOW_COLORS[int(combo_color_index)]
            combo_text = self.fonts['medium'].render(f"COMBO x{combo}!", True, combo_color)
            
            # Add pulsing glow effect for combo
            pulse_scale = 1.0 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
            scaled_combo = pygame.transform.scale(combo_text, 
                                                (int(combo_text.get_width() * pulse_scale),
                                                 int(combo_text.get_height() * pulse_scale)))
            
            # Multi-layer glow
            for i in range(5):
                glow_alpha = max(0, 100 - i * 20)
                glow_combo = pygame.transform.scale(combo_text,
                                                  (int(combo_text.get_width() * (pulse_scale + i * 0.05)),
                                                   int(combo_text.get_height() * (pulse_scale + i * 0.05))))
                glow_combo.set_alpha(glow_alpha)
                glow_rect = glow_combo.get_rect(center=(120, 180))
                screen.blit(glow_combo, glow_rect)
            
            combo_rect = scaled_combo.get_rect(center=(120, 180))
            screen.blit(scaled_combo, combo_rect)

        # Display max combo with gold effect
        if max_combo > 1:
            max_combo_text = self.fonts['small'].render(f"Max Combo: {max_combo}", True, const.GOLD)
            screen.blit(max_combo_text, (10, 210))

        # Enhanced timer with warning effects
        time_left_ms = game_duration - (pygame.time.get_ticks() - timer_start_time)
        time_left_s = max(0, time_left_ms // 1000)
        
        timer_color = const.WHITE
        timer_scale = 1.0
        
        if time_left_s <= 10:
            # Critical time: blinking red with scaling effect
            blink_factor = (pygame.time.get_ticks() // 250) % 2
            timer_color = const.RED if blink_factor else const.ORANGE
            timer_scale = 1.0 + 0.2 * math.sin(pygame.time.get_ticks() * 0.02)
        elif time_left_s <= 30:
            timer_color = const.ORANGE
            timer_scale = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() * 0.01)
        
        timer_text = self.fonts['medium'].render(f"Time: {time_left_s}", True, timer_color)
        
        if abs(timer_scale - 1.0) > 0.01:  # Avoid floating point equality check
            scaled_timer = pygame.transform.scale(timer_text,
                                                (int(timer_text.get_width() * timer_scale),
                                                 int(timer_text.get_height() * timer_scale)))
            timer_rect = scaled_timer.get_rect(topright=(const.WIDTH - 10, 10))
            screen.blit(scaled_timer, timer_rect)
        else:
            timer_rect = timer_text.get_rect(topright=(const.WIDTH - 10, 10))
            screen.blit(timer_text, timer_rect)

    def draw_menu_title(self, screen, title_text):
        """Vẽ title với hiệu ứng pulsing"""
        # Animated title with pulsing effect
        pulse_scale = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() * 0.003)
        title_surface = self.fonts['large'].render(title_text, True, const.WHITE)
        
        # Create scaled title
        scaled_width = int(title_surface.get_width() * pulse_scale)
        scaled_height = int(title_surface.get_height() * pulse_scale)
        scaled_title = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        title_rect = scaled_title.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2 - 180))
        
        # Add glow effect to title
        glow_surface = pygame.Surface((scaled_width + 10, scaled_height + 10), pygame.SRCALPHA)
        for i in range(5):
            glow_color = (*const.ZOMBIE_GREEN, 30 - i * 5)
            glow_title = pygame.transform.scale(title_surface, (scaled_width + i * 2, scaled_height + i * 2))
            glow_rect = glow_title.get_rect(center=(glow_surface.get_width() // 2, glow_surface.get_height() // 2))
            glow_surface.blit(glow_title, glow_rect)
        
        glow_rect = glow_surface.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2 - 180))
        screen.blit(glow_surface, glow_rect)
        screen.blit(scaled_title, title_rect)

    def draw_game_over_screen(self, screen, game_stats):
        """Vẽ màn hình game over"""
        hits = game_stats.get('hits', 0)
        misses = game_stats.get('misses', 0)
        difficulty_level = game_stats.get('difficulty_level', 'EASY')
        max_combo = game_stats.get('max_combo', 0)
        
        # Tạo một lớp phủ mờ
        overlay = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Màu đen trong suốt
        screen.blit(overlay, (0, 0))

        game_over_text = self.fonts['large'].render("GAME OVER!", True, const.RED)
        final_score_text = self.fonts['medium'].render(f"Final Score: {hits - misses}", True, const.WHITE)
        difficulty_text = self.fonts['small'].render(f"Difficulty: {difficulty_level}", True, const.WHITE)
        
        # Add special info for different modes
        if difficulty_level == "CLASSIC":
            info_text = self.fonts['small'].render("(Zombies don't disappear automatically)", True, const.LIGHT_GRAY)
        else:
            info_text = self.fonts['small'].render("(Zombies have limited lifetime)", True, const.LIGHT_GRAY)

        # Display max combo achieved
        max_combo_display = self.fonts['small'].render(f"Max Combo: {max_combo}", True, const.GOLD)

        text_rect = game_over_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2 - 120))
        score_rect = final_score_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2 - 60))
        difficulty_rect = difficulty_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2 - 30))
        info_rect = info_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2))
        combo_rect = max_combo_display.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2 + 30))

        screen.blit(game_over_text, text_rect)
        screen.blit(final_score_text, score_rect)
        screen.blit(difficulty_text, difficulty_rect)
        screen.blit(info_text, info_rect)
        screen.blit(max_combo_display, combo_rect)

class MouseTrail:
    def __init__(self, max_length=const.MAX_TRAIL_LENGTH):
        self.positions = []
        self.max_length = max_length

    def update(self, mouse_pos):
        """Cập nhật trail chuột"""
        self.positions.append(mouse_pos)
        if len(self.positions) > self.max_length:
            self.positions.pop(0)

    def draw(self, screen, combo=1):
        """Vẽ trail chuột với hiệu ứng nâng cao"""
        if len(self.positions) > 1:
            for i in range(len(self.positions) - 1):
                start_pos = self.positions[i]
                end_pos = self.positions[i + 1]
                alpha = int(255 * (i + 1) / len(self.positions))
                
                # Rainbow trail effect
                color_index = (i + pygame.time.get_ticks() * 0.01) % len(const.RAINBOW_COLORS)
                trail_color = const.RAINBOW_COLORS[int(color_index)]
                
                # Variable thickness based on combo
                base_thickness = max(1, i // 2)
                combo_bonus = min(combo, 10)  # Cap combo bonus
                thickness = base_thickness + combo_bonus
                
                # Draw multiple trail layers for glow effect
                for layer in range(3):
                    layer_alpha = max(0, alpha - layer * 60)
                    layer_thickness = thickness + layer * 2
                    layer_color = (*trail_color, layer_alpha)
                    
                    # Create surface for the trail segment
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    length = (dx*dx + dy*dy) ** 0.5
                    
                    if length > 0:
                        trail_surface = pygame.Surface((int(length) + layer_thickness * 2, 
                                                      layer_thickness * 2), pygame.SRCALPHA)
                        
                        # Draw the trail line
                        pygame.draw.line(trail_surface, layer_color,
                                       (layer_thickness, layer_thickness),
                                       (int(length) + layer_thickness, layer_thickness),
                                       layer_thickness)
                        
                        # Calculate rotation angle
                        angle = math.degrees(math.atan2(dy, dx))
                        rotated_surface = pygame.transform.rotate(trail_surface, angle)
                        
                        # Position the rotated surface
                        surface_rect = rotated_surface.get_rect()
                        surface_rect.center = ((start_pos[0] + end_pos[0]) // 2,
                                             (start_pos[1] + end_pos[1]) // 2)
                        
                        screen.blit(rotated_surface, surface_rect)
