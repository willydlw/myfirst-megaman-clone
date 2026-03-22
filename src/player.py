import pygame 
from pygame.math import Vector2 

from .assetManager import AssetManager
from . import constants as c

import logging 


# create a logger named "player" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # call the Sprite parent constructor
        super().__init__()

        logger.info("Returned from calling Sprite parent constructor")

        # Get image from static AssetManager
        self.image = AssetManager.get_image("player_right")

        # self.rect is for Drawing (matches the current image size)
        self.rect = self.image.get_rect(topleft=(x,y))

        # self.hitbox is for Collisions
        self.hitbox = pygame.Rect(x, y, c.PLAYER_HITBOX_WIDTH, c.PLAYER_HITBOX_HEIGHT)

        # Create the rectangle from the image's dimensions
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # movement variables
        self.velocity = Vector2(0, 0)
        self.direction = "right"
        self.jumping = False 

    def draw_debug(self, surface):
        """Draws the collision hitbox and drawing rect for debugging."""

        # draw the hitbox in red 
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

        # draw the visual rect in blue to see the image boundary 
        pygame.draw.rect(surface, (0, 0, 255), self.rect, 1)

    def update(self):
        # move the collision box 
        self.hitbox.x += self.velocity.x 
        self.hitbox.y += self.velocity.y 

        # align the drawing rect to the hitbox 
        # using midbottom keeps the player anchored to the floor correctly
        self.rect.midbottom = self.hitbox.midbottom 

    
    def update_image(self):
        pass 
        """
        if self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right 
            elif self.direction == "left":
                self.image = player_image_jump_left 
        else:  
            if self.direction == "right":
                self.image = player_image_right 
            elif self.direction == "left":
                self.image = player_image_left

        Jump Transitions 

        jump images and standing images are different sizes. The Player.rect will
        change when switching images. To keep player from sinking into floor or
        jittering:

        Ensures player stays anchored to floo rather than the top-left corner
        self.image = AssetManager.get_image("player_jump_right")
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        """