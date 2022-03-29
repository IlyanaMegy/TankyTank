from inspect import isawaitable
import pygame
from network import Network

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
        

    def draw(self, g):
        if self.dir == "left":
            g.blit(pygame.transform.rotate(self.img, 180), (self.x, self.y))
        elif self.dir == "down":
            g.blit(pygame.transform.rotate(self.img, 270), (self.x, self.y))
        elif self.dir == "up":
            g.blit(pygame.transform.rotate(self.img, 90), (self.x, self.y))
        elif self.dir == "right":
            g.blit(pygame.transform.rotate(self.img, 0), (self.x, self.y))
        

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
            self.olddir = self.dir
            self.dir = "right"

        elif dirn == 1:
            self.x -= self.velocity
            self.olddir = self.dir
            self.dir =  "left"
        elif dirn == 2:
            self.y -= self.velocity
            self.olddir = self.dir
            self.dir = "up"
        else:
            self.y += self.velocity
            self.olddir = self.dir
            self.dir = "down"

    def bullet(self, g):
        print("fire !")
        if self.dir == "left":
            pygame.draw.circle(g, RED, (self.x - 3, self.y + 14.5), 3, 10)
        
        elif self.dir =="right":
            pygame.draw.circle(g, YELLOW, (self.x + 35, self.y + 14.5), 3, 10)

        elif self.dir == "up" :
            pygame.draw.circle(g, RED, (self.x +14.5, self.y -3), 3, 10)
        else:
            pygame.draw.circle(g, YELLOW, (self.x + 14.5, self.y +35), 3, 10)
        

        

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
        bullet_state = "ready"
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] and self.player.x <= self.width - self.player.velocity:
                if isWall(self.player.x + 33, self.player.y):
                    continue
                else:
                    self.player.move(0)

            if keys[pygame.K_LEFT] and self.player.x >= self.player.velocity:
                if isWall(self.player.x, self.player.y):
                    continue
                else:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    if isWall(self.player.x, self.player.y):
                        continue
                    else:
                        self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    if isWall(self.player.x, self.player.y + 33):
                        continue
                    else:
                        self.player.move(3)

            if keys[pygame.K_SPACE]:
                bullet_state = "fire"
                

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(g)
            self.player2.draw(g)

            if bullet_state == "fire":
                self.player.bullet(g)

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

    
