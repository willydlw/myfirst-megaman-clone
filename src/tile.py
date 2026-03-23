import pygame 

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__() 
        self.image = image 

        self.rect = self.image.get_rect(topleft=(x,y))

    def __repr__(self):
        """Technical Details: Tile(x, y, size)"""
        return f"Tile(x={self.rect.x}, y={self.rect.y}), size={self.rect.size}"
    
    def __str__(self):
        """Simple Description: Tile at (x, y)"""
        return f"Tile at ({self.rect.x}, {self.rect.y})"