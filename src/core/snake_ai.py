"""
AI Snake Module for Snake Gen v11.5
Contains the SnakeAI class and genetic algorithm functions.
"""

import random
import numpy as np
import time
from ..game.config import *


class SnakeAI:
    """AI-controlled Snake that uses genetic algorithms for decision making."""
    
    def __init__(self, brain=None):
        # Initialize snake at center
        self.snake = [(GAME_AREA_X + GAME_AREA_WIDTH // 2,
                       GAME_AREA_Y + GAME_AREA_HEIGHT // 2)]
        self.direction = random.choice(DIRECTIONS)
        self.moves_made = 0
        self.score = 0
        self.fitness_score = 0
        self.length = 0
        self.alive = True
        self.start_time = time.time()
        self.last_food_time = time.time()
        self.previous_positions = []
        self.previous_directions = []

        # AI Weights
        if brain is None:
            # Smaller range for stability
            self.brain = np.random.uniform(-1.5, 1.5, 9)
            self.brain /= np.linalg.norm(self.brain)  # Keep values balanced
        else:
            self.brain = np.array(brain)  # Ensure it's a NumPy array

        self.border_walls = set()
        for x in range(GAME_AREA_X - CELL_SIZE, GAME_AREA_X + GAME_AREA_WIDTH + CELL_SIZE, CELL_SIZE):
            self.border_walls.add((x, GAME_AREA_Y - CELL_SIZE))  # Top border
            self.border_walls.add(
                (x, GAME_AREA_Y + GAME_AREA_HEIGHT))  # Bottom border

        for y in range(GAME_AREA_Y - CELL_SIZE, GAME_AREA_Y + GAME_AREA_HEIGHT + CELL_SIZE, CELL_SIZE):
            self.border_walls.add((GAME_AREA_X - CELL_SIZE, y))  # Left border
            self.border_walls.add(
                (GAME_AREA_X + GAME_AREA_WIDTH, y))  # Right border

        self.food = self.spawn_food()

    def spawn_food(self):
        """Spawn food at a random location not occupied by the snake."""
        while True:
            food_x = random.randrange(
                GAME_AREA_X, GAME_AREA_X + GAME_AREA_WIDTH, CELL_SIZE)
            food_y = random.randrange(
                GAME_AREA_Y, GAME_AREA_Y + GAME_AREA_HEIGHT, CELL_SIZE)
            if (food_x, food_y) not in self.snake:
                return food_x, food_y

    def get_lookahead_depth(self):
        """Get adaptive lookahead depth based on snake length."""
        # Adaptive lookahead: deeper when snake is small, shallower when large
        if self.length < AI_CONFIG["LOOKAHEAD_DEPTH_THRESHOLD"]:
            return AI_CONFIG["LOOKAHEAD_DEPTH_BASE"] + 1
        return AI_CONFIG["LOOKAHEAD_DEPTH_BASE"]

    def detect_loop(self):
        """Detect if the snake is stuck in a repetitive movement loop."""
        history_window = max(15, self.length * 2)
        if len(self.previous_positions) < history_window:
            return False
        position_counts = {}
        for pos in self.previous_positions[-history_window:]:
            position_counts[pos] = position_counts.get(pos, 0) + 1
        loop_threshold = 3 if self.length < 10 else 4
        return max(position_counts.values()) >= loop_threshold

    def fitness_function(self):
        """Calculate the fitness score for this snake."""
        fitness = (self.score * self.length * 5) + (time.time() -
                                                    self.start_time) * 10 - (self.moves_made / (self.score + 1))
        food_streak_bonus = (self.score ** 1.5) * 2  # Encourages streaks
        fitness += food_streak_bonus
        return fitness

    def choose_direction(self):
        """Use AI to choose the best direction for the snake to move."""
        def simulate_move(head, direction, depth=0):
            new_x = head[0] + direction[0] * CELL_SIZE
            new_y = head[1] + direction[1] * CELL_SIZE

            # Check for collision with snake or walls
            if (new_x, new_y) in self.snake or (new_x, new_y) in self.border_walls:
                return -1000

            # Heuristic evaluation:
            distance_to_food = abs(
                self.food[0] - new_x) + abs(self.food[1] - new_y)
            food_bonus = self.brain[0] * (AI_CONFIG["FOOD_BONUS_CONSTANT"]
                                          if (new_x, new_y) == self.food else 0)
            toward_food_reward = self.brain[1] * (-distance_to_food)
            visit_count = self.previous_positions.count((new_x, new_y))
            loop_penalty = self.brain[3] * \
                (-20 * visit_count if visit_count > 1 else 0)

            is_near_wall = new_x < CELL_SIZE or new_x > WIDTH - \
                CELL_SIZE or new_y < CELL_SIZE or new_y > HEIGHT - CELL_SIZE
            is_food_near_wall = self.food[0] < CELL_SIZE or self.food[0] > WIDTH - \
                CELL_SIZE or self.food[1] < CELL_SIZE or self.food[1] > HEIGHT - CELL_SIZE
            wall_penalty = self.brain[5] * \
                (-3 if is_near_wall and not is_food_near_wall else 0)

            recent_directions = self.previous_directions[-10:]
            same_direction_count = sum(
                1 for d in recent_directions if d == self.direction)
            momentum_bonus = self.brain[7] * \
                (10 if same_direction_count >= 3 else 0)

            unique_positions = len(set(self.previous_positions))
            exploration_bonus = self.brain[6] * (unique_positions / (
                len(self.previous_positions) + 1)) * np.exp(-0.05 * len(self.previous_positions))
            lookahead_positions = [
                (new_x + dx * CELL_SIZE, new_y + dy * CELL_SIZE) for dx, dy in DIRECTIONS]
            lookahead_collisions = sum(
                1 for pos in lookahead_positions if pos in self.snake)
            dead_end_penalty = self.brain[8] * \
                (-20 if lookahead_collisions >= 2 else 0)

            if depth > 0 and visit_count > 1:
                loop_penalty -= 10 * depth

            total_score = (food_bonus + toward_food_reward + loop_penalty +
                           wall_penalty + exploration_bonus + momentum_bonus + dead_end_penalty)

            # Recursive lookahead with adaptive depth:
            if depth < self.get_lookahead_depth():
                future_scores = [simulate_move(
                    (new_x, new_y), next_move, depth + 1) for next_move in DIRECTIONS]
                best_future_score = max(future_scores)
                total_score += best_future_score * 0.7 if best_future_score >= -50 else -30

            return total_score

        head = self.snake[0]
        best_move = None
        best_score = float('-inf')
        for move in DIRECTIONS:
            score = simulate_move(head, move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move if best_move is not None else random.choice(DIRECTIONS)

    def move(self):
        """Move the snake based on AI decision."""
        if not self.alive:
            return

        self.direction = self.choose_direction()
        head_x, head_y = self.snake[0]
        new_head = (
            head_x + self.direction[0] * CELL_SIZE, head_y + self.direction[1] * CELL_SIZE)

        # Collision check
        if new_head in self.snake or new_head in self.border_walls:
            self.alive = False
            return

        # Move the snake
        self.snake.insert(0, new_head)
        self.previous_positions.append(new_head)

        self.moves_made += 1  # Track the total moves the snake makes

        # Check loop detection
        if time.time() - self.last_food_time > 15:  # Extend starvation time
            self.alive = False

        if self.detect_loop():
            self.fitness_score -= 50  # Penalize fitness score
            if random.random() > 0.5:  # 50% chance to survive the loop
                self.alive = False

        # Check for food collection
        if new_head == self.food:
            self.score += 50
            self.length += 1
            self.food = self.spawn_food()
            self.last_food_time = time.time()  # Update time when food is eaten
        else:
            self.snake.pop()  # Move the snake

        # Add survival bonus
        self.score += 1 + (self.length * 2.5)

        if time.time() - self.last_food_time > 10 and self.length < 500:
            self.alive = False  # Kill snake if no food eaten in 10 seconds

        # Update fitness
        self.fitness_score = self.fitness_function()


# Genetic Algorithm Functions

def log_and_print(*args, **kwargs):
    """Prints output to the console and also writes it to a log file."""
    print(*args, **kwargs)  # Print to terminal
    with open(LOG_FILENAME, "a") as log_file:
        print(*args, **kwargs, file=log_file)  # Also write to log file


def tournament_selection(snakes, tournament_size=AI_CONFIG["TOURNAMENT_SIZE"]):
    """Selects a snake using tournament selection."""
    participants = random.sample(snakes, tournament_size)
    return max(participants, key=lambda s: s.fitness_function())


def evolve_snakes(snakes, generation_fitness):
    """Evolves the population by selecting top performers, mutating, and generating offspring."""
    top_performers = sorted(snakes, key=lambda s: s.fitness_function(), reverse=True)[:10]
    new_snakes = []

    for _ in range(len(snakes)):
        parent1 = tournament_selection(top_performers)
        parent2 = tournament_selection(top_performers)
        cut = np.random.randint(0, len(parent1.brain))
        new_brain = np.concatenate((parent1.brain[:cut], parent2.brain[cut:]))

        # Adaptive mutation
        if len(generation_fitness) > 1 and generation_fitness[-1] > generation_fitness[-2]:
            mutation_factor = AI_CONFIG["MUTATION_LOW"]
        else:
            mutation_factor = AI_CONFIG["MUTATION_HIGH"]
        
        new_brain += np.random.randn(len(new_brain)) * mutation_factor

        new_snakes.append(SnakeAI(brain=new_brain))

        # Inject random diversity occasionally
        if random.random() < AI_CONFIG["DIVERSITY_INJECTION_PROB"]:
            new_snakes.append(SnakeAI())

    return new_snakes[:len(snakes)]  # Ensure population size remains the same