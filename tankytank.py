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


# Background
background = pygame.image.load('map.png')
margin_x = 0
margin_y = 0
# Walls
dim_cube = 46

# soit l'origine en haut à gauche de l'image --> rajouter le margin de l'image après
walls = [[48,50,2],[139,5,2],[277,96,1],[322,5,3],[413,50,4],[459,95,1],[504,50,2],[139,141,2],[3,187,2],
         [48,232,2],[277,187,1],[231,232,6],[460,187,3],[505,187,1],
         [139,278,5],[184,278,2],[413,323,1],[504,278,4],[3,368,1],[48,368,5],[413,413,1],[458,413,1],
         [139,551,1],[413,506,2],[504,506,2],[458,551,1]]
big_wall = [277,2,278,5]


# let's see those walls
# for wall in walls:    
#     somewall = pygame.draw.rect(background, BLUE, (wall[0], wall[1], dim_cube+1, (dim_cube * wall[2])))
#     bigwall = pygame.draw.rect(background, RED, (big_wall[0], big_wall[2], (dim_cube * big_wall[1]), (dim_cube * big_wall[3])))

win.fill(BLACK)
pygame.display.flip()

vel = 1
run = True
dim_tank = 30

# Player 1
j1_img = pygame.image.load('j1_tank.png').convert_alpha()
j1_x = 291
j1_y = 568
dir = "right"

# Player 2
j2_img = pygame.image.load('j2_tank.png')
j2_x = 500
j2_y = 250

# Bullet
# Ready - You can't see the bullet on the win
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bullet_j1_x = j1_x+50
bullet_j1_y = j1_y+20.5
bullet_j1_state = "ready"

# Score
score_value_j1 = 0
score_value_j2 = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 50)

def bullet_dir_x(dir):
    if dir == "left":
        bullet_j1_x = j1_x
    elif dir =="down":
        bullet_j1_x = j1_x+20.5
    elif dir =="up":
        bullet_j1_x = j1_x+20.5
    else:
        bullet_j1_x = j1_x+50
    return bullet_j1_x


def bullet_dir_y(dir):
    if dir == "left":
        bullet_j1_y = j1_y+20.5
    elif dir =="down":
        bullet_j1_y = j1_y+50
    elif dir =="up":
        bullet_j1_y = j1_y
    else:
        bullet_j1_y = j1_y+20.5
    return bullet_j1_y


def player(x, y, dir):
        if dir == "left":
            win.blit(pygame.transform.rotate(j1_img, 180), (j1_x, j1_y))
        elif dir =="down":
            win.blit(pygame.transform.rotate(j1_img, 270), (j1_x, j1_y))
        elif dir =="up":
            win.blit(pygame.transform.rotate(j1_img, 90), (j1_x, j1_y))
        elif dir =="right":
            win.blit(pygame.transform.rotate(j1_img, 0), (j1_x, j1_y))

def show_score(x, y, score_value):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("END OF THE GAME.", True, (255, 255, 255))
    win.blit(over_text, (200, 250))


def fire_bullet(x, y):
    global bullet_j1_state
    bullet_j1_state = "fire"
    win.blit(bulletImg, (x,y))


def isCollision(enemyX, enemyY, bullet_j1_x, bullet_j1_y):
    distance = math.sqrt(math.pow(enemyX - bullet_j1_x, 2) + (math.pow(enemyY - bullet_j1_y, 2)))
    if distance < 27:
        return True
    else:
        return False

def isWall(x, y):
    for wall in walls:
        res = False
        if (wall[0] <= x <= (wall[0] + dim_cube)) and (wall[1] <= y <= (wall[1] + (wall[2] * dim_cube ))):
            res = True
            print("wall here")
            print(wall[0], wall[1])
            break 
        elif (big_wall[0]<= x <= (big_wall[0] + (big_wall[1] * dim_cube))) and (big_wall[2]<= y <= (big_wall[2] + (big_wall[3] * dim_cube))):
            res = True
            break
        else:
            continue
    return res

# infinite loop
while run:
    pygame.time.delay(10)
    print(j1_x,j1_y)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False

     # stores keys pressed 
    keys = pygame.key.get_pressed()
      
    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and j1_x>0:
        j1_x_new = j1_x - vel
        if isWall(j1_x_new, j1_y):
            continue
        else:
            # decrement in x co-ordinate
            j1_x = j1_x_new
            dir = "left"
            player(j1_x,j1_y,dir)
            

    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and j1_x<600-dim_tank:
        j1_x_new = j1_x + vel
        x = j1_x_new + dim_tank
        if isWall(x, j1_y):
            continue
        else:
            # increment in x co-ordinate
            j1_x = j1_x_new
            dir = "right"
            player(j1_x,j1_y,dir)
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and j1_y>0:
        j1_y_new = j1_y - vel
        if isWall(j1_x, j1_y_new):
            continue
        else:
            # decrement in y co-ordinate
            j1_y = j1_y_new
            dir = "up"
            player(j1_x, j1_y, dir)
            
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and j1_y<600-dim_tank:
        j1_y_new = j1_y + vel
        y = j1_y_new + dim_tank
        if isWall(j1_x, y):
            continue
        else:
            # increment in y co-ordinate
            j1_y = j1_y_new
            dir = "down"
            player(j1_x, j1_y, dir)
       
    # if keys[pygame.K_SPACE]:
    #     ##shoot that bullet
    #     if bullet_j1_state == "ready":
    #        bulletSound = mixer.Sound("one_shot_sound.wav")
    #        bulletSound.play()
    #        fire_bullet(bullet_j1_x, bullet_j1_y)
    #        print("fire!")
       
    win.fill((0, 0, 0))
    
    win.blit(background, (margin_x, margin_y))
    player(j1_x, j1_y, dir)
    # Collision
    # j2_hasbeen_shot = isCollision(j2_x, j2_y, bullet_j1_x, bullet_j1_y)
    # if j2_hasbeen_shot:
    #     explosionSound = mixer.Sound("explosion.wav")
    #     explosionSound.play()
    #     bullet_j1_x = bullet_dir_x(dir)
    #     bullet_j1_y = bullet_dir_y(dir)
    #     bullet_j1_state = "ready"
    #     score_value_j1 += 1

    if bullet_j1_state == "fire":
        fire_bullet(bullet_j1_x, bullet_j1_y)
        if dir == "right":
            bullet_j1_x += 4
        elif dir == "left":
            bullet_j1_x -= 4
        elif dir == "up":
            bullet_j1_y -= 4
        else:
            bullet_j1_y += 4
        

    if bullet_j1_y <= 0 or bullet_j1_y >= 600:
        bullet_j1_x = bullet_dir_x(dir)
        bullet_j1_y = bullet_dir_y(dir)
        bullet_j1_state = "ready"

    if bullet_j1_x <= 0 or bullet_j1_x >= 900:
        bullet_j1_x = bullet_dir_x(dir)
        bullet_j1_y = bullet_dir_y(dir)
        bullet_j1_state = "ready"
      
    show_score(textX, testY,score_value_j1)
    # show_score(textX, testY,score_value_j2)
    pygame.display.update() 