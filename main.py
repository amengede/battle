#time for Battle 2

import pygame

#sample rate, bit depth, channels (left,right), buffer size
# PyOpenAl
pygame.mixer.pre_init(44100,16,2,512)
pygame.init()

screenSize = (600,400)

GROUND = (20,128,0)
SKY = (64,64,255)
STONE = (64,64,64)

SCREEN = pygame.display.set_mode(screenSize)
MUSIC = pygame.mixer.Sound('sounds/music.wav')
groundRect = pygame.Rect(0,350,600,50)
skyRect = pygame.Rect(0,0,600,350)

#classes
class Base:
    def __init__(self,side):
        #side: 0: friend, 1: enemy
        if side==0:
            self.x = 0
        else:
            self.x = 500
        self.width = 200
        self.height = 150
        self.rect = pygame.Rect(self.x,225,self.width,self.height)

    def update(self):
        self.rect_onscreen = self.rect.move(-game_view_x,0)
    
    def draw(self):
        pygame.draw.rect(SCREEN,STONE,self.rect_onscreen)

running = True
game_view_x = 0
bases = [Base(0),Base(1)]
#MUSIC.play(-1)
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game_view_x = max(game_view_x-2,0)
    if keys[pygame.K_RIGHT]:
        game_view_x = min(game_view_x+2,2000-600)
    
    #update
    for b in bases:
        b.update()


    #draw
    pygame.draw.rect(SCREEN,GROUND,groundRect)
    pygame.draw.rect(SCREEN,SKY,skyRect)
    for b in bases:
        b.draw()
    pygame.display.update()
pygame.quit()