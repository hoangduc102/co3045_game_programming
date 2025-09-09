"""
Các hàm tiện ích cho Zombie Head Smash Game
"""

import pygame
import os
import constants as const

def init_pygame():
    """Khởi tạo Pygame và mixer"""
    pygame.init()
    pygame.mixer.init()

def create_screen():
    """Tạo màn hình game"""
    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption(const.WINDOW_TITLE)
    return screen

def load_fonts():
    """Tải và trả về các font chữ"""
    try:
        font_path = os.path.join(pygame.font.get_default_font())
        game_font_large = pygame.font.Font(font_path, const.FONT_SIZE_LARGE)
        game_font_medium = pygame.font.Font(font_path, const.FONT_SIZE_MEDIUM)
        game_font_small = pygame.font.Font(font_path, const.FONT_SIZE_SMALL)
    except Exception as e:
        print(f"Error loading font: {e}. Using default Pygame font.")
        game_font_large = pygame.font.Font(None, const.FONT_SIZE_LARGE)
        game_font_medium = pygame.font.Font(None, const.FONT_SIZE_MEDIUM)
        game_font_small = pygame.font.Font(None, const.FONT_SIZE_SMALL)
    
    return {
        'large': game_font_large,
        'medium': game_font_medium,
        'small': game_font_small
    }

def load_image(filename, scale_to=None, convert_alpha=True):
    """Tải hình ảnh với xử lý lỗi"""
    path = os.path.join(const.IMAGES_DIR, filename)
    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
        if scale_to:
            image = pygame.transform.scale(image, scale_to)
        return image
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        # Fallback image
        fallback = pygame.Surface(scale_to if scale_to else (50, 50), 
                                pygame.SRCALPHA if convert_alpha else 0)
        fallback.fill((128, 128, 128, 128) if convert_alpha else (128, 128, 128))
        pygame.draw.rect(fallback, const.RED, fallback.get_rect(), 2)
        return fallback

def load_images():
    """Tải tất cả hình ảnh cần thiết"""
    return {
        'background': load_image("background.png", (const.WIDTH, const.HEIGHT), False),
        'menu_background': load_image("menu_background.png", (const.WIDTH, const.HEIGHT), False),
        'zombie_head': load_image("zombie_head.png", const.ZOMBIE_IMAGE_SIZE),
        'splat': load_image("splat.png", const.SPLAT_IMAGE_SIZE),
        'button_normal': load_image("button_normal.png", const.BUTTON_SIZE),
        'button_hover': load_image("button_hover.png", const.BUTTON_SIZE)
    }

def load_sound(filename, volume=1.0):
    """Tải âm thanh với xử lý lỗi"""
    path = os.path.join(const.SOUNDS_DIR, filename)
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except pygame.error as e:
        print(f"Error loading sound {filename}: {e}")
        return None

def load_sounds():
    """Tải tất cả âm thanh cần thiết"""
    # Load background music
    try:
        pygame.mixer.music.load(os.path.join(const.SOUNDS_DIR, "background_music.mp3"))
        pygame.mixer.music.set_volume(const.BACKGROUND_MUSIC_VOLUME)
    except pygame.error as e:
        print(f"Error loading background music: {e}")
    
    # Load sound effects
    return {
        'splat': load_sound("splat_sound.wav", const.SPLAT_SOUND_VOLUME),
        'click': load_sound("click_sound.wav", const.CLICK_SOUND_VOLUME)
    }

def play_background_music():
    """Phát nhạc nền"""
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error playing background music: {e}")

def fade_out_music(fade_time=500):
    """Fade out nhạc nền"""
    try:
        pygame.mixer.music.fadeout(fade_time)
    except Exception as e:
        print(f"Error fading out music: {e}")

def clamp(value, min_value, max_value):
    """Giới hạn giá trị trong khoảng min_value đến max_value"""
    return max(min_value, min(value, max_value))

def distance(pos1, pos2):
    """Tính khoảng cách giữa hai điểm"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return (dx*dx + dy*dy) ** 0.5
