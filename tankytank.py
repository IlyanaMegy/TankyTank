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

vel = 1.2
run = True
dim_tank = 33


# Player 1
j1_img = pygame.image.load('j1_tank.png').convert_alpha()
j1_x = 291
j1_y = 568
dir_j1 = "right"


# Player 2
j2_img = pygame.image.load('j2_tank.png').convert_alpha()
j2_x = 237
j2_y = 51
dir_j2 = "up"


# Bullet
# Ready - You can't see the bullet on the win
# Fire - The bullet is currently moving
bullet_j1_x = j1_x + dim_tank 
bullet_j1_y = j1_y + (dim_tank/2)
bullet_j1_state = "ready"

bullet_j2_x = j2_x
bullet_j2_y = j2_y
bullet_j2_state = "ready"
bullet_j1 =  pygame.draw.circle(win, WHITE, (bullet_j1_x,bullet_j1_y), 5, 10)


# Score
score_value_j1 = 0
score_value_j2 = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 50)

def fire_bullet(x, y):
    pygame.draw.circle(win, WHITE, (bullet_j1_x,bullet_j1_y), 3, 10)

def bullet_dir_x(dir):
    if dir == "left":
        bullet_j1_x = j1_x
    elif dir =="down":
        bullet_j1_x = j1_x + (dim_tank/2)
    elif dir =="up":
        bullet_j1_x = j1_x + (dim_tank/2)
    else:
        bullet_j1_x = j1_x + dim_tank
    return bullet_j1_x

def bullet_dir_y(dir):
    if dir == "left":
        bullet_j1_y = j1_y + (dim_tank/2)
    elif dir =="down":
        bullet_j1_y = j1_y + dim_tank
    elif dir =="up":
        bullet_j1_y = j1_y
    else:
        bullet_j1_y = j1_y + (dim_tank/2)
    return bullet_j1_y

def player(x, y, dir, img):
        if dir == "left":
            win.blit(pygame.transform.rotate(img, 180), (x, y))
        elif dir =="down":
            win.blit(pygame.transform.rotate(img, 270), (x, y))
        elif dir =="up":
            win.blit(pygame.transform.rotate(img, 90), (x, y))
        elif dir =="right":
            win.blit(pygame.transform.rotate(img, 0), (x, y))

def show_score(x, y, score_value):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("END OF THE GAME.", True, (255, 255, 255))
    win.blit(over_text, (200, 250))

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
            break 
        elif (big_wall[0]<= x <= (big_wall[0] + (big_wall[1] * dim_cube))) and (big_wall[2]<= y <= (big_wall[2] + (big_wall[3] * dim_cube))):
            res = True
            break
        else:
            continue
    return res


#################################################################################################################################
####################################################          GAME            ###################################################
#################################################################################################################################


