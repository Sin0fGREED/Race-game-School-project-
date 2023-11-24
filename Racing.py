import pygame
import sys
import pytmx
import math
import pygame.mixer


# Initializes Pygame and pygame mixer
pygame.init()
pygame.mixer.init()


# Constants for the game window
WIDTH, HEIGHT = 1390, 768
FPS = 60
WHITE = (255, 255, 255)
ROAD_COLOR = (100, 100, 100)
CAR_COLOR = (255, 0, 0)  # Red color for the player's car
MAP_SCALE = 3  # Scale factor for the map

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formula 1 Racing Course")

# Create a clock object
clock = pygame.time.Clock()

# Load the TMX map
tmx_map = pytmx.load_pygame('Road.tmx')

# Get the road layers
road_layers = [layer for layer in tmx_map.visible_layers if isinstance(layer, pytmx.TiledTileLayer)]

# Calculate the scaled map dimensions
scaled_tilewidth = tmx_map.tilewidth * MAP_SCALE
scaled_tileheight = tmx_map.tileheight * MAP_SCALE
scaled_width = tmx_map.width * scaled_tilewidth
scaled_height = tmx_map.height * scaled_tileheight

# Create a surface for the scaled map
original_car_image = pygame.Surface((8, 8))
original_car_image.fill(CAR_COLOR)
scaled_car_image = pygame.transform.scale(original_car_image, (7 * MAP_SCALE, 5 * MAP_SCALE))

# Create a rectangle for the player's car
player_car_rect = scaled_car_image.get_rect()
player_car_rect.center = (150, 85)  # Initial position of the player's car
player_velocity = pygame.Vector2(0, 0)
player_angle = 0

# Load music and set volume
pygame.mixer.music.load('Music.wav')
pygame.mixer.music.set_volume(0.15)  # 15% volume

# Start playing music (you can specify the number of loops)
pygame.mixer.music.play(-1)  # -1 means play indefinitely

# Tile ID for collision (the tile ID is 253)
COLLISION_TILE_ID = 253

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the pressed keys
    keys = pygame.key.get_pressed()
    player_velocity.x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3
    player_velocity.y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 3

    new_player_rect = player_car_rect.move(player_velocity)
    for x in range(int(new_player_rect.left / scaled_tilewidth), int(new_player_rect.right / scaled_tilewidth)):
        for y in range(int(new_player_rect.top / scaled_tileheight), int(new_player_rect.bottom / scaled_tileheight)):
            tile = tmx_map.get_tile_layer_by_name("BORDERS").get_tile_gid(x, y)
            if tile == COLLISION_TILE_ID:
            # Collision detected, prevent movement
                player_velocity.x = 0
                player_velocity.y = 0

    # Move the player's car
    player_car_rect.x += player_velocity.x
    player_car_rect.y += player_velocity.y

    # Check if the player's car is colliding with the road
    if player_velocity.length() > 0:
        player_angle = math.degrees(math.atan2(player_velocity.y, player_velocity.x))

    # Rotate the player's car
    rotated_car_image = pygame.transform.rotate(scaled_car_image, player_angle)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the road layers
    for layer in road_layers:
        for x, y, image in layer.tiles():
            scaled_image = pygame.transform.scale(image, (scaled_tilewidth, scaled_tileheight))
            screen.blit(scaled_image, (x * scaled_tilewidth, y * scaled_tileheight))

    # Draw the player's car
    rotated_rect = rotated_car_image.get_rect(center=player_car_rect.center)
    screen.blit(rotated_car_image, rotated_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Set the FPS
    clock.tick(FPS)

# Stops the music
pygame.mixer.music.stop()

# Quit the game
pygame.quit()
sys.exit()