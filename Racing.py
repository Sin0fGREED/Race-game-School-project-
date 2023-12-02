from tracemalloc import start
import pygame
import sys
import pytmx
import math
import pygame.mixer
from vector2d import Vector2D
import os
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1390, 768
FPS = 60
WHITE = (255, 255, 255)
ROAD_COLOR = (100, 100, 100)
MAP_SCALE = 3
BLUE = (255, 255, 255)
font = pygame.font.SysFont(None, 50)
font_size = 50
text_home = ("""Press ENTER to start. To win you must complete 2 laps of the track.""")
img = font.render(text_home, True, BLUE)
imgRect = img.get_rect()
imgRect.center = (WIDTH // 2, HEIGHT // 2)
backgrounds = pygame.image.load("./mainMenu/car.jpg")
lights = pygame.image.load("./mainMenu/lights.jpg")
victory = pygame.image.load("./mainMenu/victory.jpeg")
lose = pygame.image.load("./mainMenu/freddy.png")
clock = pygame.time.Clock()
counter = 5
timer_event = pygame.USEREVENT + 1
text = font.render(str(counter), True, (255, 0, 0))
pygame.time.set_timer(timer_event, 1000)
drag = 0.04
other_car_speed = 4
target_position = pygame.Vector2(1310, 55)
is_moving_to_target = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formula 1 Racing Course")

clock = pygame.time.Clock()

frame_rate = 60
frame_count = 0
start_time = 0

tmx_map = pytmx.load_pygame('Road.tmx')
road_layers = [layer for layer in tmx_map.visible_layers if isinstance(layer, pytmx.TiledTileLayer)]
scaled_tilewidth = tmx_map.tilewidth * MAP_SCALE
scaled_tileheight = tmx_map.tileheight * MAP_SCALE
scaled_width = tmx_map.width * scaled_tilewidth
scaled_height = tmx_map.height * scaled_tileheight

original_car_image = pygame.image.load("./Vehicles/CARS.png")
scaled_car_image = pygame.transform.scale(original_car_image, (40, 20))

ai_car_image = pygame.image.load("./Vehicles/aiCARS.png")
ai_scaled_car_image = pygame.transform.scale(ai_car_image, (40, 20))

player_car_rect = scaled_car_image.get_rect()
player_car_rect.x = 150
player_car_rect.y = 85

other_car_rect = ai_scaled_car_image.get_rect()
other_car_rect.x = 150
other_car_rect.y = 55

player_velocity = pygame.Vector2(0, 0)
player_angle = 0



COLLISION_TILE_ID = 148

def screen_to_world(screen_x, screen_y):
    world_x = (screen_x / WIDTH) * 29
    world_y = (screen_y / HEIGHT) * 16
    return [world_x, world_y]

running = True
checkpoint1 = False
checkpoint2 = False
checkpoint3 = False
checkpoint4 = False
game = 0
step1 = False
step2 = False
step3 = False
play = False


win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
pygame.mixer.music.load("Music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)


win_sound.set_volume(2)


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
        print(tileX, tileY)

        tile_layer = tmx_map.get_layer_by_name("BORDERS")
        tile = tile_layer.data[tileY][tileX]
        print (tile)

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
            print("finished achieved")
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

            if other_car_speed == 4:
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
                if other_car_rect.x == 50 and step1 and step2 and step3:
                    target_position = pygame.Vector2(50, 55)
                if other_car_rect.y == 52 and step1 and step2 and step3:
                    target_position = pygame.Vector2(120, 55)
                    game = 4
        # Timer display
        text = font.render(f'Time: {frame_count // frame_rate:02}:{frame_count % frame_rate:02}', True, (255, 255, 0))
        screen.blit(text, [6, 6])

        pygame.display.flip()
        clock.tick(FPS)

    elif game == 0:
        screen.blit(backgrounds, (0, 0))
        screen.blit(img, imgRect)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
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
        font_size = 120
        font = pygame.font.Font(None, font_size)
        text_rect = text.get_rect(center=screen.get_rect().center)
        text = font.render(f'Time: {frame_count // frame_rate:02}:{frame_count % frame_rate:02}', True, (255, 255, 0))
        screen.blit(text, text_rect,)
        pygame.display.flip()
        turn = 1
    elif game == 4:
        screen.blit(lose, (0, 0))
        lose_sound.play()
        lose_sound.set_volume(5)
        pygame.display.flip()
        turn = 1

pygame.quit()
sys.exit()
