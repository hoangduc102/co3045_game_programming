"""
Constants và cấu hình cho Zombie Head Smash Game
"""

import os

# --- Screen Setup ---
WIDTH, HEIGHT = 800, 600
WINDOW_TITLE = "Zombie Head Smash"

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
NEON_GREEN = (57, 255, 20)
ELECTRIC_BLUE = (125, 249, 255)
HOT_PINK = (255, 20, 147)
GOLD = (255, 215, 0)

# Gradient color arrays for various effects
SCORE_COLORS = [GREEN, YELLOW, ORANGE, RED, PURPLE, CYAN, HOT_PINK, GOLD]
BLOOD_RED = (139, 0, 0)
ZOMBIE_GREEN = (34, 139, 34)
RAINBOW_COLORS = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, HOT_PINK]

# --- Đường dẫn tài nguyên ---
CURRENT_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(CURRENT_DIR, "images")
SOUNDS_DIR = os.path.join(CURRENT_DIR, "sounds")

# --- Vị trí xuất hiện zombie ---
ZOMBIE_SPAWN_POINTS = [
    (100, 150), (350, 150), (600, 150),
    (100, 300), (350, 300), (600, 300),
    (100, 450), (350, 450), (600, 450)
]

# --- Font sizes ---
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 24

# --- Game settings ---
DEFAULT_FPS = 60
COMBO_TIME_WINDOW = 2000  # 2 seconds for combo
MAX_TRAIL_LENGTH = 15

# --- Difficulty settings ---
DIFFICULTY_SETTINGS = {
    "CLASSIC": {
        "game_duration": 120 * 1000,  # 120 seconds
        "zombie_speed_multiplier": 0,  # Zombies don't disappear automatically
        "max_zombies_on_screen": 3,
        "spawn_interval_min": 2000,
        "spawn_interval_max": 4000
    },
    "EASY": {
        "game_duration": 75 * 1000,  # 75 seconds
        "zombie_speed_multiplier": 0.8,  # Zombies live longer
        "max_zombies_on_screen": 4,
        "spawn_interval_min": 1500,
        "spawn_interval_max": 2500
    },
    "MEDIUM": {
        "game_duration": 60 * 1000,  # 60 seconds
        "zombie_speed_multiplier": 1.0,
        "max_zombies_on_screen": 5,
        "spawn_interval_min": 1000,
        "spawn_interval_max": 2000
    },
    "HARD": {
        "game_duration": 45 * 1000,  # 45 seconds
        "zombie_speed_multiplier": 1.2,  # Zombies live shorter
        "max_zombies_on_screen": 6,
        "spawn_interval_min": 700,
        "spawn_interval_max": 1500
    }
}

# --- Zombie settings ---
ZOMBIE_IMAGE_SIZE = (70, 70)
ZOMBIE_POP_ANIMATION_DURATION = 300  # ms
ZOMBIE_SPLAT_DURATION = 400  # ms
ZOMBIE_WARNING_TIME = 500  # ms before disappearing

# --- Splat settings ---
SPLAT_IMAGE_SIZE = (80, 80)

# --- Button settings ---
BUTTON_SIZE = (200, 70)

# --- Particle settings ---
PARTICLE_SIZE = (4, 4)
PARTICLE_GRAVITY = 0.2
BLOOD_PARTICLE_COUNT_BASE = 20
BLOOD_PARTICLE_COUNT_COMBO_BONUS = 3
BLOOD_PARTICLE_COUNT_MAX = 50

# --- Effect settings ---
EXPLOSION_MAX_RADIUS = 60
EXPLOSION_GROWTH_RATE = 3
EXPLOSION_FADE_RATE = 15

WAVE_MAX_RADIUS = 100
WAVE_SPEED = 4
WAVE_COUNT = 3
WAVE_FADE_RATE = 8

STAR_SPAWN_INTERVAL = 3000  # Every 3 seconds
STAR_SIZE_MIN = 2
STAR_SIZE_MAX = 6
STAR_ROTATION_SPEED_MIN = 2
STAR_ROTATION_SPEED_MAX = 8

# --- Sound settings ---
BACKGROUND_MUSIC_VOLUME = 0.5
SPLAT_SOUND_VOLUME = 0.8
CLICK_SOUND_VOLUME = 0.7

# --- Game states ---
GAME_STATE_MENU = "MENU"
GAME_STATE_DIFFICULTY = "DIFFICULTY"
GAME_STATE_PLAYING = "PLAYING"
GAME_STATE_GAME_OVER = "GAME_OVER"
