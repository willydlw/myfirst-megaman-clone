import pygame 
import sys 

from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR, ASSETS_CONFIG_PATH
from .assetManager import AssetManager

class Game:
    def __init__(self):
        # 1. Initialize pygame modules 
        pygame.init() 

        # 2. Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() 
        self.running = True 

        # 3. Create the Assets manager and load resources 
        self.assets = AssetManager()
        self.load_resources()
    
    def load_resources(self):
        """Centralized method to load all files at startup."""
        self.assets.load_all(ASSETS_CONFIG_PATH)

    def run(self):
        """The main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw() 
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit() 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        pygame.display.flip()

if __name__ == "__main__":
    my_game = Game()
    my_game.run()