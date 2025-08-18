"""
Configuration file for Snake Gen v11.5
Contains all constants, colors, and game settings used across the application.
"""

# Game Constants
WIDTH, HEIGHT = 600, 600
TOP_BAR_HEIGHT = 50
SIDE_BAR_WIDTH = 200
PADDING = 20
CELL_SIZE = 20
GAP = 2
FPS = 60

# Menu Constants
MENU_WIDTH, MENU_HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

# Manual Gameplay Constants
MANUAL_FPS = 10

# 80s Sci-Fi Neon Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (15, 15, 25)  # Deep space background
NEON_CYAN = (0, 255, 255)  # Electric cyan
NEON_MAGENTA = (255, 0, 255)  # Hot magenta
NEON_GREEN = (0, 255, 127)  # Electric green
NEON_BLUE = (0, 191, 255)  # Electric blue
NEON_ORANGE = (255, 165, 0)  # Neon orange
ELECTRIC_PURPLE = (138, 43, 226)  # Electric purple
CYBER_PINK = (255, 20, 147)  # Deep pink
MATRIX_GREEN = (0, 255, 65)  # Matrix-style green

# UI Element Colors
UI_BORDER = NEON_CYAN
UI_HIGHLIGHT = NEON_MAGENTA
UI_ACCENT = ELECTRIC_PURPLE
UI_SUCCESS = NEON_GREEN
UI_WARNING = NEON_ORANGE
UI_DANGER = CYBER_PINK
HOVER_COLOR = (150, 150, 150)

# Game Element Colors
SNAKE_COLOR = NEON_GREEN
FOOD_COLOR = CYBER_PINK
WALL_COLOR = NEON_BLUE
HUD_COLOR = NEON_CYAN

# Legacy color mappings for compatibility
BACKGROUND_GRAY = DARK_BG
GRAY = (64, 64, 80)
GREEN = SNAKE_COLOR
RED = FOOD_COLOR
BROWN = WALL_COLOR
BLUE = NEON_BLUE

# Game Area Calculations
GAME_AREA_X = PADDING
GAME_AREA_Y = PADDING + TOP_BAR_HEIGHT
GAME_AREA_WIDTH = WIDTH - 2 * PADDING
GAME_AREA_HEIGHT = HEIGHT - 2 * PADDING

# Directions
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# AI Configuration & Hyperparameters
AI_CONFIG = {
    # Base lookahead depth (can be adaptive)
    "LOOKAHEAD_DEPTH_BASE": 2,
    "LOOKAHEAD_DEPTH_THRESHOLD": 10,    # Snake length threshold for adjusting depth
    "FOOD_BONUS_CONSTANT": 75,
    "MUTATION_LOW": 0.1,                # Mutation factor when generation is improving
    "MUTATION_HIGH": 0.3,               # Mutation factor when improvement stalls
    "ELITISM_COUNT": 3,                 # Number of top snakes carried directly over
    "TOURNAMENT_SIZE": 3,               # Number of participants for tournament selection
    "DIVERSITY_INJECTION_PROB": 0.05      # Chance to insert a completely random snake
}

# Pre-trained AI Models
PRETRAINED_MODELS = {
    "Hunter":       [4.583, 1.024, -0.472, 0.315, -2.127, -1.038, 1.143, -1.476, -1.018],
    "Strategist":   [3.472, 0.832, -0.754, 0.206, -2.473, -0.482, 0.583, -1.219, -1.452],
    "Explorer": 	[2.765, 0.746, -0.621, 0.381, -1.825, -0.752, 1.493, -0.975, -1.189],
    "Risk Taker": 	[5.218, 1.217, -0.347, 0.089, -0.493, -2.013, -0.472, -1.839, -2.047],
    "AI Mastery":   [4.590, 0.791, 5.276, -0.006, -2.184, -3.037, 2.219, -1.856, -0.787],
}

# Model Descriptions
MODEL_DESCRIPTIONS = {
    "Hunter": "Moves aggressively toward food.",
    "Strategist": "Balances food collection with long-term survival.",
    "Explorer": "Mix of exploration and food-seeking.",
    "Risk Taker": "Adapts risky strategies for short period of time.",
    "AI Mastery": "Advanced AI with optimized weights."
}

# Training Recommendations
TRAINING_RECOMMENDATIONS = [
    ("Quick Testing", "10-15", "5-10", "Test behavior changes"),
    ("Balanced Learning", "20-30", "15-25", "Good learning vs. performance"),
    ("Deep Optimization", "40-50", "30-50", "Best for AI mastery")
]

# File Paths
LOG_FILENAME = "training_log.txt"
BACKGROUND_IMAGE_PATH = "assets/background.webp"
FONT_PATH = "assets/PressStart2P-Regular.ttf"

# Menu Button Definitions
MENU_BUTTONS = [
    {"text": "Manual Play", "action": "manual"},
    {"text": "Train AI", "action": "train"},
    {"text": "Pre-Trained AI", "action": "pretrained"},
    {"text": "Quit", "action": "quit"},
]

# AI Parameter Labels
AI_PARAMETER_LABELS = [
    "- Food Bonus", "- Toward Food", "- Away Penalty", "- Loop Penalty",
    "- Survival Bonus", "- Wall Penalty", "- Exploration Bonus",
    "- Momentum Bonus", "- Dead-End Penalty"
]

# Default Population Settings
DEFAULT_SNAKE_POPULATION = 50