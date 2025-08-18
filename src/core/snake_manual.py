"""
Manual Snake Module for Snake Gen v11.5
Contains the ManualKeysSnake class for user-controlled gameplay.
"""

import random
import time
import pygame
from ..game.config import *


# Manual controls mapping (UP, DOWN, LEFT, RIGHT)
MANUAL_DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


class ManualKeysSnake:
    """Snake controlled by user keyboard input."""
    
    def __init__(self):
        # Initialize Snake First
        self.snake = [(GAME_AREA_X + GAME_AREA_WIDTH // 2,
                       GAME_AREA_Y + GAME_AREA_HEIGHT // 2)]
        self.direction = MANUAL_DIRECTIONS[pygame.K_RIGHT]
        self.score = 0
        self.length = 0
        self.alive = True
        self.start_time = time.time()
        self.last_food_time = time.time()
        self.moves_made = 0  # Track total moves
        self.food_collected = 0  # Track total food eaten

        # Define Border Walls Before Spawning Food
        self.border_walls = set()
        for x in range(GAME_AREA_X - CELL_SIZE, GAME_AREA_X + GAME_AREA_WIDTH + CELL_SIZE, CELL_SIZE):
            self.border_walls.add((x, GAME_AREA_Y - CELL_SIZE))  # Top border
            self.border_walls.add(
                (x, GAME_AREA_Y + GAME_AREA_HEIGHT))  # Bottom border

        for y in range(GAME_AREA_Y - CELL_SIZE, GAME_AREA_Y + GAME_AREA_HEIGHT + CELL_SIZE, CELL_SIZE):
            self.border_walls.add((GAME_AREA_X - CELL_SIZE, y))  # Left border
            self.border_walls.add(
                (GAME_AREA_X + GAME_AREA_WIDTH, y))  # Right border

        # Now Spawn Food After Everything is Initialized
        self.food = self.spawn_food()

    def spawn_food(self):
        """Spawn food at a random location not occupied by snake or walls."""
        while True:
            food_x = random.randrange(
                GAME_AREA_X, GAME_AREA_X + GAME_AREA_WIDTH, CELL_SIZE)
            food_y = random.randrange(
                GAME_AREA_Y, GAME_AREA_Y + GAME_AREA_HEIGHT, CELL_SIZE)
            if (food_x, food_y) not in self.snake and (food_x, food_y) not in self.border_walls:
                return food_x, food_y

    def move(self):
        """Move the snake based on current direction."""
        head_x, head_y = self.snake[0]
        new_head = (
            head_x + self.direction[0] * CELL_SIZE, head_y + self.direction[1] * CELL_SIZE)

        # Wall Collision Detection
        if (
            new_head in self.snake  # Self-collision
            or new_head[0] < GAME_AREA_X  # Hits left wall
            or new_head[0] >= GAME_AREA_X + GAME_AREA_WIDTH  # Hits right wall
            or new_head[1] < GAME_AREA_Y  # Hits top wall
            # Hits bottom wall
            or new_head[1] >= GAME_AREA_Y + GAME_AREA_HEIGHT
        ):
            self.alive = False
            return  # Prevents further execution

        # Move the snake
        self.snake.insert(0, new_head)
        self.moves_made += 1
        
        # Food Collection Detection
        if new_head == self.food:  # Checks correct position
            self.score += 50
            self.length += 1
            self.food = self.spawn_food()
            self.last_food_time = time.time()
        else:
            self.snake.pop()  # Move the snake

        # Starvation Mechanism
        if time.time() - self.last_food_time > 10:
            self.alive = False  # Only starve if 10s passes without food


def get_manual_direction_from_key(event_key, current_direction):
    """Get new direction from keyboard input, preventing reversal."""
    if event_key in MANUAL_DIRECTIONS:
        new_direction = MANUAL_DIRECTIONS[event_key]
        # Prevent reversing
        if new_direction != (-current_direction[0], -current_direction[1]):
            return new_direction
    return current_direction