# Configuration File Path 
ASSETS_CONFIG_PATH = "assets.json"

# game 
SCREEN_WIDTH = 512 
SCREEN_HEIGHT = 512
FPS = 60

# player starting position
PLAYER_START_X = SCREEN_WIDTH / 2 
PLAYER_START_Y = SCREEN_HEIGHT / 2



# Acceleration and Velocity
GRAVITY = 0.8          # How fast the player falls back down

ACCELERATION = 0.5     # How fast they speed up on X-axis
FRICTION = 0.9         # How fast they slide to a stop



# tiles
TILE_SIZE = 32 

# colors
BACKGROUND_COLOR = (255,255,255) #(25, 52, 230)


# mapping symbols 
SKY          = 0
ROCK_TILE_1  = 1
ROCK_TILE_2  = 2
ROCK_TILE_3  = 3
ROCK_TILE_4  = 4
FLOOR_TILE   = 5
WALL_TILE    = 6
BEAM_TILE    = 7 
SPIKE_TILE   = 8 
DOOR_TILE    = 9 
ROOM_TILE    = 10 
METALL       = 11 
BLADER       = 12


NON_COLLISION_TILE_THRESHOLD = 5


