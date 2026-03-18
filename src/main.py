# Tutorial 9: Enemies

import pygame
from sys import exit 
import os 

# game varibles
WINDOW_WIDTH = 512 
WINDOW_HEIGHT = 512

TILE_SIZE = 32 

PLAYER_X = WINDOW_WIDTH / 2 
PLAYER_Y = WINDOW_HEIGHT / 2

# maintaining 7 to 8 ratio of image 
PLAYER_WIDTH = 42 
PLAYER_HEIGHT = 48 

PLAYER_JUMP_WIDTH = 52 
PLAYER_JUMP_HEIGHT = 60

PLAYER_DISTANCE = 5

GRAVITY = 0.5
FRICTION = 0.4 

PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -11     # for jumping upwards

# enemy variables 
METALL_WIDTH = 36
METALL_HEIGHT = 30 

# initilaize pygame
pygame.init()   # always need to initialize pygame

# load images 
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("../images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("background.png")
player_image_right = load_image("megaman-right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("megaman-left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right = load_image("megaman-right-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_left = load_image("megaman-left-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
floor_tile_image = load_image("floor-tile.png", (TILE_SIZE, TILE_SIZE))

metall_image_left = load_image("metall-left.png", (METALL_WIDTH, METALL_HEIGHT))


# set diplay mode, create window
pygame.display.set_caption("Kenny Yip Tutorial 9, Enemies")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# clock required to control frame rate
clock = pygame.time.Clock()

# Player Class 
class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right 
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False 
    
    def update_image(self):
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


class Metall(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, METALL_WIDTH, METALL_HEIGHT)
        self.image = metall_image_left 
        self.velocity_y = 0
        self.direction = "left"
        self.jumping = False 

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image 


def create_map():
    # four horizontal tiles place in relation to player position
    for i in range(4):
        tile = Tile(player.x + i * TILE_SIZE, player.y + TILE_SIZE * 2, floor_tile_image)
        tiles.append(tile)
    
    # horizontal tiles across the entire game window 
    # x position changes, y position does not change 
    # vertically tiles are 5 tiles below player.y
    for i in range(16):
        tile = Tile(i*TILE_SIZE, player.y + TILE_SIZE * 5, floor_tile_image)
        tiles.append(tile)
    
    # vertical tiles, starting at y 10 tiles down from top
    # x position does not change for vertical tiles. 
    for i in range(3):
        tile = Tile(TILE_SIZE * 3, (i+10)*TILE_SIZE, floor_tile_image)
        tiles.append(tile)

def check_tile_collision(character):
    for tile in tiles:
        if character.colliderect(tile):
            return tile 
    return None     

def check_tile_collision_x(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_x < 0:
            # player is moving to the left, collision is with right side of tile
            # position player to the right side of the tile
            character.x = tile.x + tile.width  
        elif character.velocity_x > 0:
            # player is moving to the right, collision is with left side of tile 
            # position player on left side of tile 
            character.x = tile.x - character.width 
        character.velocity_x = 0

def check_tile_collision_y(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_y < 0:
            # player is moving upward, collision with bottom of tile 
            # position player at bottom of tile
            character.y = tile.y + tile.height
        elif character.velocity_y > 0:
            # player is moving downward, collision iwth top of tile 
            # position player at top of tile 
            character.y = tile.y - character.height 
            character.jumping = False 
        character.velocity_y = 0

def move():
    # x movement
    if player.direction ==  "left" and player.velocity_x < 0:
        player.velocity_x += FRICTION 
    elif player.direction == "right" and player.velocity_x > 0:
        player.velocity_x -= FRICTION 
    else:
        player.velocity_x = 0
        
    player.x += player.velocity_x

    if player.x < 0:
        player.x = 0 
    elif player.x + player.width > WINDOW_WIDTH:
        player.x = WINDOW_WIDTH - player.width

    check_tile_collision_x(player)

    # y movement
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    check_tile_collision_y(player)

    # enemy y movement 
    metall.velocity_y += GRAVITY 
    metall.y += metall.velocity_y 
    check_tile_collision_y(metall)

    if player.colliderect(metall):
        print("player collision with metall")



def draw():
    window.fill((20, 18, 167))
    window.blit(background_image, (0, 80))
    for tile in tiles:
        window.blit(tile.image, tile)

    player.update_image()
    window.blit(player.image, player)
    window.blit(metall.image, metall)


# start game
player = Player()
metall = Metall(player.x + TILE_SIZE * 3, TILE_SIZE * 6, metall_image_left)
tiles = []
create_map()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            # call exit to clean up
            exit()
    
    keys = pygame.key.get_pressed() 
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping = True 

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity_x = -PLAYER_VELOCITY_X
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity_x = PLAYER_VELOCITY_X
        player.direction = "right"

    move()
    draw()
    pygame.display.update()
    clock.tick(60) # 60 frames per second


def main():
    print("Hello from myfirst-megaman-clone!")
    print(f"pygame version: {pygame.version.ver}")

if __name__ == "__main__":
    main()
