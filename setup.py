import pygame
import random
import math

def getxy(rc,size):
    x = size[0]/2 + (rc[1]-1) * size[0]
    y = size[1]/2 + (rc[0]-1) * size[1]
    return (x,y)

# super class -> BulletClass
# all the bullet should be inherit from this class
class BulletClass(pygame.sprite.Sprite):
    def __init__(self, init_rc, size, direc, color, speed):
        pygame.sprite.Sprite.__init__(self)
        # Size
        self.size = size
        # row col
        self.r, self.c = init_rc
        # direction
        self.direc = direc
        # create size surface
        self.image = pygame.Surface((self.size[0]/2,self.size[1]/2))
        # fill color
        self.image.fill(color)
        # get rect and set position
        self.rect = self.image.get_rect()
        self.rect.center = getxy((self.r, self.c),self.size)
        # moving speed
        self.speed = speed
    def update(self):
        # # direc is a tuple NSWE
        # # (-1,0) is W
        # # (1,0) is E
        # # (0,-1) is N
        # # (0,1) is S
        # self.c += self.speed * self.direc[0]
        # self.r += self.speed * self.direc[1]
        # self.rect.center = getxy((self.r, self.c),self.size)
        pass


class Bullet(BulletClass):
    def __init__(self, init_rc, size, direc):
        #self.B_image = pygame.image.load("resources/REIMU_RED.png")
        super().__init__(init_rc,size,direc,(0,100,100),3)
    def update(self):
        # direc is a tuple NSWE
        # (-1,0) is W
        # (1,0) is E
        # (0,-1) is N
        # (0,1) is S
        self.c += self.speed * self.direc[0]
        self.r += self.speed * self.direc[1]
        self.rect.center = getxy((self.r, self.c),self.size)

class head(pygame.sprite.Sprite):
    def __init__(self, init_rc, speed, startl, size):
        pygame.sprite.Sprite.__init__(self)
        
        # Row -> Y
        # Col -> X
        self.size = size
        self.r, self.c = init_rc
        self.speed = speed
        self.life = startl
        self.image = pygame.Surface(self.size)
        self.image.fill((255,0,0))
        self.reset()
        self.rect = self.image.get_rect()
        self.rect.center = getxy((self.r, self.c),self.size)
        self.charge = 3 # init charge
    def shoot(self):
        # create bullet, add bullet to the group
        bullet = Bullet((self.r,self.c),self.size,self.direc)
        self.bullets.add(bullet)
    def update(self, direc):
        if self.hit:
            self.direc = direc
            # direc is a tuple NSWE
            # (-1,0) is W
            # (1,0) is E
            # (0,-1) is N
            # (0,1) is S
            self.c += self.speed * self.direc[0]
            self.r += self.speed * self.direc[1]
            self.rect.center = getxy((self.r, self.c),self.size)
            self.hitTimer -= 1
            if self.hitTimer < 0:
                self.reset()
        else:
            self.direc = direc
            # direc is a tuple NSWE
            # (-1,0) is W
            # (1,0) is E
            # (0,-1) is N
            # (0,1) is S
            self.c += self.speed * self.direc[0]
            self.r += self.speed * self.direc[1]
            self.rect.center = getxy((self.r, self.c),self.size)
    # reset is to reset the player to beginning to reset the hitTimer, so that we have a protection time
    def reset(self):
        #self.image = self.image.convert()
        self.hit = False
        # 40 frame -> 2 second
        self.hitTimer = 40
        self.bullets = pygame.sprite.Group()
        self.fire = True
    # start hit timer
    def explode(self):
        # player cannot fire in protection time
        self.hit = True
        self.fire = False

