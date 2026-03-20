import pygame 
import json 
import os 

class Assets:
    def __init__(self):
        # Dictionaries to cache loaded assets 
        self.images = {}
        self.fonts = {} 

    def load_all(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Load Images
        for name, path in config.get("images", {}).items():
            if os.path.exists(path):
                # .convert_alpha() improves performance fro transparent images 
                self.images[name] = pygame.image.load(path).convert_alpha
            else:
                print(f"Warning: Image not found at {path}")

        # load fonts 
        for name, data in config.get("fonts", {}).items():
            path = data["path"]
            size = data["size"]
            if os.path.exists(path):
                self.fonts[name] = pygame.font.Font(path, size)
            else:
                print(f"Warning: Font not found at {path}")
    

    def get_image(self, name):
        return self.images.get(name)
    
    def get_font(self, name):
        return self.fonts.get(name)