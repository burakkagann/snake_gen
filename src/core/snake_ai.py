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
    
    def __init__(self, brain=None, use_enhanced_network=False):
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
        self.use_enhanced_network = use_enhanced_network

        # AI Weights - Enhanced network has more parameters
        if self.use_enhanced_network:
            # Enhanced network: 15 parameters with hidden layer weights
            if brain is None:
                # Initialize with Xavier/He initialization for better training
                self.brain = np.random.randn(15) * np.sqrt(2.0 / 15)
            else:
                self.brain = np.array(brain)
                # Pad old 9-parameter brains to 15 parameters if needed
                if len(self.brain) == 9:
                    self.brain = np.pad(self.brain, (0, 6), 'constant', constant_values=0.1)
        else:
            # Original 9-parameter network
            if brain is None:
                self.brain = np.random.uniform(-1.5, 1.5, 9)
                self.brain /= np.linalg.norm(self.brain)
            else:
                self.brain = np.array(brain)

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
        """Calculate the fitness score for this snake using multi-objective optimization."""
        # Survival time component (normalized)
        survival_time = time.time() - self.start_time
        survival_score = min(survival_time / 60.0, 1.0)  # Normalize to [0,1] over 60 seconds
        
        # Food collection efficiency (normalized)
        food_efficiency = self.score / max(self.moves_made, 1)  # Food per move
        food_efficiency_score = min(food_efficiency * 100, 1.0)  # Normalize to [0,1]
        
        # Length achievement (normalized)
        length_score = min(self.length / 100.0, 1.0)  # Normalize to [0,1] over 100 length
        
        # Movement efficiency (penalize excessive movement without progress)
        movement_efficiency = max(0, 1.0 - (self.moves_made / (self.score * 50 + 100)))
        
        # Food streak bonus (exponential reward for consecutive food collection)
        if self.score > 0:
            streak_bonus = min((self.score ** 0.8) / 50.0, 1.0)  # Diminishing returns
        else:
            streak_bonus = 0
        
        # Distance-based food seeking (reward for moving toward food when not eating)
        time_since_food = min((time.time() - self.last_food_time) / 10.0, 1.0)
        food_seeking_penalty = max(0, time_since_food - 0.5)  # Penalty after 5 seconds
        
        # Weighted combination of normalized components
        weights = {
            'survival': 0.25,
            'food_efficiency': 0.30,
            'length': 0.20,
            'movement_efficiency': 0.15,
            'streak_bonus': 0.10
        }
        
        fitness = (
            weights['survival'] * survival_score +
            weights['food_efficiency'] * food_efficiency_score +
            weights['length'] * length_score +
            weights['movement_efficiency'] * movement_efficiency +
            weights['streak_bonus'] * streak_bonus -
            food_seeking_penalty * 0.1
        )
        
        # Scale to reasonable range and ensure positivity
        return max(fitness * 1000, 1.0)

    def sigmoid(self, x):
        """Sigmoid activation function for non-linearity."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def tanh(self, x):
        """Hyperbolic tangent activation function."""
        return np.tanh(x)
    
    def relu(self, x):
        """ReLU activation function."""
        return np.maximum(0, x)

    def choose_direction(self):
        """Use AI to choose the best direction for the snake to move."""
        def calculate_features(new_x, new_y):
            """Calculate input features for the neural network."""
            features = []
            
            # Distance to food (normalized)
            distance_to_food = abs(self.food[0] - new_x) + abs(self.food[1] - new_y)
            features.append(distance_to_food / (WIDTH + HEIGHT))
            
            # Food direction (unit vector)
            food_dx = np.sign(self.food[0] - new_x)
            food_dy = np.sign(self.food[1] - new_y)
            features.append(food_dx)
            features.append(food_dy)
            
            # Wall distances (normalized)
            wall_dist_left = new_x / WIDTH
            wall_dist_right = (WIDTH - new_x) / WIDTH
            wall_dist_top = new_y / HEIGHT
            wall_dist_bottom = (HEIGHT - new_y) / HEIGHT
            features.append(min(wall_dist_left, wall_dist_right))
            features.append(min(wall_dist_top, wall_dist_bottom))
            
            # Loop detection
            visit_count = self.previous_positions.count((new_x, new_y))
            features.append(min(visit_count / 5.0, 1.0))
            
            # Safe moves available
            lookahead_positions = [(new_x + dx * CELL_SIZE, new_y + dy * CELL_SIZE) for dx, dy in DIRECTIONS]
            safe_moves = sum(1 for pos in lookahead_positions if pos not in self.snake and pos not in self.border_walls)
            features.append(safe_moves / 4.0)
            
            # Snake length context
            features.append(min(self.length / 100.0, 1.0))
            
            return np.array(features)
        
        def enhanced_neural_evaluation(features):
            """Enhanced neural network with non-linear activation."""
            if self.use_enhanced_network:
                # Split brain into layers for a simple feedforward network
                # We have 8 input features and 15 total parameters
                # Architecture: 8 inputs -> 4 hidden neurons -> 1 output
                
                # Weight allocation:
                # Hidden layer weights: 8 features * 4 neurons = 32 weights (but we only have 15)
                # So we'll use: 8 weights for hidden layer, 4 for output, 3 for biases
                
                # Hidden layer (simplified for 15 parameters)
                hidden_weights = self.brain[:8]  # 8 weights
                hidden_bias = self.brain[12]  # 1 bias
                
                # Linear combination with subset of features
                hidden_input = np.dot(features, hidden_weights) + hidden_bias
                hidden_activated = self.tanh(hidden_input)
                
                # Create hidden layer representation (expand scalar to vector if needed)
                if np.isscalar(hidden_activated):
                    hidden_vector = np.array([hidden_activated, hidden_activated * 0.5, 
                                            hidden_activated * 0.3, hidden_activated * 0.7])
                else:
                    hidden_vector = np.array([hidden_activated])
                
                # Output layer
                output_weights = self.brain[8:12]  # 4 weights  
                output_bias = self.brain[13]  # 1 bias
                
                # Ensure dimensions match
                weight_len = min(len(hidden_vector), len(output_weights))
                output = np.dot(hidden_vector[:weight_len], output_weights[:weight_len]) + output_bias
                
                # Apply sigmoid and scale
                return self.sigmoid(output) * 1000  # Scale to reasonable range
            else:
                # Original linear evaluation
                return np.dot(features, self.brain[:len(features)])
        
        def simulate_move(head, direction, depth=0):
            new_x = head[0] + direction[0] * CELL_SIZE
            new_y = head[1] + direction[1] * CELL_SIZE

            # Check for collision with snake or walls
            if (new_x, new_y) in self.snake or (new_x, new_y) in self.border_walls:
                return -1000

            # Calculate features and evaluate with neural network
            features = calculate_features(new_x, new_y)
            
            if self.use_enhanced_network:
                # Use enhanced neural network evaluation
                base_score = enhanced_neural_evaluation(features)
            else:
                # Original heuristic evaluation for backward compatibility
                distance_to_food = abs(self.food[0] - new_x) + abs(self.food[1] - new_y)
                food_bonus = self.brain[0] * (AI_CONFIG["FOOD_BONUS_CONSTANT"] if (new_x, new_y) == self.food else 0)
                toward_food_reward = self.brain[1] * (-distance_to_food)
                visit_count = self.previous_positions.count((new_x, new_y))
                loop_penalty = self.brain[3] * (-20 * visit_count if visit_count > 1 else 0)
                
                is_near_wall = new_x < CELL_SIZE or new_x > WIDTH - CELL_SIZE or new_y < CELL_SIZE or new_y > HEIGHT - CELL_SIZE
                is_food_near_wall = self.food[0] < CELL_SIZE or self.food[0] > WIDTH - CELL_SIZE or self.food[1] < CELL_SIZE or self.food[1] > HEIGHT - CELL_SIZE
                wall_penalty = self.brain[5] * (-3 if is_near_wall and not is_food_near_wall else 0)
                
                recent_directions = self.previous_directions[-10:]
                same_direction_count = sum(1 for d in recent_directions if d == self.direction)
                momentum_bonus = self.brain[7] * (10 if same_direction_count >= 3 else 0)
                
                unique_positions = len(set(self.previous_positions))
                exploration_bonus = self.brain[6] * (unique_positions / (len(self.previous_positions) + 1)) * np.exp(-0.05 * len(self.previous_positions))
                
                lookahead_positions = [(new_x + dx * CELL_SIZE, new_y + dy * CELL_SIZE) for dx, dy in DIRECTIONS]
                lookahead_collisions = sum(1 for pos in lookahead_positions if pos in self.snake)
                dead_end_penalty = self.brain[8] * (-20 if lookahead_collisions >= 2 else 0)
                
                base_score = (food_bonus + toward_food_reward + loop_penalty + wall_penalty + exploration_bonus + momentum_bonus + dead_end_penalty)

            # Recursive lookahead with adaptive depth
            if depth < self.get_lookahead_depth():
                future_scores = [simulate_move((new_x, new_y), next_move, depth + 1) for next_move in DIRECTIONS]
                best_future_score = max(future_scores)
                base_score += best_future_score * 0.5 if best_future_score >= -50 else -30

            return base_score

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
            # Add bonus for collecting food (scales with length)
            self.score += self.length * 2.5
        else:
            self.snake.pop()  # Move the snake
            # Small survival bonus (much smaller than before)
            self.score += 0.1

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


def rank_based_selection(snakes):
    """Select a snake using rank-based selection (linear ranking)."""
    sorted_snakes = sorted(snakes, key=lambda s: s.fitness_function())
    ranks = np.arange(1, len(sorted_snakes) + 1)
    probabilities = ranks / ranks.sum()
    selected_idx = np.random.choice(len(sorted_snakes), p=probabilities)
    return sorted_snakes[selected_idx]


def roulette_wheel_selection(snakes):
    """Select a snake using fitness-proportionate roulette wheel selection."""
    fitnesses = np.array([s.fitness_function() for s in snakes])
    # Ensure all fitnesses are positive
    min_fitness = min(fitnesses)
    if min_fitness < 0:
        fitnesses = fitnesses - min_fitness + 1
    
    # Calculate selection probabilities
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        # If all fitnesses are 0, select randomly
        return random.choice(snakes)
    
    probabilities = fitnesses / total_fitness
    selected_idx = np.random.choice(len(snakes), p=probabilities)
    return snakes[selected_idx]


def uniform_crossover(parent1_brain, parent2_brain, crossover_rate=0.5):
    """Perform uniform crossover between two parent brains."""
    new_brain = np.zeros_like(parent1_brain)
    for i in range(len(new_brain)):
        if random.random() < crossover_rate:
            new_brain[i] = parent1_brain[i]
        else:
            new_brain[i] = parent2_brain[i]
    return new_brain


def multi_point_crossover(parent1_brain, parent2_brain, num_points=2):
    """Perform multi-point crossover between two parent brains."""
    length = len(parent1_brain)
    if num_points >= length - 1:
        num_points = max(1, length - 2)
    
    # Generate random crossover points
    points = sorted(random.sample(range(1, length), num_points))
    points = [0] + points + [length]
    
    new_brain = np.zeros_like(parent1_brain)
    for i in range(len(points) - 1):
        if i % 2 == 0:
            new_brain[points[i]:points[i+1]] = parent1_brain[points[i]:points[i+1]]
        else:
            new_brain[points[i]:points[i+1]] = parent2_brain[points[i]:points[i+1]]
    
    return new_brain


def calculate_population_diversity(snakes):
    """Calculate the genetic diversity of the population."""
    if len(snakes) < 2:
        return 0.0
    
    brains = np.array([s.brain for s in snakes])
    # Calculate pairwise distances
    diversity = 0
    count = 0
    for i in range(len(brains)):
        for j in range(i + 1, len(brains)):
            diversity += np.linalg.norm(brains[i] - brains[j])
            count += 1
    
    return diversity / count if count > 0 else 0.0


def adaptive_mutation(brain, generation_fitness, population_diversity):
    """Apply adaptive mutation based on fitness progress and population diversity."""
    # Base mutation rate
    if len(generation_fitness) > 1 and generation_fitness[-1] > generation_fitness[-2]:
        base_mutation = AI_CONFIG["MUTATION_LOW"]
    else:
        base_mutation = AI_CONFIG["MUTATION_HIGH"]
    
    # Adjust based on population diversity (low diversity = higher mutation)
    diversity_factor = 1.0
    if population_diversity < 0.5:  # Low diversity threshold
        diversity_factor = 2.0
    elif population_diversity < 1.0:
        diversity_factor = 1.5
    
    mutation_rate = base_mutation * diversity_factor
    
    # Apply mutation with variable probability per gene
    mutated_brain = brain.copy()
    for i in range(len(mutated_brain)):
        if random.random() < 0.3:  # 30% chance to mutate each gene
            mutated_brain[i] += np.random.randn() * mutation_rate
    
    return mutated_brain


def evolve_snakes(snakes, generation_fitness):
    """Enhanced evolution with multiple selection and crossover strategies."""
    # Calculate current population diversity
    population_diversity = calculate_population_diversity(snakes)
    
    # Sort snakes by fitness
    sorted_snakes = sorted(snakes, key=lambda s: s.fitness_function(), reverse=True)
    
    # Elitism: Keep top performers
    elite_count = min(AI_CONFIG.get("ELITISM_COUNT", 3), len(snakes) // 10)
    new_snakes = [SnakeAI(brain=snake.brain.copy()) for snake in sorted_snakes[:elite_count]]
    
    # Selection strategy probabilities (dynamic based on diversity)
    if population_diversity < 0.5:
        # Low diversity: favor diverse selection methods
        selection_probs = {'tournament': 0.3, 'rank': 0.4, 'roulette': 0.3}
    else:
        # Good diversity: favor fitness-based selection
        selection_probs = {'tournament': 0.5, 'rank': 0.3, 'roulette': 0.2}
    
    # Generate offspring
    while len(new_snakes) < len(snakes):
        # Choose selection method
        selection_method = np.random.choice(
            list(selection_probs.keys()),
            p=list(selection_probs.values())
        )
        
        # Select parents
        if selection_method == 'tournament':
            parent1 = tournament_selection(sorted_snakes[:max(10, len(snakes)//2)])
            parent2 = tournament_selection(sorted_snakes[:max(10, len(snakes)//2)])
        elif selection_method == 'rank':
            parent1 = rank_based_selection(snakes)
            parent2 = rank_based_selection(snakes)
        else:  # roulette
            parent1 = roulette_wheel_selection(snakes)
            parent2 = roulette_wheel_selection(snakes)
        
        # Choose crossover method
        crossover_method = random.choice(['uniform', 'multi_point', 'single_point'])
        
        if crossover_method == 'uniform':
            new_brain = uniform_crossover(parent1.brain, parent2.brain)
        elif crossover_method == 'multi_point':
            new_brain = multi_point_crossover(parent1.brain, parent2.brain)
        else:  # single_point (original method)
            cut = np.random.randint(0, len(parent1.brain))
            new_brain = np.concatenate((parent1.brain[:cut], parent2.brain[cut:]))
        
        # Apply adaptive mutation
        new_brain = adaptive_mutation(new_brain, generation_fitness, population_diversity)
        
        # Create new snake
        new_snakes.append(SnakeAI(brain=new_brain))
        
        # Diversity injection with adaptive probability
        diversity_injection_prob = AI_CONFIG["DIVERSITY_INJECTION_PROB"]
        if population_diversity < 0.3:  # Very low diversity
            diversity_injection_prob *= 3
        
        if random.random() < diversity_injection_prob and len(new_snakes) < len(snakes):
            new_snakes.append(SnakeAI())  # Add completely random snake
    
    return new_snakes[:len(snakes)]  # Ensure population size remains the same