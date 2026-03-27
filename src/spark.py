import pygame 
import random 
from pygame.math import Vector2 

class Spark(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 

        # create a tine 4x4 or 2x2 sqaure 
        self.image = pygame.Surface((4,4))
        self.image.fill((255,200, 0))
        self.rect = self.image.get_rect(center=(x,y))

        self.position = Vector2(x, y)
        # explode outwards in random directions 
        self.velocity = Vector2(random.uniform(-4, 4), random.uniform(-6, -2))
        self.gravity = 0.3 
        self.lifetime = 20      # frames until it vanishes 

    def update(self):
        self.velocity.y += self.gravity 
        self.position += self.velocity 
        self.rect.center = self.position 

        self.lifetime -= 1 
        if self.lifetime <= 0:
            self.kill()