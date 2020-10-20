import pygame
import math
import random

pygame.mixer.pre_init(44100, 16, 2, 512)
pygame.init()

screenSize = (600,400)
SCREEN = pygame.display.set_mode(screenSize)

GROUND = (20,128,0)
SKY = (64,64,255)
STONE = (64,64,64)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

FONT = pygame.font.Font('freesansbold.ttf', 24)

MUSIC = pygame.mixer.Sound('sounds/music.wav')

class Base:
    def __init__(self,side):
        self.side = side
        if side==0:
            self.x = 0
            self.owner = "my"
            self.text_rect = pygame.Rect(16,100,200,64)
        else:
            self.x = 2800
            self.owner = "enemy"
            self.text_rect = pygame.Rect(384,100,200,64)
        
        self.width = 200
        self.height = 150
        self.health = 3000
        self.rect = pygame.Rect(self.x,225,self.width,self.height)
    
    def update(self):
        self.rect_onscreen = self.rect.move(-game_view_x,0)
    
    def draw(self):
        pygame.draw.rect(SCREEN,STONE,self.rect_onscreen)
        text = FONT.render(f"{self.owner} Base: {self.health}", True, BLACK)
        SCREEN.blit(text,self.text_rect)

class Soldier:
    def __init__(self,side):
        self.side = side
        self.health = 50
        self.max_health = 50
        self.damage = random.randint(8,16)

        self.body = pygame.image.load('images/soldier_body.png').convert()
        if side==1:
            self.body = pygame.transform.flip(self.body,True,False)
        self.body.set_colorkey(WHITE,pygame.RLEACCEL)
        self.body_rect = self.body.get_rect()

        self.club = pygame.image.load("images/soldier_club2.png").convert()
        self.club.set_colorkey(WHITE,pygame.RLEACCEL)
        self.club_rect = self.club.get_rect()

        self.message = None

        self.state = "walking"
        self.swung = False

        self.clubAngle = 0

        if side==0:
            self.x = 217
        else:
            self.x = 2750
        
        self.y = 300
    
    def enemy_within(self,distance):
        """Pick an enemy within the given distance"""
        for s in soldiers:
            if s.side != self.side:
                if abs(s.x - self.x)<=distance:
                    return s
        for b in bases:
            if b.side != self.side:
                if abs(b.x - self.x)<=distance:
                    return b
        return None

    def update(self):
        #check health
        if self.health <= 0:
            self.destroy()

        #state based behaviour
        if self.state=="walking":
            #self.x += 1*(1-2*self.side)
            if self.side == 0:
                self.x += 1
            else:
                self.x -= 1
            if self.enemy_within(64) != None:
                self.state = "attack"

        elif self.state=="attack":
            self.clubAngle += 0.2
            if self.clubAngle > 135:
                self.state = "swinging"

        elif self.state=="swinging":
            self.clubAngle -= 0.4
            if self.clubAngle <= 0 and not self.swung:
                #test for hit
                enemy = self.enemy_within(64)
                if enemy != None:
                    enemy.health -= self.damage
                self.swung = True
            
            if self.clubAngle < -45:
                if self.enemy_within(64) != None:
                    self.state = "attack"
                else:
                    self.state = "walking"
                self.swung = False
        
        if self.message != None:
            #print(self.message)
            self.message = None

        #transform images
        self.body_onscreen = self.body_rect.move(self.x - game_view_x,self.y)

        self.club_spun = pygame.transform.rotate(self.club,self.clubAngle)
        club_center = (-16,0)
        if self.side==1:
            self.club_spun = pygame.transform.flip(self.club_spun,True,False)
        self.club_spun_rect = self.club_spun.get_rect(center = club_center)
        self.club_onscreen = self.club_spun_rect.move(self.x + 34 - game_view_x,self.y+40)
    
    def draw(self):
        SCREEN.blit(self.body,self.body_onscreen)
        SCREEN.blit(self.club_spun,self.club_onscreen)
        #pillow
        #health bar
        pygame.draw.rect(SCREEN,RED,(self.x - 16 - game_view_x,self.y + 16,32,4))
        pygame.draw.rect(SCREEN,GREEN,(int(self.x - 16 - game_view_x),int(self.y + 16),int(32*self.health/self.max_health),4))

    def destroy(self):
        soldiers.pop(soldiers.index(self))

############################# Create ##########################################
game_view_x = 0
groundRect = pygame.Rect(0,350,600,50)
skyRect = pygame.Rect(0,0,600,350)

bases = [Base(0),Base(1)]

soldiers = [Soldier(0),Soldier(1)]

#MUSIC.play(-1)

############################# Game Loop #######################################
running = True
while running:

    ############################# Input #######################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #print("LEFT")
        game_view_x = max(game_view_x-2,0)
    elif keys[pygame.K_RIGHT]:
        #print("RIGHT")
        game_view_x = min(game_view_x+2,2400)
    ############################# Update ######################################
    for b in bases:
        b.update()
    
    for s in soldiers:
        s.update()
    ############################# Draw ########################################
    pygame.draw.rect(SCREEN,GROUND,groundRect)
    pygame.draw.rect(SCREEN,SKY,skyRect)

    for b in bases:
        b.draw()

    for s in soldiers:
        s.draw()

    pygame.display.update()
    


pygame.quit()