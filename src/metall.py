import pygame 

from pygame.math import Vector2 

from .assetManager import AssetManager

class Metall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # can drop down from the sky. Does not move horizontally 
        self.velocity = Vector2(0, 0)
        self.direction = "left"


        # Set self.image and self.rect based on current state
        self.image = AssetManager.get_image("metall_left")

        # self.rect is for Drawing (matches the current image size)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)