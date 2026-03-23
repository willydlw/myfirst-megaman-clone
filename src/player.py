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

        # Movement variables 
        self.position = Vector2(x,y)
        self.velocity = Vector2(0, 0)
        self.jumping = False 
        self.direction = "right"

        # Walking Animation Frame Lists
        self.walk_left_frames = [
            AssetManager.get_image("player-left-walk-0"),
            AssetManager.get_image("player-left-walk-1"),
            AssetManager.get_image("player-left-walk-2"),
            AssetManager.get_image("player-left-walk-3"),
        ]

        self.walk_right_frames = [
            AssetManager.get_image("player-right-walk-0"),
            AssetManager.get_image("player-right-walk-1"),
            AssetManager.get_image("player-right-walk-2"),
            AssetManager.get_image("player-right-walk-3"),
        ]

        # Animation State 
        self.frame_index = 0 
        self.animation_speed = 100      # ms between frames 
        self.last_update = pygame.time.get_ticks()

        # Group animations for easy access 
        self.animations = {
            "idle_right": [AssetManager.get_image("player_right")],
            "idle_left":  [AssetManager.get_image("player_left")],
            "jump_right": [AssetManager.get_image("player_jump_right")],
            "jump_left":  [AssetManager.get_image("player_jump_left")],
            "walk_right": self.walk_right_frames,
            "walk_left":  self.walk_left_frames
        }

        # Set initial state 
        current_state = f"idle_{self.direction}"

        # self.hitbox is for Collisions
        self.hitbox = pygame.Rect(x, y, c.PLAYER_HITBOX_WIDTH, c.PLAYER_HITBOX_HEIGHT)

        # Set self.image and self.rect based on current state
        self.image = self.animations[current_state][0]

        # self.rect is for Drawing (matches the current image size)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

        logger.info("Player initialized")      


    def draw_debug(self, surface):
        """Draws the collision hitbox and drawing rect for debugging."""

        # draw the hitbox in red 
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

        # draw the visual rect in blue to see the image boundary 
        pygame.draw.rect(surface, (0, 0, 255), self.rect, 1)

    def animate(self, moving_this_frame):
        now = pygame.time.get_ticks() 

        # 1. Determine the state 
        if self.jumping:
            state = "jump_" + self.direction 
        elif moving_this_frame and abs(self.velocity.x) > c.MIN_SPEED:
            state = "walk_" + self.direction 
        else:
            state = "idle_" + self.direction 

        # 2. Get the current frame list 
        current_frames = self.animations.get(state, self.animations["idle_right"])

        # 3. Cycle frames base on timer 
        if now - self.last_update > self.animation_speed:
            self.last_update = now 
            # reset frame index if switching to idle (idle only has 1 frame)
            if len(current_frames) == 1:
                self.frame_index = 0
            else:
                self.frame_index = (self.frame_index + 1) % len(current_frames)
            
            self.image = current_frames[self.frame_index]


    def jump(self):
        # only allow a jump if the player is not already jumping 
        if not self.jumping:
            self.velocity.y = -c.JUMP_STRENGTH 
            self.jumping = True 


    def update(self, tiles, moving):
        # apply gravity 
        self.velocity.y += c.GRAVITY

        # Apply sliding friction only if player isn't pressing a key
        if not moving:
            self.velocity.x *= c.FRICTION
            # When velocity gets very small, zero it to prevent "creeping"
            if abs(self.velocity.x) < c.MIN_SPEED:
                self.velocity.x = 0

        # Cap maximum speed 
        if self.velocity.x > c.MAX_SPEED:
            self.velocity.x = c.MAX_SPEED 
        elif self.velocity.x < -c.MAX_SPEED:
            self.velocity.x = -c.MAX_SPEED 

        
        # X-AXIS Movement and Collision
        self.position.x += self.velocity.x 
        self.hitbox.x = round(self.position.x)

        # create a temporary "wal-check" box that is 2 pixels shorter at the top and at the bottom
        wall_check_rect = self.hitbox.inflate(0, -4)
        for tile in tiles:
            #if self.hitbox.colliderect(tile.rect):
            if wall_check_rect.colliderect(tile.rect):
                if self.velocity.x > 0:                         # moving right
                    logging.debug(f"collided with tile LEFT")
                    self.hitbox.right = tile.rect.left 
                else:
                    logging.debug(f"collided with tile RIGHT")
                    self.hitbox.left = tile.rect.right
                self.velocity.x = 0
                self.position.x = self.hitbox.x 
                break # Stop checking tiles once we collide
                  
        # 5. Y-Axis Movement and Collision
        self.position.y += self.velocity.y
        self.hitbox.y = round(self.position.y)
        for tile in tiles:
             if self.hitbox.colliderect(tile.rect):
                if self.velocity.y > 0:                   # moving down, hit floor 
                    self.hitbox.bottom = tile.rect.top 
                    self.jumping = False
                elif self.velocity.y < 0:                   # moving up, hit ceiling 
                    #logging.debug(f"collided with tile BOTTOM")
                    self.hitbox.top = tile.rect.bottom 
                self.velocity.y = 0
                self.position.y = self.hitbox.y
                break # stop checking tiles once we collide
                
        # 6. Update the visual 
        self.animate(moving) 


        # 7. Sync image rect to hitbox 
        #    Ensure that feet stay anchored to bottom of collision box 
        #    when image size changes (jumping versus standing)
        self.rect.midbottom = self.hitbox.midbottom 


    def __repr__(self):
        """Developer-friendly representation: Player(x, y, direction)"""
        msg = (
            f"Player, position(x={self.hitbox.x}, y={self.hitbox.y}, " 
            f"velocity(x={self.velocity.x}, y={self.velocity.y})"
            f"direction='{self.direction})'"
        )
        return msg
    
    def __str__(self):
        """User-friendly summary: Player at (x, y) facing [direction]"""
        return f"Player at ({self.hitbox.x}, {self.hitbox.y}) facing {self.direction}"