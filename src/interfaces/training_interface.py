"""
Training Interface Module for Snake Gen v11.5
Contains functions for AI training setup and monitoring interfaces.
"""

import pygame
import sys
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


def draw_training_setup_screen(surface, input_values, active_box, submit_button):
    """Draw the main training setup screen elements."""
    surface.fill(BACKGROUND_GRAY)
    
    # Fonts
    font_large = pygame.font.SysFont(None, 50)
    font_small = pygame.font.SysFont(None, 30)
    font_table_small = pygame.font.SysFont(None, 24)
    
    # Title
    draw_text_centered(surface, "AI Training Setup", font_large, BLACK, 
                      WIDTH // 2, HEIGHT // 4)
    
    # Input boxes
    input_boxes = {
        "snakes_per_gen": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 40),
        "num_generations": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 40),
    }
    
    # Draw input boxes
    for key, box in input_boxes.items():
        bg_color = WHITE
        border_color = UI_HIGHLIGHT if active_box == key else GRAY
        border_width = 3 if active_box == key else 1
        
        pygame.draw.rect(surface, bg_color, box, border_radius=5)
        pygame.draw.rect(surface, border_color, box, width=border_width, border_radius=5)
        
        text_surface = font_small.render(input_values[key], True, BLACK)
        surface.blit(text_surface, (box.x + 10, box.y + 10))
    
    # Draw labels
    label_x_offset = input_boxes["snakes_per_gen"].width // 2
    surface.blit(font_small.render("# of Snakes:", True, BLACK),
                (input_boxes["snakes_per_gen"].x + label_x_offset - 50, 
                 input_boxes["snakes_per_gen"].y - 35))
    surface.blit(font_small.render("# of Generations:", True, BLACK),
                (input_boxes["num_generations"].x + label_x_offset - 80, 
                 input_boxes["num_generations"].y - 35))
    
    # Draw submit button
    draw_button(surface, submit_button, "Start", font_small, GREEN, UI_SUCCESS, WHITE)
    
    # Draw training recommendations table
    table_start_y = submit_button.y + 60
    draw_training_recommendations_table(surface, font_small, font_table_small, table_start_y)
    
    return input_boxes


def get_training_parameters():
    """Get training parameters from user input with a clean, modular interface."""
    input_values = {"snakes_per_gen": "", "num_generations": ""}
    active_box = None
    submit_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 100, 100, 40)
    
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


def draw_pretrained_model_screen(surface, model_buttons, hovered_button):
    """Draw the pre-trained model selection screen."""
    surface.fill(BACKGROUND_GRAY)
    font_large = pygame.font.SysFont(None, 50)
    font_small = pygame.font.SysFont(None, 30)
    
    # Title
    draw_text_centered(surface, "Select Pre-Trained Model", font_large, BROWN,
                      WIDTH // 2, HEIGHT // 6)
    
    # Draw model buttons with descriptions
    for button_rect, model_name, params in model_buttons:
        is_hovered = (hovered_button == model_name)
        color = UI_SUCCESS if is_hovered else GREEN
        
        draw_button(surface, button_rect, model_name, font_small, color, UI_HIGHLIGHT, WHITE, is_hovered)
        
        # Display model explanation next to the button
        explanation = MODEL_DESCRIPTIONS[model_name]
        explanation_text = font_small.render(explanation, True, BLACK)
        surface.blit(explanation_text, (button_rect.x + button_rect.width + 20, button_rect.y + 10))


def show_pretrained_models():
    """Show pre-trained model selection interface with improved modularity."""
    model_buttons = []
    button_width, button_height = 200, 50
    button_y = HEIGHT // 3.2
    
    # Create button rectangles
    for i, (model_name, params) in enumerate(PRETRAINED_MODELS.items()):
        button_x = WIDTH // 4 - button_width // 2
        button_rect = pygame.Rect(button_x, button_y + i * 80, button_width, button_height)
        model_buttons.append((button_rect, model_name, params))
    
    hovered_button = None
    
    while True:
        # Draw the interface
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


# Import screen reference (will be set when this module is imported)
screen = None