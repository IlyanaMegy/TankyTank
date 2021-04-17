import sys, pygame
from pygame.locals import*

pygame.init()

WIDTH = 900
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Tanky Tanks')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

win.fill(BLACK)
pygame.display.flip()

#init values
x1 = 200
y1 = 200

width = 20
height = 20

vel = 3
run = True
  
# infinite loop 
while run:
    pygame.time.delay(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # stores keys pressed 
    keys = pygame.key.get_pressed()
      
    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and x1>0:
          
        # decrement in x co-ordinate
        x1 -= vel
          
    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and x1<900-width:
          
        # increment in x co-ordinate
        x1 += vel
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and y1>0:
          
        # decrement in y co-ordinate
        y1 -= vel
          
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and y1<600-height:
        # increment in y co-ordinate
        y1 += vel
         
              
    # completely fill the surface object  
    # with black colour  
    win.fill((0, 0, 0))
      
    # drawing object on win which is rectangle here 
    j1 = pygame.draw.rect(win, (255, 0, 0), (x1, y1, width, height))
    j2 = pygame.draw.rect(win, (255, 0, 0), (100, 100, 40, 40))
      

    x3 = x1 + (width/2)
    y3 = y1 + (height/2)

    pygame.draw.line(win, BLUE, (120, 120), (x3, y3), width=3)
    
    # it refreshes the window
    pygame.display.update() 
  
# closes the pygame window 
pygame.quit()