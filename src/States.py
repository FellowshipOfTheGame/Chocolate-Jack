#coding: utf-8
import pygame
import sys
import Fighters


class StateMachine:
    def __init__(self):
        self.left = False
        self.right = False
        self.jump = False
        self.punch = False
        self.kick = False
    def execute(self, message):
        #CHANGE STATES
        if(message == 'mvLKeyPressed' and not self.right):
            self.left = True
        elif(message == 'mvRKeyPressed' and not self.left):
            self.right = True
        elif(message == 'mvUKeyPressed' and not (self.punch or self.kick)):
            self.jump =True
        elif(message == 'pcKeyPressed'):
            self.punch = True
        elif(message == 'kcKeyPressed'):
            self.kick = True
        elif(message == 'mvLKeyReleased' or message == 'mvRKeyPressed'):
            self.left = False
        elif (message == 'mvRKeyReleased' or message == 'mvLKeyPressed'):
            self.right = False
    def isPunching(self):
        return self.punch
    def isKicking(self):
        return self.kick
    def isJumping(self):
        return self.jump
    def isMovingLeft(self):
        return self.left
    def isMovingRight(self):
        return self.right
    def isStopped(self):
        return not (self.left or self.right or self.jump or self.punch or self.kick)
###
#   State "Machine"
###
class States:

    def Enter(self,Object):
        pass
    def Execute(self,Object, message):
        pass
    def Exit(self,Object):
        pass

###
#   Fighter States
###

class f_stopped(States):

    def Enter(self, Fighter):
        #Fighter.mvCooldown = 0 #why?
        Fighter.drawPx = Fighter.px
        Fighter.drawPy = Fighter.py
        Fighter.frameNum = -1;
        halfQtdFrames = int(len(Fighter.stopFrames)/2)
        Fighter.curFrame = Fighter.stopFrames[Fighter.facing*halfQtdFrames]
        
    def Execute(self,Fighter, machine):
        
        #considerando que a primeira metade tem movimentos facing right e a segunda facing left
        halfQtdFrames = int(len(Fighter.stopFrames)/2)

        Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames) + Fighter.facing*halfQtdFrames
        Fighter.curFrame = Fighter.stopFrames[Fighter.frameNum]

        #CHANGE STATES
        if (machine.isMovingLeft()):
            Fighter.mvDir = 1
            Fighter.changeState(f_moving())
        elif(machine.isMovingRight()):
            Fighter.mvDir = 0
            Fighter.changeState(f_moving())
        elif(machine.isJumping()):
            if (Fighter.jumping == False):
                Fighter.jumping = True
                Fighter.changeState(f_jumping_stopped())
        elif(machine.isPunching()):
            Fighter.changeState(f_punching())
        elif(machine.isKicking()):
            Fighter.changeState(f_kicking())

    def Exit(self,Fighter):
        pass

class f_dazzed(States):

    def Enter(self, Fighter):
        self.dazzed = 10
        #Fighter.mvCooldown = 0 #why?
        Fighter.drawPx = Fighter.px
        Fighter.drawPy = Fighter.py
        Fighter.frameNum = -1;
        halfQtdFrames = int(len(Fighter.stopFrames)/2)
        Fighter.curFrame = Fighter.stopFrames[Fighter.facing*halfQtdFrames]
        
    def Execute(self,Fighter, machine):
        self.dazzed = self.dazzed -1
        if (self.dazzed <= 0):
            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            halfQtdFrames = int(len(Fighter.stopFrames)/2)
    
            Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames) + Fighter.facing*halfQtdFrames
            Fighter.curFrame = Fighter.stopFrames[Fighter.frameNum]
    
            #CHANGE STATES
            if (machine.isMovingLeft()):
                Fighter.mvDir = 1
                Fighter.changeState(f_moving())
            elif(machine.isMovingRight()):
                Fighter.mvDir = 0
                Fighter.changeState(f_moving())
            elif(machine.isJumping()):
                if (Fighter.jumping == False):
                    Fighter.jumping = True
                    Fighter.changeState(f_jumping_stopped())
            elif(machine.isPunching()):
                Fighter.changeState(f_punching())
            elif(machine.isKicking()):
                Fighter.changeState(f_kicking())

    def Exit(self,Fighter):
        pass
