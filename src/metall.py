import logging 
import pygame 

from pygame.math import Vector2 

from .assetManager import AssetManager
from .constants import METALL_HITBOX_HEIGHT, METALL_HITBOX_WIDTH, GRAVITY


# create a logger named "player" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)

class Metall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Movement variables 
        self.position = Vector2(x,y)
        self.velocity = Vector2(0, 0)   # Can drop down from sky, no horizontal movement
        self.guarding = False 
        self.direction = "left"

         # Animation State 
        self.frame_index = 0 

      
        # Group animations for faster/easier access
        self.animations = {
            "metall_left": [AssetManager.get_image("metall_left")],
            "metall_right": [AssetManager.get_image("metall_right")],
            "metall_guard_left": [AssetManager.get_image("metall_guard_left")],
            "metall_guard_right": [AssetManager.get_image("metall_guard_right")],
        }

       
        # Set initial animation state 
        current_state = f"metall_{self.direction}"

        # self.hitbox is for Collisions
        self.hitbox = pygame.Rect(x, y, METALL_HITBOX_WIDTH, METALL_HITBOX_HEIGHT)

        # Set self.image and self.rect based on current state
        self.image = self.animations[current_state][0]

        # self.rect is for Drawing (matches the current image size)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

        logger.info("Metall initialized")     

    
    def update(self, tiles):
        # apply gravity 
        self.velocity.y += GRAVITY

        # Y-Axis Movement and Collision
        self.position.y += self.velocity.y
        self.hitbox.y = round(self.position.y)

        for tile in tiles:
             if self.hitbox.colliderect(tile.rect):
                if self.velocity.y > 0:                   # moving down, hit floor 
                    self.hitbox.bottom = tile.rect.top 
                    self.velocity.y = 0
                self.position.y = self.hitbox.y
                break # stop checking tiles once we collide

        # Sync image rect to hitbox 
        self.rect.midbottom = self.hitbox.midbottom 


    def __repr__(self):
        """Developer-friendly representation: Metall(x, y, direction)"""
        msg = (
            f"Metall, position(x={self.hitbox.x}, y={self.hitbox.y}, " 
            f"velocity(x={self.velocity.x}, y={self.velocity.y})"
            f"direction='{self.direction})'"
        )
        return msg
    
    def __str__(self):
        """User-friendly summary: Metall at (x, y) facing [direction]"""
        return f"Metall at ({self.hitbox.x}, {self.hitbox.y}) facing {self.direction}"