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
bullet_start_x = j1_x+64
bullet_start_y = j1_y+26
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def bullet_dir_x(dir):
    if dir == "left":
        bullet_start_x = j1_x
    elif dir =="down":
        bullet_start_x = j1_x+26
    elif dir =="up":
        bullet_start_x = j1_x+26
    else:
        bullet_start_x = j1_x+64
    return bullet_start_x


def bullet_dir_y(dir):
    if dir == "left":
        bullet_start_y = j1_y+26
    elif dir =="down":
        bullet_start_y = j1_y+63
    elif dir =="up":
        bullet_start_y = j1_y
    else:
        bullet_start_y = j1_y+26
    return bullet_start_y


def player(x, y,dir):
    if dir == "left":
        win.blit(pygame.transform.rotate(j1_img, 180), (j1_x, j1_y))
    elif dir =="down":
        win.blit(pygame.transform.rotate(j1_img, 270), (j1_x, j1_y))
    elif dir =="up":
        win.blit(pygame.transform.rotate(j1_img, 90), (j1_x, j1_y))
    else:
        win.blit(pygame.transform.rotate(j1_img, 0), (j1_x, j1_y))

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


def isCollision(enemyX, enemyY, bullet_start_x, bullet_start_y):
    distance = math.sqrt(math.pow(enemyX - bullet_start_x, 2) + (math.pow(enemyY - bullet_start_y, 2)))
    if distance < 27:
        return True
    else:
        return False


 
# infinite loop
while run:
    pygame.time.delay(10) 
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False

     # stores keys pressed 
    keys = pygame.key.get_pressed()
      
    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and j1_x>0:
        if keys[pygame.K_UP] and j1_y>0:
            continue
        elif keys[pygame.K_DOWN] and j1_y<600-dim_tank:
            continue
        else:
            # decrement in x co-ordinate
            j1_x -= vel
            dir = "left"
          
    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and j1_x<900-dim_tank:
        if keys[pygame.K_UP] and j1_y>0:
            continue
        elif keys[pygame.K_DOWN] and j1_y<600-dim_tank:
            continue
        else:
            # increment in x co-ordinate
            j1_x += vel
            dir = "right"
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and j1_y>0:
        if keys[pygame.K_RIGHT] and j1_x<900-dim_tank:
            continue
        elif keys[pygame.K_LEFT] and j1_x>0:
            continue
        else:
            # decrement in y co-ordinate
            j1_y -= vel
            dir = "up"
            
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and j1_y<600-dim_tank:
        if keys[pygame.K_RIGHT] and j1_x<900-dim_tank:
            continue
        elif keys[pygame.K_LEFT] and j1_x>0:
            continue
        else:
            # increment in y co-ordinate
            j1_y += vel
            dir = "down"

    if keys[pygame.K_SPACE]:
        ##shoot that bullet
        if bullet_state == "ready":
           bulletSound = mixer.Sound("one_shot_sound.wav")
           bulletSound.play()
           fire_bullet(bullet_start_x, bullet_start_y)
           print("fire!")
       
    win.fill((0, 0, 0))

    if bullet_state == "fire":
        fire_bullet(bullet_start_x, bullet_start_y)
        if dir == "right":
            bullet_start_x += 4
        elif dir == "left":
            bullet_start_x -= 4
        elif dir == "up":
            bullet_start_y -= 4
        else:
            bullet_start_y += 4
        

    if bullet_start_y <= 0 or bullet_start_y >= 600:
        bullet_state = "ready"
        bullet_start_x = bullet_dir_x(dir)
        bullet_start_y = bullet_dir_y(dir)

    if bullet_start_x <= 0 or bullet_start_x >= 900:
        bullet_state = "ready"
        bullet_start_x = bullet_dir_x(dir)
        bullet_start_y = bullet_dir_y(dir)
      

    player(j1_x,j1_y,dir)
    show_score(textX, testY)
    pygame.display.update() 