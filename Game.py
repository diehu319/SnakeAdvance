import pygame
import random
from pygame.locals import *
from setup import *
pygame.init()

def newbody(rc,direc):
    x = direc[0]
    y = direc[1]
    r = rc[0]
    c = rc[1]
    newr = r - y
    newc = c - x
    return (newr,newc)

def reset(g1,g2):
    g1.reset()
    g2.empty

W = 1100
WG = 800
H = 800
col = 80 # 10
row = 80 # 10
w1 = WG/col
h1 = H/row

psize = (w1,h1)




def main():
    KB = True
    MS = False
    # import high score
    try:
        f = open("gameProject/hs.txt","r")
        strhs = f.read()
        f.close
        strhs = strhs[:len(strhs)-1]
        scorelist = []
        for i in strhs.split(","):
            scorelist.append(int(i))
    except:
        scorelist = [0,0,0]
    
    # Display
    screen = pygame.display.set_mode((W, H))#,pygame.FULLSCREEN)
    pygame.display.set_caption("Final Project -------- ADVANCE SNAKE")
    #Object


    # speed: change position in row/col not in x/y
    speed = 1
    # direc is a tuple NSWE
    # (-1,0) is W
    # (1,0) is E
    # (0,-1) is N
    # (0,1) is S
    direc = (1,0)
    # start at the center of the game scene
    startpos = (int(col/2),int(row/2))
    # start with 10 life(length)
    startl = 10
    # player shoot frequency and enemy spawn frequency
    # can have enemy shoot frequency too
    shoot_frequency = 0
    enemy_frequency = 0
    # ef is to calculate when shoot_frequency % ef == 0. spawn enemy
    ef = 100

    # start to create sprites with classes
    # small Background (800*800) for gameplay
    gbg = GameBG(WG,H)
    # large Background (1000*800) for game and score
    bg = BG(W,H)
    # create player (head)
    player = head(startpos, speed, startl, psize)
    # create the first body part that protect the collide of head and first body part
    fbody = body((newbody(startpos,direc)),psize)
    # score board current score
    scoreboard1 = Scoreboard1(WG)
    # score board high score
    hs = HighScore(WG)
    hs1 = HighScore1(scorelist[0],WG)
    hs2 = HighScore2(scorelist[1],WG)
    hs3 = HighScore3(scorelist[2],WG)
    # score board current life
    scoreboard2 = Scoreboard2(WG)
    # score board current charge
    scoreboard3 = Scoreboard3(WG)
    # insturction board
    i1 = instruction1(WG)
    i2 = instruction2(WG)
    i3 = instruction3(WG)
    i4 = instruction4(WG)
    i5 = instruction5(WG)
    i6 = instruction6(WG)
    i7 = instruction7(WG)
    i8 = instruction8(WG)
    i9 = instruction9(WG)

    # create sprite.Group() for containing sprites
    firstbody = pygame.sprite.Group()
    bodyg = pygame.sprite.Group()
    foodg = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    bsprites = bodyg.sprites()
    fsprites = foodg.sprites()

    # create clock for fps
    clock = pygame.time.Clock()

    # when keepgoing is False, close game
    keepGoing = True

    # add the first body part to the group
    firstbody.add(fbody)

    # start row/col of body
    init_bodyrc = newbody(newbody(startpos,direc),direc)

    # create start body parts by start life/length
    for i in range(startl):
        bd = body(init_bodyrc,psize)
        init_bodyrc = newbody(init_bodyrc,direc)
        bodyg.add(bd)

    # while the game keep going
    while keepGoing:
        

        # 20 fps
        clock.tick(20)
        #Events

        for event in pygame.event.get():
            # quit game, check high score, write high score
            if event.type == pygame.QUIT:
                sclst = sorted((scorelist + [scoreboard1.score]),reverse = True)[0:3]
                try:
                    f = open("gameProject/hs.txt","w")
                    for i in sclst:
                        f.write("%s," % i)
                    f.close
                except:
                    f = open("gameProject/hs.txt","w+")
                    for i in sclst:
                        f.write("%s," % i)
                    f.close
                keepGoing = False
            # key ↑ ↓ ← → change the direction
            # z fire bullet
            if event.type == pygame.KEYDOWN and KB:
                if event.key == pygame.K_UP:
                    if (player.r - 1,player.c) != fbody.rc:
                        direc = (0,-1)
                if event.key == pygame.K_DOWN:
                    if (player.r + 1,player.c) != fbody.rc:
                        direc = (0,1)
                if event.key == pygame.K_LEFT:
                    if (player.r,player.c - 1) != fbody.rc:
                        direc = (-1,0)
                if event.key == pygame.K_RIGHT:
                    if (player.r,player.c + 1) != fbody.rc:
                        direc = (1,0)
                if event.key == pygame.K_z and player.fire:
                    if not player.bullets.sprites():
                        player.shoot()
                if event.key == pygame.K_x and player.charge > 0:
                    i = 0
                    player.charge -= 1
                    for e in enemy:
                        if i % 2 == 0:
                            bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                            bodyg.add(body(newbody(bfinal.rc,direc),psize))
                            scoreboard1.score += 5
                            player.life += 1
                        enemy.remove(e)
                        i += 1
            # if event.type == pygame.MOUSEMOTION and MS:
            #     x
                if event.key == pygame.K_c:
                    KB = not KB
                    MS = not MS
            if MS and pygame.mouse.get_focused():
                x,y = pygame.mouse.get_pos()
                if abs(player.rect.centerx - x) >= abs(player.rect.centerx - y):
                    if x >= player.rect.centerx:
                        if (player.r,player.c + 1) != fbody.rc:
                            direc = (1,0)
                    if x < player.rect.centerx:
                        if (player.r,player.c - 1) != fbody.rc:
                            direc = (-1,0)
                if abs(player.rect.centerx - x) < abs(player.rect.centerx - y):
                    if y >= player.rect.centery:
                        if (player.r + 1,player.c) != fbody.rc:
                            direc = (0,1)
                    if y < player.rect.centery:
                        if (player.r - 1,player.c) != fbody.rc:
                            direc = (0,-1)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == BUTTON_LEFT and MS:
                if player.fire:
                    if not player.bullets.sprites():
                        player.shoot()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == BUTTON_RIGHT and MS and player.charge > 0:
                i = 0
                player.charge -= 1
                for e in enemy:
                    if i % 2 == 0:
                        bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                        bodyg.add(body(newbody(bfinal.rc,direc),psize))
                        scoreboard1.score += 5
                        player.life += 1
                    enemy.remove(e)
                    i += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == BUTTON_MIDDLE and MS:
                MS = not MS
                KB = not KB


                
        ##########################
        # create sprite group
        bgSprites = pygame.sprite.OrderedUpdates(bg,gbg)
        highscoreSprite = pygame.sprite.Group(hs,hs1,hs2,hs3)
        scoreSprite = pygame.sprite.Group(scoreboard1)
        scoreSprite1 = pygame.sprite.Group(scoreboard2)
        scoreSprite2 = pygame.sprite.Group(scoreboard3)
        instructionSprite = pygame.sprite.Group(i1,i2,i3,i4,i5,i6,i7,i8,i9)
        playerSprite = pygame.sprite.Group(player)
        ##########################
        # update sprite group
        bgSprites.update()
        scoreSprite.update()
        
        playerSprite.update(direc)
        firstbody.update((player.r - direc[1],player.c - direc[0]))
        scoreSprite1.update(player.life)
        scoreSprite2.update(player.charge)
        ##########################
        # draw group using draw method
        bgSprites.draw(screen)
        highscoreSprite.draw(screen)
        scoreSprite.draw(screen)
        scoreSprite1.draw(screen)
        scoreSprite2.draw(screen)
        instructionSprite.draw(screen)
        foodg.draw(screen)
        
        playerSprite.draw(screen)
        bodyg.draw(screen)
        firstbody.draw(screen)
        
        player.bullets.draw(screen)
        enemy.draw(screen)


        # move body toward first body part
        temp1 = (fbody.rc)
        for b in bodyg:
            temp2 = b.rc
            b.update(temp1)
            temp1 = temp2
            if (player.r,player.c) == b.rc:
                if player.hit == False:
                    player.life -= 1
                    player.explode()
                    scoreboard1.score -= 10
                    #direc = (direc[1],direc[0])
                    if bodyg.sprites():
                        bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                        bodyg.remove(bfinal)
        
        # when bullet go out of scene
        # when hit enemy
        for b in player.bullets:
            b.update()
            if b.r > row:
                player.bullets.remove(b)
            if b.r < 0:
                player.bullets.remove(b)
            if b.c > col:
                player.bullets.remove(b)
            if b.c < 0:
                player.bullets.remove(b)
        # create food object on the screen
        # I will take care of putting this thing on the screen
        for f in foodg:
            f.update()
            if (player.r,player.c) == f.rc:
                bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                bodyg.add(body(newbody(bfinal.rc,direc),psize))
                foodg.remove(f)
                scoreboard1.score += 20
                player.life += 1
                if f.charge % 4 == 0:
                    player.charge += 1
                #enemy.empty
        # only 1 food object is allowed on the screen
        if not foodg.sprites():
            foodg.add(food((random.randint(8,col-8), random.randint(7,row-7)), psize))
        
        # enemy group
        for t in enemy:
            # enemy bullets
            for b in t.bullets:
                # collide check
                if (b.r, b.c) == (player.r, player.c):
                    if player.hit == False:
                        player.life -= 1
                        player.explode()
                        scoreboard1.score -= 50
                        if bodyg.sprites():
                            bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                            bodyg.remove(bfinal)
                    t.bullets.remove(b) 
                for bb in bodyg:
                    if (b.r, b.c) == bb.rc:
                        if player.hit == False:
                            player.life -= 1
                            player.explode()
                            scoreboard1.score -= 10
                            if bodyg.sprites():
                                bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                                bodyg.remove(bfinal)
                        t.bullets.remove(b)
                # update bullet
                b.update()
                # if bullet off the screen, remove
                if b.r > row:
                    t.bullets.remove(b)
                if b.r < 0:
                    t.bullets.remove(b)
                if b.c > col:
                    t.bullets.remove(b)
                if b.c < 0:
                    t.bullets.remove(b)
            # if player hit enemy, eat it but harm player
            if (player.r,player.c) == t.rc:
                enemy.remove(t)
                if player.hit == False:
                    player.life -= 1
                    player.explode()
                    scoreboard1.score -= 10
                    if bodyg.sprites():
                        bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                        bodyg.remove(bfinal)
            # update enemy
            t.update()
            # draw bullet on screen
            t.bullets.draw(screen)
            # only 1 bullet is allowed on the screen
            if not t.bullets.sprites():
                t.shoot()
        # add enemy depend on frequency, ef = 100
        if enemy_frequency % ef == 0:
            if player.life > 20 and random.randint(0,10) % 3 == 0:
                enemy.add(lturrent((random.randint(1,col), random.randint(1,row)), psize, (-1 * direc[0], -1 * direc[1])))
                enemy_frequency = 1
            else:
                enemy.add(turrent((random.randint(1,col), random.randint(1,row)), psize, (-1 * direc[0], -1 * direc[1])))
                enemy_frequency = 1
        enemy_frequency += 1

        
        # player bullets
        for b in player.bullets:
            # check collide with every enemy
            for t in enemy:
                if pygame.sprite.collide_circle(b,t):
                    player.bullets.remove(b)
                    enemy.remove(t)
                    scoreboard1.score += 50

        # if player touch wall, turn the player and -1 life, -10 score, no protection
        if player.r > row - 7:
            player.life -= 1
            player.r = row - 7
            scoreboard1.score -= 10
            direc = (-1 * direc[1],direc[0])
            if bodyg.sprites():
                bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                bodyg.remove(bfinal)
        if player.c > col - 6:
            player.life -= 1
            player.c = col - 6
            scoreboard1.score -= 10
            direc = (direc[1],direc[0])
            if bodyg.sprites():
                bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                bodyg.remove(bfinal)
        if player.r < 8:
            player.life -= 1
            player.r = 8
            scoreboard1.score -= 10
            direc = (-1 * direc[1],direc[0])
            if bodyg.sprites():
                bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                bodyg.remove(bfinal)
        if player.c < 7:
            player.life -= 1
            player.c = 7
            scoreboard1.score -= 10
            direc = (direc[1],direc[0])
            if bodyg.sprites():
                bfinal = bodyg.sprites()[len(bodyg.sprites())-1]
                bodyg.remove(bfinal)

        
        # if life <= 0, Game over, print score, write high score to the file, maybe able to do scoreboard but later
        if player.life <= 0:
            sclst = sorted((scorelist + [scoreboard1.score]),reverse = True)[0:3]
            try:
                f = open("gameProject/hs.txt","w")
                for i in sclst:
                    f.write("%s," % i)
                f.close
            except:
                f = open("gameProject/hs.txt","w+")
                for i in sclst:
                    f.write("%s," % i)
                f.close
            keepGoing = False
            print("GAME OVER___________YOUR SCORE IS: " + str(scoreboard1.score))
            pygame.init()
            break

        
        
        pygame.display.flip()
    
    # For Windows 
    pygame.quit()


if __name__ == "__main__":
    main()
