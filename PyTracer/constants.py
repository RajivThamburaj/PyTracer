"""
Ray tracing constants

Author: Rajiv Thamburaj
"""

import numpy as np

# Colors
WHITE = np.array([1, 1, 1], float)
BLACK = np.array([0, 0, 0], float)
RED = np.array([1, 0, 0], float)

# Screen constants
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
PIXEL_WIDTH = 1.0
GAMMA = 1.0
GAMMA_INVERSE = 1.0

# Mathematical constants
EPSILON = 1.0E-10