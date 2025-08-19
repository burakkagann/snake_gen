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
BUTTON_WIDTH, BUTTON_HEIGHT = 280, 65

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
DARK_GREEN = (0, 120, 30)  # Dark green for text
DARK_BLUE = (0, 30, 120)  # Dark blue for text

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

# Glow Effect Color Variants (with alpha for transparency)
GLOW_CYAN_OUTER = (*NEON_CYAN, 30)      # Outer glow layer
GLOW_CYAN_INNER = (*NEON_CYAN, 80)      # Inner glow layer
GLOW_MAGENTA_OUTER = (*NEON_MAGENTA, 30)
GLOW_MAGENTA_INNER = (*NEON_MAGENTA, 80)
GLOW_GREEN_OUTER = (*NEON_GREEN, 30)
GLOW_GREEN_INNER = (*NEON_GREEN, 80)
GLOW_BLUE_OUTER = (*NEON_BLUE, 30)
GLOW_BLUE_INNER = (*NEON_BLUE, 80)
GLOW_ORANGE_OUTER = (*NEON_ORANGE, 30)
GLOW_ORANGE_INNER = (*NEON_ORANGE, 80)
GLOW_PURPLE_OUTER = (*ELECTRIC_PURPLE, 30)
GLOW_PURPLE_INNER = (*ELECTRIC_PURPLE, 80)
GLOW_PINK_OUTER = (*CYBER_PINK, 30)
GLOW_PINK_INNER = (*CYBER_PINK, 80)

# Glow Parameters
GLOW_RADIUS_OUTER = 8    # Outer glow spread
GLOW_RADIUS_INNER = 4    # Inner glow spread
GLOW_ALPHA_MAX = 120     # Maximum glow opacity
GLOW_ALPHA_MIN = 30      # Minimum glow opacity

# Animation Timing Constants
PULSE_SPEED = 0.02       # Speed of pulsing animations
SCAN_LINE_SPEED = 2.0    # Speed of scan line movement
FADE_DURATION = 30       # Frames for fade in/out effects
HOVER_TRANSITION = 15    # Frames for hover state transitions

# Circuit Board Pattern Constants
CIRCUIT_LINE_WIDTH = 1   # Width of circuit traces
CIRCUIT_GRID_SIZE = 40   # Grid spacing for circuit patterns
CIRCUIT_ALPHA = 40       # Transparency of circuit patterns
ENERGY_PULSE_SPEED = 1.5 # Speed of energy pulses along circuits

# Typography Enhancement Constants
FONT_RETRO_LARGE = 48    # Large retro font size
FONT_RETRO_MEDIUM = 32   # Medium retro font size
FONT_RETRO_SMALL = 20    # Small retro font size (reduced for better button fit)
TEXT_GLOW_OFFSET = 2     # Offset for text glow effect
TEXT_SHADOW_ALPHA = 60   # Transparency of text shadows

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

# Font System Configuration
RETRO_FONTS = [
    "assets/PressStart2P-Regular.ttf",  # Primary retro font
    "assets/Orbitron-Regular.ttf",     # Futuristic alternative
    "Courier New",                      # Monospace fallback
    "Monaco",                          # macOS monospace
    "Consolas"                         # Windows monospace
]

# Font loading function (to be used in other modules)
def load_retro_font(size):
    """Load the best available retro font at specified size."""
    import pygame
    for font_name in RETRO_FONTS:
        try:
            if font_name.endswith('.ttf'):
                # Try loading from file
                font = pygame.font.Font(font_name, size)
                return font
            else:
                # Try system font with reduced boldness
                font = pygame.font.SysFont(font_name, size, bold=False)
                return font
        except:
            continue
    # Ultimate fallback - clean system font
    return pygame.font.SysFont('arial', size, bold=False)

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