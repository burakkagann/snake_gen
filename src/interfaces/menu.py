import pygame
import sys
from ..game.config import *

# Initialize pygame
pygame.init()

# Create Pygame Screen
screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pygame.display.set_caption("Gen Snake - Main Menu")

# Load Font
font = pygame.font.SysFont(None, 40)

background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)


def draw_menu():
    screen.blit(pygame.transform.scale(
        background_image, (MENU_WIDTH, MENU_HEIGHT)), (0, 0))

    # Draw Buttons
    for i, button in enumerate(MENU_BUTTONS):
        x = MENU_WIDTH // 2 - BUTTON_WIDTH // 2
        y = MENU_HEIGHT // 2 - 100 + i * (BUTTON_HEIGHT + 20)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        color = HOVER_COLOR if x <= mouse_x <= x + \
            BUTTON_WIDTH and y <= mouse_y <= y + BUTTON_HEIGHT else GRAY

        pygame.draw.rect(screen, color, (x, y, BUTTON_WIDTH,
                         BUTTON_HEIGHT), border_radius=10)
        text = font.render(button["text"], True, WHITE)
        screen.blit(text, (x + BUTTON_WIDTH // 2 - text.get_width() //
                    2, y + BUTTON_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()


def menu_screen():
    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for button in MENU_BUTTONS:
                    x = MENU_WIDTH // 2 - BUTTON_WIDTH // 2
                    y = MENU_HEIGHT // 2 - 100 + \
                        MENU_BUTTONS.index(button) * (BUTTON_HEIGHT + 20)

                    if x <= mouse_x <= x + BUTTON_WIDTH and y <= mouse_y <= y + BUTTON_HEIGHT:
                        return button["action"]  # Return the selected action
