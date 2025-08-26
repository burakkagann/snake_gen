import pygame
import sys
import time
import math
from ..game.config import *
from ..core.snake_manual import ManualKeysSnake, get_manual_direction_from_key
from .ui_components import *

# Initialize Pygame
pygame.init()

# Setup Game Window (Enhanced Mission Control with Sidebar)
screen = pygame.display.set_mode((WIDTH + SIDE_BAR_WIDTH, HEIGHT + TOP_BAR_HEIGHT))
pygame.display.set_caption("SNAKE GEN - MISSION CONTROL")
clock = pygame.time.Clock()

# Enhanced Fonts
font_hud = load_retro_font(20)
font_status = load_retro_font(16)
font_large = load_retro_font(32)

# ManualKeysSnake class now imported from snake_manual.py


def draw_mission_control_background():
    """Draw the mission control background with technical aesthetics."""
    # Fill with deep space background
    screen.fill(DARK_BG)
    
    # Draw subtle circuit pattern in background
    draw_circuit_pattern(screen, grid_size=80, line_color=NEON_BLUE, 
                        line_alpha=20, animate=True)
    
    # Add grid overlay for technical look
    draw_grid_overlay(screen, grid_size=40, line_color=NEON_CYAN, line_alpha=10)


def draw_enhanced_monitoring_hud(snake):
    """Draw the enhanced monitoring HUD matching AI training format."""
    elapsed_time = round(time.time() - snake.start_time, 2)
    
    # Calculate efficiency metric
    efficiency = (snake.score / max(elapsed_time, 1)) * 100 if elapsed_time > 0 else 0
    
    # Enhanced monitoring sections with shorter labels matching AI training
    hud_sections = [
        ("TIME", f"{elapsed_time:.1f}s"),
        ("SCORE", str(snake.score)),
        ("LENGTH", str(snake.length)),
        ("EFFICIENCY", f"{efficiency:.1f}%")
    ]
    
    # Use smaller font matching AI training interface
    font_hud_small = load_retro_font(12)
    draw_top_bar(screen, hud_sections, font_hud_small, TOP_BAR_HEIGHT, DARK_BG, NEON_CYAN)
    
    # Add scan lines to HUD for retro effect
    hud_surface = pygame.Surface((WIDTH + SIDE_BAR_WIDTH, TOP_BAR_HEIGHT), pygame.SRCALPHA)
    draw_scan_lines(hud_surface, line_spacing=4, line_alpha=20, animate=True)
    screen.blit(hud_surface, (0, 0))


def draw_enhanced_game_area(snake):
    """Draw enhanced game area with monitoring system styling matching AI training."""
    # Game area border with enhanced glow (matching AI training)
    border_rect = pygame.Rect(GAME_AREA_X - 5, GAME_AREA_Y - 5, 
                             GAME_AREA_WIDTH + 10, GAME_AREA_HEIGHT + 10)
    draw_glow_rect(screen, border_rect, NEON_CYAN, glow_radius=4, 
                   glow_alpha=80, border_radius=12)
    
    # Interior game area with semi-transparent overlay
    game_rect = pygame.Rect(GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
    game_surface = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(game_surface, (*DARK_BG, 180), (0, 0, GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
    screen.blit(game_surface, game_rect.topleft)
    
    # Add subtle scan lines to game area
    scan_surface = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT), pygame.SRCALPHA)
    draw_scan_lines(scan_surface, line_spacing=8, line_alpha=15, animate=True)
    screen.blit(scan_surface, game_rect.topleft)

def draw_enhanced_player_snake(snake):
    """Draw player snake with enhanced neon visualization matching AI training."""
    # Enhanced snake with player-specific colors
    for i, segment in enumerate(snake.snake):
        segment_rect = pygame.Rect(segment[0] + GAP, segment[1] + GAP, 
                                  CELL_SIZE - GAP * 2, CELL_SIZE - GAP * 2)
        
        # Head gets special treatment with directional indicator
        if i == 0:
            draw_glow_rect(screen, segment_rect, MATRIX_GREEN, 
                          glow_radius=4, glow_alpha=120, border_radius=5)
            
            # Add directional indicator on head
            center_x = segment_rect.centerx
            center_y = segment_rect.centery
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 2)
        else:
            # Body segments with gradient fade
            fade_alpha = max(100 - i * 3, 40)
            draw_glow_rect(screen, segment_rect, NEON_GREEN, 
                          glow_radius=2, glow_alpha=fade_alpha, border_radius=5)
    
    # Enhanced food with pulsing effect matching AI training
    food_center = (snake.food[0] + CELL_SIZE // 2, snake.food[1] + CELL_SIZE // 2)
    food_radius = CELL_SIZE // 2 - 2
    pulse_alpha = get_pulse_alpha(100)
    draw_glow_circle(screen, food_center, food_radius, CYBER_PINK, 
                    glow_radius=GLOW_RADIUS_INNER, glow_alpha=pulse_alpha)
    
    # Enhanced walls with technical borders
    for wall in snake.border_walls:
        wall_rect = pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE)
        draw_glow_rect(screen, wall_rect, WALL_COLOR, 
                      glow_radius=2, glow_alpha=80, border_radius=5)


