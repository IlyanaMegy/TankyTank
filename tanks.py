import math
import random

import pygame
from pygame import mixer

# soient (j1_x;j1_y) coordonnées j1
#      (j2_x;j2_y) coordonnées j2
#      (bulletX_j1;bulletY_j1) coordonées balle de tir depuis j1 vers j2
#      a coefficient directeur ligne de tir
#      b ordonnée à l'origine de la ligne de tir
#      y l'équation de la droite (ligne de tir)

# or:
# y = ax + b
# a = (y2 - y1)/(x2 - x1)
# b = y - ax

# pour trouver valeur de bulletX pour bulletY -= 1 :
# bulletY = ax + b
# x = (bulletY - b) / a


pygame.init()

win = pygame.display.set_mode((900, 600))

pygame.display.set_caption('Tanky Tanks')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

win.fill(BLACK)
pygame.display.flip()

# init values

vel = 1
run = True
dim_tank = 20

# player 1
j1_x = 200
j1_y = 200


j1_x_new = 0
j1_y_new = 0

# j1 = pygame.image.load('usa.png')

# player 2
j2_x = 500
j2_y = 500
j2_x_new = 0
j2_y_new = 0

# j2 = pygame.image.load('urss.png')


# Bullet
# Ready - You can't see the bullet on the win
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_new = 0
bulletY_new = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)



def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(over_text, (200, 250))


# def player(x, y):
#     win.blit(j1, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

  
# infinite loop 
run = True
while run:
    pygame.time.delay(10)
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False

    # stores keys pressed 
    keys = pygame.key.get_pressed()
      
    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and j1_x>0:
          
        # decrement in x co-ordinate
        j1_x -= vel
          
    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and j1_x<900-dim_tank:
          
        # increment in x co-ordinate
        j1_x += vel
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and j1_y>0:
          
        # decrement in y co-ordinate
        j1_y -= vel
          
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and j1_y<600-dim_tank:
        # increment in y co-ordinate
        j1_y += vel

    if keys[pygame.K_SPACE]:
        ##shoot that bullet
        if bullet_state == "ready":
           bulletSound = mixer.Sound("one_shot_sound.wav")
           bulletSound.play()
           # Get the current x cordinate of the spaceship
           bulletX = j1_x # top of cannon
           fire_bullet(bulletX, bulletY)
       
    # j1_x += j1_x_new
    # if j1_x <= 0:
    #     j1_x = 0
    # elif j1_x >= 900:
    #     j1_x = 900

    # j1_y += j1_y_new
    # if j1_y <= 0:
    #     j1_y = 0
    # elif j1_y >= 600:
    #     j1_y = 600

    win.fill((0, 0, 0))

    # drawing object on win which is rectangle here 
    j1 = pygame.draw.rect(win, RED, (j1_x, j1_y, dim_tank, dim_tank))
    j2 = pygame.draw.rect(win, BLUE, (j2_x, j2_y, dim_tank, dim_tank))

    gunline_x = j1_x + (dim_tank/2)
    gunline_y = j1_y + (dim_tank/2)

    # gun guideline
    gunline = pygame.draw.line(win, BLUE, (120, 120), (gunline_x, gunline_y), width=3)
    # canon = pygame.draw.line(gunline, GREEN, width=6) 

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_new

    show_score(textX, testY)
    pygame.display.update() 
  
# closes the pygame window 
pygame.quit()