###
class f_moving(States):

    def Enter(self,Fighter):
        Fighter.drawPx = Fighter.px
        Fighter.drawPy = Fighter.py
        Fighter.mvCooldown = 0
        Fighter.frameNum = -1

    def Execute(self,Fighter, machine):
        halfQtdFrames = int(len(Fighter.movFrames)/2)
        #considerando que a primeira metade tem movimentos facing right e a segunda facing left
        Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames+1)
        if(Fighter.frameNum < halfQtdFrames):
            Fighter.curFrame = Fighter.movFrames[Fighter.frameNum+Fighter.mvDir*halfQtdFrames]
            
            #Posicao aumenta em mvInc caso dir igual a 0 (indo para a dir), caso contrario decrementa.
            Fighter.px = Fighter.px + (Fighter.mvDir*(-2)+1)*Fighter.mvInc
            Fighter.drawPx = Fighter.px
            if (Fighter.frameNum == halfQtdFrames):
                Fighter.changeState(f_stopped())
        else:
            #CHANGE STATE
            if (machine.isJumping()):
                if (Fighter.jumping == False):
                    Fighter.jumping = True
                    Fighter.changeState(f_jumping_moving())
            elif (machine.isMovingLeft()):
                Fighter.mvDir = 1
                Fighter.changeState(f_moving())
            elif(machine.isMovingRight()):
                Fighter.mvDir = 0
                Fighter.changeState(f_moving())
            elif(machine.isPunching()):
                Fighter.changeState(f_punching())
            elif(machine.isKicking()):
                Fighter.changeState(f_kicking())
            elif(machine.isStopped()):
                Fighter.changeState(f_stopped())


        
    def Exit(self,Fighter):
        pass

class f_jumping_stopped(States):

    def Enter(self, Fighter):

        print ("pulando")
        self.force = Fighter.getForceJump()
        Fighter.jumping = True
        Fighter.machine.jump = False
        #Fighter.mvCooldown = 0 #why?
        Fighter.drawPx = Fighter.px
        Fighter.drawPy = Fighter.py
        Fighter.frameNum = -1;
        halfQtdFrames = int(len(Fighter.stopFrames)/2)
        Fighter.curFrame = Fighter.stopFrames[Fighter.facing*halfQtdFrames]
        
    def Execute(self,Fighter, message):
        
        if(Fighter.mvCooldown <= 0):
            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            halfQtdFrames = int(len(Fighter.stopFrames)/2)
    
            Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames) + Fighter.facing*halfQtdFrames
            Fighter.curFrame = Fighter.stopFrames[Fighter.frameNum]
            Fighter.drawPy = Fighter.py
            Fighter.mvCooldown = Fighter.mvMaxCooldown + 1 #esse +1 serah removido na linha seguinte
    
            if (self.force >=1):
                Fighter.py -= self.force
                self.force = self.force /2
            elif (self.force <=-Fighter.getForceJump()):
                Fighter.machine.jump = False
                Fighter.changeState(f_stopped())
            elif (self.force <0):
                self.force = self.force *2
                Fighter.py -= self.force
                pass
            else:
                self.force = -self.force
            
        Fighter.mvCooldown = Fighter.mvCooldown - 1

    def Exit(self,Fighter):
        Fighter.jumping = False
        Fighter.machine.jump = False

