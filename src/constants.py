# Configuration File Path 
ASSETS_CONFIG_PATH = "assets.json"

# game 
SCREEN_WIDTH = 512 
SCREEN_HEIGHT = 512
FPS = 60

# player starting position
PLAYER_START_X = SCREEN_WIDTH / 2 
PLAYER_START_Y = SCREEN_HEIGHT / 2

# Player 
PLAYER_HITBOX_WIDTH =  24
PLAYER_HITBOX_HEIGHT = 40 


# Acceleration and Velocity
GRAVITY = 0.8          # How fast the player falls back down
JUMP_STRENGTH = 14     # How high the player launches (negative velocity)
ACCELERATION = 0.5     # How fast they speed up on X-axis
FRICTION = 0.9         # How fast they slide to a stop
MAX_SPEED = 5          # Speed cap
MIN_SPEED = 0.1        # Threshold to stop "creeping"


# enemy variables 
METALL_WIDTH = 36
METALL_HEIGHT = 30 


# tiles
TILE_SIZE = 32 

# colors
BACKGROUND_COLOR = (255,255,255) #(25, 52, 230)


COYOTE_DURATION = 150   # milliseconds of grace period