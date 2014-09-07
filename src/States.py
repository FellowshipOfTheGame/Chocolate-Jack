#coding: utf-8
import builtins
import pygame
import sys
import Fighters
import globals
from Animations import *

class StateMachine:
    def __init__(self):
        self.left = False
        self.right = False
        self.jump = False
        self.punch = False
        self.kick = False
    def execute(self, message):
        #CHANGE STATES
        if(message == 'mvLKeyReleased' or (message == 'mvRKeyPressed' and self.left)):
            self.left = False
        elif (message == 'mvRKeyReleased' or (message == 'mvLKeyPressed' and self.right)):
            self.right = False
        elif(message == 'mvLKeyPressed' and not self.right):
            self.left = True
        elif(message == 'mvRKeyPressed' and not self.left):
            self.right = True
        elif(message == 'mvUKeyPressed' and not (self.punch or self.kick)):
            self.jump =True
        elif(message == 'pcKeyPressed'):
            self.punch = True
            self.left = False
            self.right = False
        elif(message == 'kcKeyPressed'):
            self.kick = True
            self.left = False
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
class State:
    def Enter(self,Object, frames):
        pass
    def Execute(self, message):
        pass
    def Exit(self):
        pass

###
#   self.Fighter States
###
class States:
    class f_stopped(State):

        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            #self.Fighter.mvCooldown = 0 #why?
            self.Fighter.drawPx = self.Fighter.px
            self.Fighter.drawPy = self.Fighter.py
            self.Fighter.frameNum = -1;

            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message):

            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            self.halfQtdFrames = int(len(self.frames)/2)

            self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames) + self.Fighter.facing*self.halfQtdFrames
            self.Fighter.curFrame = self.frames[self.Fighter.frameNum]

            #CHANGE STATES
            self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message))
            """if (self.Fighter.machine.isMovingLeft()):
                self.Fighter.moviment.mvDir = 1
                self.Fighter.changeState(States.f_moving())
            elif(self.Fighter.machine.isMovingRight()):
                self.Fighter.moviment.mvDir = 0
                self.Fighter.changeState(States.f_moving())
            elif(self.Fighter.machine.isJumping()):
                if (self.Fighter.moviment.jumping == False):
                    self.Fighter.moviment.jumping = True
                    self.Fighter.changeState(States.f_jumping_stopped())
            elif(self.Fighter.machine.isPunching()):
                self.Fighter.changeState(States.f_punching())
            elif(self.Fighter.machine.isKicking()):
                self.Fighter.changeState(States.f_kicking())"""

        def Exit(self):
            pass

    class f_dazzed(State):

        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            self.dazzed = 10
            #self.Fighter.mvCooldown = 0 #why?
            self.Fighter.drawPx = self.Fighter.px
            self.Fighter.drawPy = self.Fighter.py
            self.Fighter.frameNum = -1;
            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message):
            self.dazzed = self.dazzed -1
            if (self.dazzed <= 0):
                #considerando que a primeira metade tem movimentos facing right e a segunda facing left
                self.halfQtdFrames = int(len(self.frames)/2)

                self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames) + self.Fighter.facing*self.halfQtdFrames
                self.Fighter.curFrame = self.frames[self.Fighter.frameNum]

                #CHANGE STATES
                self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message))

        def Exit(self):
            pass
    ###
    class f_moving(State):
        isMovimentState = True
        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            self.Fighter.drawPx = self.Fighter.px
            self.Fighter.drawPy = self.Fighter.py
            self.Fighter.mvCooldown = 0
            #self.Fighter.frameNum = -1
            self.frames = frames

#            if (self.Fighter.machine.isMovingLeft()):
 #               self.Fighter.moviment.mvDir = 1
