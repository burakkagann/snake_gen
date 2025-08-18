"""
Core Snake Classes
Contains the main snake implementations for AI and manual control.
"""

from .snake_ai import SnakeAI, evolve_snakes, log_and_print, tournament_selection
from .snake_manual import ManualKeysSnake, get_manual_direction_from_key

__all__ = [
    'SnakeAI', 'evolve_snakes', 'log_and_print', 'tournament_selection',
    'ManualKeysSnake', 'get_manual_direction_from_key'
]