import pygame 
import os 

class Assets:
    def __init__(self):
        # Dictionaries to cache loaded assets 
        self.images = {}
        self.fonts = {} 

    def load_image(self, name, path):
        """Loads and optimizes an image then stores in the dictionary"""
        try:
            # .convert_alpha() is essential for PNGs with transparency 
            image = pygame.image.load(path).convert_alpha()
            self.images[name] = image 
        except pygame.error as e:
            print(f"Unable to load image at {path}: {e}")

    def load_font(self, name, path_or_sysname, size, is_system=False):
        """Loads a font (either from a file or system) and stores it"""
        try:
            if is_system:
                # Use SysFont for built-in system fonts like Arial 
                font = pygame.font.SysFont(path_or_sysname, size)
            else:
                font = pygame.font.Font(path_or_sysname, size)
            self.fonts[name] = font 
        except pygame.error as e:
            print(f"Unable to load font {path_or_sysname}: {e}")

    def get_image(self, name):
        return self.images.get(name)
    
    def get_font(self, name):
        return self.fonts.get(name)