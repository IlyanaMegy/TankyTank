from pygame import mixer
import pygame
from pygame.time import delay
import os
score_file = open("score.txt", 'at')

x = 450
y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

win = pygame.display.set_mode((600, 450))
pygame.display.set_caption('Tanky Tanks')
icon = pygame.image.load('j1_tank.png')
pygame.display.set_icon(icon)


# Background
background = pygame.image.load('map.png')
margin_x = 0
margin_y = 0

# Font
font = pygame.font.Font("8-Bit-Madness.ttf", 50)
font_sub = pygame.font.Font("8-Bit-Madness.ttf", 35)
font_text = pygame.font.Font("8-Bit-Madness.ttf", 24)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Walls
dim_cube = 46

# soit l'origine en haut à gauche de l'image --> rajouter le margin de l'image après
walls = [[48, 50, 2], [139, 5, 2], [277, 96, 1], [322, 5, 3], [413, 50, 4], [459, 95, 1], [504, 50, 2], [139, 141, 2], [3, 187, 2],
         [48, 232, 2], [277, 187, 1], [231, 232, 6], [
             460, 187, 3], [505, 187, 1],
         [139, 278, 5], [184, 278, 2], [413, 323, 1], [504, 278, 4], [
             3, 368, 1], [48, 368, 5], [413, 413, 1], [458, 413, 1],
         [139, 551, 1], [413, 506, 2], [504, 506, 2], [458, 551, 1]]
big_wall = [277, 2, 278, 5]

mainClock = pygame.time.Clock()
# show those walls
# for wall in walls:
#     somewall = pygame.draw.rect(background, BLUE, (wall[0], wall[1], dim_cube+1, (dim_cube * wall[2])))
#     bigwall = pygame.draw.rect(background, RED, (big_wall[0], big_wall[2], (dim_cube * big_wall[1]), (dim_cube * big_wall[3])))

pygame.display.flip()
click = False


