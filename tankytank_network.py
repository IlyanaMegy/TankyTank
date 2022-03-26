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
    


    def __init__(self, startx, starty, color, dir, img):
        self.x = startx
        self.y = starty
        self.velocity = 1.8
        # self.color = color
        self.dir = dir
        self.olddir = dir
        self.img = img

    def draw(self, g):
        # pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height))
        # pygame.draw.rect(g, WHITE, (self.x+15,self.y, 3, 15))

        g.blit(self.img, (self.x, self.y))
        
    def rotate(self, g):        
        if self.olddir != "left" and self.dir == "left":
            print("turn left!")
            pygame.transform.rotate(self.img, 180)
        elif self.olddir != "down" and self.dir == "down":
            print("turn down!")
            pygame.transform.rotate(self.img, 270)
        elif self.olddir != "up" and self.dir == "up":
            print("turn up!")
            pygame.transform.rotate(g, 90)   
        elif self.olddir != "right" and self.dir == "right":
            print("turn right!")
            pygame.transform.rotate(g, 0)

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
        

    

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(291, 568, (255,0,0), "right", pygame.image.load("j1_tank.png"))
        self.player2 = Player(400,180, (0,255,0), "top", pygame.image.load("j2_tank.png"))
        self.canvas = Canvas(self.width, self.height, "Tanky Tank")
        self.background = pygame.image.load('map.png')

    

    def run(self):
        clock = pygame.time.Clock()
        run = True
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

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player.rotate(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.player2.rotate(self.canvas.get_canvas())
            self.canvas.update()

            print(self.player.olddir, " to " ,self.player.dir)

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
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

    
