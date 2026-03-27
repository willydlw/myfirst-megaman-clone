import pygame 
from pygame.math import Vector2
import random

from .assetManager import AssetManager

import logging 

# create a logger named "item" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)


class RewardItem(pygame.sprite.Sprite):
    # Physics and movement
    DEFAULT_VELOCITY_Y = -8
    GRAVITY = 0.5 

    # Timing in milliseconds 
    LIFESPAN = 5000             # Total time item exists
    BLINK_THRESHOLD = 2000      # start blinking when 2 seconds remain

    def __init__(self, x, y, name):
        super().__init__()

        # Asset loading and rect setup
        self.name = name 
        self.image = AssetManager.get_image(name)

        self.rect = self.image.get_rect(center=(x,y))
        self.hitbox = self.rect.copy()

        # Physics and movement
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, self.DEFAULT_VELOCITY_Y) 

        # Lifetime
        self.spawn_time = pygame.time.get_ticks() 
        self.visible = True 

        self.energy = self.__gen_energy(name)

        logger.info(f"Item {name} initialized")

    def __gen_energy(self):
        if self.name == "life_energy":
            return random.randint(2,4)
        elif self.name == "big_life_energy":
            return random.randint(8,12)
        else:
            logger.warning(f"unknown reward item name: {self.name}")
            return 0


    def update(self, collision_tiles):
        # Apply physics
        self.velocity.y += self.GRAVITY
        self.position += self.velocity 

        # update hitbox and rect positions 
        self.hitbox.center = self.position 

        # Basic floor collision so items don't fall through the world 
        for tile in collision_tiles: 
            if self.hitbox.colliderect(tile.rect):
                if self.velocity.y > 0: # falling 
                    self.hitbox.bottom = tile.rect.top 
                    self.velocity.y = 0 
                    self.position.y = self.hitbox.centery 

        self.rect.center = self.hitbox.center

        # life span and blinking 
        current_time = pygame.time.get_ticks() 
        time_elapsed = current_time - self.spawn_time 
        time_remaining = self.LIFESPAN - time_elapsed 

        if time_remaining <= 0:
            self.kill() 
        elif time_remaining < self.BLINK_THRESHOLD:
            # flicker every 100ms (10 times per second)
            self.visible = (current_time % 200) < 100
        else:
            self.visible = True 

    def draw(self, surface):
        pass