###
class f_jumping_moving(States):

    def Enter(self,Fighter):
        self.force = 50
        Fighter.jumping = True
        Fighter.machine.jump = False
        Fighter.drawPx = Fighter.px
        Fighter.drawPy = Fighter.py
        Fighter.mvCooldown = 0
        Fighter.frameNum = -1

    def Execute(self,Fighter, machine):
        if(Fighter.mvCooldown <= 0):
            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            halfQtdFrames = int(len(Fighter.movFrames)/2)

            Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames) + Fighter.mvDir*halfQtdFrames
            Fighter.curFrame = Fighter.movFrames[Fighter.frameNum]

            #Posicao aumenta em mvInc caso dir igual a 0 (indo para a dir), caso contrario decrementa.
            Fighter.px = Fighter.px + (Fighter.mvDir*(-2)+1)*Fighter.mvInc
            Fighter.drawPx = Fighter.px
            Fighter.drawPy = Fighter.py

            
        if (self.force >=1):
            Fighter.py -= self.force
            self.force = self.force /2
        elif (self.force <=-50):
            Fighter.machine.jump = False
            Fighter.changeState(f_moving())
        elif (self.force <0):
            self.force = self.force *2
            Fighter.py -= self.force
            pass
        else:
            self.force = -self.force

        Fighter.mvCooldown = Fighter.mvCooldown - 1

        
    def Exit(self,Fighter):
        Fighter.jumping = False

###
class f_punching(States):

    def Enter(self, Fighter):
        self.stateTime = 10
        Fighter.pcCooldown = Fighter.pcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
        Fighter.frameNum = -1
        Fighter.machine.punch = False

    def Execute(self, Fighter, machine):
        self.stateTime = self.stateTime -1
        if (self.stateTime > 0):
            if(Fighter.pcCooldown <=0):
                Fighter.pcCooldown = Fighter.pcMaxCooldown + 1 #esse +1 serah removido na linha seguinte
                halfQtdFrames = int(len(Fighter.pcFrames)/2)
    
                Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames+1)
                if(Fighter.frameNum < halfQtdFrames):
                    Fighter.curFrame = Fighter.pcFrames[Fighter.frameNum+Fighter.facing*halfQtdFrames]
        
                    #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
                    #Fighter.pcPx = Fighter.px - Fighter.facing*Fighter.pcDist
                    Fighter.pcPx = Fighter.px - (Fighter.facing)*(Fighter.pcDist)
                    Fighter.pcPy = Fighter.py
                    Fighter.drawPx = Fighter.pcPx
                    Fighter.drawPy = Fighter.pcPy
                    
                    #checando colisao
                    for coll in Fighter.curFrame.getCollisionsRect(Fighter.pcPx, Fighter.pcPy):
                        if(coll.collidelist(Fighter.enemy.curFrame.getCollisionsRect(Fighter.enemy.drawPx,
                                                                                     Fighter.enemy.drawPy)) > -1):
                            Fighter.soco = 1
                            Fighter.enemy.hp = Fighter.enemy.hp - (Fighter.attack - Fighter.enemy.defense)
                else:
                    #CHANGE STATE
                    if (machine.isMovingLeft()):
                        Fighter.mvDir = 1
                        Fighter.changeState(f_moving())
                    elif(machine.isMovingRight()):
                        Fighter.mvDir = 0
                        Fighter.changeState(f_moving())
                    elif(machine.isJumping()):
                        if (Fighter.jumping == False):
                            Fighter.jumping = True
                            Fighter.changeState(f_jumping_moving())
                    elif(machine.isPunching()):
                        Fighter.changeState(f_punching_2())
                    elif(machine.isKicking()):
                        Fighter.changeState(f_kicking())
            Fighter.pcCooldown = Fighter.pcCooldown - 1
        else:
            Fighter.changeState(f_stopped())
            
            

    def Exit(self, Fighter):
        pass


