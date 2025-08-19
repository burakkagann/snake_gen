"""
UI Components Module for Snake Gen v11.5
Contains reusable UI drawing functions and components.
"""

import pygame
import math
import time
from ..game.config import *


# ===== CORE GLOW EFFECT FUNCTIONS =====

def draw_glow_rect(surface, rect, color, glow_radius=GLOW_RADIUS_OUTER, glow_alpha=GLOW_ALPHA_MAX, border_radius=0):
    """Draw a rectangle with multi-layer glow effect."""
    # Create a temporary surface for alpha blending
    temp_surface = pygame.Surface((rect.width + glow_radius * 4, rect.height + glow_radius * 4), pygame.SRCALPHA)
    
    # Draw multiple glow layers from outer to inner
    for i in range(glow_radius, 0, -1):
        alpha = int(glow_alpha * (1 - i / glow_radius) * 0.3)
        glow_color = (*color[:3], alpha)
        
        glow_rect = pygame.Rect(glow_radius * 2 - i, glow_radius * 2 - i, 
                               rect.width + i * 2, rect.height + i * 2)
        pygame.draw.rect(temp_surface, glow_color, glow_rect, border_radius=border_radius)
    
    # Draw the main rectangle
    main_rect = pygame.Rect(glow_radius * 2, glow_radius * 2, rect.width, rect.height)
    pygame.draw.rect(temp_surface, color, main_rect, border_radius=border_radius)
    
    # Blit to main surface
    surface.blit(temp_surface, (rect.x - glow_radius * 2, rect.y - glow_radius * 2))


def draw_glow_circle(surface, center, radius, color, glow_radius=GLOW_RADIUS_OUTER, glow_alpha=GLOW_ALPHA_MAX):
    """Draw a circle with radial glow effect."""
    total_radius = radius + glow_radius
    temp_surface = pygame.Surface((total_radius * 2, total_radius * 2), pygame.SRCALPHA)
    temp_center = (total_radius, total_radius)
    
    # Draw glow layers
    for i in range(glow_radius, 0, -1):
        alpha = int(glow_alpha * (1 - i / glow_radius) * 0.4)
        glow_color = (*color[:3], alpha)
        pygame.draw.circle(temp_surface, glow_color, temp_center, radius + i)
    
    # Draw main circle
    pygame.draw.circle(temp_surface, color, temp_center, radius)
    
    # Blit to main surface
    surface.blit(temp_surface, (center[0] - total_radius, center[1] - total_radius))


