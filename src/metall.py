import logging 
import pygame 

from pygame.math import Vector2 

from .assetManager import AssetManager
from . import constants as c
from .metallBullet import MetallBullet



# create a logger named "player" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)

class Metall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # States: GUARD, POP_UP, SHOOT, HIDE
        self.state = "GUARD"
        self.guarding = True 
        self.state_timer = pygame.time.get_ticks() 
        self.detection_range = c.METALL_DETECTION_RANGE 

        # Movement variables 
        self.position = Vector2(x,y)
        self.velocity = Vector2(0, 0)   # Can drop down from sky, no horizontal movement
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
        self.hitbox = pygame.Rect(x, y, c.METALL_HITBOX_WIDTH, c.METALL_HITBOX_HEIGHT)

        # Set self.image and self.rect based on current state
        self.image = self.animations[current_state][0]

        # self.rect is for Drawing (matches the current image size)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

        logger.info("Metall initialized")     

    
    def update(self, collision_tiles, player_pos, bullet_group):
        # apply gravity
        self.velocity.y += c.GRAVITY
        self.position.y += self.velocity.y
        self.hitbox.y = round(self.position.y)

        self.__check_tile_collision(collision_tiles)        
        self.__update_state(player_pos, bullet_group)
        self.__update_animation() 

        # Sync image rect to hitbox 
        self.rect.midbottom = self.hitbox.midbottom 

    
    def __check_tile_collision(self, collision_tiles):
        """Metalls dropping from sky stop when colliding with floor tiles"""
        for tile in collision_tiles:
             if self.hitbox.colliderect(tile.rect):
                if self.velocity.y > 0:                   # moving down, hit floor 
                    self.hitbox.bottom = tile.rect.top 
                    self.velocity.y = 0
                self.position.y = self.hitbox.y
                break # stop checking tiles once we collide
        

    def __update_state(self, player_pos, bullet_group):
        current_time = pygame.time.get_ticks()
        
        if self.state == "GUARD":
            self.guarding = True 
            # Face the player
            if player_pos.x < self.position.x:
                self.direction = "left"
            else:
                self.direction = "right"

            dist_to_player = self.position.distance_to(player_pos) 
            if dist_to_player < self.detection_range:
                self.state = "POP_UP"
                self.state_timer = current_time 

        elif self.state == "POP_UP":
            self.guarding = False 
            if current_time - self.state_timer > 500: # half second to pop up
                self.state = "SHOOT"
                self.__shoot(bullet_group) 
                self.state_timer = current_time 

        elif self.state == "SHOOT":
            # wait a momemnt after shooting before hiding
            if current_time - self.state_timer > 300:
                self.state = "HIDE"
                self.state_timer = current_time

        elif self.state == "HIDE":
            self.guarding = True   # start hiding during the animation
            if current_time - self.state_timer > 500:
                self.state = "GUARD"

    
    def __update_animation(self):
        # swap images based on state and direction 
        suffix = "guard" if self.guarding else ""
        state_key = f'metall_{suffix}_{self.direction}'.replace("__", "_")
        self.image = self.animations[state_key][0]


    def __shoot(self, bullet_group):
        # Determine horizontal base direction 
        dir_mulitiplier = -1 if self.direction == "left" else 1 

        # Spawn 3 bullets: Diagonally up, straight, diagonally down 
        # Velocities: (x, -y), (x, 0), (x, y)
        bullet_data = [
            (c.METALL_BULLET_VELOCITY_X * dir_mulitiplier, -c.METALL_BULLET_VELOCITY_Y),
            (c.METALL_BULLET_VELOCITY_X * dir_mulitiplier, 0),
            (c.METALL_BULLET_VELOCITY_X * dir_mulitiplier, c.METALL_BULLET_VELOCITY_Y)
        ]

        for vx, vy in bullet_data:
            bullet = MetallBullet(self.rect.centerx, self.rect.centery, vx, vy)
            bullet_group.add(bullet)

        logger.debug(f"Metall fired a 3-way spread {self.direction}")


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