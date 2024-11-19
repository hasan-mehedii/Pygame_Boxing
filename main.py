import pygame
import random
import math
from pygame import mixer

pygame.init()

window_x = 1200
window_y = 800
player_health = 50
enemy_health = 50

# Initialize screen
screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Real Fighting")

# Load background music
mixer.music.load("battle.mp3")
mixer.music.play(-1)

# Load images
background = pygame.image.load("boxing.jpg")
background = pygame.transform.scale(background, (window_x, window_y))
icon = pygame.image.load("boxing_background.png")
pygame.display.set_icon(icon)

# Player images
player_offense = pygame.image.load("blue_punch.png")
player_defence = pygame.image.load("blue_defence.png")
player_offense = pygame.transform.scale(player_offense, (400, 400))
player_defence = pygame.transform.scale(player_defence, (400, 400))

# Enemy images
enemy_offense = pygame.image.load("red_punch.png")
enemy_defence = pygame.image.load("red_defence.png")
enemy_offense = pygame.transform.scale(enemy_offense, (400, 400))
enemy_defence = pygame.transform.scale(enemy_defence, (400, 400))

font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)  # Larger font for game over text
text_y = 10
player_text_x = 1000
enemy_text_x = 10

# Player and enemy coordinates
player_x = 610
player_y = 300
enemy_x = 300
enemy_y = 300

# Initialize player and enemy states
player_image = player_defence
enemy_image = enemy_defence
space_pressed = False
enemy_switch_time = 0
enemy_in_offense = False
game_over_time = 0

def draw_player(x, y, image):
    screen.blit(image, (x, y))

def draw_enemy(x, y, image):
    screen.blit(image, (x, y))

def player_score(x, y, health):
    sc = font.render("Health: "+str(health), True, (255, 255, 255))
    screen.blit(sc, (x, y))

# Function to display game over message
def display_game_over():
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (window_x // 2 - game_over_text.get_width() // 2, (window_y // 2 - game_over_text.get_height() // 2) - 200))

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    if player_health == 0 or enemy_health == 0:
        if game_over_time == 0:
            game_over_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - game_over_time < 2000:  # Display Game Over for 2 seconds
            display_game_over()
        else:
            running = False  # After 2 seconds, terminate the game loop

    # Hide the player whose health is zero
    if player_health == 0:
        player_image = None 
    if enemy_health == 0:
        enemy_image = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Forcefully exit")
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= 35

            if event.key == pygame.K_RIGHT:
                player_x += 35  

            if event.key == pygame.K_SPACE:
                player_image = player_offense
                punch_sound = mixer.Sound("punch.mp3")
                punch_sound.play()
                space_pressed = True
                player_switch_time = pygame.time.get_ticks()
                distaance = math.sqrt(math.pow((enemy_x - player_x), 2) + math.pow((enemy_y - player_y), 2))
                if distaance < 300:
                    enemy_health -= 2
                    enemy_sound = mixer.Sound("tom_hurt.mp3")
                    enemy_sound.play()
                    print("1 Punch delivered!!!")

    if not enemy_in_offense:
        random_chance = random.randint(1, 100)  # Random chance (1% chance per frame)
        if random_chance > 98: 
            enemy_image = enemy_offense
            enemy_in_offense = True
            enemy_switch_time = pygame.time.get_ticks()
            distaance = math.sqrt(math.pow((enemy_x - player_x), 2) + math.pow((enemy_y - player_y), 2))
            if distaance < 300:
                player_health -= 2
                print("1 Punch got!!!")

    if enemy_in_offense and pygame.time.get_ticks() - enemy_switch_time > 150:
        enemy_image = enemy_defence
        enemy_in_offense = False

    if space_pressed and pygame.time.get_ticks() - player_switch_time > 150:
        player_image = player_defence
        space_pressed = False

    # Draw player and enemy only if they have health
    if player_image:
        draw_player(player_x, player_y, player_image)
    if enemy_image:
        draw_enemy(enemy_x, enemy_y, enemy_image)

    player_score(player_text_x, text_y, player_health)
    player_score(enemy_text_x, text_y, enemy_health)

    pygame.display.update()

pygame.quit()