def draw_glow_text(surface, text, font, color, x, y, glow_radius=TEXT_GLOW_OFFSET, glow_alpha=TEXT_SHADOW_ALPHA, centered=True, antialias=True):
    """Draw text with outer glow effect."""
    # Render the main text with antialiasing for smoother appearance
    text_surface = font.render(text, antialias, color)
    
    # Calculate position
    if centered:
        text_x = x - text_surface.get_width() // 2
        text_y = y - text_surface.get_height() // 2
    else:
        text_x, text_y = x, y
    
    # Draw subtle glow by rendering text with reduced opacity
    if glow_radius > 0:
        glow_color = (*color[:3], glow_alpha // 2)  # Reduced glow intensity
        for offset_x in range(-glow_radius, glow_radius + 1, 2):  # Skip every other pixel for lighter effect
            for offset_y in range(-glow_radius, glow_radius + 1, 2):
                if offset_x != 0 or offset_y != 0:  # Skip center position
                    glow_surface = font.render(text, antialias, glow_color)
                    surface.blit(glow_surface, (text_x + offset_x, text_y + offset_y))
    
    # Draw main text on top
    surface.blit(text_surface, (text_x, text_y))
    
    return text_surface.get_rect(topleft=(text_x, text_y))


def draw_scan_lines(surface, line_spacing=4, line_alpha=30, animate=True):
    """Draw animated horizontal scan lines across the surface."""
    width, height = surface.get_size()
    
    if animate:
        # Animate scan lines moving down
        offset = int((time.time() * SCAN_LINE_SPEED * 10) % (line_spacing * 2))
    else:
        offset = 0
    
    scan_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for y in range(-line_spacing + offset, height + line_spacing, line_spacing * 2):
        pygame.draw.line(scan_surface, (255, 255, 255, line_alpha), (0, y), (width, y), 1)
    
    surface.blit(scan_surface, (0, 0))


# ===== ANIMATION FRAMEWORK =====

def get_pulse_alpha(base_alpha=GLOW_ALPHA_MAX, speed=PULSE_SPEED):
    """Calculate pulsing alpha value based on time."""
    pulse = (math.sin(time.time() * speed * math.pi * 2) + 1) / 2  # 0 to 1
    return int(base_alpha * (0.5 + 0.5 * pulse))


def get_glow_intensity(base_intensity=1.0, speed=PULSE_SPEED):
    """Calculate variable glow intensity based on time."""
    pulse = (math.sin(time.time() * speed * math.pi * 2) + 1) / 2
    return base_intensity * (0.7 + 0.3 * pulse)


def get_scan_line_position(speed=SCAN_LINE_SPEED, line_spacing=4):
    """Calculate animated scan line position."""
    return int((time.time() * speed * 10) % (line_spacing * 2))


def get_fade_alpha(start_time, duration=FADE_DURATION, max_alpha=255):
    """Calculate fade in/out alpha based on elapsed time."""
    elapsed = time.time() - start_time
    if elapsed < 0:
        return 0
    elif elapsed > duration:
        return max_alpha
    else:
        return int(max_alpha * (elapsed / duration))


def get_hover_transition(is_hovered, transition_state, speed=1.0):
    """Calculate smooth hover transition values (0.0 to 1.0)."""
    target = 1.0 if is_hovered else 0.0
    current = transition_state
    
    # Smooth transition
    diff = target - current
    return current + diff * speed * 0.1


# ===== ENHANCED NEON BUTTON SYSTEM =====

def draw_neon_button(surface, rect, text, font, base_color=NEON_CYAN, 
                    hover_color=NEON_MAGENTA, text_color=WHITE, 
                    is_hovered=False, is_pulsing=False, border_radius=10):
    """Draw a futuristic neon button with glow effects and animations."""
    # Choose colors
    button_color = hover_color if is_hovered else base_color
    
    # Add pulsing effect if enabled
    if is_pulsing:
        glow_alpha = get_pulse_alpha()
        glow_intensity = get_glow_intensity()
    else:
        glow_alpha = GLOW_ALPHA_MAX if is_hovered else GLOW_ALPHA_MIN
        glow_intensity = 1.2 if is_hovered else 1.0
    
    # Draw glow effect
    glow_radius = int(GLOW_RADIUS_OUTER * glow_intensity)
    draw_glow_rect(surface, rect, button_color, glow_radius, glow_alpha, border_radius)
    
    # Draw inner border for extra neon effect
    inner_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4)
    pygame.draw.rect(surface, (*button_color[:3], 60), inner_rect, 
                    width=1, border_radius=max(0, border_radius - 2))
    
    # Draw text with glow
    text_x = rect.centerx
    text_y = rect.centery
    draw_glow_text(surface, text, font, text_color, text_x, text_y, 
                   glow_radius=2, glow_alpha=80, centered=True)


def draw_holographic_button(surface, rect, text, font, base_color=ELECTRIC_PURPLE,
                           hover_color=NEON_CYAN, text_color=WHITE,
                           is_hovered=False, border_radius=10):
    """Draw a holographic-style button with scan lines and transparency."""
    # Main button color with transparency
    button_color = hover_color if is_hovered else base_color
    alpha = 200 if is_hovered else 150
    
    # Create button surface with alpha
    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(button_surface, (*button_color[:3], alpha), 
                    (0, 0, rect.width, rect.height), border_radius=border_radius)
    
    # Add scan lines effect
    draw_scan_lines(button_surface, line_spacing=6, line_alpha=40, animate=is_hovered)
    
    # Draw border glow
    if is_hovered:
        draw_glow_rect(surface, rect, button_color, GLOW_RADIUS_INNER, GLOW_ALPHA_MAX, border_radius)
    
    # Blit button to main surface
    surface.blit(button_surface, rect.topleft)
    
    # Draw text with minimal glow for cleaner appearance
    text_x = rect.centerx
    text_y = rect.centery
    draw_glow_text(surface, text, font, text_color, text_x, text_y, 
                   glow_radius=1, glow_alpha=20, centered=True)


