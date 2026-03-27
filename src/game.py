import pygame 
import sys 
import logging 

from . import constants as c

from .assetManager import AssetManager
from .metall import Metall
from .player import Player 
from .tile import Tile 
from .tile_map import GAME_MAP_1

# create a logger named "game" (the filename)
# Automatically sends its messages up to the Root logger
# configured in main.py 
logger = logging.getLogger(__name__)


class Game:
    def __init__(self, level):
        
        logger.info("Initializing Game object")

        # 1. Initialize pygame modules 
        pygame.init() 

        # 2. Set up the display
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() 
        self.running = True 

        # Create groups for collision and non-collision tiles 
        self.collision_tiles = pygame.sprite.Group()
        self.non_collision_tiles = pygame.sprite.Group()

        self.metalls = pygame.sprite.Group()
        self.metall_bullets = pygame.sprite.Group()

        # 3. Load asset and then create the mape
        AssetManager.load_all(c.ASSETS_CONFIG_PATH)
        self.setup_level(level)

        # 4. Set up player 
        self.player = Player(c.PLAYER_START_X, c.PLAYER_START_Y)
        self.player_moving_this_frame = False 

        # 5. Setup background 
        self.background_image = AssetManager.get_image("background")
    

    def add_tiles(self, code, tile):
        """ Append tiles to collision or non-collision list, depending on code."""
        if code < c.NON_COLLISION_TILE_THRESHOLD:
            self.non_collision_tiles.add(tile)
        else:
            self.collision_tiles.add(tile)

    def create_map(self, level_map):

        # create map 
        for row, row_data in enumerate(level_map):
            for col, code in enumerate(row_data):
                code = level_map[row][col]
                x = col * c.TILE_SIZE 
                y = row * c.TILE_SIZE

                if code == c.SKY: # pygame window background color
                    continue    
                elif code == c.ROCK_TILE_1:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_1"), code))
                elif code == c.ROCK_TILE_2:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_2"), code))
                elif code == c.ROCK_TILE_3:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_3"), code))
                elif code == c.ROCK_TILE_4:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("rock_tile_4"), code))
                elif code == c.FLOOR_TILE:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("floor_tile"), code))
                elif code == c.WALL_TILE:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("wall_tile"), code))
                elif code == c.BEAM_TILE:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("beam_tile"), code))
                elif code == c.SPIKE_TILE:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("spike_tile"), code))
                elif code == c.ROOM_TILE:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("room_tile"), code))
                elif code == c.METALL:
                    self.metalls.add(Metall(x, y))
                elif code == c.BLADER:
                    self.add_tiles(code, Tile(x, y, AssetManager.get_image("blader_left"), code))
                   
        

    def setup_level(self, level):

        # TODO: add functionality for setting up different levels 
        # and switching between levels

        level_map = None

        if level == 1:
            level_map = GAME_MAP_1 

        self.create_map(level_map)


    def run(self):
        """The main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw() 
            self.clock.tick(c.FPS)


    def handle_events(self):
        moving = False      # Track is keys are held this frame

        # Handle "one-time" events (Closing window, single-press Jump)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    self.player.shoot()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.player.stop_jump()  # cut the jump height

        # Handle continuous movement events 
        keys = pygame.key.get_pressed() 

        # continuous key press jumping
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                    self.player.jump() 

        # continuous key press left/right
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.velocity.x -= c.ACCELERATION
            self.player.direction = "left"
            moving = True 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.velocity.x += c.ACCELERATION
            self.player.direction = "right"
            moving = True 
        
        self.player_moving_this_frame = moving 
    

    def update(self):
        self.player.update(self.collision_tiles, self.player_moving_this_frame)
        self.player.bullets.update()

        for metall in self.metalls:
            metall.update(self.collision_tiles, self.player.position, self.metall_bullets)

        self.metall_bullets.update()

        # Handle Collisions
        self.__check_metall_bullet_player_collision()
        self.__check_metall_bullet_tile_collision()

        self.__check_player_bullet_tile_collision()
        self.__check_player_bullet_metall_collision()
        self.__check_player_metall_collision()
        
        
    def __check_metall_bullet_player_collision(self):
        """Handle Metall Bullet collision with Player"""
        if not self.player.is_invincible:
            # check if enemy bullet hit the player's hitbox 
            if pygame.sprite.spritecollide(self.player, self.metall_bullets, True, collided=hitbox_collide):
                self.player.take_damage()

    def __check_metall_bullet_tile_collision(self):
        """Handle Metall Bullet collisions with Tiles"""

        # Bullets disappear when hitting walls 
        pygame.sprite.groupcollide(self.metall_bullets, self.collision_tiles, True, False)

    def __check_player_bullet_metall_collision(self):
        """Handle Player Bullet collision with Metall"""

        # Returns a dict: {bullet: [metals_hit]}
        # dokill1 = True (bullet disappears), dokill2=False (metall stays, for now)
        enemy_hits = pygame.sprite.groupcollide(
            self.player.bullets, 
            self.metalls, 
            True, 
            False,
            collided=hitbox_collide         # use hitbox for collisions instead of rects
        )

        for bullet, metalls in enemy_hits.items():
            for metall in metalls:
                # if metall is not guarding, it takes damage/dies
                if not metall.guarding:
                    metall.kill()
                else:
                    logger.debug("Bullet pinge off Metall's helmet!")
                    logger.debug("Optional: spawn a spark particle here")

    def __check_player_metall_collision(self):
        """Player collision with Metall"""
        self.player.handle_invincibility()  # update the timer 

        if not self.player.is_invincible:
            # player is not in a group, so we use spritecollide 
            if pygame.sprite.spritecollide(self.player, self.metalls, False, collided=hitbox_collide):
                logger.info("Player touched a Mettal! Take damage.")
                self.player.take_damage()

    def __check_player_bullet_tile_collision(self):
        """ Player Bullet collision with Environment Tiles """

        #  dokill1=True kills the bullet, dokill2=False keeps the tile
        hits = pygame.sprite.groupcollide(
            self.player.bullets, 
            self.collision_tiles, 
            True, 
            False, 
            collided=hitbox_collide
        )

        # loop through the hits to decide which tiles to destroy 
        for bullett, tiles_hit in hits.items():
            for tile in tiles_hit:
                if tile.code in [c.ROCK_TILE_1, c.ROCK_TILE_2, c.ROCK_TILE_3, c.ROCK_TILE_4]:
                    logger.info("Bullet struck rock tile. Killing roce tile")
                    tile.kill() 
                elif tile.code == c.WALL_TILE or tile.code == c.FLOOR_TILE:
                    logger.debug("Bullet hit an indestructable wall.")



    def draw(self):
        self.screen.fill(c.BACKGROUND_COLOR)

        # draw the level tiles
        self.non_collision_tiles.draw(self.screen)
        self.collision_tiles.draw(self.screen)

        # draw enemies 
        self.metalls.draw(self.screen)
        self.metall_bullets.draw(self.screen)

        draw_player = True 
        if self.player.is_invincible:
            # Flicker every 100 ms 
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                draw_player = False 

        if draw_player:
            self.screen.blit(self.player.image, self.player.rect)
            # draw debug boxes (optional, for troubleshooting)
            #self.player.draw_debug(self.screen)

        self.player.bullets.draw(self.screen) 
        pygame.display.flip()



def hitbox_collide(sprite_a, sprite_b):
    """Callbackk to chec collision using the .hitbox attribute."""
    return sprite_a.hitbox.colliderect(sprite_b.hitbox)