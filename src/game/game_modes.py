"""
Game Modes Module for Snake Gen v11.5
Contains handlers for different game modes to simplify main() function.
"""

import time
import sys
import pygame
from .config import *
from ..core.snake_ai import SnakeAI, log_and_print
from ..interfaces.training_interface import get_training_parameters, show_pretrained_models
from ..interfaces.manual_gameplay import run_manual_mode


def handle_manual_mode():
    """Handle manual gameplay mode."""
    print("Starting Manual Play...")
    return run_manual_mode()


def reset_training_data(generation_fitness, generation_avg_fitness, 
                       generation_lengths, generation_avg_lengths):
    """Reset all training history data."""
    generation_fitness.clear()
    generation_avg_fitness.clear()
    generation_lengths.clear()
    generation_avg_lengths.clear()


def run_training_session(snakes_per_gen, num_generations, generation_fitness,
                        generation_avg_fitness, generation_lengths, 
                        generation_avg_lengths, run_generation_func):
    """Run a complete AI training session."""
    # Initialize snake population
    snakes = [SnakeAI() for _ in range(snakes_per_gen)]
    print(f"Starting AI Training with {snakes_per_gen} snakes per generation for {num_generations} generations.")
    print("Population size:", len(snakes))
    
    training_start_time = time.time()
    best_weights = None
    
    for generation in range(num_generations):
        # Get current generation stats
        best_score = max((snake.score for snake in snakes if snake.alive), default=0)
        best_length = max((snake.length for snake in snakes if snake.alive), default=0)
        elapsed_time = round(time.time() - training_start_time, 2)
        
        # Find best snake and save its weights
        best_snake = max(snakes, key=lambda s: s.fitness_function(), default=None)
        if best_snake:
            best_weights = best_snake.brain.tolist()
        
        # Log generation progress
        log_and_print(f"Generation {generation+1} - Best Score: {best_score}, Length: {best_length}, Time: {elapsed_time}s")
        
        # Run the generation
        snakes = run_generation_func()
    
    training_time = round(time.time() - training_start_time, 2)
    return best_weights, training_time


def handle_training_mode(best_score_overall, best_length_overall, 
                        generation_fitness, generation_avg_fitness,
                        generation_lengths, generation_avg_lengths,
                        run_generation_func, show_training_summary_func,
                        run_pretrained_from_training_func):
    """Handle AI training mode with replay functionality."""
    while True:  # Allow replaying AI training
        snakes_per_gen, num_generations = get_training_parameters()
        
        # Reset training history
        reset_training_data(generation_fitness, generation_avg_fitness,
                           generation_lengths, generation_avg_lengths)
        
        # Run training session
        best_weights, training_time = run_training_session(
            snakes_per_gen, num_generations, generation_fitness,
            generation_avg_fitness, generation_lengths, generation_avg_lengths,
            run_generation_func)
        
        # Show training summary and handle user choice
        action = show_training_summary_func(best_score_overall, best_length_overall, training_time)
        
        if action == "replay":
            continue
        elif action == "pretrain":
            run_pretrained_from_training_func(best_weights)
            return "menu"  # Return to main menu
        elif action == "menu":
            return "menu"  # Return to main menu
        
        break  # Exit training mode


def handle_pretrained_mode(run_pretrained_ai_func):
    """Handle pre-trained AI mode."""
    model_name, model_params = show_pretrained_models()
    print(f"Selected {model_name} with parameters: {model_params}")
    return run_pretrained_ai_func(model_params)


def handle_quit_mode():
    """Handle game quit."""
    print("Exiting Game...")
    pygame.quit()
    sys.exit()


def get_mode_handler(selection):
    """Get the appropriate handler function for the selected mode."""
    handlers = {
        "manual": handle_manual_mode,
        "quit": handle_quit_mode
    }
    return handlers.get(selection, None)