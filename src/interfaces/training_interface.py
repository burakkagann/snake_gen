"""
Training Interface Module for Snake Gen v11.5
Contains functions for AI training setup and monitoring interfaces.
"""

import pygame
import sys
import time
import math
from ..game.config import *
from .ui_components import *


def draw_training_recommendations_table(surface, font_small, font_table_small, start_y):
    """Draw the training recommendations table."""
    col_widths = [180, 120, 120, 220]  # Define column widths for spacing
    
    # Column Headers
    headers = ["Training Type", "# Snakes", "# Gens", "Best Use Case"]
    for i, header in enumerate(headers):
        header_text = font_small.render(header, True, BROWN)
        surface.blit(header_text, (WIDTH // 2 - 275 + sum(col_widths[:i]), start_y))
    
    # Render Table Rows
    for row, (name, snakes, gens, desc) in enumerate(TRAINING_RECOMMENDATIONS):
        name_text = font_table_small.render(name, True, BLACK)
        snakes_text = font_table_small.render(snakes, True, BLACK)
        gens_text = font_table_small.render(gens, True, BLACK)
        desc_text = font_table_small.render(desc, True, BLACK)
        
        surface.blit(name_text, (WIDTH // 2 - 275, start_y + (row + 1) * 30))
        surface.blit(snakes_text, (WIDTH // 2 - 100, start_y + (row + 1) * 30))
        surface.blit(gens_text, (WIDTH // 2 + 20, start_y + (row + 1) * 30))
        surface.blit(desc_text, (WIDTH // 2 + 100, start_y + (row + 1) * 30))


def handle_training_input(input_values, active_box, event):
    """Handle keyboard input for training parameter input boxes."""
    if event.type == pygame.KEYDOWN and active_box:
        if event.key == pygame.K_BACKSPACE:
            input_values[active_box] = input_values[active_box][:-1]
        elif event.key in range(pygame.K_0, pygame.K_9 + 1):
            input_values[active_box] += event.unicode


def validate_training_input(input_values):
    """Validate that training input values are valid integers."""
    return (input_values["snakes_per_gen"].isdigit() and 
            input_values["num_generations"].isdigit())


def draw_neural_network_background(surface):
    """Draw neural network configuration background."""
    surface.fill(DARK_BG)
    
    # Draw subtle circuit pattern (reduced opacity to minimize distraction)
    draw_circuit_pattern(surface, grid_size=50, line_color=ELECTRIC_PURPLE, 
                        line_alpha=12, animate=True)
    
    # Add minimal data grid overlay
    draw_grid_overlay(surface, grid_size=30, line_color=NEON_CYAN, line_alpha=8)
    
    # Draw very subtle animated neural connections
    draw_animated_lines(surface, num_lines=2, line_color=MATRIX_GREEN, speed=0.3)


def draw_futuristic_input_box(surface, rect, value, label, font, is_active=False):
    """Draw a futuristic input box with neon styling."""
    # Input box with cleaner glow
    box_color = NEON_CYAN if is_active else NEON_BLUE
    glow_alpha = 80 if is_active else 50
    
    # Draw subtle glowing input box
    draw_glow_rect(surface, rect, box_color, glow_radius=3, 
                   glow_alpha=glow_alpha, border_radius=8)
    
    # Brighter inner box for better contrast
    inner_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4)
    inner_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(inner_surface, (*DARK_BG, 240), (0, 0, inner_rect.width, inner_rect.height), 
                    border_radius=6)
    surface.blit(inner_surface, inner_rect.topleft)
    
    # Draw label above box with standardized font
    label_font = load_retro_font(12)
    label_surface = label_font.render(label, True, NEON_ORANGE)
    label_x = rect.centerx - label_surface.get_width() // 2
    label_y = rect.y - 20
    surface.blit(label_surface, (label_x, label_y))
    
    # Draw input text with clean rendering
    if value:
        text_font = load_retro_font(16)
        text_surface = text_font.render(value, True, WHITE)
        text_x = rect.centerx - text_surface.get_width() // 2
        text_y = rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))
    else:
        # Improved placeholder text visibility
        placeholder_font = load_retro_font(14)
        placeholder_surface = placeholder_font.render("ENTER VALUE", True, NEON_BLUE)
        placeholder_x = rect.centerx - placeholder_surface.get_width() // 2
        placeholder_y = rect.centery - placeholder_surface.get_height() // 2
        surface.blit(placeholder_surface, (placeholder_x, placeholder_y))


def draw_enhanced_recommendations_table(surface, start_y):
    """Draw enhanced training recommendations with neon styling."""
    font_header = load_retro_font(12)
    font_data = load_retro_font(11)
    
    # Calculate center based on total window width
    total_width = WIDTH + SIDE_BAR_WIDTH
    center_x = total_width // 2
    
    # Table title with clean rendering - centered on full window
    title_font = load_retro_font(14)
    title_surface = title_font.render("NEURAL TRAINING PROTOCOLS", True, NEON_CYAN)
    title_x = center_x - title_surface.get_width() // 2
    surface.blit(title_surface, (title_x, start_y - 25))
    
    # Table headers with optimized spacing
    headers = ["PROTOCOL", "UNITS", "CYCLES", "OPTIMIZATION TARGET"]
    header_y = start_y
    # Column positioning centered on full window width
    col_positions = [center_x - 320, center_x - 120, center_x - 40, center_x + 80]
    
    for i, header in enumerate(headers):
        # Use clean text for headers
        header_surface = font_header.render(header, True, NEON_ORANGE)
        surface.blit(header_surface, (col_positions[i], header_y))
    
    # Add subtle column separators aligned with header positions
    separator_positions = [center_x - 200, center_x - 65, center_x + 50]
    for separator_x in separator_positions:
        pygame.draw.line(surface, (*NEON_CYAN, 30), 
                        (separator_x, header_y), 
                        (separator_x, header_y + 90), 1)
    
    # Table data with improved spacing and alignment
    for row, (name, snakes, gens, desc) in enumerate(TRAINING_RECOMMENDATIONS):
        row_y = header_y + 30 + row * 22
        
        # Protocol name in readable green
        name_surface = font_data.render(name, True, NEON_GREEN)
        surface.blit(name_surface, (col_positions[0], row_y))
        
        # Units and cycles in clean white for high contrast
        snakes_surface = font_data.render(snakes, True, WHITE)
        surface.blit(snakes_surface, (col_positions[1], row_y))
        
        gens_surface = font_data.render(gens, True, WHITE)
        surface.blit(gens_surface, (col_positions[2], row_y))
        
        # Description in lighter blue for better readability
        desc_surface = font_data.render(desc, True, NEON_CYAN)
        surface.blit(desc_surface, (col_positions[3], row_y))


def draw_training_setup_screen(surface, input_values, active_box, submit_button):
    """Draw the enhanced neural network configuration panel centered on full window."""
    # Draw futuristic background
    draw_neural_network_background(surface)
    
    # Get total screen dimensions for proper centering
    total_width = WIDTH + SIDE_BAR_WIDTH
    total_height = HEIGHT + TOP_BAR_HEIGHT
    center_x = total_width // 2
    
    # Title with readable text - centered on full window
    font_title = load_retro_font(24)
    title_surface = font_title.render("NETWORK CONFIGURATION", True, NEON_CYAN)
    title_x = center_x - title_surface.get_width() // 2
    surface.blit(title_surface, (title_x, total_height // 6))
    
    # Subtitle with cleaner appearance - centered on full window
    font_subtitle = load_retro_font(14)
    draw_glow_text(surface, "CONFIGURE AI TRAINING PARAMETERS", font_subtitle, NEON_MAGENTA, 
                   center_x, total_height // 6 + 30, glow_radius=0, glow_alpha=10, centered=True)
    
    # Enhanced input boxes with improved sizing and spacing - centered on full window
    input_box_width = 240
    input_box_height = 45
    
    input_boxes = {
        "snakes_per_gen": pygame.Rect(center_x - input_box_width // 2, total_height // 2 - 100, input_box_width, input_box_height),
        "num_generations": pygame.Rect(center_x - input_box_width // 2, total_height // 2 - 30, input_box_width, input_box_height),
    }
    
    # Draw futuristic input boxes with simplified, clearer labels
    draw_futuristic_input_box(surface, input_boxes["snakes_per_gen"], 
                             input_values["snakes_per_gen"], "UNITS", 
                             load_retro_font(16), active_box == "snakes_per_gen")
    
    draw_futuristic_input_box(surface, input_boxes["num_generations"], 
                             input_values["num_generations"], "TRAINING CYCLES", 
                             load_retro_font(16), active_box == "num_generations")
    
    # Enhanced submit button with orange theme matching pre-trained AI cards
    button_font = load_retro_font(14)  # Reduced font size to fit inside button
    draw_neon_button(surface, submit_button, "START TRAINING", button_font, 
                    ELECTRIC_PURPLE, NEON_MAGENTA, NEON_ORANGE, False, False)  # Orange text matching pre-trained cards
    
    # Enhanced recommendations table with better spacing
    table_start_y = submit_button.y + 100
    draw_enhanced_recommendations_table(surface, table_start_y)
    
    # Add energy nodes around the interface
    node_positions = [
        (50, 50), (WIDTH - 50, 50), 
        (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50)
    ]
    draw_energy_nodes(surface, node_positions, ELECTRIC_PURPLE, pulse=True)
    
    # Add subtle scan lines overlay for retro effect
    draw_scan_lines(surface, line_spacing=12, line_alpha=8, animate=True)
    
    return input_boxes


def get_training_parameters():
    """Get training parameters from user input with a clean, modular interface."""
    input_values = {"snakes_per_gen": "", "num_generations": ""}
    active_box = None
    
    # Get total screen dimensions for proper centering
    total_width = WIDTH + SIDE_BAR_WIDTH
    total_height = HEIGHT + TOP_BAR_HEIGHT
    center_x = total_width // 2
    
    # Improved button sizing and positioning - centered on full window
    button_width, button_height = 200, 45  # Made thinner (55 -> 45)
    submit_button = pygame.Rect(center_x - button_width // 2, total_height // 2 + 60, button_width, button_height)
    
    while True:
        # Draw the interface
        input_boxes = draw_training_setup_screen(screen, input_values, active_box, submit_button)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle input box clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_box = None  # Reset active box
                for key, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                        active_box = key
                        break
                
                # Check submit button
                if submit_button.collidepoint(event.pos):
                    if validate_training_input(input_values):
                        return int(input_values["snakes_per_gen"]), int(input_values["num_generations"])
            
            # Handle keyboard input
            handle_training_input(input_values, active_box, event)
        
        pygame.display.flip()


def draw_ai_database_background(surface):
    """Draw the AI unit database background with optimized effects."""
    surface.fill(DARK_BG)
    
    # Phase 5: Reduced background pattern intensity for better readability
    draw_circuit_pattern(surface, grid_size=50, line_color=ELECTRIC_PURPLE, 
                        line_alpha=15, animate=True)  # Reduced from 25 to 15
    
    # Phase 5: Subtle data grid overlay
    draw_grid_overlay(surface, grid_size=25, line_color=NEON_CYAN, line_alpha=8)  # Reduced from 15 to 8
    
    # Phase 5: Minimal animated data streams
    draw_animated_lines(surface, num_lines=2, line_color=MATRIX_GREEN, speed=0.5)  # Reduced lines and speed


def draw_ai_unit_card(surface, rect, model_name, params, description, is_hovered, is_selected=False):
    """Draw a futuristic AI unit profile card with optimized typography."""
    # Phase 3: Reduced glow effects for cleaner appearance
    card_color = NEON_MAGENTA if is_selected else (NEON_CYAN if is_hovered else ELECTRIC_PURPLE)
    glow_alpha = 40 if is_hovered else 25  # Reduced from 120/80 to 40/25
    
    # Draw card with minimal glow
    draw_glow_rect(surface, rect, card_color, glow_radius=2,  # Reduced from 6 to 2
                   glow_alpha=glow_alpha, border_radius=10)
    
    # Clean card interior without scan lines
    inner_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width - 10, rect.height - 10)  # More padding
    card_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, (*DARK_BG, 220), (0, 0, inner_rect.width, inner_rect.height), 
                    border_radius=7)
    
    # Removed scan lines from cards for cleaner appearance
    
    surface.blit(card_surface, inner_rect.topleft)
    
    # Updated model name with different color and moved down to fit better in card
    font_name = load_retro_font(18)  # Smaller font for shorter cards
    name_y = rect.y + 15   # Moved down from 8 to 15 for better fit
    draw_glow_text(surface, model_name, font_name, NEON_ORANGE,  # Changed color to orange
                   rect.centerx, name_y, glow_radius=0, glow_alpha=20, centered=True)  # Minimal glow
    
    # Phase 4: Removed redundant classification text to save space and improve hierarchy
    # (Removing "NEURAL COMBAT UNIT" as recommended to declutter the card)
    
    # Updated description with compact layout for shorter cards - moved down
    font_desc = load_retro_font(10)  # Smaller font for compact layout
    desc_start_y = name_y + 22  # Keep spacing from title
    
    # Compact text wrapping for shorter cards - leave space for right-side indicators
    max_width = rect.width - 60  # Leave space for performance indicators on right
    line_height = 12  # Reduced line spacing
    
    if font_desc.size(description)[0] > max_width:
        # Split description into multiple lines with better word wrapping
        words = description.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = " ".join(current_line + [word])
            if font_desc.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Draw wrapped lines with tighter spacing - limit to 2 lines for compact cards
        for i, line in enumerate(lines[:2]):  # Limit to 2 lines
            draw_glow_text(surface, line, font_desc, NEON_GREEN, 
                           rect.centerx, desc_start_y + i * line_height, 
                           glow_radius=0, glow_alpha=15, centered=True)
    else:
        draw_glow_text(surface, description, font_desc, NEON_GREEN, 
                       rect.centerx, desc_start_y, glow_radius=0, glow_alpha=15, centered=True)
    
    # Add performance indicators to the right side of each card
    performance_score = sum(abs(p) for p in params) / len(params)
    perf_bars = int(performance_score * 2)  # Scale to 0-10 bars
    
    # Position performance indicators on the right side of the card
    indicator_x = rect.x + rect.width - 25  # Right side with margin
    indicator_start_y = rect.y + 25  # Start below title area
    
    # Draw vertical performance bars on the right side
    bar_width = 3
    bar_height = 8
    bar_spacing = 2
    max_bars = 5  # Limit to 5 bars for compact layout
    actual_bars = min(max_bars, max(1, perf_bars))
    
    for i in range(actual_bars):
        bar_y = indicator_start_y + i * (bar_height + bar_spacing)
        bar_color = NEON_GREEN if i < 3 else NEON_ORANGE if i < 4 else UI_DANGER
        bar_rect = pygame.Rect(indicator_x, bar_y, bar_width, bar_height)
        draw_glow_rect(surface, bar_rect, bar_color, glow_radius=1, glow_alpha=60)


def draw_database_header(surface):
    """Draw the AI database header with optimized typography and positioning."""
    # Get total screen dimensions including sidebar
    total_width = WIDTH + SIDE_BAR_WIDTH
    total_height = HEIGHT + TOP_BAR_HEIGHT
    
    # Center everything relative to total screen width
    center_x = total_width // 2
    
    # Updated main title to 'DATABASE' - centered on full screen
    font_title = load_retro_font(28)
    draw_glow_text(surface, "DATABASE", font_title, NEON_CYAN, 
                   center_x, 70, glow_radius=1, glow_alpha=30, centered=True)
    
    # Subtitle centered on full screen
    font_subtitle = load_retro_font(16)
    draw_glow_text(surface, "SELECT NEURAL COMBAT UNIT", font_subtitle, NEON_MAGENTA, 
                   center_x, 105, glow_radius=0, glow_alpha=20, centered=True)
    
    # System status centered on full screen
    font_status = load_retro_font(12)
    current_time = time.time()
    units_online = len(PRETRAINED_MODELS)
    status_text = f"UNITS ONLINE: {units_online} | STATUS: OPERATIONAL"
    draw_glow_text(surface, status_text, font_status, MATRIX_GREEN, 
                   center_x, 135, glow_radius=0, glow_alpha=15, centered=True)


def draw_pretrained_model_screen(surface, model_buttons, hovered_button):
    """Draw the enhanced AI unit database selection screen."""
    # Draw background
    draw_ai_database_background(surface)
    
    # Draw header
    draw_database_header(surface)
    
    # Get total screen dimensions for proper centering
    total_width = WIDTH + SIDE_BAR_WIDTH
    total_height = HEIGHT + TOP_BAR_HEIGHT
    
    # Updated card layout to fit all 5 units on screen - centered on full screen
    cards_per_row = 1  # Single column layout
    card_width = 320   # Keep good width for content
    card_height = 85   # Reduced height to fit all 5 units
    card_spacing_x = 0  # Not needed for single column
    card_spacing_y = 15  # Minimal spacing between cards
    
    start_x = (total_width - card_width) // 2  # Center relative to full screen width
    start_y = 170
    
    for i, (button_rect, model_name, params) in enumerate(model_buttons):
        # Phase 2: Updated positioning for single-column centered layout
        card_x = start_x  # All cards centered horizontally
        card_y = start_y + i * (card_height + card_spacing_y)  # Vertical stacking
        
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        is_hovered = (hovered_button == model_name)
        
        # Update button rect for click detection
        model_buttons[i] = (card_rect, model_name, params)
        
        # Draw AI unit card
        description = MODEL_DESCRIPTIONS[model_name]
        draw_ai_unit_card(surface, card_rect, model_name, params, description, is_hovered)
    
    # Phase 5: Optimized energy nodes for single-column layout
    node_positions = [
        (50, 50), (WIDTH - 50, 50), 
        (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50)
    ]
    draw_energy_nodes(surface, node_positions, ELECTRIC_PURPLE, pulse=True)
    
    # Phase 5: Consistent scan lines overlay with reduced intensity
    draw_scan_lines(surface, line_spacing=12, line_alpha=10, animate=True)  # Reduced intensity


def show_pretrained_models():
    """Show enhanced AI unit database selection interface."""
    # Initialize model cards (positions will be calculated in draw function)
    model_buttons = []
    for model_name, params in PRETRAINED_MODELS.items():
        # Updated placeholder rect with new smaller dimensions
        button_rect = pygame.Rect(0, 0, 320, 85)  # Updated to match new smaller card size
        model_buttons.append((button_rect, model_name, params))
    
    hovered_button = None
    clock = pygame.time.Clock()
    
    while True:
        # Draw the enhanced interface
        draw_pretrained_model_screen(screen, model_buttons, hovered_button)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                hovered_button = None
                for button_rect, model_name, params in model_buttons:
                    if button_rect.collidepoint(event.pos):
                        hovered_button = model_name
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, model_name, params in model_buttons:
                    if button_rect.collidepoint(event.pos):
                        return model_name, params
        
        pygame.display.flip()
        clock.tick(60)  # Smooth animations


# Import screen reference (will be set when this module is imported)
screen = None