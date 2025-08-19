"""
Real-time Monitoring System Module for Snake Gen v12.0
Transformed interface for AI training visualization and monitoring.
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


def draw_monitoring_hud(surface, best_score, best_length, avg_length, elapsed_time, snakes, current_generation=1):
    """Draw the futuristic monitoring HUD with real-time data."""
    # Calculate additional monitoring metrics
    units_active = len([s for s in snakes if s.alive])
    total_units = len(snakes)
    
    # Enhanced monitoring sections with generation number instead of fitness
    sections = [
        ("TIME", f"{elapsed_time:.1f}s"),
        ("# GEN", str(current_generation)),
        ("UNITS", f"{units_active}/{total_units}"),
        ("LENGTH", str(best_length))
    ]
    
    font_hud = load_retro_font(12)  # Smaller font to fit in grid sections
    draw_top_bar(surface, sections, font_hud, TOP_BAR_HEIGHT, DARK_BG, NEON_CYAN)
    
    # Add scan lines for retro monitoring effect
    hud_surface = pygame.Surface((surface.get_width(), TOP_BAR_HEIGHT), pygame.SRCALPHA)
    draw_scan_lines(hud_surface, line_spacing=3, line_alpha=25, animate=True)
    surface.blit(hud_surface, (0, 0))


def draw_neural_monitoring_panel(surface, generation_lengths, snakes):
    """Draw enhanced neural network monitoring panel."""
    panel_x = WIDTH + 10  # Move closer to game area
    panel_y = GAME_AREA_Y  # Align with game area top border
    panel_width = SIDE_BAR_WIDTH - 20  # Slightly wider by reducing margins
    panel_height = GAME_AREA_HEIGHT  # Match game area height for consistent borders
    
    # Draw panel background with glow
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    draw_glow_rect(surface, panel_rect, ELECTRIC_PURPLE, glow_radius=4, 
                   glow_alpha=60, border_radius=8)
    
    # Panel interior
    inner_rect = pygame.Rect(panel_x + 3, panel_y + 3, panel_width - 6, panel_height - 6)
    inner_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(inner_surface, (*DARK_BG, 200), (0, 0, inner_rect.width, inner_rect.height), 
                    border_radius=5)
    surface.blit(inner_surface, inner_rect.topleft)
    
    # Title
    font_title = load_retro_font(14)
    title_surface = font_title.render("GENERATIONS", True, NEON_CYAN)
    title_x = panel_x + panel_width // 2 - title_surface.get_width() // 2
    surface.blit(title_surface, (title_x, panel_y + 10))
    
    # Generation data
    font_data = load_retro_font(10)
    current_y = panel_y + 35
    
    # Show recent generations (more due to matching game area height)
    max_generations = (panel_height - 60) // 16  # Calculate based on available space
    recent_gens = generation_lengths[-max_generations:] if len(generation_lengths) > max_generations else generation_lengths
    for i, length in enumerate(recent_gens):
        gen_num = len(generation_lengths) - len(recent_gens) + i + 1
        text = f"GEN {gen_num:02d}: {length:03d}"
        color = NEON_GREEN if i == len(recent_gens) - 1 else NEON_BLUE
        
        text_surface = font_data.render(text, True, color)
        surface.blit(text_surface, (panel_x + 10, current_y))
        current_y += 16
    
    # Add circuit pattern overlay
    circuit_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    draw_circuit_pattern(circuit_surface, grid_size=20, line_color=NEON_CYAN, 
                        line_alpha=15, animate=True)
    surface.blit(circuit_surface, (panel_x, panel_y))


def draw_ai_unit_diagnostics(surface, model_params, snake=None):
    """Draw enhanced AI unit diagnostic panel with improved layout."""
    if model_params is None:
        return
        
    # Center the panel both horizontally and vertically in the right side
    total_width = WIDTH + SIDE_BAR_WIDTH
    total_height = HEIGHT + TOP_BAR_HEIGHT
    panel_width = SIDE_BAR_WIDTH - 10  # Make wider to fit title properly
    panel_height = 280  # Reduced height since removing ACTIVE status
    panel_x = WIDTH + (SIDE_BAR_WIDTH - panel_width) // 2  # Center in sidebar area
    # Center vertically on the page
    panel_y = TOP_BAR_HEIGHT + (HEIGHT - panel_height) // 2
    
    # Draw diagnostic panel background
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    draw_glow_rect(surface, panel_rect, NEON_MAGENTA, glow_radius=4, 
                   glow_alpha=60, border_radius=8)
    
    # Panel interior
    inner_rect = pygame.Rect(panel_x + 3, panel_y + 3, panel_width - 6, panel_height - 6)
    inner_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(inner_surface, (*DARK_BG, 200), (0, 0, inner_rect.width, inner_rect.height), 
                    border_radius=5)
    surface.blit(inner_surface, inner_rect.topleft)
    
    # Updated title to 'HYPERPARAMETERS'
    font_title = load_retro_font(12)
    title_surface = font_title.render("HYPERPARAMETERS", True, NEON_MAGENTA)
    title_x = panel_x + panel_width // 2 - title_surface.get_width() // 2
    surface.blit(title_surface, (title_x, panel_y + 8))
    
    # Clean hyperparameters layout without separators or bars
    font_param = load_retro_font(9)
    current_y = panel_y + 28  # Start closer to title
    
    param_labels = [
        "Food Bonus", "Toward Food", "Away Penalty", "Loop Penalty",
        "Survival", "Wall Penalty", "Exploration", "Momentum", "Dead-End"
    ]
    
    for i, (label, value) in enumerate(zip(param_labels, model_params)):
        # Parameter name
        param_text = f"{label}:"
        param_surface = font_param.render(param_text, True, NEON_ORANGE)
        surface.blit(param_surface, (panel_x + 5, current_y))
        
        # Parameter value positioned right after parameter text
        value_color = NEON_GREEN if value > 0 else UI_DANGER if value < -1 else NEON_CYAN
        value_text = f"{value:+.2f}"
        value_surface = font_param.render(value_text, True, value_color)
        # Position value right after the parameter text
        param_text_width = param_surface.get_width()
        value_x = panel_x + 5 + param_text_width + 5  # 5px gap after parameter text
        surface.blit(value_surface, (value_x, current_y))
        
        current_y += 24  # Standard spacing
    
    # Removed ACTIVE status section as requested


def draw_enhanced_game_area(surface, snakes):
    """Draw enhanced game area with monitoring system styling."""
    # Game area border with enhanced glow
    border_rect = pygame.Rect(GAME_AREA_X - 5, GAME_AREA_Y - 5, 
                             GAME_AREA_WIDTH + 10, GAME_AREA_HEIGHT + 10)
    draw_glow_rect(surface, border_rect, NEON_CYAN, glow_radius=4, 
                   glow_alpha=80, border_radius=12)
    
    # Interior game area
    game_rect = pygame.Rect(GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
    game_surface = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(game_surface, (*DARK_BG, 180), (0, 0, GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
    surface.blit(game_surface, game_rect.topleft)
    
    # Add subtle scan lines to game area
    scan_surface = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT), pygame.SRCALPHA)
    draw_scan_lines(scan_surface, line_spacing=8, line_alpha=15, animate=True)
    surface.blit(scan_surface, game_rect.topleft)

def draw_enhanced_ai_units(surface, snakes):
    """Draw AI units with enhanced neon visualization."""
    for i, snake in enumerate(snakes):
        if snake.alive:
            # Enhanced snake with unit-specific colors
            unit_color = NEON_GREEN if i == 0 else MATRIX_GREEN  # Lead unit gets special color
            draw_enhanced_snake(surface, snake.snake, unit_color, snake.alive)
            
            # Enhanced food with pulsing effect
            food_center = (snake.food[0] + CELL_SIZE // 2, snake.food[1] + CELL_SIZE // 2)
            food_radius = CELL_SIZE // 2 - 2
            pulse_alpha = get_pulse_alpha(100)
            draw_glow_circle(surface, food_center, food_radius, CYBER_PINK, 
                           glow_radius=GLOW_RADIUS_INNER, glow_alpha=pulse_alpha)

def draw_enhanced_snake(surface, snake_segments, unit_color, is_alive):
    """Draw individual AI unit with enhanced visual effects."""
    alpha_modifier = 1.0 if is_alive else 0.3
    
    for i, segment in enumerate(snake_segments):
        segment_rect = pygame.Rect(segment[0] + GAP, segment[1] + GAP, 
                                  CELL_SIZE - GAP * 2, CELL_SIZE - GAP * 2)
        
        # Head gets special treatment
        if i == 0:
            head_color = tuple(int(c * alpha_modifier) for c in unit_color)
            draw_glow_rect(surface, segment_rect, head_color, 
                          glow_radius=4, glow_alpha=int(120 * alpha_modifier), border_radius=5)
            
            # Add directional indicator on head
            center_x = segment_rect.centerx
            center_y = segment_rect.centery
            pygame.draw.circle(surface, WHITE, (center_x, center_y), 2)
        else:
            # Body segments with gradient fade
            fade_alpha = max(int((100 - i * 3) * alpha_modifier), int(40 * alpha_modifier))
            body_color = tuple(int(c * alpha_modifier) for c in unit_color)
            draw_glow_rect(surface, segment_rect, body_color, 
                          glow_radius=2, glow_alpha=fade_alpha, border_radius=5)


def draw_monitoring_background(surface):
    """Draw the real-time monitoring system background."""
    surface.fill(DARK_BG)
    
    # Draw circuit pattern for monitoring aesthetic
    draw_circuit_pattern(surface, grid_size=50, line_color=NEON_BLUE, 
                        line_alpha=20, animate=True)
    
    # Add data grid overlay
    draw_grid_overlay(surface, grid_size=30, line_color=NEON_CYAN, line_alpha=12)
    
    # Draw animated data streams
    draw_animated_lines(surface, num_lines=2, line_color=MATRIX_GREEN, speed=0.5)

def draw_game(surface, snakes, generation_start_time, generation_lengths, 
              game_mode="train_ai", model_params=None, fps_clock=None, current_generation=1):
    """Enhanced real-time monitoring system interface."""
    # Draw monitoring background
    draw_monitoring_background(surface)
    
    # Calculate game statistics
    best_score, best_length, avg_length, elapsed_time = calculate_game_stats(snakes, generation_start_time)
    
    # Draw HUD
    draw_monitoring_hud(surface, best_score, best_length, avg_length, elapsed_time, snakes, current_generation)
    
    # Draw mode-specific monitoring panels
    if game_mode == "train_ai":
        draw_neural_monitoring_panel(surface, generation_lengths, snakes)
    
    if game_mode == "pretrained_ai" and model_params:
        active_snake = next((s for s in snakes if s.alive), snakes[0] if snakes else None)
        draw_ai_unit_diagnostics(surface, model_params, active_snake)
    
    # Draw enhanced game area
    draw_enhanced_game_area(surface, snakes)
    
    # Draw enhanced AI units
    draw_enhanced_ai_units(surface, snakes)
    
    # Add energy nodes for monitoring system aesthetic
    node_positions = [
        (30, TOP_BAR_HEIGHT + 30), (30, surface.get_height() - 30),
        (WIDTH - 30, TOP_BAR_HEIGHT + 30), (WIDTH - 30, surface.get_height() - 30)
    ]
    draw_energy_nodes(surface, node_positions, ELECTRIC_PURPLE, pulse=True)
    
    # Overall scan lines for retro monitoring effect
    draw_scan_lines(surface, line_spacing=15, line_alpha=8, animate=True)
    
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