def draw_directional_indicator(snake):
    """Draw directional arrow indicator for enhanced feedback."""
    # Calculate arrow position (above game area)
    arrow_x = GAME_AREA_X + GAME_AREA_WIDTH // 2
    arrow_y = GAME_AREA_Y - 20
    
    # Direction mapping
    direction_arrows = {
        (-1, 0): "◀",   # Left
        (1, 0): "▶",    # Right  
        (0, -1): "▲",   # Up
        (0, 1): "▼"     # Down
    }
    
    arrow_symbol = direction_arrows.get(snake.direction, "●")
    draw_glow_text(screen, arrow_symbol, font_large, NEON_CYAN, 
                   arrow_x, arrow_y, glow_radius=2, centered=True)


def draw_player_stats_panel(snake):
    """Draw enhanced player statistics monitoring panel."""
    panel_x = WIDTH + 10  # Match AI training layout
    panel_y = GAME_AREA_Y  # Align with game area top border
    panel_width = SIDE_BAR_WIDTH - 20  # Match AI training width
    panel_height = GAME_AREA_HEIGHT  # Match game area height for consistency
    
    # Draw panel background with glow
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    draw_glow_rect(screen, panel_rect, ELECTRIC_PURPLE, glow_radius=4, 
                   glow_alpha=60, border_radius=8)
    
    # Panel interior
    inner_rect = pygame.Rect(panel_x + 3, panel_y + 3, panel_width - 6, panel_height - 6)
    inner_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(inner_surface, (*DARK_BG, 200), (0, 0, inner_rect.width, inner_rect.height), 
                    border_radius=5)
    screen.blit(inner_surface, inner_rect.topleft)
    
    # Title
    font_title = load_retro_font(14)
    title_surface = font_title.render("PLAYER STATS", True, NEON_CYAN)
    title_x = panel_x + panel_width // 2 - title_surface.get_width() // 2
    screen.blit(title_surface, (title_x, panel_y + 10))
    
    # Calculate performance metrics
    elapsed_time = time.time() - snake.start_time
    moves_per_second = len(snake.snake) / max(elapsed_time, 1)
    efficiency = (snake.score / max(elapsed_time, 1)) * 100
    food_efficiency = (snake.score / max(len(snake.snake), 1)) * 100 if len(snake.snake) > 1 else 0
    
    # Player statistics data
    font_data = load_retro_font(10)
    current_y = panel_y + 40
    
    stats_data = [
        ("Current Score", str(snake.score), NEON_GREEN),
        ("Snake Length", str(snake.length), NEON_BLUE),
        ("Time Elapsed", f"{elapsed_time:.1f}s", NEON_CYAN),
        ("Moves/Second", f"{moves_per_second:.1f}", NEON_ORANGE),
        ("Score/Time", f"{efficiency:.1f}%", NEON_MAGENTA),
        ("Food Efficiency", f"{food_efficiency:.1f}%", MATRIX_GREEN),
        ("", "", WHITE),  # Spacer
        ("Performance Rating", "", WHITE),
    ]
    
    for i, (label, value, color) in enumerate(stats_data):
        if label:  # Skip empty spacers
            # Label
            label_surface = font_data.render(f"{label}:", True, NEON_ORANGE)
            screen.blit(label_surface, (panel_x + 8, current_y))
            
            # Value
            if value:
                value_surface = font_data.render(value, True, color)
                screen.blit(value_surface, (panel_x + 110, current_y))
        
        current_y += 18
    
    # Performance rating bars
    rating_y = current_y - 18
    performance_score = min(100, efficiency)  # Cap at 100%
    bar_segments = int(performance_score / 10)  # 0-10 segments
    
    for i in range(10):
        bar_x = panel_x + 8 + i * 16
        bar_color = NEON_GREEN if i < 6 else NEON_ORANGE if i < 8 else UI_DANGER
        bar_alpha = 120 if i < bar_segments else 30
        
        if i < bar_segments:
            bar_rect = pygame.Rect(bar_x, rating_y, 12, 6)
            draw_glow_rect(screen, bar_rect, bar_color, glow_radius=2, glow_alpha=bar_alpha)
        else:
            # Dim unfilled bars
            pygame.draw.rect(screen, (*bar_color[:3], 30), (bar_x, rating_y, 12, 6))
    
    # Add circuit pattern overlay
    circuit_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    draw_circuit_pattern(circuit_surface, grid_size=20, line_color=NEON_CYAN, 
                        line_alpha=15, animate=True)
    screen.blit(circuit_surface, (panel_x, panel_y))


