"""
Gameplay Interface Module for Snake Gen v11.5
Contains functions for game rendering and HUD management.
"""

import pygame
import numpy as np
import time
from ..game.config import *
from .ui_components import *


def calculate_game_stats(snakes, generation_start_time):
    """Calculate current game statistics from snake population."""
    best_score = max((snake.score for snake in snakes if snake.alive), default=0)
    best_length = max((snake.length for snake in snakes if snake.alive), default=0)
    avg_length = np.mean([snake.length for snake in snakes]) if snakes else 0
    elapsed_time = round(time.time() - generation_start_time, 2)
    
    return best_score, best_length, avg_length, elapsed_time


def draw_game_hud(surface, best_score, best_length, avg_length, elapsed_time):
    """Draw the top HUD bar with game statistics."""
    # Create sections for the top bar
    sections = [
        ("Time", f"{elapsed_time}s"),
        ("Length", best_length),
        ("Avg Len", f"{avg_length:.2f}"),
        ("Score", best_score)
    ]
    
    font = pygame.font.SysFont(None, 30)
    draw_top_bar(surface, sections, font, TOP_BAR_HEIGHT, BLACK, WHITE)


def draw_training_sidebar(surface, generation_lengths):
    """Draw the training mode sidebar with generation information."""
    font = pygame.font.SysFont(None, 30)
    text_x = WIDTH + 30
    text_y = 100
    
    title = "Generations"
    info_list = [f"- Gen {i}: {length}" for i, length in enumerate(generation_lengths)]
    
    draw_sidebar_info(surface, title, info_list, font, text_x, text_y, 
                     title_color=BLACK, text_color=GREEN)


def draw_pretrained_sidebar(surface, model_params):
    """Draw the pre-trained AI mode sidebar with parameter weights."""
    if model_params is None:
        return
        
    font = pygame.font.SysFont(None, 24)
    text_x = WIDTH + 2
    text_y = 100
    
    title = "Parameter Weights"
    info_list = []
    
    for i, (label, value) in enumerate(zip(AI_PARAMETER_LABELS, model_params)):
        info_list.append(f"{label}: {value:.2f}")
    
    draw_sidebar_info(surface, title, info_list, font, text_x, text_y,
                     title_color=BLACK, text_color=GREEN, line_spacing=22)


def draw_snakes_and_food(surface, snakes):
    """Draw all active snakes and their food."""
    for snake in snakes:
        if snake.alive:
            # Draw snake
            draw_snake(surface, snake.snake)
            # Draw food
            draw_food(surface, snake.food)


def draw_game(surface, snakes, generation_start_time, generation_lengths, 
              game_mode="train_ai", model_params=None, fps_clock=None):
    """Main game drawing function with improved modularity."""
    # Clear screen
    surface.fill(BACKGROUND_GRAY)
    
    # Calculate game statistics
    best_score, best_length, avg_length, elapsed_time = calculate_game_stats(snakes, generation_start_time)
    
    # Draw HUD
    draw_game_hud(surface, best_score, best_length, avg_length, elapsed_time)
    
    # Draw mode-specific sidebar
    if game_mode == "train_ai":
        draw_training_sidebar(surface, generation_lengths)
    elif game_mode == "pretrained_ai":
        draw_pretrained_sidebar(surface, model_params)
    
    # Draw game borders
    draw_game_border(surface)
    
    # Draw snakes and food
    draw_snakes_and_food(surface, snakes)
    
    # Update display
    pygame.display.flip()
    if fps_clock:
        fps_clock.tick(FPS)


def draw_snake_length_visualization(surface, snakes):
    """Display the length of the best snake visually on the right side of the screen."""
    bar_x = WIDTH + 50
    bar_y = 100
    bar_width = 20
    unit_height = 10
    spacing = 2
    
    best_length = max((snake.length for snake in snakes if snake.alive), default=0)
    
    for i in range(best_length):
        pygame.draw.rect(surface, GREEN, 
                        (bar_x, bar_y + i * (unit_height + spacing), bar_width, unit_height))