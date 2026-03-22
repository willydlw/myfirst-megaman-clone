import pygame 
import sys 
import logging 

from . import constants as c

from .assetManager import AssetManager
from .player import Player 
from .tile import Tile 

# create a logger named "game" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        
        logger.info("Initializing Game object")

        # 1. Initialize pygame modules 
        pygame.init() 

        # 2. Set up the display
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() 
        self.running = True 

        # Create a group for collision tiles 
        self.tiles = pygame.sprite.Group()

        # 3. Load asset and then create the mape
        AssetManager.load_all(c.ASSETS_CONFIG_PATH)
        self.setup_level()

        # 4. Set up player 
        self.player = Player(c.PLAYER_START_X, c.PLAYER_START_Y)

        # 5. Setup background 
        self.background_image = AssetManager.get_image("background")
    

    def setup_level(self):
        # 'X' represents a floor tile, ' ' is empty space
        level_map = [
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "    XXXX        ",
            "                ",
            "XXXXXXXXXXXXXXXX",
            "                "
        ]

        floor_tile_image = AssetManager.get_image("floor_tile")

        for row_idx, row in enumerate(level_map):
            for col_idx, cell in enumerate(row):
                if cell == "X":
                    x = col_idx * c.TILE_SIZE
                    y = row_idx * c.TILE_SIZE 
                    tile = Tile(x, y, floor_tile_image)
                    self.tiles.add(tile)


    def run(self):
        """The main game loop."""
        while self.running:
            self.handle_events()
            #self.update()
            self.draw() 
            self.clock.tick(c.FPS)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 

            keys = pygame.key.get_pressed() 
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                logger.info("UP arrow or w key pressed")
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                logger.info("DOWN arrow or s key pressed")
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                logger.info("LEFT arrow or a key pressed")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                logger.info("RIGHT arrow or d key pressed")
    

    def draw(self):
        self.screen.fill(c.BACKGROUND_COLOR)
        self.tiles.draw(self.screen)
        self.player.draw_debug(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    my_game = Game()
    my_game.run()