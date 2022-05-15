from inspect import isawaitable
import pygame
from network import Network
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)


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



def isWall(x, y):
    for wall in walls:
        res = False
        if (wall[0] <= x <= (wall[0] + dim_cube)) and (wall[1] <= y <= (wall[1] + (wall[2] * dim_cube))):
            res = True
            break
        elif (big_wall[0] <= x <= (big_wall[0] + (big_wall[1] * dim_cube))) and (big_wall[2] <= y <= (big_wall[2] + (big_wall[3] * dim_cube))):
            res = True
            break
        elif (1 <= x <= 599) == False or (1 <= y <= 799) == False :
            res = True
            break
        else:
            continue
    return res

class Player():
    width = height = 33
    def __init__(self, startx, starty, dir, img):
        self.x = startx
        self.y = starty
        self.velocity = 1.8
        self.dir = dir
        self.olddir = dir
        self.img = img

        self.bullet_x = 0
        self.bullet_y = 0
        self.bullet_y_old = 0
        self.bullet_x_old = 0
        self.bullet_state = "ready"
        

    def draw(self, g):
        if self.dir == "left":
            g.blit(pygame.transform.rotate(self.img, 180), (self.x, self.y))
        elif self.dir == "down":
            g.blit(pygame.transform.rotate(self.img, 270), (self.x, self.y))
        elif self.dir == "up":
            g.blit(pygame.transform.rotate(self.img, 90), (self.x, self.y))
        elif self.dir == "right":
            g.blit(pygame.transform.rotate(self.img, 0), (self.x, self.y))
        

    def update_bullet_position(self):
        if self.dir == "left":
            self.bullet_x = self.x - 3
            self.bullet_y = self.y + 14.5
        elif self.dir == "right":
            self.bullet_x = self.x + 35
            self.bullet_y = self.y + 14.5
        elif self.dir == "up":
            self.bullet_x = self.x +14.5
            self.bullet_y = self.y -3
        else:
            self.bullet_x = self.x + 14.5
            self.bullet_y = self.y +35
            

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
            self.olddir = self.dir
            self.dir = "right"
            self.bullet_x = self.x + 35
            self.bullet_y = self.y + 14.5

        elif dirn == 1:
            self.x -= self.velocity
            self.olddir = self.dir
            self.dir =  "left"
            self.bullet_x = self.x - 3
            self.bullet_y = self.y + 14.5
        elif dirn == 2:
            self.y -= self.velocity
            self.olddir = self.dir
            self.dir = "up"
            self.bullet_x = self.x +14.5
            self.bullet_y = self.y -3
        else:
            self.y += self.velocity
            self.olddir = self.dir
            self.dir = "down"
            self.bullet_x = self.x + 14.5
            self.bullet_y = self.y +35

    def shootBullet(self, x, y, g):
        print("dot")
        pygame.draw.circle(g, RED, (x, y), 3, 10)
        
    def bullet(self,g):
        while self.bullet_state == "fire":
            if isWall(self.bullet_x, self.bullet_y) == False:
                self.shootBullet(self.bullet_x_old, self.bullet_y_old, g)
                if self.olddir == "left":
                    self.bullet_x -= self.velocity
                elif self.olddir == "right":
                    self.bullet_x += self.velocity
                elif self.olddir == "up":
                    self.bullet_y -= self.velocity
                else:
                    self.bullet_y += self.velocity
                print(self.bullet_x, self.bullet_y)
            else:
                print(self.bullet_x, self.bullet_y)
                print("wall here!")
                self.bullet_state = "ready"
                self.update_bullet_position()
                print(self.bullet_x, self.bullet_y)
                break
            print(self.bullet_state)
            
        
        
class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(291, 568, "right", pygame.image.load("j1_tank.png"))
        self.player2 = Player(400,180, "up", pygame.image.load("j2_tank.png"))
        
        self.canvas = Canvas(self.width, self.height, "Tanky Tank")
        self.background = pygame.image.load('map.png')

    

    def run(self):
        clock = pygame.time.Clock()
        run = True
        g = self.canvas.get_canvas()
        start_ticks = pygame.time.get_ticks()  # starter tick
        while run:
            clock.tick(60)
            # arrondir au dixieme près
            seconds = (pygame.time.get_ticks()-start_ticks) / \
                1000  # calculate how many seconds


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_RIGHT] and self.player.x <= self.width - 35:
                if isWall(self.player.x + 33, self.player.y):
                    continue
                else:
                    self.player.move(0)

            if keys[pygame.K_LEFT] and self.player.x > 1:
                if isWall(self.player.x, self.player.y):
                    continue
                else:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y > 1:
                    if isWall(self.player.x, self.player.y):
                        continue
                    else:
                        self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y < self.height - 35:
                    if isWall(self.player.x, self.player.y + 33):
                        continue
                    else:
                        self.player.move(3)

            if keys[pygame.K_SPACE]:
                if self.player.bullet_state == "ready":
                    self.player.bullet_state = "fire"
                    # bulletSound = mixer.Sound("one_shot_sound.wav")
                    # bulletSound.play()
                    # self.player.shootBullet(self.player.bullet_x, self.player.bullet_y, g)
                

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(g)
            self.player2.draw(g)

            self.player.bullet(g)
            self.player.bullet_x_old = self.player.bullet_x
            self.player.bullet_y_old = self.player.bullet_y

            self.canvas.update()
            
        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + "," + str(self.player.dir)
        reply = self.net.send(data)
        return reply
        

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), int(d[2])
        except:
            return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)
        background_image = pygame.image.load('map.png')
        self.screen.blit(background_image, (0, 0))
        pygame.display.flip()
        
        
        # # show those walls
        # for wall in walls:
        #     pygame.draw.rect(background_image, BLUE, (wall[0], wall[1], dim_cube+1, (dim_cube * wall[2])))
        #     pygame.draw.rect(background_image, RED, (big_wall[0], big_wall[2], (dim_cube * big_wall[1]), (dim_cube * big_wall[3])))



    @staticmethod
    def update():
        time.sleep(0.008)
        pygame.display.update()

    # def draw_text(self, text, size, x, y):
    #     pygame.font.init()
    #     font = pygame.font.SysFont("comicsans", size)
    #     render = font.render(text, 1, (0,0,0))

    #     self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        background_image = pygame.image.load('map.png')
        self.screen.blit(background_image, (0, 0))
        pygame.display.flip()
        # self.screen.fill((255,255,255))

    
