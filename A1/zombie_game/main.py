"""
Entry point for Zombie Head Smash (modularized).
Uses: constants.py, utils.py, ui.py, game.py, effects.py, zombie.py
"""

import pygame
import constants as const
from utils import init_pygame, create_screen, load_fonts, load_images, load_sounds
from game import Game
from ui import Button, UIRenderer  # Button for game-over actions

def draw_menu(screen, game: Game):
    # Background
    screen.blit(game.images['menu_background'], (0, 0))
    # Title
    game.ui_renderer.draw_menu_title(screen, "Zombie Head Smash")
    # Buttons
    for btn in game.menu_buttons:
        btn.draw(screen)

def draw_difficulty(screen, game: Game):
    screen.blit(game.images['menu_background'], (0, 0))
    game.ui_renderer.draw_menu_title(screen, "Choose Difficulty")
    for btn in game.difficulty_buttons:
        btn.draw(screen)

def draw_playing(screen, game: Game):
    # Separate surface so we can apply screen shake only to gameplay layer
    game_surface = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)

    # Background
    game_surface.blit(game.images['background'], (0, 0))

    # Sprites
    for sprite in game.all_sprites:
        game_surface.blit(sprite.image, sprite.rect)

    # Enhanced splat layers for hit zombies
    game.draw_splat_effects(game_surface)

    # Effects layers
    for group in (game.special_effects, game.particles, game.floating_texts):
        for sprite in group:
            game_surface.blit(sprite.image, sprite.rect)

    # Apply screen shake
    shake_offset = game.screen_shake.get_offset()
    screen.blit(game_surface, shake_offset)

    # UI (not affected by shake)
    game.ui_renderer.draw_enhanced_ui(screen, game.get_game_stats())

    # Mouse trail
    mouse_pos = pygame.mouse.get_pos()
    game.mouse_trail.update(mouse_pos)
    game.mouse_trail.draw(screen, combo=game.combo)

def draw_game_over(screen, game: Game):
    # Dim overlay + stats
    game.ui_renderer.draw_game_over_screen(screen, game.get_game_stats())

    # Action buttons
    play_again_button = Button(
        const.WIDTH // 2 - 100, const.HEIGHT // 2 + 70, 200, 70,
        "Play Again", game.fonts['medium'],
        action=lambda: game.set_state(const.GAME_STATE_DIFFICULTY),
        normal_image=game.images['button_normal'], hover_image=game.images['button_hover']
    )
    menu_button = Button(
        const.WIDTH // 2 - 100, const.HEIGHT // 2 + 150, 200, 70,
        "Main Menu", game.fonts['medium'],
        action=lambda: game.set_state(const.GAME_STATE_MENU),
        normal_image=game.images['button_normal'], hover_image=game.images['button_hover']
    )

    play_again_button.draw(screen)
    menu_button.draw(screen)

    return play_again_button, menu_button

def main():
    init_pygame()
    screen = create_screen()
    clock = pygame.time.Clock()

    # Assets
    fonts = load_fonts()
    images = load_images()
    sounds = load_sounds()

    # Game instance
    game = Game(fonts, images, sounds)

    # Start background music (menu)
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    except Exception:
        pass

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # ESC: back to menu (or quit if already at menu)
                if game.state == const.GAME_STATE_MENU:
                    running = False
                else:
                    game.set_state(const.GAME_STATE_MENU)
            else:
                # Delegate state-specific event handling
                if game.state == const.GAME_STATE_MENU:
                    if game.handle_menu_events(event) == "QUIT":
                        running = False
                elif game.state == const.GAME_STATE_DIFFICULTY:
                    game.handle_difficulty_events(event)
                elif game.state == const.GAME_STATE_PLAYING and not game.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        game.handle_click(event.pos)

        # Update
        game.update()

        # Render
        if game.state == const.GAME_STATE_MENU:
            draw_menu(screen, game)
        elif game.state == const.GAME_STATE_DIFFICULTY:
            draw_difficulty(screen, game)
        elif game.state == const.GAME_STATE_PLAYING:
            # Gameplay layer
            draw_playing(screen, game)
            # If game over, draw overlay + buttons and process their events
            if game.game_over:
                play_again_btn, menu_btn = draw_game_over(screen, game)
                # Handle clicks on these buttons for current frame
                for event in events:
                    game.handle_game_over_events(event, play_again_btn, menu_btn)

        pygame.display.flip()
        clock.tick(const.DEFAULT_FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
