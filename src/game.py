import pygame 
import sys 
import logging 

from . import constants as c

from .assetManager import AssetManager
from .player import Player 

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


        # 3. Load all assets 
        AssetManager.load_all(c.ASSETS_CONFIG_PATH)

        # 4. Set up player 
        self.player = Player(c.PLAYER_START_X, c.PLAYER_START_Y)
       

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
        self.player.draw_debug(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    my_game = Game()
    my_game.run()