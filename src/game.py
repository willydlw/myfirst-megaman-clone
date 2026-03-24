import pygame 
import sys 
import logging 

from . import constants as c

from .assetManager import AssetManager
from .player import Player 
from .tile import Tile 
from .tile_map import GAME_MAP_1

# create a logger named "game" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)


class Game:
    def __init__(self, level):
        
        logger.info("Initializing Game object")

        # 1. Initialize pygame modules 
        pygame.init() 

        # 2. Set up the display
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() 
        self.running = True 

        # Create groups for collision and non-collision tiles 
        self.collision_tiles = pygame.sprite.Group()
        self.non_collision_tiles = pygame.sprite.Group()

        # 3. Load asset and then create the mape
        AssetManager.load_all(c.ASSETS_CONFIG_PATH)
        self.setup_level(level)

        # 4. Set up player 
        self.player = Player(c.PLAYER_START_X, c.PLAYER_START_Y)
        self.player_moving_this_frame = False 

        # 5. Setup background 
        self.background_image = AssetManager.get_image("background")
    

    def add_tiles(self, code, tile):
        """ Append tiles to collision or non-collision list, depending on code."""
        if code < c.NON_COLLISION_TILE_THRESHOLD:
            self.non_collision_tiles.add(tile)
        else:
            self.collision_tiles.add(tile)

    def create_map(self, level_map):

        # create map 
        for row, row_data in enumerate(level_map):
            for col, code in enumerate(row_data):
                code = level_map[row][col]
                x = col * c.TILE_SIZE 
                y = row * c.TILE_SIZE

                if code == c.SKY: # pygame window background color
                    continue    
                elif code == c.ROCK_TILE_1:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_1")))
                elif code == c.ROCK_TILE_2:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_2")))
                elif code == c.ROCK_TILE_3:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_3")))
                elif code == c.ROCK_TILE_4:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_4")))
                elif code == c.FLOOR_TILE:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("floor_tile")))
                   
        

    def setup_level(self, level):

        # TODO: add functionality for setting up different levels 
        # and switching between levels

        level_map = None

        if level == 1:
            level_map = GAME_MAP_1 

        self.create_map(level_map)


    def run(self):
        """The main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw() 
            self.clock.tick(c.FPS)


    def handle_events(self):
        moving = False      # Track is keys are held this frame

        # Handle "one-time" events (Closing window, single-press Jump)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    self.player.shoot()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.player.stop_jump()  # cut the jump height

        # Handle continuous movement events 
        keys = pygame.key.get_pressed() 

        # continuous key press jumping
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                    self.player.jump() 

        # continuous key press left/right
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.velocity.x -= c.ACCELERATION
            self.player.direction = "left"
            moving = True 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.velocity.x += c.ACCELERATION
            self.player.direction = "right"
            moving = True 
        
        self.player_moving_this_frame = moving 
    

    def update(self):
        self.player.update(self.collision_tiles, self.player_moving_this_frame)
        self.player.bullets.update()

    def draw(self):
        self.screen.fill(c.BACKGROUND_COLOR)

        # draw the level tiles
        self.non_collision_tiles.draw(self.screen)
        self.collision_tiles.draw(self.screen)

        # draw megaman image
        self.screen.blit(self.player.image, self.player.rect)

        # draw debug boxes (optional, for troubleshooting)
        self.player.draw_debug(self.screen)
        self.player.bullets.draw(self.screen) 
        pygame.display.flip()

