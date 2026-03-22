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
    # 1. Define class-level dictionaries (static variables)
    _images = {}
    _fonts = {}

    @classmethod 
    def load_all(cls, config_path):
        logger.info(f"Loading assets, config_path: {config_path}")

        # 1. Setup base directory (One level up from where this script resides)
        # .resolve() gets the absolute path, .parent is the script's folder,
        # and the second .parent goe up one more level 
        BASE_DIR = Path(__file__).resolve().parent.parent 

        # 2. Load json configuration file
        try:
            # Join BASE_DIR with the config_path provided 
            full_config_path = BASE_DIR / config_path
            with open(full_config_path, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            logger.error(f"Critical: Could not load config at {full_config_path}. Error: {e}")
            return 
        
        # 3. Load Images 
        for name, data in config.get("images", {}).items():
            if isinstance(data, dict):
                path = data.get("path")
                scale = data.get("scale")
            else:
                path = data 
                scale = None 

            full_path = BASE_DIR / path 
            img = cls._safe_load_image(full_path)

            # scale only once, when loading 
            if scale:
                logger.info(f"scaling image {name}, scale: {scale[0]}, {scale[1]}")
                img = pygame.transform.scale(img, (scale[0], scale[1]))

            cls._images[name] = img 

        # 4. Load fonts 
        for name, data in config.get("fonts", {}).items():
            full_path = BASE_DIR / data.get("path", "")
            cls._fonts[name] = cls._safe_load_font(full_path, data.get("size", 24))
            
    @staticmethod 
    def _safe_load_image(path):
        """Tries to load an image; returns a magenta square on failure"""
        try:
            # pygame.image requires a string, convert Path object
            # .convert_alpha() improves performance fro transparent images 
            return pygame.image.load(str(path)).convert_alpha()
        
        except (pygame.error, FileNotFoundError):
            logger.warning(f"Image missing: {path}")
            # Create a 32x32 magenta square as a placeholder 
            fallback = pygame.Surface((32,32))
            fallback.fill((255, 0, 255)) # bright magenta 
            return fallback

    @staticmethod
    def _safe_load_font(path, size):
        """Tries to load a font; returns system default on failure"""
        try:
            return pygame.font.Font(str(path), size)
        except (pygame.error, FileNotFoundError):
            logger.warning(f"Font missing at {path}. Using system default.")
            return pygame.font.SysFont("Arial", size)

    @classmethod
    def get_image(cls, name):
        return cls._images.get(name)
    
    @classmethod
    def get_font(cls, name):
        return cls._fonts.get(name)