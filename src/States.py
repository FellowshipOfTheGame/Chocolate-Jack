#coding: utf-8
import pygame
import sys
import Fighters

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
        
    def Execute(self,Fighter, message):
        #considerando que a primeira metade tem movimentos facing right e a segunda facing left
        halfQtdFrames = int(len(Fighter.stopFrames)/2)

        Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames) + Fighter.facing*halfQtdFrames
        Fighter.curFrame = Fighter.stopFrames[Fighter.frameNum]

        #CHANGE STATES
        if(message == 'mvLKeyPressed'):
            Fighter.mvDir = 1
            Fighter.changeState(f_moving())
        elif(message == 'mvRKeyPressed'):
            Fighter.mvDir = 0
            Fighter.changeState(f_moving())
        elif(message == 'mvUKeyPressed'):
            print ("u")
            if (Fighter.jumping == False):
                Fighter.jumping = True
                Fighter.changeState(f_jumping_stopped())
        elif(message == 'pcKeyPressed'):
            Fighter.changeState(f_punching())
        elif(message == 'kcKeyPressed'):
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

    def Execute(self,Fighter, message):
        if(Fighter.mvCooldown <= 0):
            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            halfQtdFrames = int(len(Fighter.movFrames)/2)

            Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames) + Fighter.mvDir*halfQtdFrames
            Fighter.curFrame = Fighter.movFrames[Fighter.frameNum]

            #Posicao aumenta em mvInc caso dir igual a 0 (indo para a dir), caso contrario decrementa.
            Fighter.px = Fighter.px + (Fighter.mvDir*(-2)+1)*Fighter.mvInc
            Fighter.drawPx = Fighter.px
            Fighter.mvCooldown = Fighter.mvMaxCooldown + 1 #esse +1 serah removido na linha seguinte

        Fighter.mvCooldown = Fighter.mvCooldown - 1

        #CHANGE STATE
        if(message == 'mvLKeyPressed'):
            Fighter.mvDir = 1
            Fighter.changeState(f_moving())
        elif(message == 'mvRKeyPressed'):
            Fighter.mvDir = 0
            Fighter.changeState(f_moving())
        elif(message == 'mvUKeyPressed'):
            if (Fighter.jumping == False):
                Fighter.jumping = True
                Fighter.changeState(f_jumping_moving())
        elif(message == 'pcKeyPressed'):
            Fighter.changeState(f_punching())
        elif(message == 'kcKeyPressed'):
            Fighter.changeState(f_kicking())
        elif(message == 'mvLKeyReleased'):
            #so para o movimento caso o release seja da tecla certa.
            if(Fighter.mvDir==1):
                Fighter.changeState(f_stopped())
                
        elif (message == 'mvRKeyReleased'):
            #so para o movimento caso o release seja da tecla certa.
            if(Fighter.mvDir==0):
                Fighter.changeState(f_stopped())

        
    def Exit(self,Fighter):
        pass

class f_jumping_stopped(States):

    def Enter(self, Fighter):
        print ("pulando")
        self.force = Fighter.getForceJump()
        Fighter.jumping = True
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
                Fighter.changeState(f_stopped())
            elif (self.force <0):
                self.force = self.force *2
                Fighter.py -= self.force
                pass
            else:
                self.force = -self.force
            
        Fighter.mvCooldown = Fighter.mvCooldown - 1
        #CHANGE STATES
        #if(message == 'pcKeyPressed'):
        #    Fighter.changeState(f_punching())
        #elif(message == 'kcKeyPressed'):
        #    Fighter.changeState(f_kicking())

    def Exit(self,Fighter):
        Fighter.jumping = False

