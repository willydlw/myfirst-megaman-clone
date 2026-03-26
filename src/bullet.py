import pygame 

from .assetManager import AssetManager
from .constants import SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__() 

        # Use pygame surface (no image for bullet)
        self.image = AssetManager.get_image("bullet")
        self.rect = self.image.get_rect(center=(x,y))
        self.hitbox = self.rect.copy()
        self.speed = 10
        self.direction = direction 

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed 

        # Kill if it leaves the screen:
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()