import pygame 
from pygame.math import Vector2 

from .assetManager import AssetManager
from . import constants as c
from .bullet import Bullet

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

        # To add Coyote Time, you need a timer that tracks how long it has been since 
        # the player was last touching the ground. If the player walks off a ledge, 
        # they get a small window (usually 100–200ms) where they can still trigger a jump.
        self.last_grounded_time = 0
        self.coyote_duration = c.COYOTE_DURATION  # milliseconds of grace period

        # Jump buffering: remember" a jump press that happened slightly before the 
        # player touched the ground. If they land within a small window (usually 100–150ms) 
        # after pressing the button, the jump triggers automatically.
        self.jump_buffer_time = 0
        self.jump_buffer_duration = 150  # ms to "remember" the jump press


        # Walking Animation Frame Lists
        self.walk_left_frames = [
            AssetManager.get_image("player_left_walk_0"),
            AssetManager.get_image("player_left_walk_1"),
            AssetManager.get_image("player_left_walk_2"),
            AssetManager.get_image("player_left_walk_3"),
        ]

        self.walk_right_frames = [
            AssetManager.get_image("player_right_walk_0"),
            AssetManager.get_image("player_right_walk_1"),
            AssetManager.get_image("player_right_walk_2"),
            AssetManager.get_image("player_right_walk_3"),
        ]

        # Animation State 
        self.frame_index = 0 
        self.animation_speed = 100      # ms between frames 
        self.last_update = pygame.time.get_ticks()

        # Invincibility State 
        self.is_invincible = False 
        self.invincibility_duration = 1500     # milliseconds 
        self.last_hit_time = 0 

        # Group animations for easy access 
        self.animations = {
            "idle_right": [AssetManager.get_image("player_right")],
            "idle_left":  [AssetManager.get_image("player_left")],
            "jump_right": [AssetManager.get_image("player_jump_right")],
            "jump_left":  [AssetManager.get_image("player_jump_left")],
            "walk_right": self.walk_right_frames,
            "walk_left":  self.walk_left_frames,
            "shoot_right": [AssetManager.get_image("player_shoot_right")],
            "shoot_left": [AssetManager.get_image("player_shoot_left")],
            "jump_shoot_right": [AssetManager.get_image("player_jump_shoot_right")],
            "jump_shoot_left": [AssetManager.get_image("player_jump_shoot_left")]
        }

        # Set initial state 
        current_state = f"idle_{self.direction}"

        # self.hitbox is for Collisions
        self.hitbox = pygame.Rect(x, y, c.PLAYER_HITBOX_WIDTH, c.PLAYER_HITBOX_HEIGHT)

        # Set self.image and self.rect based on current state
        self.image = self.animations[current_state][0]

        # self.rect is for Drawing (matches the current image size)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

        # shooting state 
        self.is_shooting = False 
        self.shoot_timer = 0 
        self.shoot_duration = 300 # ms to show the shooting frame 
        self.bullets = pygame.sprite.Group()

        logger.info("Player initialized")      


    def draw_debug(self, surface):
        """Draws the collision hitbox and drawing rect for debugging."""

        # draw the hitbox in red 
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

        # draw the visual rect in blue to see the image boundary 
        pygame.draw.rect(surface, (0, 0, 255), self.rect, 1)


    def animate(self, moving_this_frame):
        now = pygame.time.get_ticks() 

        # reset shooting state after duration 
        if self.is_shooting and now - self.shoot_timer > self.shoot_duration:
            self.is_shooting = False 

        # build the state string dynamically 
        shoot_part = "shoot_" if self.is_shooting else ""

        # 1. Determine the state 
        if self.jumping:
            state = f"jump_{shoot_part}{self.direction}" 
        elif moving_this_frame and abs(self.velocity.x) > c.MIN_SPEED:
            state = f"{shoot_part if self.is_shooting else "walk_"}{self.direction}"
        else:
            state = f"{shoot_part if self.is_shooting else "idle_"}{self.direction}"

        # 2. Get the current frame list 
        current_frames = self.animations.get(state, self.animations[f"idle_{self.direction}"])

        # 3. Cycle frames base on timer 
        if now - self.last_update > self.animation_speed:
            self.last_update = now 
            # reset frame index if switching to idle (idle only has 1 frame)
            if len(current_frames) == 1:
                self.frame_index = 0
            else:
                self.frame_index = (self.frame_index + 1) % len(current_frames)
            
            self.image = current_frames[self.frame_index] 

        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)


    def jump(self):
        # Record the time the player TRIED to jump
        self.jump_buffer_time = pygame.time.get_ticks()
        
        # Check if we can jump immediately (normal jump or coyote time)
        now = pygame.time.get_ticks()
        if not self.jumping or (now - self.last_grounded_time < self.coyote_duration):
            self.perform_jump()

    def perform_jump(self):
        """The actual physics of jumping."""
        self.velocity.y = -c.JUMP_STRENGTH 
        self.jumping = True 
        self.last_grounded_time = 0 
        self.jump_buffer_time = 0 # Clear buffer so we don't double jump
        logger.info("Jump executed")

    def stop_jump(self):
        """Called when jump key is released to allow variable jump height"""
        # if moving upwards, reduce the upward velocity significantly 
        if self.velocity.y < -c.MIN_JUMP_HEIGHT:
            self.velocity.y = -c.MIN_JUMP_HEIGHT 

    def shoot(self):
        self.is_shooting = True 
        self.shoot_timer = pygame.time.get_ticks() 

        # adjust bullet spawn point so it comes out of the arm 
        spawn_x = self.rect.right if self.direction == "right" else self.rect.left
        new_bullet = Bullet(spawn_x, self.rect.centery, self.direction)
        self.bullets.add(new_bullet)

    def handle_invincibility(self):
        if self.is_invincible:
            current_time = pygame.time.get_ticks() 
            if current_time - self.last_hit_time > self.invincibility_duration:
                self.is_invincible = False 

    def take_damage(self):
        if not self.is_invincible:
            self.is_invincible = True 
            self.last_hit_time = pygame.time.get_ticks() 
            logger.info("Player hit! Invincibility started")
            logger.info("TODO: add health reduction here")

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

        now = pygame.time.get_ticks()
        for tile in tiles:
             if self.hitbox.colliderect(tile.rect):
                if self.velocity.y > 0:                   # moving down, hit floor 
                    self.hitbox.bottom = tile.rect.top 
                    self.velocity.y = 0
                    self.jumping = False 
                    # update last time on solid ground
                    self.last_grounded_time = now 

                    # JUMP BUFFER CHECK: 
                    # If the player pressed jump recently, jump now!
                    if now - self.jump_buffer_time < self.jump_buffer_duration:
                        self.perform_jump()

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