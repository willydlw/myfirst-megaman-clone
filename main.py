import pygame
import logging 
from pathlib import Path 

from src import Game 


def configure_logger():

    # Define the absolute path for the log file 
    BASE_DIR = Path(__file__).resolve().parent      # points to folder where main.py resides
    LOG_FILE = BASE_DIR / "game_errors.log"

    # Configure the root logger using the absolute path
    # all loggers in the project are children of the root and 
    # automatically inherit settings
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(str(LOG_FILE), mode="w"),
            logging.StreamHandler()                  # prints to console
        ]
    )

    # Creates a branch logger named __main__ 
    logger = logging.getLogger(__name__) # create a logger for this file

    logger.info(f"Log file initialized at: {LOG_FILE}")


def main():

    configure_logger()

    try:
        game = Game(1) 
        game.run()
    finally:
        # This blocks runs no matter what (even if the game crashes)
        pygame.quit()


    
if __name__ == "__main__":
    main()

    