def draw_game(snake):
    """Enhanced mission control game drawing function."""
    # Draw all visual layers
    draw_mission_control_background()
    draw_enhanced_game_area(snake)
    draw_enhanced_player_snake(snake)
    draw_enhanced_monitoring_hud(snake)
    draw_directional_indicator(snake)
    draw_player_stats_panel(snake)
    
    # Add energy nodes for monitoring system aesthetic (matching AI training)
    node_positions = [
        (30, TOP_BAR_HEIGHT + 30), (30, screen.get_height() - 30),
        (WIDTH - 30, TOP_BAR_HEIGHT + 30), (WIDTH - 30, screen.get_height() - 30)
    ]
    draw_energy_nodes(screen, node_positions, ELECTRIC_PURPLE, pulse=True)
    
    # Add overall scan lines for retro monitoring effect
    draw_scan_lines(screen, line_spacing=15, line_alpha=8, animate=True)
    
    pygame.display.flip()


def show_futuristic_game_over_screen(snake):
    """Display enhanced game over screen with sci-fi terminal aesthetics."""
    elapsed_time = round(time.time() - snake.start_time, 2)
    
    # Updated button dimensions to match main menu
    button_width, button_height = 180, 55
    button_spacing = 25
    # Center relative to total screen height (including top bar)
    total_height = HEIGHT + TOP_BAR_HEIGHT
    menu_button = pygame.Rect(WIDTH // 2 - button_width - button_spacing // 2, total_height // 2 + 80, button_width, button_height)
    replay_button = pygame.Rect(WIDTH // 2 + button_spacing // 2, total_height // 2 + 80, button_width, button_height)
    
    # Game over screen loop
    while True:
        # Draw background with circuit pattern
        screen.fill(DARK_BG)
        draw_circuit_pattern(screen, grid_size=60, line_color=UI_DANGER, 
                            line_alpha=30, animate=True)
        
        # Mission failed title with reduced glow for cleaner look - centered on total screen
        total_height = HEIGHT + TOP_BAR_HEIGHT
        draw_glow_text(screen, "MISSION TERMINATED", font_large, UI_DANGER, 
                       WIDTH // 2, total_height // 2 - 120, glow_radius=2, glow_alpha=40, centered=True)
        
        # Mission stats with enhanced styling
        stats_data = [
            ("MISSION DURATION", f"{elapsed_time:.1f}s"),
            ("TARGETS ACQUIRED", f"{float(snake.score):.2f}"),
            ("FINAL LENGTH", str(snake.length)),
            ("STATUS", "TERMINATED")
        ]
        
        # Draw stats with cleaner neon styling - centered on total screen
        stats_y = total_height // 2 - 60
        for i, (label, value) in enumerate(stats_data):
            stat_text = f"{label}: {value}"
            color = NEON_ORANGE if i < 3 else UI_DANGER
            draw_glow_text(screen, stat_text, font_status, color, 
                           WIDTH // 2, stats_y + i * 22, glow_radius=1, glow_alpha=25, centered=True)
        
        # Enhanced buttons with hover detection
        mouse_pos = pygame.mouse.get_pos()
        menu_hovered = menu_button.collidepoint(mouse_pos)
        replay_hovered = replay_button.collidepoint(mouse_pos)
        
        # Draw holographic buttons with smaller text (matching main menu style)
        button_font = load_retro_font(18)  # Smaller font for buttons
        draw_holographic_button(screen, menu_button, "COMMAND", button_font, 
                               UI_BORDER, UI_HIGHLIGHT, WHITE, menu_hovered)
        draw_holographic_button(screen, replay_button, "RETRY", button_font, 
                               UI_SUCCESS, NEON_GREEN, WHITE, replay_hovered)
        
        # Add scan lines for terminal effect
        draw_scan_lines(screen, line_spacing=8, line_alpha=15, animate=True)
        
        # Add energy nodes in corners with better positioning for total screen
        total_height = HEIGHT + TOP_BAR_HEIGHT
        corner_positions = [
            (50, 50), (WIDTH - 50, 50), 
            (50, total_height - 50), (WIDTH - 50, total_height - 50)
        ]
        draw_energy_nodes(screen, corner_positions, UI_DANGER, pulse=True)
        
        # Add grid overlay for consistency with main menu
        draw_grid_overlay(screen, grid_size=40, line_color=UI_DANGER, line_alpha=10)
        
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    return "menu"
                elif replay_button.collidepoint(event.pos):
                    return "replay"


def show_game_over_screen(snake):
    """Wrapper function for compatibility."""
    return show_futuristic_game_over_screen(snake)


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
