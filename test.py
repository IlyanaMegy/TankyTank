import math
import random
import pygame
from pygame import mixer

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

win = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Tanky Tanks')
icon = pygame.image.load('j1_tank.png')
pygame.display.set_icon(icon)

# Walls
pygame.draw.rect(win, BLUE, (350,350,100,200))

win.fill(BLACK)
pygame.display.flip()

vel = 1
run = True
dim_tank = 40 

# Player 1
j1_img = pygame.image.load('j1_tank.png').convert_alpha()
j1_x = 115
j1_y = 130
dir = "right"

# Score
score_value_j1 = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 50)

def player(x, y, dir):
        if dir == "left":
            win.blit(pygame.transform.rotate(j1_img, 180), (j1_x, j1_y))
        elif dir =="down":
            win.blit(pygame.transform.rotate(j1_img, 270), (j1_x, j1_y))
        elif dir =="up":
            win.blit(pygame.transform.rotate(j1_img, 90), (j1_x, j1_y))
        elif dir =="right":
            win.blit(pygame.transform.rotate(j1_img, 0), (j1_x, j1_y))
        else:
            win.blit(j1_img, (x,y))

def show_score(x, y, score_value):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("END OF THE GAME.", True, (255, 255, 255))
    win.blit(over_text, (200, 250))


def isWall(x, y):
    if (350 - dim_tank) <= x <= (450 + dim_tank) and (350 - dim_tank) <= y <= (550 + dim_tank):
        print("in wall")
        print(j1_x,j1_y)
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
        j1_x_new = j1_x - vel
        if keys[pygame.K_UP] and j1_y>0:
            continue
        elif keys[pygame.K_DOWN] and j1_y<600-dim_tank:
            continue
        elif isWall(j1_x_new, j1_y):
            continue
        else:
            # decrement in x co-ordinate
            j1_x = j1_x_new
            dir = "left"
            player(j1_x,j1_y,dir)
            

    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and j1_x<600-dim_tank:
        j1_x_new = j1_x + vel
        if keys[pygame.K_UP] and j1_y>0:
            continue
        elif keys[pygame.K_DOWN] and j1_y<600-dim_tank:
            continue
        elif isWall(j1_x, j1_y):
            continue
        else:
            # increment in x co-ordinate
            j1_x = j1_x_new
            dir = "right"
            player(j1_x,j1_y,dir)
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and j1_y>0:
        j1_y_new = j1_y - vel
        if keys[pygame.K_RIGHT] and j1_x<600-dim_tank:
            continue
        elif keys[pygame.K_LEFT] and j1_x>0:
            continue
        elif isWall(j1_x, j1_y):
            continue
        else:
            # decrement in y co-ordinate
            j1_y = j1_y_new
            dir = "up"
            player(j1_x, j1_y, dir)
            
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and j1_y<600-dim_tank:
        j1_y_new = j1_y + vel
        if keys[pygame.K_RIGHT] and j1_x<600-dim_tank:
            continue
        elif keys[pygame.K_LEFT] and j1_x>0:
            continue
        elif isWall(j1_x, j1_y):
            continue
        else:
            # increment in y co-ordinate
            j1_y = j1_y_new
            dir = "down"
            player(j1_x, j1_y, dir)
       
    win.fill((0, 0, 0))
    player(j1_x, j1_y, dir)
    pygame.draw.rect(win, BLUE, (350,350,100,200))
    
    show_score(textX, testY,score_value_j1)
    # show_score(textX, testY,score_value_j2)
    pygame.display.update() 