"""Configuration settings for the Resistor Recognition system."""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Image paths (relative to project root)
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, 'background_equations.png')
LOGO_IMAGE = os.path.join(ASSETS_DIR, 'logo.png')
TEMPLATE_IMAGE = os.path.join(ASSETS_DIR, 'resistor_template.jpg')
REFERENCE_IMAGE = os.path.join(ASSETS_DIR, 'reference.jpg')

# Window dimensions
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 550
FRAME_WIDTH = 830
FRAME_HEIGHT = 490

# Image processing thresholds
THRESHOLD_VALUE = 140
MIN_CONTOUR_AREA = 200
CAMERA_UPDATE_INTERVAL = 10

# Color detection parameters
HSV_RANGES = {
    'gold': {'lower': [11, 32, 54], 'upper': [22, 53, 141]},
    'brown': {'lower': [0, 50, 50], 'upper': [180, 76, 120]},
    'black': {'lower': [25, 0, 20], 'upper': [150, 90, 86]},
    'green': {'lower': [40, 130, 62], 'upper': [74, 180, 115]},
    'yellow': {'lower': [23, 98, 138], 'upper': [53, 190, 240]},
    'red': {'lower': [150, 110, 90], 'upper': [180, 180, 210]},
    'violet': {'lower': [125, 50, 100], 'upper': [167, 125, 160]},
    'blue': {'lower': [90, 94, 79], 'upper': [120, 148, 138]},
    'orange': {'lower': [0, 110, 145], 'upper': [30, 174, 205]},
    'white': {'lower': [20, 12, 134], 'upper': [30, 40, 170]},
    'grey': {'lower': [44, 0, 46], 'upper': [180, 20, 90]}
}