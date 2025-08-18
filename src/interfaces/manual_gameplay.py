import pygame
import sys
import time
from ..game.config import *
from ..core.snake_manual import ManualKeysSnake, get_manual_direction_from_key

# Initialize Pygame
pygame.init()

# Setup Game Window (Same size and layout as AI mode)
screen = pygame.display.set_mode((WIDTH, HEIGHT + TOP_BAR_HEIGHT))
pygame.display.set_caption("Snake - Manual Play (Arrow Keys)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# ManualKeysSnake class now imported from snake_manual.py


def draw_game(snake):
    screen.fill(BACKGROUND_GRAY)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH +
                     SIDE_BAR_WIDTH, TOP_BAR_HEIGHT))

    # **Display Score, Length, and Time**
    elapsed_time = round(time.time() - snake.start_time, 2)
    score_text = font.render(f"Score: {snake.score}", True, WHITE)
    time_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
    length_text = font.render(f"Length: {snake.length}", True, WHITE)

    # **Position Each Text in the Top Bar**
    section_width = WIDTH // 3
    screen.blit(score_text, (section_width * 0.2, 10))
    screen.blit(time_text, (section_width * 1.2, 10))
    screen.blit(length_text, (section_width * 2.2, 10))

    # ✅ **Adjust Food Border Radius to Match AI Mode**
    pygame.draw.rect(
        screen, RED, (snake.food[0] + 2, snake.food[1] + 2, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=5)

    # ✅ **Adjust Snake Border Radius to Match AI Mode**
    for segment in snake.snake:
        pygame.draw.rect(
            screen, GREEN, (segment[0] + 2, segment[1] + 2, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=5)

    # ✅ **Adjust Walls Border Radius to Match AI Mode**
    for wall in snake.border_walls:
        pygame.draw.rect(
            screen, BROWN, (wall[0], wall[1], CELL_SIZE, CELL_SIZE), border_radius=5)

    pygame.display.flip()


def show_game_over_screen(snake):
    """Display a game over screen with game results and wait for user input to either replay or return to menu."""
    screen.fill(BACKGROUND_GRAY)
    font_large = pygame.font.SysFont(None, 50)
    font_small = pygame.font.SysFont(None, 30)

    # **Game Over Message**
    game_over_text = font_large.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))

    # **Calculate Game Stats**
    elapsed_time = round(time.time() - snake.start_time, 2)
    stats_text = [
        f"Time: {elapsed_time}s",
        f"Score: {snake.score}",
        f"Length: {snake.length}",
    ]

    # **Display Game Stats**
    stats_start_y = HEIGHT // 2 - 80  # Move stats higher to avoid overlapping buttons
    for i, text in enumerate(stats_text):
        stat_render = font_small.render(text, True, BLACK)
        screen.blit(stat_render, (WIDTH // 2 - stat_render.get_width() // 2, stats_start_y + i * 30))

    # **Button Positions**
    button_width, button_height = 150, 50
    button_spacing = 20

    menu_button = pygame.Rect(WIDTH // 2 - button_width - button_spacing // 2, HEIGHT // 2 + 50, button_width, button_height)
    replay_button = pygame.Rect(WIDTH // 2 + button_spacing // 2, HEIGHT // 2 + 50, button_width, button_height)

    pygame.draw.rect(screen, BROWN, menu_button, border_radius=10)
    pygame.draw.rect(screen, GREEN, replay_button, border_radius=10)

    # **Render Button Text**
    menu_text = font_small.render("Menu", True, WHITE)
    replay_text = font_small.render("Replay", True, WHITE)
    screen.blit(menu_text, (menu_button.x + menu_button.width // 2 - menu_text.get_width() // 2,
                            menu_button.y + menu_button.height // 2 - menu_text.get_height() // 2))
    screen.blit(replay_text, (replay_button.x + replay_button.width // 2 - replay_text.get_width() // 2,
                              replay_button.y + replay_button.height // 2 - replay_text.get_height() // 2))

    pygame.display.flip()

    # **Wait for User Input**
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_button.collidepoint(pos):
                    return "menu"
                elif replay_button.collidepoint(pos):
                    return "replay"
    return "menu"


def run_manual_mode():
    snake = ManualKeysSnake()

    while snake.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle Key Press for Direction Change
            if event.type == pygame.KEYDOWN:
                snake.direction = get_manual_direction_from_key(event.key, snake.direction)

        snake.move()
        draw_game(snake)
        clock.tick(MANUAL_FPS)
    action = show_game_over_screen(snake)
    return action
