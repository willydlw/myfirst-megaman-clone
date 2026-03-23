# Configuration File Path 
ASSETS_CONFIG_PATH = "assets.json"

# game 
SCREEN_WIDTH = 512 
SCREEN_HEIGHT = 512

FPS = 60


# player 

# player starting position
PLAYER_START_X = SCREEN_WIDTH / 2 
PLAYER_START_Y = SCREEN_HEIGHT / 2

# Player 
PLAYER_HITBOX_WIDTH =  24
PLAYER_HITBOX_HEIGHT = 40 

# player jump images have 13:15 ratio
PLAYER_JUMP_WIDTH = 52 
PLAYER_JUMP_HEIGHT = 60

PLAYER_DISTANCE = 5

PLAYER_WALK_SIZE = 48 

# Forces
GRAVITY = 0.8       # higher gravity keeps jump snappy, not floaty
FRICTION = 0.9      # Keeps 90% of velocity (slippery)

# Acceleration when key pressed 
ACCELERATION = 0.5


JUMP_STRENGTH = 11   # try range 10 to  15


MAX_SPEED = 11
MIN_SPEED = 0.1


# enemy variables 
METALL_WIDTH = 36
METALL_HEIGHT = 30 


# tiles
TILE_SIZE = 32 

# colors
BACKGROUND_COLOR = (255,255,255) #(25, 52, 230)