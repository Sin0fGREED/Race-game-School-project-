import pygame # Import pygame module
import sys  # Import sys module
import pytmx # Import pytmx module
import math # Import math module
import pygame.mixer # Import pygame mixer module
from vector2d import Vector2D
# pip install vector2d.py

# Initializes Pygame and pygame mixer

pygame.init()  # Initialize pygame
pygame.mixer.init()  # Initialize pygame mixer


# Constants for the game window
WIDTH, HEIGHT = 1390, 768  # Width and height of the game window
FPS = 60  # Frames per second
WHITE = (255, 255, 255)  # White color for the background
ROAD_COLOR = (100, 100, 100)  # Gray color for the road
MAP_SCALE = 3  # Scale factor for the map
BLUE = (255, 255, 255)
font = pygame.font.SysFont(None, 100)
img = font.render('press ENTER to start', True, BLUE)
imgRect = img.get_rect()
imgRect.center = (WIDTH // 2, HEIGHT // 2)
backgrounds = pygame.image.load("./mainMenu/car.jpg")
lights = pygame.image.load("./mainMenu/lights.jpg")
clock = pygame.time.Clock()
counter = 5
timer_event = pygame.USEREVENT+1
text = font.render(str(counter), True, (255, 0, 0))
pygame.time.set_timer(timer_event, 1000)
drag = 0.04
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
original_car_image = pygame.image.load("./Vehicles/CARS.png")  # Create a surface for the original car image
scaled_car_image = pygame.transform.scale(original_car_image, (40, 20))  # Scale the car image

# Create a rectangle for the player's car
player_car_rect = scaled_car_image.get_rect()  # Create a rectangle for the player's car
player_car_rect.x = 150
player_car_rect.y = 135

player_velocity = pygame.Vector2(0, 0)  # Initial velocity of the player's car
player_angle = 0  # Initial angle of the player's car

# Load music and set volume
pygame.mixer.music.load('Music.wav')  # Load music
pygame.mixer.music.set_volume(0)  # 15% volume (0 to 1.0)

# Start playing music (you can specify the number of loops)
pygame.mixer.music.play(-1)  # -1 means play indefinitely

# Tile ID for collision (the tile ID is 253)
COLLISION_TILE_ID = 8  # Tile ID for collision (the tile ID is 253)

def screen_to_world(screen_x, screen_y): #convert pixel location to tile location
    world_x = (screen_x / WIDTH ) * 29
    world_y = (screen_y / HEIGHT) * 16
    return [world_x, world_y]

running = True  # Boolean variable to control the game loop
checkpoint1 = False
checkpoint2 = False
checkpoint3 = False
checkpoint4 = False
game = 0
clock.tick(60)
while running: # Loop that runs while the game is running
    for event in pygame.event.get(): # Loop that gets all the events that happen in the game
        if event.type == pygame.QUIT: # If the user clicks on the close button
            running = False # Set running to False to exit the game loop
        elif event.type == timer_event and game == 2:
            counter -= 1
            text = font.render(str(counter), True, (255, 0, 0))
            if counter == 0:
                timer_event = False
                game = 1
    if game == 1:
        # Get the pressed keys
        keys = pygame.key.get_pressed() # Get the pressed keys

        # Adjust the horizontal velocity
        if keys[pygame.K_RIGHT]:
            player_velocity.x += 0.2
        elif keys[pygame.K_LEFT]:
            player_velocity.x -= 0.2

        # Adjust the vertical velocity
        if keys[pygame.K_DOWN]:
            player_velocity.y += 0.2
        elif keys[pygame.K_UP]:
            player_velocity.y -= 0.2

        # Apply drag to slow down the car when no keys are pressed
        player_velocity *= (1 - drag)
                
        
                
        previousLocation = (player_car_rect.x, player_car_rect.y) # grabs location before collision
        
        player_car_rect.x += player_velocity.x
        player_car_rect.y += player_velocity.y

        tileX = math.floor(screen_to_world(player_car_rect.x, player_car_rect.y)[0])
        tileY = math.floor(screen_to_world(player_car_rect.x, player_car_rect.y)[1])
        xivo = screen_to_world(player_car_rect.x, player_car_rect.y)[0]
        yivo = screen_to_world(player_car_rect.x, player_car_rect.y)[1]
        print(f"x: {xivo:.2f} y: {yivo:.2f}, tileX: {tileX} tileY: {tileY}")
        
        tile_layer = tmx_map.get_layer_by_name("BORDERS")
        tile = tile_layer.data[tileY][tileX] # gets current tile location
        if tileX == 10 and tileY == 1:
                print("checkpoint 1 achieved nigga")
                checkpoint1 = True
        if tileX == 27 and tileY == 9 and checkpoint1:
                print("checkpoint 2 achieved nigga")
                checkpoint2 = True
        if tileX == 18 and tileY == 8 and checkpoint2:
                print("checkpoint 3 achieved nigga")
                checkpoint3 = True
        if tileX == 1 and tileY == 4 and checkpoint3:
                print("checkpoint 4 achieved nigga")
                checkpoint4 = True
        if tileX == 1 and tileY == 1 and checkpoint1 == True and checkpoint2 == True and checkpoint3 == True and checkpoint4 == True:
                print("finished achieved nigga")
                exit()
            
        if tile == COLLISION_TILE_ID: # checks if current tile location is allowed
            player_car_rect.x = previousLocation[0] #revert to previous state 
            player_car_rect.y = previousLocation[1] #revert to previous state 

        # Check if the player's car is colliding with the road
        if player_velocity.length() > 0: # If the player's car is moving
            player_angle = math.degrees(math.atan2(-player_velocity.y, player_velocity.x))  # Adjust the angle calculation

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
        rotated_rect = rotated_car_image.get_rect(center=(player_car_rect.x, player_car_rect.y))  # Get the rectangle of the rotated car image
        screen.blit(rotated_car_image, rotated_rect.topleft)  # Draw the rotated car image

        # Update the display
        pygame.display.flip()  # Update the display

        clock.tick(FPS)  # Set the FPS
    elif game == 0:
        screen.blit(backgrounds, (0,0))
        screen.blit(img, imgRect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game = 2
        pygame.display.flip()
        clock.tick(FPS)
    elif game == 2:
        screen.blit(lights, (0,0))
        text_rect = text.get_rect(center = screen.get_rect().center)
        screen.blit(text, text_rect)
        pygame.display.flip()
        
pygame.quit() # Quit pygame
sys.exit() # Quit the program