# infinite loop
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
     # stores keys pressed 
    keys = pygame.key.get_pressed()

    
    #################################################################################################################################
    #################################################           PLAYER 1            #################################################
    #################################################################################################################################

    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and j1_x>0:
        j1_x_new = j1_x - vel
        if isWall(j1_x_new, j1_y):
            continue
        elif keys[pygame.K_DOWN]:
            continue
        elif keys[pygame.K_UP]:
            continue
        else:
            # decrement in x co-ordinate
            j1_x = j1_x_new
            dir_j1 = "left"
            player(j1_x,j1_y,dir_j1,j1_img)

    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and j1_x<600-dim_tank:
        j1_x_new = j1_x + vel
        x = j1_x_new + dim_tank
        if isWall(x, j1_y):
            continue
        elif keys[pygame.K_DOWN]:
            continue
        elif keys[pygame.K_UP]:
            continue
        else:
            # increment in x co-ordinate
            j1_x = j1_x_new
            dir_j1 = "right"
            player(j1_x,j1_y,dir_j1,j1_img)
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and j1_y>0:
        j1_y_new = j1_y - vel
        if isWall(j1_x, j1_y_new):
            continue
        elif keys[pygame.K_LEFT]:
            continue
        elif keys[pygame.K_RIGHT]:
            continue
        else:
            # decrement in y co-ordinate
            j1_y = j1_y_new
            dir_j1 = "up"
            player(j1_x, j1_y, dir_j1, j1_img)
            
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and j1_y<600-dim_tank:
        j1_y_new = j1_y + vel
        y = j1_y_new + dim_tank
        if isWall(j1_x, y):
            continue
        elif keys[pygame.K_LEFT]:
            continue
        elif keys[pygame.K_RIGHT]:
            continue
        else:
            # increment in y co-ordinate
            j1_y = j1_y_new
            dir_j1 = "down"
            player(j1_x, j1_y, dir_j1, j1_img)

    if keys[pygame.K_SPACE]:
        # shoot that bullet
        if bullet_j1_state == "ready":
           bulletSound = mixer.Sound("one_shot_sound.wav")
           bulletSound.play()
           bullet_j1_state = "fire"
           fire_bullet(bullet_j1_x, bullet_j1_y)
           old_dir_j1 = dir_j1


    #################################################################################################################################
    #################################################           PLAYER 2            #################################################
    #################################################################################################################################

    # if left arrow key is pressed
    if keys[pygame.K_q] and j2_x>0:
        j2_x_new = j2_x - vel
        if isWall(j2_x_new, j2_y):
            continue
        elif keys[pygame.K_z]:
            continue
        elif keys[pygame.K_s]:
            continue
        else:
            # decrement in x co-ordinate
            j2_x = j2_x_new
            dir_j2 = "left"
            player(j2_x,j2_y,dir_j2,j2_img)

    # if left arrow key is pressed
    if keys[pygame.K_d] and j2_x<600-dim_tank:
        j2_x_new = j2_x + vel
        x = j2_x_new + dim_tank
        if isWall(x, j2_y):
            continue
        elif keys[pygame.K_z]:
            continue
        elif keys[pygame.K_s]:
            continue
        else:
            # increment in x co-ordinate
            j2_x = j2_x_new
            dir_j2 = "right"
            player(j2_x,j2_y,dir_j2,j2_img)
         
    # if left arrow key is pressed   
    if keys[pygame.K_z] and j2_y>0:
        j2_y_new = j2_y - vel
        if isWall(j2_x, j2_y_new):
            continue
        elif keys[pygame.K_d]:
            continue
        elif keys[pygame.K_q]:
            continue
        else:
            # decrement in y co-ordinate
            j2_y = j2_y_new
            dir_j2 = "up"
            player(j2_x, j2_y, dir_j2, j2_img)
              
    if keys[pygame.K_s] and j2_y<600-dim_tank:
        j2_y_new = j2_y + vel
        y = j2_y_new + dim_tank
        if isWall(j2_x, y):
            continue
        elif keys[pygame.K_d]:
            continue
        elif keys[pygame.K_q]:
            continue
        else:
            # increment in y co-ordinate
            j2_y = j2_y_new
            dir_j2 = "down"
            player(j2_x, j2_y, dir_j2, j2_img)

    if keys[pygame.K_a]:
        # shoot that bullet
        if bullet_j2_state == "ready":  #try to remove that condition later
           bulletSound = mixer.Sound("one_shot_sound.wav")
           bulletSound.play()
           fire_bullet(bullet_j2_x, bullet_j2_y)
           old_dir_j2 = dir_j2

    ##################################################################################################################################
    

    win.fill((0, 0, 0))
    win.blit(background, (margin_x, margin_y))
    player(j1_x, j1_y, dir_j1, j1_img)
    player(j2_x, j2_y, dir_j2, j2_img)


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
        if old_dir_j1 == "right":
            bullet_j1_x += 4
        elif old_dir_j1 == "left":
            bullet_j1_x -= 4
        elif old_dir_j1 == "up":
            bullet_j1_y -= 4
        else:
            bullet_j1_y += 4

    if bullet_j2_state == "fire":
        fire_bullet(bullet_j2_x, bullet_j2_y)
        if old_dir_j2 == "right":
            bullet_j2_x += 4
        elif old_dir_j2 == "left":
            bullet_j2_x -= 4
        elif old_dir_j2 == "up":
            bullet_j2_y -= 4
        else:
            bullet_j2_y += 4
        
    ## Collision
    ## Reset bullet data
    if bullet_j1_y <= 0 or bullet_j1_y >= 600:
        print("reset 1")
        bullet_j1_x = bullet_dir_x(dir_j1)
        bullet_j1_y = bullet_dir_y(dir_j1)
        bullet_j1_state = "ready"

    if bullet_j1_x <= 0 or bullet_j1_x >= 600:
        print("reset")
        bullet_j1_x = bullet_dir_x(dir_j1)
        bullet_j1_y = bullet_dir_y(dir_j1)
        bullet_j1_state = "ready"
      
    show_score(textX, testY,score_value_j1)
    # show_score(textX, testY,score_value_j2)
    pygame.display.update() 