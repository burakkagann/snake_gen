from src.interfaces.menu import menu_screen
from src.interfaces.manual_gameplay import run_manual_mode
from src.core.snake_manual import ManualKeysSnake
from src.core.snake_ai import SnakeAI, evolve_snakes, log_and_print
from src.interfaces.training_interface import get_training_parameters, show_pretrained_models
from src.interfaces.gameplay_interface import draw_game
from src.game.game_modes import (handle_manual_mode, handle_training_mode, 
                                handle_pretrained_mode, handle_quit_mode)
import pygame
import random
import numpy as np
import time
import sys
from src.game.config import *

sys.stdout.reconfigure(encoding='utf-8')
# Initialize Pygame
pygame.init()

# All constants now imported from config.py

# Screen Configurations
screen = pygame.display.set_mode(
    (WIDTH + SIDE_BAR_WIDTH, HEIGHT + TOP_BAR_HEIGHT))
pygame.display.set_caption("Gen Snake")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont(None, 30)

background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)

# Set screen reference for training interface
from src.interfaces import training_interface
training_interface.screen = screen

# Global Time Tracker for Generations
generation_start_time = time.time()
best_score_overall = 0
best_length_overall = 0
# Track learning metrics across generations
generation_fitness = []
generation_avg_fitness = []
generation_lengths = []
generation_avg_lengths = []


# Configuration now imported from config.py

# SnakeAI class now imported from snake_ai.py


def draw_snake_length_visualization():
    """Displays the length of the best snake visually on the right side of the screen."""
    bar_x = WIDTH + 50  # Position to the right of the game area
    bar_y = 100  # Start position for visualization
    bar_width = 20  # Width of each unit in visualization
    unit_height = 10  # Height of each unit
    spacing = 2  # Space between units

    best_length = max(
        (snake.length for snake in snakes if snake.alive), default=0)

    for i in range(best_length):
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y + i *
                         (unit_height + spacing), bar_width, unit_height))


# draw_game function moved to gameplay_interface.py


def run_generation():
    global snakes, generation_start_time, best_score_overall, best_length_overall
    generation_start_time = time.time()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        alive_snakes = [s for s in snakes if s.alive]
        if not alive_snakes:
            break  # Stop the generation if all snakes are dead

        for snake in alive_snakes:
            snake.move()

        draw_game(screen, snakes, generation_start_time, generation_lengths, 
                  "train_ai", None, clock)

    # **Calculate Key Metrics**
    best_snake = max(snakes, key=lambda s: s.fitness_function(), default=None)
    if best_snake is not None:
        # If this generation's snake is better, update overall
        if best_snake.score > best_score_overall:
            best_score_overall = best_snake.score
        if best_snake.length > best_length_overall:
            best_length_overall = best_snake.length
    best_fitness = best_snake.fitness_function() if best_snake else 0
    avg_fitness = np.mean([snake.fitness_function() for snake in snakes])

    best_length = max((snake.length for snake in snakes), default=0)
    avg_length = np.mean([snake.length for snake in snakes])

    # **Retrieve Best Snake's Weights (Brain Parameters)**
    best_weights = best_snake.brain if best_snake else np.zeros(9)

    # **Print Generation Summary**
    log_and_print("=" * 50)
    log_and_print(f" Generation {len(generation_fitness) + 1} Summary ")
    log_and_print("=" * 50)
    log_and_print(f" Best Fitness Score: {best_fitness:.2f}")
    log_and_print(f" Average Fitness Score: {avg_fitness:.2f}")
    log_and_print(f" Best Length Achieved: {best_length}")
    log_and_print(f" Average Length of Snakes: {avg_length:.2f}")
    log_and_print("-" * 50)
    log_and_print(" Inherited Weights (Brain Parameters)")
    log_and_print(f"  - Food Bonus Weight: {best_weights[0]:.3f}")
    log_and_print(f"  - Toward Food Weight: {best_weights[1]:.3f}")
    log_and_print(f"  - Away Food Penalty: {best_weights[2]:.3f}")
    log_and_print(f"  - Loop Penalty: {best_weights[3]:.3f}")
    log_and_print(f"  - Survival Bonus: {best_weights[4]:.3f}")
    log_and_print(f"  - Wall Penalty: {best_weights[5]:.3f}")
    log_and_print(f"  - Exploration Bonus: {best_weights[6]:.3f}")
    log_and_print(f"  - Momentum Bonus: {best_weights[7]:.3f}")
    log_and_print(f"  - Dead-End Penalty: {best_weights[8]:.3f}")
    log_and_print("=" * 50)

    # **Store Data for Future Analysis**
    generation_fitness.append(best_fitness)
    generation_avg_fitness.append(avg_fitness)
    generation_lengths.append(best_length)

    # **Evolve Snakes for Next Generation**
    snakes = evolve_snakes(snakes, generation_fitness)


