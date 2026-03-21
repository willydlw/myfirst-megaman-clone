import os 
import json 
import pygame 
from pathlib import Path

import logging 

# create a logger named "assetManager" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)


class AssetManager:
    def __init__(self):
        # Dictionaries to cache loaded assets 
        self.images = {}
        self.fonts = {} 

    def load_all(self, config_path):
        logger.info("Loading assets...")
        # 1. Setup base directory (One level up from where this script resides)
        # .resolve() gets the absolute path, .parent is the script's folder,
        # and the second .parent goe up one more level 
        BASE_DIR = Path(__file__).resolve().parent.parent 

        print(f"config_path: {config_path}")
        print(f"BASE_DIR: {BASE_DIR}")


        # 2. Load Config 
        try:
            # Join BASE_DIR with the config_path provided 
            full_config_path = BASE_DIR / config_path
            with open(full_config_path, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Critical: Could not load config at {full_config_path}. Error: {e}")
            return 
        
        # 3. Load Images 
        for name, relative_path in config.get("images", {}).items():
            full_path = BASE_DIR / relative_path 
            self.images[name] = self._safe_load_image(full_path)

        # 4. Load fonts 
        for name, data in config.get("fonts", {}).items():
            full_path = BASE_DIR / data.get("path", "")
            self.fonts[name] = self._safe_load_font(full_path, data.get("size", 24))
            
    
    def _safe_load_image(self, path):
        """Tries to load an image; returns a magenta square on failure"""
        try:
            # pygame.image requires a string, convert Path object
            # .convert_alpha() improves performance fro transparent images 
            return pygame.image.load(str(path)).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print(f"Warning Image missing: {path}")
            # Create a 32x32 magenta square as a placeholder 
            fallback = pygame.Surface((32,32))
            fallback.fill((255, 0, 255)) # bright magenta 
            return fallback
        
    def _safe_load_font(self, path, size):
        """Tries to load a font; returns system default on failure"""
        try:
            return pygame.font.Font(str(path), size)
        except (pygame.error, FileNotFoundError):
            print(f"Warning:Font missing at {path}. Using system default.")
            return pygame.font.SysFont("Arial", size)


    def get_image(self, name):
        return self.images.get(name)
    
    def get_font(self, name):
        return self.fonts.get(name)