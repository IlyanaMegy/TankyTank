import math
import random
import pygame
from pygame import mixer

pygame.init()

win = pygame.display.set_mode((900, 600))

pygame.display.set_caption('Tanky Tanks')
icon = pygame.image.load('j1_tank.png')
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

win.fill(BLACK)
pygame.display.flip()

# # Background
# background = pygame.image.load('background.png')

vel = 1
run = True
dim_tank = 20
dir = "right"

# Player 1
j1_img = pygame.image.load('j1_tank.png').convert_alpha()
j1_x = 250
j1_y = 250

# Player 2
j2_img = pygame.image.load('j2_tank.png')
j2_x = 500
j2_y = 250

# Bullet
# Ready - You can't see the bullet on the win
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = j1_x
bulletY = j1_y
bullet_state = "ready"


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def player(x, y):
    win.blit(j1_img, (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(over_text, (200, 250))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bulletImg, (x,y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


 
# infinite loop
while run:
    pygame.time.delay(10)
    print(dir)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False

     # stores keys pressed 
    keys = pygame.key.get_pressed()
      
    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and j1_x>0:
          
        # decrement in x co-ordinate
        j1_x -= vel
        dir = "left"
          
    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and j1_x<900-dim_tank:
          
        # increment in x co-ordinate
        j1_x += vel
        dir = "right"
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and j1_y>0:
          
        # decrement in y co-ordinate
        j1_y -= vel
        dir = "up"
          
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and j1_y<600-dim_tank:
        # increment in y co-ordinate
        j1_y += vel
        dir = "down"

    if keys[pygame.K_SPACE]:
        ##shoot that bullet
        if bullet_state == "ready":
           bulletSound = mixer.Sound("one_shot_sound.wav")
           bulletSound.play()
           fire_bullet(bulletX, bulletY)
       
    win.fill((0, 0, 0))

    if dir == "left":
        pygame.transform.rotate(j1_img, 40)
        print("turn left")
    elif dir =="down":
        pygame.transform.rotate(j1_img, 56)
    elif dir =="up":
        pygame.transform.rotate(j1_img, 80)
    else:
        pygame.transform.rotate(j1_img, 160)
    
    player(j1_x, j1_y)
    show_score(textX, testY)
    pygame.display.update() 