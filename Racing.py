from tracemalloc import start
import pygame
import sys
import pytmx
import math
import pygame.mixer
from vector2d import Vector2D
import os


# Initialize pygame
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1390, 768 # Screen dimensions
FPS = 60 # Frames per second
WHITE = (255, 255, 255) # White color
ROAD_COLOR = (100, 100, 100) # Road color
MAP_SCALE = 3 # Map scale
BLUE = (255, 255, 255) # Blue color
GREEN = (2, 247, 15) # Green color
font = pygame.font.SysFont(None, 39) # Font 
fontTimer = pygame.font.SysFont(None, 50)   # Font for timer
font_size = 50   # Font size
text_home = ("""Press ENTER for hard mode and BACKSPACE for easy mode. To win you must complete 3 laps of the track.""")    # Text for home screen
Start_TXT = font.render(text_home, True, BLUE)  # Text for home screen
Victory_TXT = font.render("You Won!", True, GREEN)  # Text for victory screen
imgRect = Start_TXT.get_rect()  # Text for home screen
imgRect.center = (WIDTH // 2, HEIGHT // 2)  # Text for home screen
imgRects = Victory_TXT.get_rect()   # Text for victory screen
imgRects.center = (WIDTH // 2, HEIGHT // 1.7)   # Text for victory screen
backgrounds = pygame.image.load("./mainMenu/car.jpg")   # Background for home screen
lights = pygame.image.load("./mainMenu/lights.jpg") # Background for timer screen
victory = pygame.image.load("./mainMenu/victory.jpeg")  # Background for victory screen
lose = pygame.image.load("./mainMenu/freddy.png")   # Background for lose screen
clock = pygame.time.Clock() # Clock
counter = 5 # Timer
timer_event = pygame.USEREVENT + 1  # Timer event
text = fontTimer.render(str(counter), True, (255, 0, 0))    # Timer text
pygame.time.set_timer(timer_event, 1000)    # Timer event
target_position = pygame.Vector2(1310, 55)  # Target position
drag = 0.04 # Drag
other_car_speed = 2 # AI car speed
is_moving_to_target = True  # AI car movement

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Screen
pygame.display.set_caption("Formula 1 Racing Course")   # Screen caption

clock = pygame.time.Clock()     # Clock

# Game state variables
frame_rate = 60
frame_count = 0
start_time = 0

# Load the map
tmx_map = pytmx.load_pygame('Road.tmx')
road_layers = [layer for layer in tmx_map.visible_layers if isinstance(layer, pytmx.TiledTileLayer)]
scaled_tilewidth = tmx_map.tilewidth * MAP_SCALE
scaled_tileheight = tmx_map.tileheight * MAP_SCALE
scaled_width = tmx_map.width * scaled_tilewidth
scaled_height = tmx_map.height * scaled_tileheight

# Load the car image
original_car_image = pygame.image.load("./Vehicles/CARS.png")
scaled_car_image = pygame.transform.scale(original_car_image, (40, 20))

# Load the AI car image
ai_car_image = pygame.image.load("./Vehicles/aiCARS.png")
ai_scaled_car_image = pygame.transform.scale(ai_car_image, (40, 20))

# Create the player car rectangle
player_car_rect = scaled_car_image.get_rect()
player_car_rect.x = 150
player_car_rect.y = 85

# Create the AI car rectangle
other_car_rect = ai_scaled_car_image.get_rect()
other_car_rect.x = 150
other_car_rect.y = 55

# Create the player velocity vector
player_velocity = pygame.Vector2(0, 0)
player_angle = 0


COLLISION_TILE_ID = 148

# Function to convert screen coordinates to world coordinates
def screen_to_world(screen_x, screen_y):
    # Calculate the world x-coordinate based on the screen x-coordinate and the width of the screen
    world_x = (screen_x / WIDTH) * 29
    # Calculate the world y-coordinate based on the screen y-coordinate and the height of the screen
    world_y = (screen_y / HEIGHT) * 16
    # Return the world coordinates as a list [world_x, world_y]
    return [world_x, world_y]

# Game state variables
running = True
checkpoint1 = False
checkpoint2 = False
checkpoint3 = False
checkpoint4 = False
checkpoint5 = False
checkpoint6 = False
checkpoint7 = False
checkpoint8 = False
checkpoint9 = False
checkpoint10 = False
checkpoint11 = False
checkpoint12 = False

# Game settings
game = 0
step1 = False
step2 = False
step3 = False
step5 = False
play = False

# Sound effects
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
pygame.mixer.music.load("Music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)

# Sound effects volume
win_sound.set_volume(2)

# Game loop
laps = 0
lapsai = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event and game == 2:
            counter -= 1
            text = font.render(str(counter), True, (255, 0, 0))
            if counter == 0:
                timer_event = False
                game = 1
                pygame.mixer.music.load("drive.wav")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.15)
    if game == 1:
        frame_count += 1
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            player_velocity.x += 0.2
        elif keys[pygame.K_LEFT]:
            player_velocity.x -= 0.2

        if keys[pygame.K_DOWN]:
            player_velocity.y += 0.2
        elif keys[pygame.K_UP]:
            player_velocity.y -= 0.2

        player_velocity *= (1 - drag)

        previousLocation = (player_car_rect.x, player_car_rect.y)

        player_car_rect.x += player_velocity.x
        player_car_rect.y += player_velocity.y

        tileX = math.floor(screen_to_world(player_car_rect.x, player_car_rect.y)[0])
        tileY = math.floor(screen_to_world(player_car_rect.x, player_car_rect.y)[1])
        
        tile_layer = tmx_map.get_layer_by_name("BORDERS")
        tile = tile_layer.data[tileY][tileX]
        
        # Checkpoints and laps
        if tileX == 10 and tileY == 1:
            print("checkpoint 1 achieved")
            checkpoint1 = True
        if tileX == 27 and tileY == 9 and checkpoint1:
            print("checkpoint 2 achieved")
            checkpoint2 = True
        if tileX == 18 and tileY == 8 and checkpoint2:
            print("checkpoint 3 achieved")
            checkpoint3 = True
        if tileX == 1 and tileY == 4 and checkpoint3:
            print("checkpoint 4 achieved")
            checkpoint4 = True
        if tileX == 1 and tileY == 1 and checkpoint1 and checkpoint2 and checkpoint3 and checkpoint4:
            print("lap 1 achieved")
            laps = 1
        if tileX == 2 and tileY == 1 and laps == 1:
            print("checkpoint 5 achieved")
            checkpoint5 = True
        if tileX == 27 and tileY == 9 and laps == 1 and checkpoint5:
            print("checkpoint 6 achieved")
            checkpoint6 = True
        if tileX == 18 and tileY == 8 and laps == 1 and checkpoint6:
            print("checkpoint 7 achieved")
            checkpoint7 = True
        if tileX == 1 and tileY == 4 and laps == 1 and checkpoint7:
            print("checkpoint 8 achieved")
            checkpoint8 = True
        if tileX == 1 and tileY == 1 and laps == 1 and checkpoint5 and checkpoint6 and checkpoint7 and checkpoint8:
            print("lap 2 achieved")
            laps = 2
        if tileX == 2 and tileY == 1 and laps == 2:
            print("checkpoint 9 achieved")
            checkpoint9 = True
        if tileX == 27 and tileY == 9 and laps == 2 and checkpoint9 and checkpoint8 and checkpoint4:
            print("checkpoint 10 achieved")
            checkpoint10 = True
        if tileX == 18 and tileY == 8 and laps == 2 and checkpoint10 and checkpoint8 and checkpoint4:
            print("checkpoint 11 achieved")
            checkpoint11 = True
        if tileX == 1 and tileY == 4 and laps == 2 and checkpoint11 and checkpoint8 and checkpoint4:
            print("checkpoint 12 achieved")
            checkpoint12 = True
        if tileX == 1 and tileY == 1 and laps == 2 and checkpoint9 and checkpoint10 and checkpoint11 and checkpoint12:
            print("victory")
            game = 3

        if tile == COLLISION_TILE_ID:
            frame_count += 2
            player_car_rect.x = previousLocation[0]
            player_car_rect.y = previousLocation[1]

        if player_velocity.length() > 0:
            player_angle = math.degrees(math.atan2(-player_velocity.y, player_velocity.x))

        rotated_car_image = pygame.transform.rotate(scaled_car_image, player_angle)
        screen.fill(WHITE)

        for layer in road_layers:
            for x, y, image in layer.tiles():
                scaled_image = pygame.transform.scale(image, (scaled_tilewidth, scaled_tileheight))
                screen.blit(scaled_image, (x * scaled_tilewidth, y * scaled_tileheight))

        rotated_rect = rotated_car_image.get_rect(center=(player_car_rect.x, player_car_rect.y))
        screen.blit(rotated_car_image, rotated_rect.topleft)

        # AI Car Movement
        if is_moving_to_target:
            direction = target_position - pygame.Vector2(other_car_rect.x, other_car_rect.y)

            if direction.length() > 0:
                direction.normalize_ip()

            other_car_rect.x += direction.x * other_car_speed 
            other_car_rect.y += direction.y * other_car_speed
            
            angle = math.degrees(math.atan2(direction.y, direction.x))
            rotated_ai_car_image = pygame.transform.rotate(ai_scaled_car_image, -angle)
            rotated_ai_rect = rotated_ai_car_image.get_rect(center=(other_car_rect.centerx, other_car_rect.centery))
            
            screen.blit(rotated_ai_car_image, rotated_ai_rect.topleft)
            print(f"x: {other_car_rect.x} y: {other_car_rect.y}")
            if other_car_speed == 4:
                if lapsai <= 2:
                    if other_car_rect.x == 1310:
                        is_moving_to_target = False
                        target_position = pygame.Vector2(1310, 451)
                        step1 = True
                        is_moving_to_target = True
                    if other_car_rect.y == 451:
                        target_position = pygame.Vector2(1100, 450)
                        step2 = True
                    if other_car_rect.x == 1102 and step1:
                        target_position = pygame.Vector2(1100, 650)
                    if other_car_rect.y == 650 and step1:
                        target_position = pygame.Vector2(880, 650)
                        step3 = True
                    if other_car_rect.x == 880 and step1 and step2 and step3:
                        target_position = pygame.Vector2(880, 390)
                    if other_car_rect.y == 390 and step1 and step2 and step3:
                        target_position = pygame.Vector2(350, 390)
                    if other_car_rect.x == 352 and step1 and step2 and step3:
                        target_position = pygame.Vector2(350, 200)
                    if other_car_rect.y == 202 and step1 and step2 and step3:
                        target_position = pygame.Vector2(50, 200)
                        step4 = True
                    if other_car_rect.x == 50 and step1 and step2 and step3 and step4:
                        target_position = pygame.Vector2(50, 55)
                    if other_car_rect.y == 52 and step1 and step2 and step3 and step4:
                        target_position = pygame.Vector2(120, 55)
                        step5 = True
                        if lapsai == 2:
                            game = 4
                    if other_car_rect.x == 122 and step1 and step2 and step3 and step4 and step5:
                        target_position = pygame.Vector2(1310, 55)
                        lapsai += 1
                        step1 = False
                        step2 = False
                        step3 = False
                        step5 = False
            elif other_car_speed == 2:
                if lapsai <= 2:
                    if other_car_rect.x == 1310:
                        is_moving_to_target = False
                        target_position = pygame.Vector2(1310, 451)
                        step1 = True
                        is_moving_to_target = True
                    if other_car_rect.y == 451:
                        target_position = pygame.Vector2(1100, 450)
                        step2 = True
                    if other_car_rect.x == 1102 and step1:
                        target_position = pygame.Vector2(1100, 650)
                    if other_car_rect.y == 651 and step1:
                        target_position = pygame.Vector2(880, 650)
                        step3 = True
                    if other_car_rect.x == 880 and step1 and step2 and step3:
                        target_position = pygame.Vector2(880, 390)
                    if other_car_rect.y == 390 and step1 and step2 and step3:
                        target_position = pygame.Vector2(350, 390)
                    if other_car_rect.x == 352 and step1 and step2 and step3:
                        target_position = pygame.Vector2(350, 200)
                    if other_car_rect.y == 202 and step1 and step2 and step3:
                        target_position = pygame.Vector2(50, 200)
                        step4 = True
                    if other_car_rect.x == 51 and step1 and step2 and step3 and step4:
                        target_position = pygame.Vector2(50, 55)
                    if other_car_rect.y == 54 and step1 and step2 and step3 and step4:
                        target_position = pygame.Vector2(120, 55)
                        step5 = True
                        if lapsai == 2:
                            game = 4
                    if other_car_rect.x == 120 and step1 and step2 and step3 and step4 and step5:
                        target_position = pygame.Vector2(1310, 55)
                        lapsai += 1
                        step1 = False
                        step2 = False
                        step3 = False
                        step5 = False



                    
        # Timer display
        text = fontTimer.render(f'Time: {frame_count // frame_rate:02}:{frame_count % frame_rate:02}', True, (0, 0, 0))
        screen.blit(text, [6, 6])

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    
    elif game == 0:
        screen.blit(backgrounds, (0, 0))
        screen.blit(Start_TXT, imgRect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            other_car_speed = 4
            game = 2
        if keys[pygame.K_BACKSPACE]:
            other_car_speed = 2
            game = 2
        pygame.display.flip()
        clock.tick(FPS)

    elif game == 2:
        screen.blit(lights, (0, 0))
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        pygame.display.flip()

    elif game == 3:
        screen.blit(victory, (0, 0))
        pygame.mixer.music.stop()
        win_sound.play()
        win_sound.set_volume(5)
        font_size = 120
        font = pygame.font.Font(None, font_size)
        text_rect = text.get_rect(center=screen.get_rect().center)
        text = fontTimer.render(f'Time: {frame_count // frame_rate:02}:{frame_count % frame_rate:02}', True, (2, 247, 15))
        screen.blit(text, text_rect,)
        screen.blit(Victory_TXT, imgRects)
        pygame.display.flip()
        turn = 1
        
    elif game == 4:
        screen.blit(lose, (0, 0))
        lose_sound.play()
        lose_sound.set_volume(10)
        pygame.display.flip()
        turn = 1

# Quit the game	
pygame.quit()
sys.exit()
