import pygame 
from pygame.math import Vector2

import logging 

from .assetManager import AssetManager
from . import constants as c 


# create a logger named "player" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)


class MetallBullet(pygame.sprite.Sprite):

    BULLET_WIDTH = 12
    BULLET_HEIGHT = BULLET_WIDTH 
    BULLET_VELOCITY_X = 2 
    BULLET_VELOCITY_Y = BULLET_VELOCITY_X 

    def __init__(self, x, y, vel_x, vel_y):
        super().__init__() 
        self.image = AssetManager.get_image("metall_bullet")
        self.rect = self.image.get_rect(center=(x,y))
        self.hitbox = self.rect.copy() 

        self.velocity = pygame.math.Vector2(vel_x, vel_y)
        self.position = pygame.math.Vector2(x, y)

    
    def update(self):
        self.position += self.velocity 
        self.hitbox.center = (round(self.position.x), round(self.position.y))
        self.rect.center = self.hitbox.center 

        # Kill bullet if it leaves the screen 
        if not (0 <= self.rect.x <= c.SCREEN_WIDTH and 0 <= self.rect.y <= c.SCREEN_HEIGHT):
            self.kill()