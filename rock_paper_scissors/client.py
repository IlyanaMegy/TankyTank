import pygame
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.width = 150
        self.height = 100

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (250,250,250))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
        
        win.blit(pygame.image.load(r'feuille.jpg'), (470, 500))
        win.blit(pygame.image.load(r'ciseaux.jpg'), (270, 500))
        win.blit(pygame.image.load(r'pierre.jpg'), (70, 500))
        

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((0,0,0))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("En attente d'un autre joueur...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Ton tour", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Adversaire", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (250,250,250))
            text2 = font.render(move2, 1, (250,250,250))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (250,250,250))
            elif game.p1Went:
                text1 = font.render("Bloqué", 1, (250,250,250))
            else:
                text1 = font.render("...", 1, (250,250,250))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (250,250,250))
            elif game.p2Went:
                text2 = font.render("Bloqué", 1, (250,250,250))
            else:
                text2 = font.render("...", 1, (250,250,250))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 60, 500), Button("Scissors", 260, 500), Button("Paper", 460, 500)]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Tu ne peux pas jouer...")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Tu ne peux pas jouer...")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Gagné!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Match Nul!", 1, (255,0,0))
            else:
                text = font.render("Perdu...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0,0,0))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Clique pour jouer!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