# ===== CIRCUIT BOARD BACKGROUND SYSTEM =====

def draw_circuit_pattern(surface, grid_size=CIRCUIT_GRID_SIZE, line_color=NEON_CYAN, 
                        line_alpha=CIRCUIT_ALPHA, animate=True):
    """Draw a procedural circuit board pattern background."""
    width, height = surface.get_size()
    circuit_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Animated offset for energy pulses
    if animate:
        pulse_offset = int((time.time() * ENERGY_PULSE_SPEED * 10) % 20)
    else:
        pulse_offset = 0
    
    # Draw horizontal lines
    for y in range(0, height, grid_size):
        # Main circuit trace
        pygame.draw.line(circuit_surface, (*line_color[:3], line_alpha), 
                        (0, y), (width, y), CIRCUIT_LINE_WIDTH)
        
        # Add connection nodes at intersections
        for x in range(0, width, grid_size):
            if (x // grid_size + y // grid_size) % 3 == 0:  # Sparse node placement
                node_color = (*line_color[:3], line_alpha * 2)
                pygame.draw.circle(circuit_surface, node_color, (x, y), 2)
    
    # Draw vertical lines
    for x in range(0, width, grid_size):
        # Vary line intensity for visual interest
        alpha = line_alpha if (x // grid_size) % 2 == 0 else line_alpha // 2
        pygame.draw.line(circuit_surface, (*line_color[:3], alpha), 
                        (x, 0), (x, height), CIRCUIT_LINE_WIDTH)
    
    # Add energy pulse lines
    if animate:
        pulse_color = (*NEON_MAGENTA[:3], 80)
        for i in range(0, width + height, 200):
            pulse_x = (i + pulse_offset) % (width + 100) - 50
            if 0 <= pulse_x <= width:
                pygame.draw.line(circuit_surface, pulse_color, 
                               (pulse_x, 0), (pulse_x, height), 2)
    
    surface.blit(circuit_surface, (0, 0))


def draw_grid_overlay(surface, grid_size=20, line_color=NEON_CYAN, line_alpha=20):
    """Draw a subtle technical grid overlay."""
    width, height = surface.get_size()
    grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw grid lines
    for x in range(0, width, grid_size):
        pygame.draw.line(grid_surface, (*line_color[:3], line_alpha), 
                        (x, 0), (x, height), 1)
    
    for y in range(0, height, grid_size):
        pygame.draw.line(grid_surface, (*line_color[:3], line_alpha), 
                        (0, y), (width, y), 1)
    
    surface.blit(grid_surface, (0, 0))


def draw_animated_lines(surface, num_lines=3, line_color=ELECTRIC_PURPLE, speed=1.0):
    """Draw moving energy lines across the surface."""
    width, height = surface.get_size()
    
    for i in range(num_lines):
        # Calculate animated position
        progress = ((time.time() * speed + i * 0.3) % 2.0)  # 0 to 2
        
        if progress <= 1.0:
            # Line moving from left to right
            x = int(progress * width)
            start_pos = (x, 0)
            end_pos = (x, height)
        else:
            # Line moving from top to bottom
            y = int((progress - 1.0) * height)
            start_pos = (0, y)
            end_pos = (width, y)
        
        # Draw line with fade effect
        alpha = int(120 * math.sin(progress * math.pi))  # Fade in/out
        if alpha > 0:
            line_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.line(line_surface, (*line_color[:3], alpha), 
                           start_pos, end_pos, 2)
            surface.blit(line_surface, (0, 0))


def draw_energy_nodes(surface, positions, node_color=NEON_GREEN, pulse=True):
    """Draw pulsing energy nodes at specified positions."""
    for pos in positions:
        if pulse:
            radius = int(4 + 2 * math.sin(time.time() * 3 + pos[0] * 0.01))
            alpha = get_pulse_alpha(150, 0.05)
        else:
            radius = 4
            alpha = 150
        
        draw_glow_circle(surface, pos, radius, (*node_color[:3], alpha), 
                        glow_radius=6, glow_alpha=alpha // 2)


# ===== ENHANCED DRAWING FUNCTIONS =====

def draw_button(surface, rect, text, font, base_color=GRAY, hover_color=HOVER_COLOR, 
                text_color=WHITE, is_hovered=False, border_radius=10):
    """Draw a standardized button with hover effects."""
    color = hover_color if is_hovered else base_color
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)
    
    # Render text centered on button
    text_surface = font.render(text, True, text_color)
    text_x = rect.x + rect.width // 2 - text_surface.get_width() // 2
    text_y = rect.y + rect.height // 2 - text_surface.get_height() // 2
    surface.blit(text_surface, (text_x, text_y))


def draw_text_centered(surface, text, font, color, x, y):
    """Draw text centered at the given position."""
    text_surface = font.render(text, True, color)
    text_x = x - text_surface.get_width() // 2
    text_y = y - text_surface.get_height() // 2
    surface.blit(text_surface, (text_x, text_y))


def draw_hud_section(surface, text, value, font, x, y, text_color=WHITE):
    """Draw a HUD information section with label and value."""
    display_text = f"{text}: {value}"
    text_surface = font.render(display_text, True, text_color)
    surface.blit(text_surface, (x, y))


def draw_game_border(surface, border_color=WALL_COLOR, border_thickness=CELL_SIZE):
    """Draw the game area borders."""
    # Draw borders one grid outside the game area
    for x in range(GAME_AREA_X - border_thickness, GAME_AREA_X + GAME_AREA_WIDTH + border_thickness, border_thickness):
        pygame.draw.rect(surface, border_color, 
                        (x, GAME_AREA_Y - border_thickness, border_thickness, border_thickness), 
                        border_radius=5)
        pygame.draw.rect(surface, border_color, 
                        (x, GAME_AREA_Y + GAME_AREA_HEIGHT, border_thickness, border_thickness), 
                        border_radius=5)

    for y in range(GAME_AREA_Y - border_thickness, GAME_AREA_Y + GAME_AREA_HEIGHT + border_thickness, border_thickness):
        pygame.draw.rect(surface, border_color, 
                        (GAME_AREA_X - border_thickness, y, border_thickness, border_thickness), 
                        border_radius=5)
        pygame.draw.rect(surface, border_color, 
                        (GAME_AREA_X + GAME_AREA_WIDTH, y, border_thickness, border_thickness), 
                        border_radius=5)


def draw_snake(surface, snake_segments, color=SNAKE_COLOR, cell_size=CELL_SIZE, gap=GAP):
    """Draw a snake with the specified segments."""
    for segment in snake_segments:
        pygame.draw.rect(surface, color, 
                        (segment[0] + gap, segment[1] + gap, 
                         cell_size - gap * 2, cell_size - gap * 2), 
                        border_radius=5)


def draw_food(surface, food_position, color=FOOD_COLOR, cell_size=CELL_SIZE, gap=GAP):
    """Draw food at the specified position."""
    pygame.draw.rect(surface, color, 
                    (food_position[0] + gap, food_position[1] + gap, 
                     cell_size - gap * 2, cell_size - gap * 2), 
                    border_radius=5)


def draw_top_bar(surface, sections, font, bar_height=TOP_BAR_HEIGHT, bg_color=BLACK, text_color=WHITE):
    """Draw a top information bar with multiple sections."""
    # Fill background
    pygame.draw.rect(surface, bg_color, (0, 0, surface.get_width(), bar_height))
    
    # Draw vertical dividers and text
    section_width = surface.get_width() // len(sections)
    for i, (label, value) in enumerate(sections):
        # Draw divider (except for first section)
        if i > 0:
            pygame.draw.line(surface, text_color, 
                           (i * section_width, 0), 
                           (i * section_width, bar_height), 2)
        
        # Draw text centered in each section
        text = f"{label}: {value}"
        text_surface = font.render(text, True, text_color)
        x = i * section_width + (section_width - text_surface.get_width()) // 2
        y = (bar_height - text_surface.get_height()) // 2
        surface.blit(text_surface, (x, y))


def draw_game_over_dialog(surface, snake, font_large, font_small, 
                         background_color=BACKGROUND_GRAY, text_color=BLACK):
    """Draw a standardized game over dialog with statistics."""
    surface.fill(background_color)
    
    # Game Over title
    draw_text_centered(surface, "Game Over", font_large, text_color, 
                      surface.get_width() // 2, surface.get_height() // 3)
    
    # Statistics
    import time
    elapsed_time = round(time.time() - snake.start_time, 2)
    stats = [
        f"Time: {elapsed_time}s",
        f"Score: {snake.score}",
        f"Length: {snake.length}"
    ]
    
    stats_y = surface.get_height() // 2 - 40
    for i, stat in enumerate(stats):
        draw_text_centered(surface, stat, font_small, text_color,
                          surface.get_width() // 2, stats_y + i * 35)


def draw_three_button_layout(surface, button_texts, button_actions, font, 
                            button_width=150, button_height=50, 
                            y_position=None, colors=None):
    """Draw three buttons in a horizontal layout and return their rectangles."""
    if y_position is None:
        y_position = surface.get_height() // 2 + 50
    
    if colors is None:
        colors = [BROWN, GREEN, RED]  # Default colors
    
    button_spacing = 20
    total_width = 3 * button_width + 2 * button_spacing
    start_x = (surface.get_width() - total_width) // 2
    
    buttons = []
    for i, (text, action, color) in enumerate(zip(button_texts, button_actions, colors)):
        x = start_x + i * (button_width + button_spacing)
        rect = pygame.Rect(x, y_position, button_width, button_height)
        
        pygame.draw.rect(surface, color, rect, border_radius=10)
        draw_text_centered(surface, text, font, WHITE, rect.centerx, rect.centery)
        
        buttons.append((rect, action))
    
    return buttons


def check_button_hover(mouse_pos, button_rect):
    """Check if mouse is hovering over a button."""
    return button_rect.collidepoint(mouse_pos)


def handle_button_clicks(mouse_pos, buttons):
    """Handle button clicks and return the action of the clicked button."""
    for rect, action in buttons:
        if rect.collidepoint(mouse_pos):
            return action
    return None


def draw_sidebar_info(surface, title, info_list, font, x, y, 
                     title_color=BLACK, text_color=GREEN, line_spacing=25):
    """Draw sidebar information with a title and list of items."""
    # Draw title
    title_surface = font.render(title, True, title_color)
    surface.blit(title_surface, (x, y))
    
    # Draw information items
    for i, info in enumerate(info_list):
        info_surface = font.render(info, True, text_color)
        surface.blit(info_surface, (x, y + (i + 1) * line_spacing))


def create_input_box(x, y, width, height, font, initial_text="", 
                    bg_color=WHITE, text_color=BLACK, border_color=GRAY):
    """Create an input box for text entry."""
    return {
        'rect': pygame.Rect(x, y, width, height),
        'text': initial_text,
        'font': font,
        'bg_color': bg_color,
        'text_color': text_color,
        'border_color': border_color,
        'active': False
    }


def draw_input_box(surface, input_box):
    """Draw an input box with current text."""
    rect = input_box['rect']
    
    # Draw background
    pygame.draw.rect(surface, input_box['bg_color'], rect, border_radius=5)
    
    # Draw border (thicker if active)
    border_width = 3 if input_box['active'] else 1
    pygame.draw.rect(surface, input_box['border_color'], rect, 
                    width=border_width, border_radius=5)
    
    # Draw text
    if input_box['text']:
        text_surface = input_box['font'].render(input_box['text'], True, input_box['text_color'])
        surface.blit(text_surface, (rect.x + 10, rect.y + 10))


def handle_input_box_event(input_box, event):
    """Handle events for an input box (clicks and key presses)."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        input_box['active'] = input_box['rect'].collidepoint(event.pos)
    
    elif event.type == pygame.KEYDOWN and input_box['active']:
        if event.key == pygame.K_BACKSPACE:
            input_box['text'] = input_box['text'][:-1]
        elif event.key in range(pygame.K_0, pygame.K_9 + 1):
            input_box['text'] += event.unicode