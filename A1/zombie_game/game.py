"""
Class Game chính cho Zombie Head Smash Game
"""

import pygame
import random
import constants as const
from zombie import Zombie
import effects
from ui import Button, UIRenderer, MouseTrail

class Game:
    def __init__(self, fonts, images, sounds):
        self.fonts = fonts
        self.images = images
        self.sounds = sounds
        
        self.state = const.GAME_STATE_MENU
        self.all_sprites = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.floating_texts = pygame.sprite.Group()
        self.special_effects = pygame.sprite.Group()
        
        # Game statistics
        self.hits = 0
        self.misses = 0
        self.combo = 0
        self.max_combo = 0
        self.game_over = False
        self.timer_start_time = 0
        self.game_duration = 60 * 1000  # 60 seconds default
        self.difficulty_level = "EASY"
        self.zombie_speed_multiplier = 1.0
        self.max_zombies_on_screen = 5
        
        # Enhanced visual effects
        self.screen_shake = effects.ScreenShake()
        self.score_multiplier = 1
        self.last_hit_time = 0
        self.combo_time_window = const.COMBO_TIME_WINDOW
        
        # UI components
        self.ui_renderer = UIRenderer(fonts)
        self.mouse_trail = MouseTrail()
        
        # Background animation
        self.background_stars = []
        self.star_spawn_timer = 0
        
        self.menu_buttons = []
        self.difficulty_buttons = []
        self._setup_menu_buttons()
        self._setup_difficulty_buttons()
        
        # Spawn timing variables
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval_min = 1000  # ms
        self.spawn_interval_max = 2000  # ms

    def _setup_menu_buttons(self):
        """Thiết lập các button menu"""
        play_button = Button(
            const.WIDTH // 2 - 100, const.HEIGHT // 2 - 80, 200, 70, "Play Game", self.fonts['medium'],
            action=lambda: self.set_state(const.GAME_STATE_DIFFICULTY),
            normal_image=self.images['button_normal'], hover_image=self.images['button_hover']
        )
        quit_button = Button(
            const.WIDTH // 2 - 100, const.HEIGHT // 2 + 20, 200, 70, "Quit", self.fonts['medium'],
            action=lambda: "QUIT",
            normal_image=self.images['button_normal'], hover_image=self.images['button_hover']
        )
        self.menu_buttons = [play_button, quit_button]

    def _setup_difficulty_buttons(self):
        """Thiết lập các button chọn độ khó"""
        classic_button = Button(
            const.WIDTH // 2 - 100, const.HEIGHT // 2 - 160, 200, 70, "Classic", self.fonts['medium'],
            action=lambda: self.start_game("CLASSIC"),
            normal_image=self.images['button_normal'], hover_image=self.images['button_hover']
        )
        easy_button = Button(
            const.WIDTH // 2 - 100, const.HEIGHT // 2 - 80, 200, 70, "Easy", self.fonts['medium'],
            action=lambda: self.start_game("EASY"),
            normal_image=self.images['button_normal'], hover_image=self.images['button_hover']
        )
        medium_button = Button(
            const.WIDTH // 2 - 100, const.HEIGHT // 2, 200, 70, "Medium", self.fonts['medium'],
            action=lambda: self.start_game("MEDIUM"),
            normal_image=self.images['button_normal'], hover_image=self.images['button_hover']
        )
        hard_button = Button(
            const.WIDTH // 2 - 100, const.HEIGHT // 2 + 80, 200, 70, "Hard", self.fonts['medium'],
            action=lambda: self.start_game("HARD"),
            normal_image=self.images['button_normal'], hover_image=self.images['button_hover']
        )
        back_button = Button(
            const.WIDTH // 2 - 100, const.HEIGHT // 2 + 160, 200, 70, "Back", self.fonts['medium'],
            action=lambda: self.set_state(const.GAME_STATE_MENU),
            normal_image=self.images['button_normal'], hover_image=self.images['button_hover']
        )
        self.difficulty_buttons = [classic_button, easy_button, medium_button, hard_button, back_button]

    def set_state(self, new_state):
        """Đổi trạng thái game"""
        self.state = new_state
        if new_state == const.GAME_STATE_PLAYING:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(500)
            pygame.mixer.music.play(-1)
        elif new_state == const.GAME_STATE_MENU:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(500)
            pygame.mixer.music.play(-1)
            self.reset_game()

    def start_game(self, difficulty):
        """Bắt đầu game với độ khó được chọn"""
        self.difficulty_level = difficulty
        settings = const.DIFFICULTY_SETTINGS[difficulty]
        
        self.game_duration = settings['game_duration']
        self.zombie_speed_multiplier = settings['zombie_speed_multiplier']
        self.max_zombies_on_screen = settings['max_zombies_on_screen']
        self.spawn_interval_min = settings['spawn_interval_min']
        self.spawn_interval_max = settings['spawn_interval_max']

        self.reset_game()
        self.timer_start_time = pygame.time.get_ticks()
        self.state = const.GAME_STATE_PLAYING
        pygame.mixer.music.play(-1)

    def reset_game(self):
        """Reset trạng thái game"""
        self.all_sprites.empty()
        self.zombies.empty()
        self.particles.empty()
        self.floating_texts.empty()
        self.special_effects.empty()
        self.hits = 0
        self.misses = 0
        self.combo = 0
        self.max_combo = 0
        self.game_over = False
        self.timer_start_time = 0
        self.last_spawn_time = pygame.time.get_ticks()
        self.screen_shake = effects.ScreenShake()
        self.score_multiplier = 1
        self.last_hit_time = 0
        self.mouse_trail = MouseTrail()
        self.background_stars = []

    def spawn_zombie(self):
        """Tạo zombie mới"""
        current_time = pygame.time.get_ticks()
        if len(self.zombies) < self.max_zombies_on_screen and \
           current_time - self.last_spawn_time > random.randint(self.spawn_interval_min, self.spawn_interval_max):
            
            available_points = [p for p in const.ZOMBIE_SPAWN_POINTS if not self.is_point_occupied(p)]
            if available_points:
                pos_x, pos_y = random.choice(available_points)
                new_zombie = Zombie(self.images['zombie_head'].copy(), self.zombie_speed_multiplier)
                new_zombie.set_position(pos_x, pos_y)
                self.all_sprites.add(new_zombie)
                self.zombies.add(new_zombie)
                self.last_spawn_time = current_time

    def is_point_occupied(self, point):
        """Kiểm tra xem vị trí có bị chiếm không"""
        for zombie in self.zombies:
            buffer_rect = zombie.rect.inflate(-20, -20)
            if buffer_rect.collidepoint(point):
                return True
        return False

    def handle_click(self, pos):
        """Xử lý click chuột"""
        if self.game_over:
            return
        
        clicked_on_zombie = False
        zombies_to_check = list(self.zombies)
        for zombie in zombies_to_check:
            if zombie.rect.collidepoint(pos) and not zombie.hit:
                if self.sounds['splat']:
                    self.sounds['splat'].play()
                
                # Update combo system
                current_time = pygame.time.get_ticks()
                if current_time - self.last_hit_time < self.combo_time_window:
                    self.combo += 1
                else:
                    self.combo = 1
                
                self.max_combo = max(self.max_combo, self.combo)
                self.last_hit_time = current_time
                
                # Calculate score with combo multiplier
                score_gain = self.combo
                self.hits += score_gain
                
                zombie.hit_zombie()
                
                # Create visual effects based on combo
                self._create_combo_effects(zombie, score_gain)
                
                # Create blood particles
                blood_particles = effects.create_blood_particles(zombie.rect.center[0], zombie.rect.center[1], self.combo)
                self.particles.add(blood_particles)
                
                clicked_on_zombie = True
                break
        
        if not clicked_on_zombie:
            self.misses += 1
            self.combo = 0
            miss_text = effects.FloatingText(pos[0], pos[1], "MISS!", const.RED, self.fonts['small'], 1000)
            self.floating_texts.add(miss_text)

    def _create_combo_effects(self, zombie, score_gain):
        """Tạo hiệu ứng dựa trên combo"""
        zombie_center = zombie.rect.center
        
        if self.combo >= 10:
            # Epic combo effects
            self.screen_shake.add_shake(15, 400)
            explosion = effects.ExplosionEffect(zombie_center[0], zombie_center[1], const.GOLD)
            self.special_effects.add(explosion)
            
            # Rainbow text for epic combo
            score_text = f"EPIC +{score_gain} x{self.combo}!"
            rainbow_text = effects.RainbowText(zombie_center[0], zombie_center[1] - 30, 
                                     score_text, self.fonts['medium'])
            self.floating_texts.add(rainbow_text)
            
            # Star shower effect
            for _ in range(10):
                star_x = zombie_center[0] + random.randint(-50, 50)
                star_y = zombie_center[1] + random.randint(-50, 50)
                star = effects.StarEffect(star_x, star_y)
                self.special_effects.add(star)
                
        elif self.combo >= 5:
            # Great combo effects
            self.screen_shake.add_shake(10, 300)
            wave = effects.WaveEffect(zombie_center[0], zombie_center[1], const.ELECTRIC_BLUE)
            self.special_effects.add(wave)
            
            score_text = f"GREAT +{score_gain} x{self.combo}!"
            color = const.SCORE_COLORS[min(self.combo - 1, len(const.SCORE_COLORS) - 1)]
            floating_text = effects.FloatingText(zombie_center[0], zombie_center[1] - 20, 
                                       score_text, color, self.fonts['small'])
            self.floating_texts.add(floating_text)
            
            # Multiple stars
            for _ in range(5):
                star_x = zombie_center[0] + random.randint(-30, 30)
                star_y = zombie_center[1] + random.randint(-30, 30)
                star = effects.StarEffect(star_x, star_y)
                self.special_effects.add(star)
                
        else:
            # Normal hit effects
            self.screen_shake.add_shake(5, 200)
            score_text = f"+{score_gain}"
            if self.combo > 1:
                score_text += f" x{self.combo}"
            
            color = const.SCORE_COLORS[min(self.combo - 1, len(const.SCORE_COLORS) - 1)]
            floating_text = effects.FloatingText(zombie_center[0], zombie_center[1] - 20, 
                                       score_text, color, self.fonts['small'])
            self.floating_texts.add(floating_text)

    def spawn_background_stars(self):
        """Tạo sao trang trí nền"""
        current_time = pygame.time.get_ticks()
        if current_time - self.star_spawn_timer > const.STAR_SPAWN_INTERVAL:
            for _ in range(2):
                x = random.randint(0, const.WIDTH)
                y = random.randint(0, const.HEIGHT)
                star = effects.StarEffect(x, y)
                star.lifetime = 5000
                star.fade_rate = 1
                self.special_effects.add(star)
            self.star_spawn_timer = current_time

    def update(self):
        """Cập nhật trạng thái game"""
        if self.state == const.GAME_STATE_PLAYING and not self.game_over:
            self.all_sprites.update()
            self.particles.update()
            self.floating_texts.update()
            self.special_effects.update()
            self.screen_shake.update()
            self.spawn_zombie()
            self.spawn_background_stars()

            # Check game end time
            current_time = pygame.time.get_ticks()
            if current_time - self.timer_start_time > self.game_duration:
                self.game_over = True
                pygame.mixer.music.fadeout(1000)
                pygame.time.wait(1000)

            # Remove zombies that have exceeded their lifetime or been hit
            zombies_to_remove = []
            for zombie in self.zombies:
                if zombie.should_disappear():
                    if not zombie.hit:  # Zombie disappeared without being hit
                        self.misses += 1
                        self.combo = 0
                    zombies_to_remove.append(zombie)
            
            # Remove marked zombies
            for zombie in zombies_to_remove:
                self.zombies.remove(zombie)
                self.all_sprites.remove(zombie)

    def get_game_stats(self):
        """Lấy thống kê game hiện tại"""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'combo': self.combo,
            'max_combo': self.max_combo,
            'difficulty_level': self.difficulty_level,
            'timer_start_time': self.timer_start_time,
            'game_duration': self.game_duration
        }

    def handle_menu_events(self, event):
        """Xử lý sự kiện menu"""
        for button in self.menu_buttons:
            action = button.handle_event(event, self.sounds['click'])
            if action == "QUIT":
                return "QUIT"
            elif action is not None:
                break
        return None

    def handle_difficulty_events(self, event):
        """Xử lý sự kiện chọn độ khó"""
        for button in self.difficulty_buttons:
            action = button.handle_event(event, self.sounds['click'])
            if action is not None:
                break
        return None

    def handle_game_over_events(self, event, play_again_button, menu_button):
        """Xử lý sự kiện game over"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_again_button.rect.collidepoint(event.pos):
                if self.sounds['click']:
                    self.sounds['click'].play()
                self.set_state(const.GAME_STATE_DIFFICULTY)
            elif menu_button.rect.collidepoint(event.pos):
                if self.sounds['click']:
                    self.sounds['click'].play()
                self.set_state(const.GAME_STATE_MENU)

    def draw_splat_effects(self, game_surface):
        """Vẽ hiệu ứng máu cho zombie bị đánh"""
        for sprite in self.all_sprites:
            if isinstance(sprite, Zombie) and sprite.hit:
                current_time = pygame.time.get_ticks()
                splat_progress = min(1.0, (current_time - sprite.splat_time) / sprite.splat_duration)
                splat_scale = 1.0 + splat_progress * 0.8
                splat_rotation = splat_progress * 360
                
                scaled_splat = pygame.transform.scale(self.images['splat'], 
                                                    (int(self.images['splat'].get_width() * splat_scale),
                                                     int(self.images['splat'].get_height() * splat_scale)))
                rotated_splat = pygame.transform.rotate(scaled_splat, splat_rotation)
                splat_rect = rotated_splat.get_rect(center=sprite.rect.center)
                
                # Add multiple splat layers for depth
                for i in range(3):
                    layer_scale = splat_scale + i * 0.1
                    layer_alpha = max(0, 255 - i * 80 - int(splat_progress * 100))
                    layer_splat = pygame.transform.scale(self.images['splat'],
                                                       (int(self.images['splat'].get_width() * layer_scale),
                                                        int(self.images['splat'].get_height() * layer_scale)))
                    layer_splat.set_alpha(layer_alpha)
                    layer_rect = layer_splat.get_rect(center=sprite.rect.center)
                    game_surface.blit(layer_splat, layer_rect)
                
                game_surface.blit(rotated_splat, splat_rect)
