import pygame
import sys 
import logging 
from pathlib import Path 

from src import Game 


def handle_exception(exc_type, exc_value, exc_traceback):
    """Captures any uncaught exceptions and logs them."""
    # Don't log a simple 'Ctrl+C' exit as an errror 
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return 
    
    # log the crash with a full traceback 
    logging.critical("Uncaught exception occurred:",
                     exc_info=(exc_type, exc_value, exc_traceback))



def main():

    # 1. Define the absolute path for the log file 
    BASE_DIR = Path(__file__).resolve().parent      # points to folder where main.py resides
    LOG_FILE = BASE_DIR / "game_errors.log"


    # 2. Configure the root logger using the absolute path
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

    # 3. Tell python to use our function instead of the default one  for uncaught execptions
    #sys.excepthook = handle_exception


    # 4. creates a branch logger named __main__ 
    logger = logging.getLogger(__name__) # create a logger for this file
    logger.info(f"Log file initialized at: {LOG_FILE}")

    # 5. Start the game
    try:
        game = Game(1) 
        game.run()
    finally:
        # This blocks runs no matter what (even if the game crashes)
        pygame.quit()
        #sys.exit()

    
if __name__ == "__main__":
    main()

    