def main_menu():

    click = False
    win = pygame.display.set_mode((600, 450))
    while True:

        win.fill(BLACK)
        draw_text('TANKY TANK', font, RED, win, 180, 40)

        mx, my = pygame.mouse.get_pos()
        startGame_button = pygame.Rect(183, 155, 220, 45)
        score_button = pygame.Rect(183, 305, 220, 45)

        pygame.draw.rect(win, RED, [180, 150, 225, 3])
        pygame.draw.rect(win, RED, [180, 200, 225, 3])
        pygame.draw.rect(win, RED, [180, 150, 3, 50])
        pygame.draw.rect(win, RED, [405, 150, 3, 53])

        pygame.draw.rect(win, RED, [180, 300, 225, 3])
        pygame.draw.rect(win, RED, [180, 350, 225, 3])
        pygame.draw.rect(win, RED, [180, 300, 3, 50])
        pygame.draw.rect(win, RED, [405, 300, 3, 53])

        if startGame_button.collidepoint((mx, my)):
            if click:
                game()
        if score_button.collidepoint((mx, my)):
            if click:
                options()

        startGame = font_sub.render('START GAME', True, WHITE)
        scorePage = font_sub.render('VIEW SCORE', True, WHITE)
        pygame.draw.rect(win, BLACK, startGame_button)
        pygame.draw.rect(win, BLACK, score_button)
        win.blit(startGame, (210, 165))
        win.blit(scorePage, (210, 315))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def game():
    score_file = open("score.txt", 'at')
    win = pygame.display.set_mode((800, 600))
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
    old_bullet_j1_x = j1_x
    old_bullet_j1_y = j1_y
    bullet_j1_state = "ready"

    bullet_j2_x = j2_x + dim_tank
    bullet_j2_y = j2_y + (dim_tank/2)
    old_bullet_j2_x = j2_x
    old_bullet_j2_y = j2_y
    bullet_j2_state = "ready"

    # Score
    score_value_j1 = 0
    score_value_j2 = 0
    font = pygame.font.Font('8-Bit-Madness.ttf', 32)
    score_x = 650
    score_j1_y = 40
    score_j2_y = 90

    def fire_bullet_j1(x, y):
        pygame.draw.circle(win, YELLOW, (x, y), 3, 10)

    def fire_bullet_j2(x, y):
        pygame.draw.circle(win, GREEN, (x, y), 3, 10)

    def bullet_dir_x(dir, j_x):
        if dir == "left":
            x = j_x
        elif dir == "down":
            x = j_x + (dim_tank/2)
        elif dir == "up":
            x = j_x + (dim_tank/2)
        else:
            x = j_x + dim_tank
        return x

    def bullet_dir_y(dir, j_y):
        if dir == "left":
            y = j_y + (dim_tank/2)
        elif dir == "down":
            y = j_y + dim_tank
        elif dir == "up":
            y = j_y
        else:
            y = j_y + (dim_tank/2)
        return y

    def player(x, y, dir, img):
        if dir == "left":
            win.blit(pygame.transform.rotate(img, 180), (x, y))
        elif dir == "down":
            win.blit(pygame.transform.rotate(img, 270), (x, y))
        elif dir == "up":
            win.blit(pygame.transform.rotate(img, 90), (x, y))
        elif dir == "right":
            win.blit(pygame.transform.rotate(img, 0), (x, y))

    def clear_score():
        score_file.truncate()

    def show_score(x, y, score_value):
        score = font.render("Score : " + str(score_value),
                            True, (255, 255, 255))
        win.blit(score, (x, y))

    def isWall(x, y):
        for wall in walls:
            res = False
            if (wall[0] <= x <= (wall[0] + dim_cube)) and (wall[1] <= y <= (wall[1] + (wall[2] * dim_cube))):
                res = True
                break
            elif (big_wall[0] <= x <= (big_wall[0] + (big_wall[1] * dim_cube))) and (big_wall[2] <= y <= (big_wall[2] + (big_wall[3] * dim_cube))):
                res = True
                break
            else:
                continue
        return res

    def touchedEnemy(bullet_x, bullet_y, enemy_x, enemy_y):
        res = False
        if (enemy_x <= bullet_x <= enemy_x + 33) and (enemy_y <= bullet_y <= enemy_y + 33):
            print(enemy_x, "<=", bullet_x, "<=", (enemy_x + 33))
            print((enemy_y, "<=", bullet_y, "<=", (enemy_y + 33)))
            res = True
        return res
    start_ticks = pygame.time.get_ticks()  # starter tick
    # infinite loop
    while run:
        # arrondir au dixieme près
        seconds = (pygame.time.get_ticks()-start_ticks) / \
            1000  # calculate how many seconds

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
        # stores keys pressed
        keys = pygame.key.get_pressed()

        #################################################################################################################################
        #################################################           PLAYER 1            #################################################
        #################################################################################################################################
        # if left arrow key is pressed
        if keys[pygame.K_LEFT] and j1_x > 0:
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
                player(j1_x, j1_y, dir_j1, j1_img)

        # if left arrow key is pressed
        if keys[pygame.K_RIGHT] and j1_x < 600-dim_tank:
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
                player(j1_x, j1_y, dir_j1, j1_img)

        # if left arrow key is pressed
        if keys[pygame.K_UP] and j1_y > 0:
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
        if keys[pygame.K_DOWN] and j1_y < 600-dim_tank:
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
                fire_bullet_j1(bullet_j1_x, bullet_j1_y)
                old_dir_j1 = dir_j1
                old_bullet_j1_x = bullet_j1_x
                old_bullet_j1_y = bullet_j1_y

        #################################################################################################################################
        #################################################           PLAYER 2            #################################################
        #################################################################################################################################

        # if left arrow key is pressed
        if keys[pygame.K_q] and j2_x > 0:
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
                player(j2_x, j2_y, dir_j2, j2_img)

        # if left arrow key is pressed
        if keys[pygame.K_d] and j2_x < 600-dim_tank:
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
                player(j2_x, j2_y, dir_j2, j2_img)

        # if left arrow key is pressed
        if keys[pygame.K_z] and j2_y > 0:
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

        if keys[pygame.K_s] and j2_y < 600-dim_tank:
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
            if bullet_j2_state == "ready":  # try to remove that condition later
                bulletSound = mixer.Sound("one_shot_sound.wav")
                bulletSound.play()
                bullet_j2_state = "fire"
                fire_bullet_j2(bullet_j2_x, bullet_j2_y)
                old_dir_j2 = dir_j2
                old_bullet_j2_x = bullet_j2_x
                old_bullet_j2_y = bullet_j2_y

        ##################################################################################################################################

        win.fill((0, 0, 0))
        win.blit(background, (margin_x, margin_y))
        # update tank location
        player(j1_x, j1_y, dir_j1, j1_img)
        player(j2_x, j2_y, dir_j2, j2_img)

        # update bullet location
        bullet_j1_x = bullet_dir_x(dir_j1, j1_x)
        bullet_j1_y = bullet_dir_y(dir_j1, j1_y)
        bullet_j2_x = bullet_dir_x(dir_j2, j2_x)
        bullet_j2_y = bullet_dir_y(dir_j2, j2_y)

        if touchedEnemy(old_bullet_j1_x, old_bullet_j1_y, j2_x, j2_y):
            score_value_j1 += 1
            bullet_j1_state = "ready"

        if touchedEnemy(old_bullet_j2_x, old_bullet_j2_y, j1_x, j1_y):
            bullet_j2_state = "ready"
            score_value_j2 += 1

        if old_bullet_j1_y <= 0 or old_bullet_j1_y >= 600:
            bullet_j1_state = "ready"

        if old_bullet_j1_x <= 0 or old_bullet_j1_x >= 600:
            bullet_j1_state = "ready"

        if isWall(old_bullet_j1_x, old_bullet_j1_y):
            bullet_j1_state = "ready"

        if bullet_j1_state == "ready":
            old_bullet_j1_x = bullet_j1_x
            old_bullet_j1_y = bullet_j1_y

        if bullet_j2_state == "ready":
            old_bullet_j2_x = bullet_j2_x
            old_bullet_j2_y = bullet_j2_y

        if bullet_j1_state == "fire":
            fire_bullet_j1(old_bullet_j1_x, old_bullet_j1_y)
            if old_dir_j1 == "right":
                old_bullet_j1_x += 4
            elif old_dir_j1 == "left":
                old_bullet_j1_x -= 4
            elif old_dir_j1 == "up":
                old_bullet_j1_y -= 4
            else:
                old_bullet_j1_y += 4

        if old_bullet_j2_y <= 0 or old_bullet_j2_y >= 600:
            bullet_j2_state = "ready"

        if old_bullet_j2_x <= 0 or old_bullet_j2_x >= 600:
            bullet_j2_state = "ready"

        if isWall(old_bullet_j2_x, old_bullet_j2_y):
            bullet_j2_state = "ready"

        if bullet_j2_state == "fire":
            fire_bullet_j2(old_bullet_j2_x, old_bullet_j2_y)
            if old_dir_j2 == "right":
                old_bullet_j2_x += 4
            elif old_dir_j2 == "left":
                old_bullet_j2_x -= 4
            elif old_dir_j2 == "up":
                old_bullet_j2_y -= 4
            else:
                old_bullet_j2_y += 4

        win.blit(j1_img, (605, 35))
        show_score(score_x, score_j1_y, score_value_j1)
        win.blit(j2_img, (605, 85))
        show_score(score_x, score_j2_y, score_value_j2)

        print(score_value_j1)
        print(score_value_j2)

        if score_value_j1 == 3 or score_value_j2 == 3:
            score_file.write(str(score_value_j1))
            score_file.write(str("             "))
            score_file.write(str(score_value_j2))
            score_file.write(str("             "))
            score_file.write(str(seconds))
            score_file.write(str('\n'))
            # retour a la ligne
            score_file.close()
            end_game()

        pygame.display.update()


