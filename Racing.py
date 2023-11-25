import pygame
import pygame # Import pygame module
import sys  # Import sys module
import pytmx # Import pytmx module
import math # Import math module
import pygame.mixer # Import pygame mixer module


# Initializes Pygame and pygame mixer

pygame.init()  # Initialize pygame
pygame.mixer.init()  # Initialize pygame mixer


# Constants for the game window
WIDTH, HEIGHT = 1390, 768  # Width and height of the game window
FPS = 60  # Frames per second
WHITE = (255, 255, 255)  # White color for the background
ROAD_COLOR = (100, 100, 100)  # Gray color for the road
CAR_COLOR = (255, 0, 0)  # Red color for the player's car
MAP_SCALE = 3  # Scale factor for the map

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set the size of the game window
pygame.display.set_caption("Formula 1 Racing Course")  # Set the title of the game window

# Create a clock object
clock = pygame.time.Clock()  # Create a clock object to control the FPS

# Load the TMX map
tmx_map = pytmx.load_pygame('Road.tmx')  # Load the TMX map

# Get the road layers
road_layers = [layer for layer in tmx_map.visible_layers if isinstance(layer, pytmx.TiledTileLayer)]  # Get the road layers

# Calculate the scaled map dimensions
scaled_tilewidth = tmx_map.tilewidth * MAP_SCALE  # Calculate the scaled tile width
scaled_tileheight = tmx_map.tileheight * MAP_SCALE  # Calculate the scaled tile height
scaled_width = tmx_map.width * scaled_tilewidth  # Calculate the scaled width
scaled_height = tmx_map.height * scaled_tileheight  # Calculate the scaled height

# Create a surface for the scaled map
original_car_image = pygame.Surface((8, 8))  # Create a surface for the original car image
original_car_image.fill(CAR_COLOR)  # Fill the surface with the car color
scaled_car_image = pygame.transform.scale(original_car_image, (7 * MAP_SCALE, 5 * MAP_SCALE))  # Scale the car image

# Create a rectangle for the player's car
player_car_rect = scaled_car_image.get_rect()  # Create a rectangle for the player's car
player_car_rect.center = (150, 85)  # Initial position of the player's car
player_velocity = pygame.Vector2(0, 0)  # Initial velocity of the player's car
player_angle = 0  # Initial angle of the player's car

# Load music and set volume
pygame.mixer.music.load('Music.wav')  # Load music
pygame.mixer.music.set_volume(0.15)  # 15% volume (0 to 1.0)

# Start playing music (you can specify the number of loops)
pygame.mixer.music.play(-1)  # -1 means play indefinitely

# Tile ID for collision (the tile ID is 253)
COLLISION_TILE_ID = 253  # Tile ID for collision (the tile ID is 253)

# Game loop
running = True  # Boolean variable to control the game loop
while running: # Loop that runs while the game is running
    for event in pygame.event.get(): # Loop that gets all the events that happen in the game
        if event.type == pygame.QUIT: # If the user clicks on the close button
            running = False # Set running to False to exit the game loop

    # Get the pressed keys
    keys = pygame.key.get_pressed() # Get the pressed keys
    player_velocity.x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3 # Get the horizontal velocity of the player's car
    player_velocity.y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 3 # Get the vertical velocity of the player's car

    # Check if the player's car is colliding with the road
    new_player_rect = player_car_rect.move(player_velocity) # Get the new position of the player's car
    for x in range(int(new_player_rect.left / scaled_tilewidth), int(new_player_rect.right / scaled_tilewidth)): # Loop that checks the horizontal tiles
        for y in range(int(new_player_rect.top / scaled_tileheight), int(new_player_rect.bottom / scaled_tileheight)): # Loop that checks the vertical tiles
            tile = tmx_map.get_tile_layer_by_name("BORDERS").get_tile_gid(x, y) # Get the tile ID
            if tile == COLLISION_TILE_ID:
            # Collision detected, prevent movement
                player_velocity.x = 0
                player_velocity.y = 0

    # Move the player's car
    player_car_rect.x += player_velocity.x
    player_car_rect.y += player_velocity.y

    # Check if the player's car is colliding with the road
    if player_velocity.length() > 0: # If the player's car is moving
        player_angle = math.degrees(math.atan2(player_velocity.y, player_velocity.x)) # Get the angle of the player's car

    # Rotate the player's car
    rotated_car_image = pygame.transform.rotate(scaled_car_image, player_angle)  # Rotate the player's car

    # Clear the screen
    screen.fill(WHITE)  # Fill the screen with white

    # Draw the road layers
    for layer in road_layers:  # Loop that draws the road layers
        for x, y, image in layer.tiles():  # Loop that gets the tiles
            scaled_image = pygame.transform.scale(image, (scaled_tilewidth, scaled_tileheight))  # Scale the image
            screen.blit(scaled_image, (x * scaled_tilewidth, y * scaled_tileheight))  # Draw the image

    # Draw the player's car
    rotated_rect = rotated_car_image.get_rect(center=player_car_rect.center)  # Get the rectangle of the rotated car image
    screen.blit(rotated_car_image, rotated_rect.topleft)  # Draw the rotated car image

    # Update the display
    pygame.display.flip()  # Update the display

    # Set the FPS
    clock.tick(FPS)  # Set the FPS

pygame.quit() # Quit pygame
sys.exit() # Quit the program