import pygame 
from pygame.math import Vector2

from .assetManager import AssetManager

import logging 

# create a logger named "item" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)


class RewardItem(pygame.sprite.Sprite):
    DEFAULT_VELOCITY_Y = -11 

    def __init__(self, x, y, name):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, self.DEFAULT_VELOCITY_Y) 

        self.image = AssetManager.get_image(name)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

        logger.info("Item initialized")

    def update(self):
        pass

    def draw(self, surface):
        pass