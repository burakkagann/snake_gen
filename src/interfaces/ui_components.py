"""
UI Components Module for Snake Gen v11.5
Contains reusable UI drawing functions and components.
"""

import pygame
from ..game.config import *


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
    for x in range(GAME_AREA_X - CELL_SIZE, GAME_AREA_X + GAME_AREA_WIDTH + CELL_SIZE, CELL_SIZE):
        pygame.draw.rect(surface, border_color, 
                        (x, GAME_AREA_Y - CELL_SIZE, CELL_SIZE, CELL_SIZE), 
                        border_radius=5)
        pygame.draw.rect(surface, border_color, 
                        (x, GAME_AREA_Y + GAME_AREA_HEIGHT, CELL_SIZE, CELL_SIZE), 
                        border_radius=5)

    for y in range(GAME_AREA_Y - CELL_SIZE, GAME_AREA_Y + GAME_AREA_HEIGHT + CELL_SIZE, CELL_SIZE):
        pygame.draw.rect(surface, border_color, 
                        (GAME_AREA_X - CELL_SIZE, y, CELL_SIZE, CELL_SIZE), 
                        border_radius=5)
        pygame.draw.rect(surface, border_color, 
                        (GAME_AREA_X + GAME_AREA_WIDTH, y, CELL_SIZE, CELL_SIZE), 
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
        
        # Draw text
        text = f"{label}: {value}"
        text_surface = font.render(text, True, text_color)
        x = i * section_width + 10  # Add some padding
        y = (bar_height - text_surface.get_height()) // 2
        surface.blit(text_surface, (x, y))


def draw_game_over_dialog(surface, snake, font_large, font_small, 
                         background_color=BACKGROUND_GRAY, text_color=BLACK):
    """Draw a standardized game over dialog with statistics."""
    surface.fill(background_color)
    
    # Game Over title
    game_over_text = font_large.render("Game Over", True, text_color)
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