class f_punching_2(States):

    def Enter(self, Fighter):
        self.stateTime = 10
        Fighter.pcCooldown = Fighter.pcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
        Fighter.frameNum = -1
        Fighter.machine.punch = False

    def Execute(self, Fighter, machine):
        self.stateTime = self.stateTime -1
        if (self.stateTime > 0):
            if(Fighter.pcCooldown <=0):
                Fighter.pcCooldown = Fighter.pcMaxCooldown + 1 #esse +1 serah removido na linha seguinte
                halfQtdFrames = int(len(Fighter.pcFrames)/2)
    
                Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames+1)
                if(Fighter.frameNum < halfQtdFrames):
                    Fighter.curFrame = Fighter.pcFrames[Fighter.frameNum+Fighter.facing*halfQtdFrames]
        
                    #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
                    #Fighter.pcPx = Fighter.px - Fighter.facing*Fighter.pcDist
                    Fighter.pcPx = Fighter.px - (Fighter.facing)*(Fighter.pcDist)
                    Fighter.pcPy = Fighter.py
                    Fighter.drawPx = Fighter.pcPx
                    Fighter.drawPy = Fighter.pcPy
        
                    #checando colisao
                    for coll in Fighter.curFrame.getCollisionsRect(Fighter.pcPx, Fighter.pcPy):
                        if(coll.collidelist(Fighter.enemy.curFrame.getCollisionsRect(Fighter.enemy.drawPx,
                                                                                     Fighter.enemy.drawPy)) > -1):
                            Fighter.soco = 1
                            Fighter.enemy.hp = Fighter.enemy.hp - (Fighter.attack*5 - Fighter.enemy.defense)
                            Fighter.enemy.changeState(f_dazzed())
                else:
                    #CHANGE STATE
                    if (machine.isMovingLeft()):
                        Fighter.mvDir = 1
                        Fighter.changeState(f_moving())
                    elif(machine.isMovingRight()):
                        Fighter.mvDir = 0
                        Fighter.changeState(f_moving())
                    elif(machine.isJumping()):
                        if (Fighter.jumping == False):
                            Fighter.jumping = True
                            Fighter.changeState(f_jumping_moving())
                    elif(machine.isPunching()):
                        Fighter.changeState(f_punching_3())
                    elif(machine.isKicking()):
                        Fighter.changeState(f_kicking())
            Fighter.pcCooldown = Fighter.pcCooldown - 1
        else:
            Fighter.changeState(f_stopped())

    def Exit(self, Fighter):
        pass

class f_punching_3(States):

    def Enter(self, Fighter):
        self.stateTime = 10
        Fighter.pcCooldown = Fighter.pcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
        Fighter.frameNum = -1
        Fighter.machine.punch = False

    def Execute(self, Fighter, machine):
        self.stateTime = self.stateTime -1
        if (self.stateTime > 0):
            if(Fighter.pcCooldown <=0):
                Fighter.pcCooldown = Fighter.pcMaxCooldown + 1 #esse +1 serah removido na linha seguinte
                halfQtdFrames = int(len(Fighter.pcFrames)/2)
    
                Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames+1)
                if(Fighter.frameNum < halfQtdFrames):
                    Fighter.curFrame = Fighter.pcFrames[Fighter.frameNum+Fighter.facing*halfQtdFrames]
        
                    #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
                    #Fighter.pcPx = Fighter.px - Fighter.facing*Fighter.pcDist
                    Fighter.pcPx = Fighter.px - (Fighter.facing)*(Fighter.pcDist)
                    Fighter.pcPy = Fighter.py
                    Fighter.drawPx = Fighter.pcPx
                    Fighter.drawPy = Fighter.pcPy
        
                    #checando colisao
                    for coll in Fighter.curFrame.getCollisionsRect(Fighter.pcPx, Fighter.pcPy):
                        if(coll.collidelist(Fighter.enemy.curFrame.getCollisionsRect(Fighter.enemy.drawPx,
                                                                                     Fighter.enemy.drawPy)) > -1):
                            Fighter.soco = 1
                            Fighter.enemy.hp = Fighter.enemy.hp - (Fighter.attack*5 - Fighter.enemy.defense)
                else:
                    #CHANGE STATE
                    if (machine.isMovingLeft()):
                        Fighter.mvDir = 1
                        Fighter.changeState(f_moving())
                    elif(machine.isMovingRight()):
                        Fighter.mvDir = 0
                        Fighter.changeState(f_moving())
                    elif(machine.isJumping()):
                        if (Fighter.jumping == False):
                            Fighter.jumping = True
                            Fighter.changeState(f_jumping_moving())
            Fighter.pcCooldown = Fighter.pcCooldown - 1
        else:
            Fighter.changeState(f_stopped())

    def Exit(self, Fighter):
        pass