# body
class body(pygame.sprite.Sprite):
    def __init__(self, init_rc,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.rc = init_rc
        try:
            pic = pygame.image.load("gameProject/resources/head.jpg")
            pic = pic.convert()
            transColor = pic.get_at((1, 1))
            pic.set_colorkey(transColor)
            self.image = pygame.transform.scale(pic,(int(size[0])*2,int(size[1])*2))
        except:
            self.image = pygame.Surface(self.size)
            self.image.fill(255,0,0)
        self.rect = self.image.get_rect()
        self.rect.center = getxy(self.rc,self.size)
    def update(self,nextrc):
        self.rc = nextrc
        self.rect.center = getxy(self.rc,self.size)
        

class FoodClass(pygame.sprite.Sprite):
    def __init__(self, init_rc, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        #self.image = pygame.image.load("Labs/resources/food.png")
        self.rc = init_rc #row & column
        try:
            pic = pygame.image.load("gameProject/resources/apple.png")
            pic = pic.convert()
            transColor = pic.get_at((1, 1))
            pic.set_colorkey(transColor)
            self.image = pygame.transform.scale(pic,(int(size[0])*2,int(size[1])*2))
        except:
            self.image = pygame.Surface(self.size)
            self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = getxy(self.rc,self.size)

class food(FoodClass): # type normal only add 1 health and 1 body length no other effect
    def __init__(self, init_rc, size):
        super().__init__(init_rc, size, (0,0,255))
        self.charge = random.randint(1,10)


# EnemyClass

class turrent(pygame.sprite.Sprite):  
    def __init__(self, init_rc, size, direc):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("Labs/resources/food.png")
        self.rc = init_rc
        self.size = size
        try:
            pic = pygame.image.load("gameProject/resources/devil.png")
            pic = pic.convert()
            transColor = pic.get_at((1, 1))
            pic.set_colorkey(transColor)
            self.image = pygame.transform.scale(pic,(int(size[0])*2,int(size[1])*2))
        except:
            self.image = pygame.Surface(self.size)
            self.image.fill((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = getxy(self.rc,self.size)
        self.bullets = pygame.sprite.Group()
        self.direc = direc
    def shoot(self):
        bullet = EBullet(self.rc,self.size,self.direc)
        self.bullets.add(bullet)

class EBullet(BulletClass):#EBullet
    def __init__(self, init_rc, size, direc):
        #self.B_image = pygame.image.load("resources/REIMU_RED.png")
        super().__init__(init_rc,size,direc,(0,0,0),1)
    def update(self):
        # direc is a tuple NSWE
        # (-1,0) is W
        # (1,0) is E
        # (0,-1) is N
        # (0,1) is S
        self.c += self.speed * self.direc[0]
        self.r += self.speed * self.direc[1]
        self.rect.center = getxy((self.r, self.c),self.size)

class lturrent(pygame.sprite.Sprite):
    def __init__(self, init_rc, size, direc):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("Labs/resources/food.png")
        self.rc = init_rc
        self.size = size
        try:
            pic = pygame.image.load("gameProject/resources/laser.png")
            pic = pic.convert()
            transColor = pic.get_at((1, 1))
            pic.set_colorkey(transColor)
            self.image = pygame.transform.scale(pic,(int(size[0])*2,int(size[1])*2))
        except:
            self.image = pygame.Surface(self.size)
            self.image.fill((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = getxy(self.rc,self.size)
        self.bullets = pygame.sprite.Group()
        self.direc = direc
    def shoot(self):
        r, c = self.rc
        if self.direc == (0,1):
            while r < 100:
                r += 1
                bullet = EBeamV((r,c),self.size,self.direc,(255,255,0))
                self.bullets.add(bullet)
                
        if self.direc == (0,-1):
            while r > -1:
                r -= 1
                bullet = EBeamV((r,c),self.size,self.direc,(255,255,0))
                self.bullets.add(bullet)
                
        if self.direc == (1,0):
            while c < 100:
                c += 1
                bullet = EBeamH((r,c),self.size,self.direc,(255,255,0))
                self.bullets.add(bullet)
                
        if self.direc == (-1,0):
            while c > -1:
                c -= 1
                bullet = EBeamH((r,c),self.size,self.direc,(255,255,0))
                self.bullets.add(bullet)
                

class EBeamV(BulletClass):
    def __init__(self, init_rc, size, direc, color):
        pygame.sprite.Sprite.__init__(self)
        # Size
        self.size = size
        # row col
        self.r, self.c = init_rc
        # direction
        self.direc = direc
        # create size surface
        self.image = pygame.Surface((self.size[0]/2,self.size[1]))
        # fill color
        self.image.fill(color)
        # get rect and set position
        self.rect = self.image.get_rect()
        self.rect.center = getxy((self.r, self.c),self.size)
class EBeamH(BulletClass):
    def __init__(self, init_rc, size, direc, color):
        pygame.sprite.Sprite.__init__(self)
        # Size
        self.size = size
        # row col
        self.r, self.c = init_rc
        # direction
        self.direc = direc
        # create size surface
        self.image = pygame.Surface((self.size[0],self.size[1]/2))
        # fill color
        self.image.fill(color)
        # get rect and set position
        self.rect = self.image.get_rect()
        self.rect.center = getxy((self.r, self.c),self.size)

class GameBG(pygame.sprite.Sprite): # Game Area
    def __init__(self,W,H):
        pygame.sprite.Sprite.__init__(self)
        imgSize1 = (W, H)
        # tmpImg1 = pygame.Surface(imgSize1)
        # tmpImg1.fill((255,255,255))
        self.image = pygame.image.load("gameProject/resources/back.png")
        self.image = pygame.transform.scale(self.image, imgSize1)
        self.rect = self.image.get_rect()
        self.rect = (0,0)
class BG(pygame.sprite.Sprite): # Scoreboard Area
    def __init__(self,W,H):
        pygame.sprite.Sprite.__init__(self)
        imgSize1 = (W, H)
        self.image = pygame.image.load("gameProject/resources/newback.jpg")
        self.image = pygame.transform.scale(self.image, imgSize1)
        self.rect = self.image.get_rect()
        self.rect = (0,0)

        
class HighScore(pygame.sprite.Sprite):
    def __init__(self,W):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = "High Score:"
        self.x = W
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x+ self.x / 100,20)

class HighScore1(pygame.sprite.Sprite):
    def __init__(self,score,W):
        pygame.sprite.Sprite.__init__(self)
        self.score = score
        self.font = pygame.font.SysFont("None", 30)
        self.text = "Top 1: %d" % (self.score)
        self.x = W
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x+ self.x / 100,40)

class HighScore2(pygame.sprite.Sprite):
    def __init__(self,score,W):
        pygame.sprite.Sprite.__init__(self)
        self.score = score
        self.font = pygame.font.SysFont("None", 30)
        self.text = "Top 2: %d" % (self.score)
        self.x = W
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x+ self.x / 100,60)


class HighScore3(pygame.sprite.Sprite):
    def __init__(self,score,W):
        pygame.sprite.Sprite.__init__(self)
        self.score = score
        self.font = pygame.font.SysFont("None", 30)
        self.text = "Top 3: %d" % (self.score)
        self.x = W
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x+ self.x / 100,80)


class Scoreboard1(pygame.sprite.Sprite):
    def __init__(self,W): # W: input width
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.SysFont("None", 30)
        self.x = W
        
    def update(self):
        self.text = "Score: %d" % (self.score)
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x + self.x/100,100)

class Scoreboard2(pygame.sprite.Sprite):
    def __init__(self,W):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.x = W
        
    def update(self,plife):
        self.text = "Life: %d" % (plife)
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x + self.x/100,120)