def options():
    # voir score
    # reinitialiser score
    click = False
    run = True
    while run:
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        return_button = pygame.Rect(20, 20, 220, 45)

        clear_score = pygame.Rect(183, 155, 220, 45)

        pygame.draw.rect(win, RED, [50, 100, 500, 3])
        pygame.draw.rect(win, RED, [50, 350, 500, 3])
        pygame.draw.rect(win, RED, [50, 100, 3, 250])
        pygame.draw.rect(win, RED, [550, 100, 3, 253])

        pygame.draw.rect(win, RED, [400, 380, 150, 3])
        pygame.draw.rect(win, RED, [400, 420, 150, 3])
        pygame.draw.rect(win, RED, [400, 380, 3, 40])
        pygame.draw.rect(win, RED, [550, 380, 3, 43])

        if clear_score.collidepoint((mx, my)):
            if click:
                continue

        if return_button.collidepoint((mx, my)):
            if click:
                main_menu()

        return_mp = font_text.render('< Return main page', True, WHITE)
        clearScore = font_sub.render('CLEAR', True, WHITE)
        pygame.draw.rect(win, BLACK, clear_score)
        pygame.draw.rect(win, BLACK, return_button)

        draw_text('score', font_sub, RED, win, 250, 110)

        score_file = open("score.txt", 'rt')
        score = score_file.read()
        draw_text(score, font_text, WHITE, win, 180, 150)
        print(score)

        win.blit(return_mp, (20, 20))
        win.blit(clearScore, (430, 390))

        pygame.display.update()
        mainClock.tick(60)


def end_game():
    click = False
    win = pygame.display.set_mode((600, 450))
    while True:

        win.fill(BLACK)
        draw_text('GAME OVER', font, RED, win, 180, 40)
        draw_text('score', font_sub, RED, win, 200, 100)

        score_file = open("score.txt", 'rt')
        score = score_file.read()
        draw_text(score, font_text, WHITE, win, 180, 150)

        mx, my = pygame.mouse.get_pos()
        newGame_button = pygame.Rect(153, 383, 97, 37)
        mainPage_button = pygame.Rect(353, 383, 97, 37)

        pygame.draw.rect(win, RED, [150, 380, 100, 3])
        pygame.draw.rect(win, RED, [150, 420, 100, 3])
        pygame.draw.rect(win, RED, [150, 380, 3, 40])
        pygame.draw.rect(win, RED, [250, 380, 3, 43])

        pygame.draw.rect(win, RED, [350, 380, 100, 3])
        pygame.draw.rect(win, RED, [350, 420, 100, 3])
        pygame.draw.rect(win, RED, [350, 380, 3, 40])
        pygame.draw.rect(win, RED, [450, 380, 3, 43])

        if newGame_button.collidepoint((mx, my)):
            if click:
                game()
        if mainPage_button.collidepoint((mx, my)):
            if click:
                main_menu()

        newGame = font_text.render('NEW GAME', True, WHITE)
        mainPage = font_text.render('MAIN PAGE', True, WHITE)
        pygame.draw.rect(win, BLACK, newGame_button)
        pygame.draw.rect(win, BLACK, mainPage_button)
        win.blit(newGame, (155, 390))
        win.blit(mainPage, (353, 390))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


main_menu()