#            elif(self.Fighter.machine.isMovingRight()):
 #               self.Fighter.moviment.mvDir = 0

            self.halfQtdFrames = int(len(self.frames)/2)
            #self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message):
            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames+1)
            if(self.Fighter.frameNum < self.halfQtdFrames):
                self.Fighter.curFrame = self.frames[self.Fighter
                                                        .frameNum+self
                    .Fighter.moviment.mvDir*self.halfQtdFrames]

                #Posicao aumenta em mvInc caso dir igual a 0 (indo para a dir), caso contrario decrementa.
                self.Fighter.px = self.Fighter.px + (self.Fighter.moviment.mvDir*(-2)+1)*self.Fighter.moviment.mvInc
                self.Fighter.drawPx = self.Fighter.px
                if (self.Fighter.frameNum == self.halfQtdFrames):
                    self.Fighter.changeState(States.f_stopped())

                #if(self.Fighter.machine.isStopped()):
                 #   self.Fighter.changeState(self.Fighter.states.getAction(self
                  #                                                .__class__
                   #                                      .__name__,'null'))
                    #self.Fighter.changeState(States.f_stopped())
            else:
                pass
                #CHANGE STATE
            self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message, True))

        def Exit(self):
            pass

    class f_jumping_stopped(State):

        def Enter(self, Fighter, zframes):
            self.Fighter = Fighter
            '''
            print ("pulando")
            self.force = self.Fighter.getForceJump()
            self.Fighter.moviment.jumping = True
            self.Fighter.machine.jump = False
            #self.Fighter.mvCooldown = 0 #why?
            self.Fighter.drawPx = self.Fighter.px
            self.Fighter.drawPy = self.Fighter.py
            self.Fighter.frameNum = -1;
            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]
            '''
            self.force = self.Fighter.getForceJump()
            self.Fighter.moviment.jumping = True
            self.Fighter.drawPx = self.Fighter.px
            self.Fighter.drawPy = self.Fighter.py
            self.Fighter.mvCooldown = 0
            self.Fighter.frameNum = -1
            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]
            #'''
        def Execute(self, message):

            if(self.Fighter.mvCooldown <= 0):
                #considerando que a primeira metade tem movimentos facing right e a segunda facing left
                self.halfQtdFrames = int(len(self.frames)/2)

                self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames) + self.Fighter.facing*self.halfQtdFrames
                self.Fighter.curFrame = self.frames[self.Fighter.frameNum]
                self.Fighter.drawPy = self.Fighter.py
                self.Fighter.mvCooldown = self.Fighter.mvMaxCooldown + 1 #esse +1 serah removido na linha seguinte

            if (self.force >=1):
                self.Fighter.py -= self.force
                self.force = self.force /2
            elif (self.force <=-self.Fighter.getForceJump()):
                self.Fighter.changeState(self.Fighter.states.getAction(self
                                                                  .__class__
                                                         .__name__,'*'))
            elif (self.force <0):
                self.force = self.force *2
                self.Fighter.py -= self.force
                pass
            else:
                self.force = -self.force

            self.Fighter.mvCooldown = self.Fighter.mvCooldown - 1

        def Exit(self):
            self.Fighter.moviment.jumping = False

    ###
    class f_jumping_moving(State):

        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            self.force = 50
            self.Fighter.moviment.jumping = True
            self.Fighter.drawPx = self.Fighter.px
            self.Fighter.drawPy = self.Fighter.py
            self.Fighter.mvCooldown = 0
            self.Fighter.frameNum = -1

            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message, optional =0):
            if(self.Fighter.mvCooldown <= 0):
                #considerando que a primeira metade tem movimentos facing right e a segunda facing left
                self.halfQtdFrames = int(len(self.frames)/2)

                self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames) + self.Fighter.moviment.mvDir*self.halfQtdFrames
                self.Fighter.curFrame = self.frames[self.Fighter.frameNum]

                #Posicao aumenta em mvInc caso dir igual a 0 (indo para a dir), caso contrario decrementa.
                self.Fighter.px = self.Fighter.px + (self.Fighter.moviment.mvDir*(-2)+1)*self.Fighter.moviment.mvInc
                self.Fighter.drawPx = self.Fighter.px
                self.Fighter.drawPy = self.Fighter.py


            if (self.force >=1):
                self.Fighter.py -= self.force
                self.force = self.force /2
            elif (self.force <=-50):
                #self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message, True))
                self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,'*'))
            elif (self.force <0):
                self.force = self.force *2
                self.Fighter.py -= self.force
                pass
            else:
                self.force = -self.force

            self.Fighter.mvCooldown = self.Fighter.mvCooldown - 1


        def Exit(self):
            self.Fighter.moviment.jumping = False

    ###
    class f_punching(State):

        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            self.stateTime = 10
            self.Fighter.pcCooldown = self.Fighter.pcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
            self.Fighter.frameNum = -1
            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message):
            self.halfQtdFrames = int(len(self.frames)/2)
            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames+1)
            if(self.Fighter.frameNum < self.halfQtdFrames):
                self.Fighter.curFrame = self.frames[self.Fighter.frameNum+self.Fighter
                    .facing*self.halfQtdFrames]

                #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
                #self.Fighter.pcPx = self.Fighter.px - self.Fighter.facing*self.Fighter.pcDist
                self.Fighter.pcPx = self.Fighter.px - (self.Fighter.facing)*(self.Fighter.pcDist)
                self.Fighter.pcPy = self.Fighter.py
                self.Fighter.drawPx = self.Fighter.pcPx
                self.Fighter.drawPy = self.Fighter.pcPy

                #checando colisao
                for coll in self.Fighter.curFrame.getCollisionsRect(self.Fighter.pcPx, self.Fighter.pcPy):
                    if(coll.collidelist(self.Fighter.enemy.curFrame.getCollisionsRect(self.Fighter.enemy.drawPx,
                                                                                 self.Fighter.enemy.drawPy)) > -1):
                        self.Fighter.soco = 1
                        self.Fighter.enemy.hp = self.Fighter.enemy.hp - (self.Fighter.attack - self.Fighter.enemy.defense)

                        globals.globAnimations.append(Animations.StartChocoPunchAnimation(globals.globTela,
                                                                                          (self.Fighter.pcPx, self.Fighter.pcPy), self.Fighter.player))
            else:
                #CHANGE STATE
                self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message))
                """if (self.Fighter.machine.isMovingLeft()):
                    self.Fighter.moviment.mvDir = 1
                    self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isMovingRight()):
                    self.Fighter.moviment.mvDir = 0
                    self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isJumping()):
                    if (self.Fighter.moviment.jumping == False):
                        self.Fighter.moviment.jumping = True
                        self.Fighter.changeState(States.f_jumping_moving())
                elif(self.Fighter.machine.isPunching()):
                    self.Fighter.changeState(States.f_punching_2())
                elif(self.Fighter.machine.isKicking()):
                    self.Fighter.changeState(States.f_kicking())
                else:
                    self.Fighter.changeState(States.f_stopped())"""



        def Exit(self):
            pass


    class f_punching_2(State):

        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            self.stateTime = 10
            self.Fighter.pcCooldown = self.Fighter.pcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
            self.Fighter.frameNum = -1

            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message):
            self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames+1)
            if(self.Fighter.frameNum < self.halfQtdFrames):
                self.Fighter.curFrame = self.frames[self.Fighter.frameNum+self.Fighter
                    .facing*self.halfQtdFrames]

                #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
                #self.Fighter.pcPx = self.Fighter.px - self.Fighter.facing*self.Fighter.pcDist
                self.Fighter.pcPx = self.Fighter.px - (self.Fighter.facing)*(self.Fighter.pcDist)
                self.Fighter.pcPy = self.Fighter.py
                self.Fighter.drawPx = self.Fighter.pcPx
                self.Fighter.drawPy = self.Fighter.pcPy

                #checando colisao
                for coll in self.Fighter.curFrame.getCollisionsRect(self.Fighter.pcPx, self.Fighter.pcPy):
                    if(coll.collidelist(self.Fighter.enemy.curFrame.getCollisionsRect(self.Fighter.enemy.drawPx,
                                                                                 self.Fighter.enemy.drawPy)) > -1):
                        #declarando que usara a tela global
                        tela # ignore que é global

                        self.Fighter.soco = 1
                        self.Fighter.enemy.hp = self.Fighter.enemy.hp - (self.Fighter.attack - self.Fighter.enemy.defense)
            else:
                #CHANGE STATE
                self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message))
                """if (self.Fighter.machine.isMovingLeft()):
                    self.Fighter.moviment.mvDir = 1
                    self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isMovingRight()):
                    self.Fighter.moviment.mvDir = 0
                    self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isJumping()):
                    if (self.Fighter.moviment.jumping == False):
                        self.Fighter.moviment.jumping = True
                        self.Fighter.changeState(States.f_jumping_moving())
                elif(self.Fighter.machine.isPunching()):
                    self.Fighter.changeState(States.f_punching_3())
                elif(self.Fighter.machine.isKicking()):
                    self.Fighter.changeState(States.f_kicking())
                else:
                    self.Fighter.changeState(States.f_stopped())"""

        def Exit(self):
            pass

    class f_punching_3(State):

        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            self.stateTime = 10
            self.Fighter.pcCooldown = self.Fighter.pcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
            self.Fighter.frameNum = -1


            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message):
            self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames+1)
            if(self.Fighter.frameNum < self.halfQtdFrames):
                self.Fighter.curFrame = self.frames[self.Fighter.frameNum+self.Fighter
                    .facing*self.halfQtdFrames]

                #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
                #self.Fighter.pcPx = self.Fighter.px - self.Fighter.facing*self.Fighter.pcDist
                self.Fighter.pcPx = self.Fighter.px - (self.Fighter.facing)*(self.Fighter.pcDist)
                self.Fighter.pcPy = self.Fighter.py
                self.Fighter.drawPx = self.Fighter.pcPx
                self.Fighter.drawPy = self.Fighter.pcPy

                #checando colisao
                for coll in self.Fighter.curFrame.getCollisionsRect(self.Fighter.pcPx, self.Fighter.pcPy):
                    if(coll.collidelist(self.Fighter.enemy.curFrame.getCollisionsRect(self.Fighter.enemy.drawPx,
                                                                                 self.Fighter.enemy.drawPy)) > -1):
                        self.Fighter.soco = 1
                        self.Fighter.enemy.hp = self.Fighter.enemy.hp - (self.Fighter.attack - self.Fighter.enemy.defense)
            else:
                #CHANGE STATE
                self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message))
                """if (self.Fighter.machine.isMovingLeft()):
                    self.Fighter.moviment.mvDir = 1
                    self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isMovingRight()):
                    self.Fighter.moviment.mvDir = 0
                    self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isJumping()):
                    if (self.Fighter.moviment.jumping == False):
                        self.Fighter.moviment.jumping = True
                        self.Fighter.changeState(States.f_jumping_moving())
                elif(self.Fighter.machine.isPunching()):
                    self.Fighter.machine.punch = False
                elif(self.Fighter.machine.isKicking()):
                    self.Fighter.changeState(States.f_kicking())
                else:
                    self.Fighter.changeState(States.f_stopped())"""

        def Exit(self):
            pass
    ###
    class f_kicking(State):

        def Enter(self, Fighter, frames):
            self.Fighter = Fighter
            self.stateTime = 7
            self.Fighter.kcCooldown = self.Fighter.kcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
            self.Fighter.frameNum = -1


            self.frames = frames

            self.halfQtdFrames = int(len(self.frames)/2)
            self.Fighter.curFrame = self.frames[self.Fighter.facing*self.halfQtdFrames]

        def Execute(self, message):
            self.Fighter.frameNum = (self.Fighter.frameNum + 1)%(self.halfQtdFrames+1)
            if(self.Fighter.frameNum < self.halfQtdFrames):
                self.Fighter.curFrame = self.frames[self.Fighter.frameNum+self.Fighter
                    .facing*self.halfQtdFrames]

                #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
                #self.Fighter.pcPx = self.Fighter.px - self.Fighter.facing*self.Fighter.pcDist
                self.Fighter.pcPx = self.Fighter.px - (self.Fighter.facing)*(self.Fighter.pcDist)
                self.Fighter.pcPy = self.Fighter.py
                self.Fighter.drawPx = self.Fighter.pcPx
                self.Fighter.drawPy = self.Fighter.pcPy

                #checando colisao
                for coll in self.Fighter.curFrame.getCollisionsRect(self.Fighter.pcPx, self.Fighter.pcPy):
                    if(coll.collidelist(self.Fighter.enemy.curFrame.getCollisionsRect(self.Fighter.enemy.drawPx,
                                                                                 self.Fighter.enemy.drawPy)) > -1):
                        self.Fighter.soco = 1
                        self.Fighter.enemy.hp = self.Fighter.enemy.hp - (self.Fighter.attack - self.Fighter.enemy.defense)
            else:
                #CHANGE STATE
                self.Fighter.changeState(self.Fighter.states.getAction(self.__class__.__name__,message))
                """if (self.Fighter.machine.isMovingLeft()):
                    self.Fighter.moviment.mvDir = 1
                    #self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isMovingRight()):
                    self.Fighter.moviment.mvDir = 0
                    #self.Fighter.changeState(States.f_moving())
                elif(self.Fighter.machine.isJumping()):
                    if (self.Fighter.moviment.jumping == False):
                        self.Fighter.moviment.jumping = True
                        self.Fighter.changeState(States.f_jumping_moving())
                elif(self.Fighter.machine.isPunching()):
                    self.Fighter.changeState(States.f_punching())
                elif(self.Fighter.machine.isKicking()):
                    self.Fighter.machine.kick = False
                else:
                    self.Fighter.changeState(States.f_stopped())"""


        def Exit(self):
            pass
    ###
    #   Scenario States
    ###
    class s_default(State):
        def __init__(self):
            self.pScene = None
        def Enter(self, pScene):
            self.pScene = pScene
            self.pScene.frameNum = (self.pScene.frameNum + 1)%len(self.pScene.frames)
            print(self.pScene.frameNum)
            self.pScene.curFrame = self.pScene.frames[self.pScene.frameNum]

        def Execute(self,  message):
            if(self.pScene.cooldown <= 0):
                self.pScene.frameNum = (self.pScene.frameNum + 1)%len(self.pScene.frames)
                self.pScene.curFrame = self.pScene.frames[self.pScene.frameNum]
                self.pScene.cooldown = self.pScene.frameCooldown

            self.pScene.cooldown = self.pScene.cooldown - 1

        def Exit(self):
            pass