# Genetic algorithm functions now imported from snake_ai.py



snakes = [SnakeAI() for _ in range(DEFAULT_SNAKE_POPULATION)]


def show_game_over_screen(snake, mode="manual"):
    screen.fill(BACKGROUND_GRAY)
    font_large = pygame.font.SysFont(None, 50)
    font_small = pygame.font.SysFont(None, 30)

    # **Game Over Message**
    game_over_text = font_large.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 -
                game_over_text.get_width() // 2, HEIGHT // 3))

    # **Display Final Score, Time, and Length**
    elapsed_time = round(time.time() - snake.start_time, 2)
    stats_text = [
        f"Time: {elapsed_time}s",
        f"Score: {snake.score}",
        f"Length: {snake.length}"
    ]

    stats_start_y = HEIGHT // 2 - 70  # Move stats up
    for i, text in enumerate(stats_text):
        stat_render = font_small.render(text, True, BLACK)
        screen.blit(stat_render, (WIDTH // 2 - stat_render.get_width() // 2, stats_start_y + i * 35))  # Adjust line spacing


    # **Button Positions**
    button_width, button_height = 150, 50
    button_spacing = 20
    button_y = HEIGHT // 1.4

    # **New Menu Button**
    menu_button = pygame.Rect(WIDTH // 2 - button_width * 1.5 -
                              button_spacing, button_y, button_width, button_height)
    replay_button = pygame.Rect(
        WIDTH // 2 - button_width // 2, button_y, button_width, button_height)
    quit_button = pygame.Rect(WIDTH // 2 + button_width // 2 +
                              button_spacing, button_y, button_width, button_height)

    pygame.draw.rect(screen, BROWN, menu_button, border_radius=10)
    pygame.draw.rect(screen, GREEN, replay_button, border_radius=10)
    pygame.draw.rect(screen, RED, quit_button, border_radius=10)

    # **Render Button Text**
    menu_text = font_small.render("Menu", True, WHITE)
    replay_text = font_small.render("Replay", True, WHITE)
    quit_text = font_small.render("Quit", True, WHITE)

    screen.blit(menu_text, (menu_button.x + button_width // 2 - menu_text.get_width() // 2,
                            menu_button.y + button_height // 2 - menu_text.get_height() // 2))
    screen.blit(replay_text, (replay_button.x + button_width // 2 - replay_text.get_width() // 2,
                              replay_button.y + button_height // 2 - replay_text.get_height() // 2))
    screen.blit(quit_text, (quit_button.x + button_width // 2 - quit_text.get_width() // 2,
                            quit_button.y + button_height // 2 - quit_text.get_height() // 2))

    pygame.display.flip()

    # **Wait for User Input**
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    return "menu"  # Return to Main Menu
                elif replay_button.collidepoint(event.pos):
                    return mode  # Restart same mode (manual or pretrained AI)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# get_training_parameters function moved to training_interface.py


# show_pretrained_models function moved to training_interface.py



def show_training_summary(best_score, best_length, training_time):
    screen.fill(BACKGROUND_GRAY)
    font_large = pygame.font.SysFont(None, 50)
    font_small = pygame.font.SysFont(None, 30)

    # Title
    title_text = font_large.render("Training Complete", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 -
                title_text.get_width() // 2, HEIGHT // 3))

    # Stats
    stats_text = [
        f"Final Best Score: {best_score_overall}",
        f"Final Best Length: {best_length_overall}",
        f"Total Training Time: {training_time:.2f}s"
    ]
    stats_start_y = HEIGHT // 2 - 40
    for i, text_line in enumerate(stats_text):
        stat_render = font_small.render(text_line, True, BLACK)
        screen.blit(stat_render, (WIDTH // 2 - stat_render.get_width() // 2,
                                  stats_start_y + i * 40))

    # --- Define Buttons in a Single Pass ---
    button_width = 120
    button_height = 40
    button_spacing = 20

    # total width for 4 buttons = 4 * button_width + 3 * button_spacing
    total_button_width = 4 * button_width + 3 * button_spacing
    start_x = (WIDTH - total_button_width) // 2
    y = int(HEIGHT * 0.75)  # 75% down the screen

    # Create rects side by side
    menu_button = pygame.Rect(start_x, y, button_width, button_height)
    pretrain_button = pygame.Rect(
        start_x + (button_width + button_spacing), y, button_width, button_height
    )
    replay_button = pygame.Rect(
        start_x + 2*(button_width +
                     button_spacing), y, button_width, button_height
    )
    quit_button = pygame.Rect(
        start_x + 3*(button_width +
                     button_spacing), y, button_width, button_height
    )

    # Draw them
    pygame.draw.rect(screen, BROWN, menu_button, border_radius=10)
    pygame.draw.rect(screen, BLUE, pretrain_button, border_radius=10)
    pygame.draw.rect(screen, GREEN, replay_button, border_radius=10)
    pygame.draw.rect(screen, RED, quit_button, border_radius=10)

    # Button text
    def draw_button_text(rect, text):
        text_surf = font_small.render(text, True, WHITE)
        screen.blit(text_surf, (rect.x + rect.width // 2 - text_surf.get_width() // 2,
                                rect.y + rect.height // 2 - text_surf.get_height() // 2))

    draw_button_text(menu_button, "Menu")
    draw_button_text(pretrain_button, "Pre-Train")
    draw_button_text(replay_button, "Replay")
    draw_button_text(quit_button, "Quit")

    pygame.display.flip()

    # --- Wait for Clicks ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    return "menu"
                elif pretrain_button.collidepoint(event.pos):
                    return "pretrain"
                elif replay_button.collidepoint(event.pos):
                    return "replay"
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def run_pretrained_from_training(weights):
    print("Starting Pre-Trained AI Mode with Best Weights from Training...")
    run_pretrained_ai(weights)


def run_pretrained_ai(model_params):
    global snakes  # Ensure we update the global variable

    snake = SnakeAI(brain=model_params)
    snakes = [snake]  # Only one snake should be in the list

    running = True
    while running and snake.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        snake.move()  # Ensure move() is executed
        draw_game(screen, snakes, generation_start_time, generation_lengths,
                  "pretrained_ai", model_params, clock)

    # **Show Game Over Screen and Handle Replay**
    action = show_game_over_screen(snake, mode="model_selection")
    if action == "model_selection":
        # Return to Pre-Trained Model Selection
        model_name, model_params = show_pretrained_models()
        run_pretrained_ai(model_params)  # Restart with selected model
    elif action == "menu":
        selection = menu_screen()  # Return to main menu


# **Show the menu before running the game**
def main():
    """Main game loop with simplified mode handling."""
    while True:
        selection = menu_screen()

        if selection == "manual":
            handle_manual_mode()

        elif selection == "train":
            result = handle_training_mode(
                best_score_overall, best_length_overall,
                generation_fitness, generation_avg_fitness,
                generation_lengths, generation_avg_lengths,
                run_generation, show_training_summary,
                run_pretrained_from_training
            )
            if result == "menu":
                continue  # Return to main menu

        elif selection == "pretrained":
            handle_pretrained_mode(run_pretrained_ai)

        elif selection == "quit":
            handle_quit_mode()


if __name__ == "__main__":
    main()