class Scoreboard3(pygame.sprite.Sprite):
    def __init__(self,W):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.x = W
        
    def update(self,pcharge):
        self.text = "Charge: %d" % (pcharge)
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x + self.x/100,140)

class InstructionLine(pygame.sprite.Sprite):
    def __init__(self,W,pos,text):
        pygame.sprite.Sprite.__init__(self)
        self.x = W
        self.text = "1.Ueser-friendly game---use keyboard or mouse to control direction /n"
        "2.No time limited---Ten lives at the begining and game over at zero life./n"
        "3.Test your reaction---the number of blue squar eaten can be counted as life & avoid the bullet fired by pink squar turret /n"
        "4.Bomb---press key z to clean enemy turret by shooting?"
    
        self.font = pygame.font.SysFont("None", 26)
        self.text = text
        self.x = W
        self.image = self.font.render(self.text, 1, (102, 204, 255))
        self.rect = self.image.get_rect()
        self.rect = (self.x + self.x/100,pos)
        
class instruction1(InstructionLine): 
    def __init__(self,W):
        self.text = "Keyboard: (mouse by c)"
        super().__init__(W,220,self.text)

class instruction2(InstructionLine): 
    def __init__(self,W):
        self.text = "0 lives = game end"
        super().__init__(W,240,self.text)

class instruction3(InstructionLine):
    def __init__(self,W):
        self.text = "Hitting wall will -1 life"
        super().__init__(W,260,self.text)    
        
class instruction4(InstructionLine):
    def __init__(self,W):
        self.text = "Food +1 life"
        super().__init__(W,280,self.text)

class instruction5(InstructionLine):
    def __init__(self,W):
        self.text = "Shot by z, bomb by x"
        super().__init__(W,300,self.text)

class instruction6(InstructionLine):
    def __init__(self,W):
        self.text = "Mouse: (keyboard by c)"
        super().__init__(W,320,self.text)

class instruction7(InstructionLine):
    def __init__(self,W):
        self.text = "Move the mouse to change direction"
        super().__init__(W,340,self.text)

class instruction8(InstructionLine):
    def __init__(self,W):
        self.text = "Left click to shoot the turret"
        super().__init__(W,360,self.text)
class instruction9(InstructionLine):
    def __init__(self,W):
        self.text = "Right click to bomb"
        super().__init__(W,380,self.text)
"""
1.new class: Laser enemy
    fire laser beam, through the whole screen, free to choose any color
"""
