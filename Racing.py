import pygame
import sys
import pytmx
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1390, 769
FPS = 60
WHITE = (255, 255, 255)
ROAD_COLOR = (100, 100, 100)
CAR_COLOR = (255, 0, 0)  # Red color for the player's car
MAP_SCALE = 3  # Scale factor for the map

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formula 1 Racing Course")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load Tiled map (exported in TMX format)
tmx_map = pytmx.load_pygame('C:/Users/GREED/Desktop/RAcing game challenge week/Road.tmx')

# Extract road information from the TMX map
road_layers = [layer for layer in tmx_map.visible_layers if isinstance(layer, pytmx.TiledTileLayer)]

# Scale the map
scaled_tilewidth = tmx_map.tilewidth * MAP_SCALE
scaled_tileheight = tmx_map.tileheight * MAP_SCALE
scaled_width = tmx_map.width * scaled_tilewidth
scaled_height = tmx_map.height * scaled_tileheight

# Load and scale car image
original_car_image = pygame.Surface((8, 8))
original_car_image.fill(CAR_COLOR)
scaled_car_image = pygame.transform.scale(original_car_image, (8 * MAP_SCALE, 6 * MAP_SCALE))

# Player's car position, velocity, and angle
player_car_rect = scaled_car_image.get_rect()
player_car_rect.center = (150, 85)  # Initial position of the player's car
player_velocity = pygame.Vector2(0, 0)
player_angle = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input for the player car
    keys = pygame.key.get_pressed()
    player_velocity.x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3
    player_velocity.y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 3

    # Update the player's car position
    player_car_rect.x += player_velocity.x
    player_car_rect.y += player_velocity.y

    # Calculate the angle based on velocity
    if player_velocity.length() > 0:
        player_angle = math.degrees(math.atan2(player_velocity.y, player_velocity.x))

    # Rotate the car image
    rotated_car_image = pygame.transform.rotate(scaled_car_image, player_angle)

    # Update the display
    screen.fill(WHITE)

    # Draw the scaled road based on the Tiled map
    for layer in road_layers:
        for x, y, image in layer.tiles():
            scaled_image = pygame.transform.scale(image, (scaled_tilewidth, scaled_tileheight))
            screen.blit(scaled_image, (x * scaled_tilewidth, y * scaled_tileheight))

    # Draw the rotated player's car
    rotated_rect = rotated_car_image.get_rect(center=player_car_rect.center)
    screen.blit(rotated_car_image, rotated_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