###
class f_kicking(States):

    def Enter(self, Fighter):
        self.stateTime = 10
        Fighter.kcCooldown = Fighter.kcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
        Fighter.frameNum = -1
        Fighter.machine.kick = False

    def Execute(self, Fighter, machine):
        self.stateTime = self.stateTime -1
        if (self.stateTime > 0):
            if(Fighter.kcCooldown <=0):
                Fighter.kcCooldown = Fighter.kcMaxCooldown + 1 #esse +1 serah removido na linha seguinte
                halfQtdFrames = int(len(Fighter.kcFrames)/2)
    
                Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames+1)
                if(Fighter.frameNum < halfQtdFrames):
                    Fighter.curFrame = Fighter.kcFrames[Fighter.frameNum+Fighter.facing*halfQtdFrames]
        
                    #Caso o char esteja socando apara a esquerda da tela, decrementa kcDist da posicao de soco.
                    #Fighter.kcPx = Fighter.px - Fighter.facing*Fighter.kcDist
                    Fighter.kcPx = Fighter.px - (Fighter.facing)*(Fighter.kcDist)
                    Fighter.kcPy = Fighter.py
                    Fighter.drawPx = Fighter.kcPx
                    Fighter.drawPy = Fighter.kcPy
                    
                    #checando colisao
                    for coll in Fighter.curFrame.getCollisionsRect(Fighter.kcPx, Fighter.kcPy):
                        if(coll.collidelist(Fighter.enemy.curFrame.getCollisionsRect(Fighter.enemy.drawPx,
                                                                                     Fighter.enemy.drawPy)) > -1):
                            Fighter.chute = 1
                            Fighter.enemy.hp = Fighter.enemy.hp - (Fighter.attack - Fighter.enemy.defense)
                else:
                    #CHANGE STATE
                    if (machine.isMovingLeft()):
                        Fighter.mvDir = 1
                        Fighter.changeState(f_moving())
                    elif(machine.isMovingRight()):
                        Fighter.mvDir = 0
                        Fighter.changeState(f_moving())
                    elif(machine.isJumping()):
                        if (Fighter.jumping == False):
                            Fighter.jumping = True
                            Fighter.changeState(f_jumping_moving())
                    elif(machine.isPunching()):
                        Fighter.changeState(f_punching())
                    elif(machine.isKicking()):
                        Fighter.changeState(f_kicking())
            Fighter.kcCooldown = Fighter.kcCooldown - 1
        else:
            Fighter.changeState(f_stopped())
        

    def Exit(self, Fighter):
        pass
###
#   Scenario States
###
class s_default(States):

    def Enter(self, pScene):
        pScene.frameNum = (pScene.frameNum + 1)%len(pScene.frames)
        print(pScene.frameNum)
        pScene.curFrame = pScene.frames[pScene.frameNum]

    def Execute(self, pScene, message):
        if(pScene.cooldown <= 0):
            pScene.frameNum = (pScene.frameNum + 1)%len(pScene.frames)
            pScene.curFrame = pScene.frames[pScene.frameNum]
            pScene.cooldown = pScene.frameCooldown

        pScene.cooldown = pScene.cooldown - 1

    def Exit(self, pScene):
        pass