###
class f_jumping_moving(States):

    def Enter(self,Fighter):
        self.force = 50
        Fighter.jumping = True
        
        Fighter.drawPx = Fighter.px
        Fighter.drawPy = Fighter.py
        Fighter.mvCooldown = 0
        Fighter.frameNum = -1

    def Execute(self,Fighter, message):
        if(Fighter.mvCooldown <= 0):
            #considerando que a primeira metade tem movimentos facing right e a segunda facing left
            halfQtdFrames = int(len(Fighter.movFrames)/2)

            Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames) + Fighter.mvDir*halfQtdFrames
            Fighter.curFrame = Fighter.movFrames[Fighter.frameNum]

            #Posicao aumenta em mvInc caso dir igual a 0 (indo para a dir), caso contrario decrementa.
            Fighter.px = Fighter.px + (Fighter.mvDir*(-2)+1)*Fighter.mvInc
            Fighter.drawPx = Fighter.px
            Fighter.drawPy = Fighter.py
            Fighter.mvCooldown = Fighter.mvMaxCooldown + 1 #esse +1 serah removido na linha seguinte
            
        if (self.force >=1):
            Fighter.py -= self.force
            self.force = self.force /2
        elif (self.force <=-50):
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
        Fighter.pcCooldown = Fighter.pcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
        Fighter.frameNum = -1

    def Execute(self, Fighter, message):
        if(Fighter.pcCooldown <=0):
            halfQtdFrames = int(len(Fighter.pcFrames)/2)

            Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames+1)
            if(Fighter.frameNum >= halfQtdFrames):
                Fighter.changeState(f_stopped())
                return
                
            Fighter.curFrame = Fighter.pcFrames[Fighter.frameNum+Fighter.facing*halfQtdFrames]

            #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
            #Fighter.pcPx = Fighter.px - Fighter.facing*Fighter.pcDist
            Fighter.pcPx = Fighter.px - (Fighter.facing)*(Fighter.pcDist)
            Fighter.pcPy = Fighter.py
            Fighter.drawPx = Fighter.pcPx
            Fighter.drawPy = Fighter.pcPy
            Fighter.pcCooldown = Fighter.pcMaxCooldown + 1 #esse +1 serah removido na linha seguinte

            #fazer um parametro para que o Fighter tenha um "ponteiro" para seu inimigo depois
            #enemy = Fighters.Alvo(611,0)

            #checando colisao
            for coll in Fighter.curFrame.getCollisionsRect(Fighter.pcPx, Fighter.pcPy):
                if(coll.collidelist(Fighter.enemy.curFrame.getCollisionsRect(Fighter.enemy.drawPx,
                                                                             Fighter.enemy.drawPy)) > -1):
                    Fighter.soco = 1
                    Fighter.enemy.hp = Fighter.enemy.hp - (Fighter.attack - Fighter.enemy.defense)
                    #fazer enemy.getHit()

        Fighter.pcCooldown = Fighter.pcCooldown - 1


        #CHANGE STATES
        if(message == 'mvLKeyPressed'):
            Fighter.mvDir = 1
            Fighter.changeState(f_moving())
        elif(message == 'mvRKeyPressed'):
            Fighter.mvDir = 0
            Fighter.changeState(f_moving())
        elif(message == 'kcKeyPressed'):
            Fighter.changeState(f_kicking())
        elif(message == 'mvLKeyReleased'):
            #so para o movimento caso o release seja da tecla certa.
            if(Fighter.mvDir==1):
                Fighter.changeState(f_stopped())
                
        elif (message == 'mvRKeyReleased'):
            #so para o movimento caso o release seja da tecla certa.
            if(Fighter.mvDir==0):
                Fighter.changeState(f_stopped())    

    def Exit(self, Fighter):
        pass

###
class f_kicking(States):

    def Enter(self, Fighter):
        Fighter.kcCooldown = Fighter.kcMaxCooldown #ele ira demorar para comecar o soco, ao contrario de mv
        Fighter.frameNum = -1

    def Execute(self, Fighter, message):
        if(Fighter.kcCooldown <=0):
            halfQtdFrames = int(len(Fighter.kcFrames)/2)

            Fighter.frameNum = (Fighter.frameNum + 1)%(halfQtdFrames+1)
            if(Fighter.frameNum >= halfQtdFrames):
                Fighter.changeState(f_stopped())
                return
                
            Fighter.curFrame = Fighter.kcFrames[Fighter.frameNum+Fighter.facing*halfQtdFrames]

            #Caso o char esteja socando apara a esquerda da tela, decrementa pcDist da posicao de soco.
            #Fighter.pcPx = Fighter.px - Fighter.facing*Fighter.pcDist
            Fighter.kcPx = Fighter.px - (Fighter.facing)*(Fighter.kcDist)
            Fighter.kcPy = Fighter.py
            Fighter.drawPx = Fighter.kcPx
            Fighter.drawPy = Fighter.kcPy
            Fighter.kcCooldown = Fighter.kcMaxCooldown + 1 #esse +1 serah removido na linha seguinte

            #fazer um parametro para que o Fighter tenha um "ponteiro" para seu inimigo depois
            #enemy = Fighters.Alvo(611,0)

            #checando colisao
            for coll in Fighter.curFrame.getCollisionsRect(Fighter.kcPx, Fighter.kcPy):
                if(coll.collidelist(Fighter.enemy.curFrame.getCollisionsRect(Fighter.enemy.drawPx,
                                                                             Fighter.enemy.drawPy)) > -1):
                    Fighter.chute = 1
                    #fazer enemy.getHit().

        Fighter.kcCooldown = Fighter.kcCooldown - 1

        #CHANGE STATES
        if(message == 'mvLKeyPressed'):
            Fighter.mvDir = 1
            Fighter.changeState(f_moving())
        elif(message == 'mvRKeyPressed'):
            Fighter.mvDir = 0
            Fighter.changeState(f_moving())
        elif(message == 'pcKeyPressed'):
            Fighter.changeState(f_punching())
        elif(message == 'mvLKeyReleased'):
            #so para o movimento caso o release seja da tecla certa.
            if(Fighter.mvDir==1):
                Fighter.changeState(f_stopped())
                
        elif (message == 'mvRKeyReleased'):
            #so para o movimento caso o release seja da tecla certa.
            if(Fighter.mvDir==0):
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

