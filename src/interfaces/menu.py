import pygame
import sys
import time
import math
from ..game.config import *
from .ui_components import *

# Initialize pygame
pygame.init()

# Create Pygame Screen
screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pygame.display.set_caption("SNAKE GEN v12.0 - COMMAND CENTER")

# Load Enhanced Fonts
font_title = load_retro_font(FONT_RETRO_LARGE)
font_subtitle = load_retro_font(FONT_RETRO_MEDIUM)
font_button = load_retro_font(FONT_RETRO_SMALL)
font_system = load_retro_font(16)

# Load background image with fallback
try:
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
except:
    background_image = None

# Animation state
menu_start_time = time.time()
button_hover_states = {i: 0.0 for i in range(len(MENU_BUTTONS))}


def draw_command_center_background():
    """Draw the futuristic command center background."""
    # Fill with deep space background
    screen.fill(DARK_BG)
    
    # Draw circuit board pattern background
    draw_circuit_pattern(screen, grid_size=60, line_color=NEON_CYAN, 
                        line_alpha=25, animate=True)
    
    # Add subtle grid overlay
    draw_grid_overlay(screen, grid_size=30, line_color=NEON_BLUE, line_alpha=15)
    
    # Draw animated energy lines
    draw_animated_lines(screen, num_lines=2, line_color=ELECTRIC_PURPLE, speed=0.3)
    
    # Overlay original background if available (with transparency)
    if background_image:
        bg_surface = pygame.transform.scale(background_image, (MENU_WIDTH, MENU_HEIGHT))
        bg_surface.set_alpha(40)  # Make it subtle
        screen.blit(bg_surface, (0, 0))


def draw_animated_logo():
    """Draw animated neon snake logo with glow effects."""
    center_x = MENU_WIDTH // 2
    logo_y = 120
    
    # Calculate pulsing effect
    pulse = get_glow_intensity(1.0, 0.03)
    
    # Main title with reduced glow for cleaner look
    draw_glow_text(screen, "SNAKE GEN", font_title, NEON_CYAN, 
                   center_x, logo_y, glow_radius=2, glow_alpha=40, centered=True)
    
    # Version subtitle with minimal glow
    draw_glow_text(screen, "v12.0", font_subtitle, NEON_MAGENTA, 
                   center_x, logo_y + 60, glow_radius=1, glow_alpha=30, centered=True)
    
    # Command center status indicator
    status_text = "SYSTEM ONLINE"
    status_color = NEON_GREEN if pulse > 0.8 else MATRIX_GREEN
    draw_glow_text(screen, status_text, font_system, status_color, 
                   center_x, logo_y + 100, glow_radius=1, glow_alpha=25, centered=True)


def draw_futuristic_buttons():
    """Draw holographic-style command buttons."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for i, button in enumerate(MENU_BUTTONS):
        x = MENU_WIDTH // 2 - BUTTON_WIDTH // 2
        y = MENU_HEIGHT // 2 + 40 + i * (BUTTON_HEIGHT + 20)
        
        button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
        
        # Update hover transition state
        global button_hover_states
        button_hover_states[i] = get_hover_transition(is_hovered, button_hover_states[i], 1.0)
        
        # Choose button style based on action
        if button["action"] == "quit":
            # Danger style for quit button
            base_color = UI_DANGER
            hover_color = CYBER_PINK
        elif button["action"] == "train":
            # Success style for training
            base_color = UI_SUCCESS  
            hover_color = NEON_GREEN
        else:
            # Default neon style
            base_color = NEON_CYAN
            hover_color = NEON_MAGENTA
        
        # Draw holographic button with scan lines
        draw_holographic_button(screen, button_rect, button["text"], font_button,
                               base_color, hover_color, WHITE, is_hovered)


def draw_system_status():
    """Draw system status indicators around the interface."""
    current_time = time.time()
    uptime = current_time - menu_start_time
    
    # Top status bar without VERSION section (removed as requested)
    status_sections = [
        ("UPTIME", f"{uptime:.1f}s"),
        ("STATUS", "READY"),
        ("MODE", "COMMAND")
    ]
    
    draw_top_bar(screen, status_sections, font_system, 30, DARK_BG, NEON_CYAN)
    
    # Energy nodes in corners
    corner_positions = [
        (50, 50), (MENU_WIDTH - 50, 50),
        (50, MENU_HEIGHT - 50), (MENU_WIDTH - 50, MENU_HEIGHT - 50)
    ]
    draw_energy_nodes(screen, corner_positions, NEON_GREEN, pulse=True)


def draw_menu():
    """Main menu drawing function with command center aesthetics."""
    # Draw all visual layers
    draw_command_center_background()
    draw_animated_logo()
    draw_futuristic_buttons()
    draw_system_status()
    
    # Add scan lines overlay for retro effect
    draw_scan_lines(screen, line_spacing=8, line_alpha=15, animate=True)
    
    pygame.display.flip()


def menu_screen():
    """Main menu loop with enhanced command center interface."""
    clock = pygame.time.Clock()
    
    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check button clicks with updated positions
                for i, button in enumerate(MENU_BUTTONS):
                    x = MENU_WIDTH // 2 - BUTTON_WIDTH // 2
                    y = MENU_HEIGHT // 2 + 40 + i * (BUTTON_HEIGHT + 20)

                    if x <= mouse_x <= x + BUTTON_WIDTH and y <= mouse_y <= y + BUTTON_HEIGHT:
                        return button["action"]  # Return the selected action
        
        # Maintain smooth animation at 60 FPS
        clock.tick(60)
