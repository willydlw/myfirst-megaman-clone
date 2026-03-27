import pygame 
from pygame.math import Vector2 

from .assetManager import AssetManager
from .constants import SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    
    VELOCITY_X = 10

    def __init__(self, x, y, direction):
        super().__init__() 

        # Use pygame surface (no image for bullet)
        self.image = AssetManager.get_image("bullet")
        self.rect = self.image.get_rect(center=(x,y))
        self.hitbox = self.rect.copy()
        self.position = Vector2(x, y)
        self.velocity = Vector2(self.VELOCITY_X, 0)
        self.direction = direction 
        if self.direction == "left":
            self.velocity.x *= -1
        

    def update(self):
        
        self.position.x += self.velocity.x
        self.rect.x += self.velocity.x 
        self.hitbox.x = self.rect.x 
        
        # Kill if it leaves the screen:
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()