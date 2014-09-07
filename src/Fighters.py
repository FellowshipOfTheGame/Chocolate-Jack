#coding: utf-8
import pygame
import States
import sys
import Frame
from utils import safe_load

###
#   Fighters
###
class FighterStates:
    def __init__(self, Fighter):
        self.states = {}
        self.frames = {}
        self.direction = {}
        self.lastState = None
        self.Fighter = Fighter
    def add(self,thisState, key, action='f_stopped', frames=[]):
        if ((key != 'null' and key != '*')and action == 'f_stopped'):
            print ('['+thisState+','+key+'] => '+ action)
            exit('não pode haver um estado parado com key didferente de null')
        self.states[(thisState, key)] = action
        self.frames[(thisState, key)] = frames
    def addM(self,thisState, key, action='f_stopped', frames=[], direction=-1):
        if ((key != 'null' and key != '*')and action == 'f_stopped'):
            print ('['+thisState+','+key+'] => '+ action)
            exit('não pode haver um estado parado com key didferente de null')
        self.states[(thisState, key)] = action
        self.frames[(thisState, key)] = frames
        self.direction[(action, key)] = direction
    def getAction(self,thisState, key, optional = False):
        #  if(self.player == 1):
        #print(thisState)
        #print(key)
        #print(" ")

        self.lastState = getattr(States.States(),thisState)()
        # if (hasattr(self.lastState, 'isMovimentState') and optional):
        #     temp =  [state_key for state_key, state_value in self.states
        #         .items()  if state_value == thisState][0]
        #     if(self.Fighter.player == 1):
        #         print("retornou no isMoviment")
        #         print(self.states.get(temp), self.frames.get(temp))
        #     return self.states.get(temp), self.frames.get(temp)
        state, frame, direction = None, None, -1
        if (key == "null" or 'Released' in key):
            temp =  [state_key for state_key, state_value in self.states
                .items()  if state_value == 'f_stopped'][0]
            state = self.states.get(temp)
            frame = self.frames.get(temp)

        elif (key == '*'):
            temp =  [state_key for state_key, state_value in self.states
                .items()  if thisState in state_key][0]
            state = self.states.get(temp)
            frame = self.frames.get(temp)

        elif ((thisState, key) in self.states):
            state = self.states.get((thisState, key))
            frame = self.frames.get((thisState, key))
        else:
            temp =  [state_key for state_key, state_value in self.states
                .items()  if state_value == 'f_stopped'][0]
            state = self.states.get(temp)
            frame = self.frames.get(temp)
    
        if (state, key) in self.direction:
            direction = self.direction [(state, key)]
        return state, frame, direction    

class VitalAtrr:
    def __init__(self):
        self.hp = 1
        self.maxHp = 1
        self.mp = 0
        self.maxMP = 0

class CombatAtrr:
    def __init__(self):
        self.attack = 0
        self.defense = 0
        self.sp1DG = 0
        self.sp2DMG = 0
        self.spUltDMG = 0
        self.sp1Cost = 0
        self.sp2Cost = 0
        self.setpUltCost = 0

class MovimentAttr:
    def __init__(self):
        self.mvInc = 0
        self.mvDir = 0

        self.jumping = False

class Fighter:
    #Contrutor
    def __init__(self, pPyFloor = 0, pFacing=0, pPlayer = 1):
        self.player = pPlayer
        self.enemy = None

        self.px = 32 + pFacing*992
        self.heigth = 32
        self.py = pPyFloor - self.heigth
        self.facing = pFacing
        self.curFrame = 0

        self.debugTrue = 0
        self.height = 0
        self.width = 0

        self.drawPx = self.px
        self.drawPy = self.py

        self.frameNum = 0

        self.vital = VitalAtrr()
        self.combat = CombatAtrr
        self.moviment = MovimentAttr()
        self.states = FighterStates(self)
        self.lastMessage = 'null'

    #troca de estado
    def changeState(self, pNewState):
        if(self.player == 1):
            print(pNewState[2])
        self.curState.Exit()
        if pNewState[2] != -1:
            self.moviment.mvDir = pNewState[2]
        self.curState = getattr(States.States,pNewState[0])()
        self.curState.Enter(self, pNewState[1])

    #atualiza a posicao que o char olha
    #estah simplificada, o char olha sempre pro meio da tela.
    def facingUpdate(self):
        if(self.enemy != None):

            if(self.px > self.enemy.px):
                self.facing = 1
            else:
                self.facing = 0

        else:
            if(self.px > 512):
                self.facing = 1
            else:
                self.facing = 0



    #act
    def Update(self, message):
        self.facingUpdate()
        if (self.lastMessage != message and message !='null'
            or (self.lastMessage == 'pcKeyPressed' or  self.lastMessage == 'kcKeyPressed'
            or self.lastMessage == 'mvUKeyPressed')):
            self.lastMessage = message

        self.curState.Execute(self.lastMessage)

    #draw
    def draw(self, tela):
        img = safe_load(pygame.image.load, self.curFrame.img).convert_alpha()
        tela.blit(img, (self.drawPx, self.drawPy))

        if(self.debugTrue == 1):
            color = pygame.Color(255, 128, 128, 196)
            for colRect in self.curFrame.getCollisions():
                rectParams = (colRect[0] + self.drawPx, colRect[1] + self.drawPy, colRect[2], colRect[3])
                rect = pygame.Rect(rectParams)
                pygame.draw.rect(tela, color, rect)

    def toogleDebug(self):
        self.debugTrue = (self.debugTrue + 1)%2 #farah com que troque de 0 para 1 e vice-versa

    def setEnemy(self, pEnemy):
        self.enemy = pEnemy
    def drawChoise(self, tela, pdx, pdy):
        img = safe_load(pygame.image.load, self.curFrame.img).convert_alpha()
        #img = pygame.transform.scale(img, (94, 128))
        #print(self.pcx, self.pcy)
        tela.blit(img, (pdx, pdy))


        if(self.debugTrue == 1):
            color = pygame.Color(255, 128, 128, 196)
            for colRect in self.curFrame.getCollisions():
                rectParams = (colRect[0] + self.drawPx, colRect[1] + self.drawPy, colRect[2], colRect[3])
                rect = pygame.Rect(rectParams)
                pygame.draw.rect(tela, color, rect)
    def getName(self):
        return self.__class__.__name__

class Fighters:
    class Tank(Fighter):

        def __init__(self, pPyFloor = 0, pFacing=0, pPlayer=1):
            super().__init__(pPyFloor, pFacing, pPlayer)

            self.px = 32 + pFacing*992
            self.width = 128
            self.height = 128
            self.py = pPyFloor - self.height
            self.drawPx = self.px
            self.drawPy = self.py
            self.facing = pFacing

            #criando frames stopped
            sFrame1 = Frame.Frame('data\\imgs\\tank.png')

            #atribuindo frames
            self.stopFrames = [sFrame1, sFrame1]

            self.states.add('*', 'null', 'f_stopped', self.stopFrames)

            #criando frames de movimento
            mvFrameR1 = Frame.Frame('data\\imgs\\tankMvFR1.png')
            mvFrameR2 = Frame.Frame('data\\imgs\\tankMvFR2.png')
            mvFrameR3 = Frame.Frame('data\\imgs\\tankMvFR3.png')
            mvFrameL1 = Frame.Frame('data\\imgs\\tankMvFL1.png')
            mvFrameL2 = Frame.Frame('data\\imgs\\tankMvFL2.png')
            mvFrameL3 = Frame.Frame('data\\imgs\\tankMvFL3.png')

            #atribuindo frames
            self.movFrames = (mvFrameR1,mvFrameR2,mvFrameR3,mvFrameL1,mvFrameL2,mvFrameL3)

            self.states.addM('f_stopped','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_moving','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_punching','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_kicking','mvLKeyPressed','f_moving',
                            self.movFrames, 1)

            self.states.addM('f_stopped','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_moving','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_punching','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_kicking','mvRKeyPressed','f_moving',
                            self.movFrames, 0)


            #criando frames de soco
            pcFrame1 = Frame.Frame('data\\imgs\\punchtankR.png')
            pcFrame2 = Frame.Frame('data\\imgs\\punchtankL.png')

            #atribuindo frames
            self.pcFrames = (pcFrame1,pcFrame2)

            self.states.add('f_stopped','pcKeyPressed','f_punching',
                            self.movFrames)
            self.states.add('f_moving','pcKeyPressed','f_punching',
                            self.movFrames)

            self.moviment.mvInc = 64

    class Alvo(Fighter):
        def __init__(self, pPyFloor=0, pFacing=0, pPlayer = 1):
            #player
            self.player = pPlayer

            #atributos/habilidades
            self.hp = 1
            self.maxHp = 1
            self.mp = 0
            self.maxMP = 0
            self.attack = 0
            self.defense = 0
            self.sp1DMG = 0
            self.sp2DMG = 0
            self.spUltDMG = 0
            self.sp1Cost = 0
            self.sp2Cost = 0
            self.setpUltCost = 0

            #Outros
            self.debugTrue = 0
            self.soco = 0
            self.chute = 0

            self.px = 512
            self.height = 288
            self.width = 64
            self.py = pPyFloor - self.height
            self.drawPx = self.px
            self.drawPy = self.py
            self.facing = pFacing
            frame = Frame.Frame('data\\imgs\\alvo.png')
            frame.addCollision(0,0, 64,248)
            self.stopFrames = [frame,frame]
            self.movFrames = [frame,frame]
            self.pcFrames = [frame,frame]
            self.kcFrames = [frame,frame]
            self.mvInc = 0
            self.pcDist = 0
            self.mvMaxCooldown = 0
            self.mvCooldown = 0
            self.pcMaxCooldown = 0
            self.pcCooldown = 0
            self.curState = States.States.f_stopped()
            self.curState.Enter(self)
            self.kcDist = 0
            self.kcMaxCooldown = 0
            self.kcCooldown = 0

    class Alvo2(Fighter):
        def __init__(self, pPyFloor=0, pFacing=0, pPlayer = 1):
            #player
            self.player = pPlayer

            #atributos/habilidades
            self.hp = 320
            self.maxHp = 320
            self.mp = 0
            self.maxMP = 0
            self.attack = 0
            self.defense = 80
            self.sp1DMG = 0
            self.sp2DMG = 0
            self.spUltDMG = 0
            self.sp1Cost = 0
            self.sp2Cost = 0
            self.setpUltCost = 0

            #outros
            self.debugTrue = 0
            self.soco = 0
            self.chute = 0

            self.px = 420
            self.height = 288
            self.width = 195
            self.py = pPyFloor - self.height + 18
            self.drawPx = self.px
            self.drawPy = self.py
            self.facing = pFacing
            frame = Frame.Frame('data\\imgs\\alvo2.png')
            frame.addCollision(10,10, 185,278)
            self.stopFrames = [frame,frame]
            self.movFrames = [frame,frame]
            self.pcFrames = [frame,frame]
            self.kcFrames = [frame,frame]
            self.mvInc = 0
            self.pcDist = 0
            self.mvMaxCooldown = 0
            self.mvCooldown = 0
            self.pcMaxCooldown = 0
            self.pcCooldown = 0
            self.curState = States.States.f_stopped()
            self.curState.Enter(self)
            self.kcDist = 0
            self.kcMaxCooldown = 0
            self.kcCooldown = 0

    class ChocoJack(Fighter):
        def __init__(self, pPyFloor=0, pFacing=0, pPlayer=1):
            Fighter.__init__(self)
            #player
            self.player = pPlayer

            #atributos/habilidades
            self.hp = 240
            self.maxHp = 240
            self.mp = 0
            self.maxMP = 0
            self.attack = 1
            self.defense = 0
            self.sp1DMG = 0
            self.sp2DMG = 0
            self.spUltDMG = 0
            self.sp1Cost = 0
            self.sp2Cost = 0
            self.setpUltCost = 0
            self.forceJump = 100

            #outros
            self.debugTrue = 0
            self.soco = 0
            self.chute = 0


            self.width = 94
            self.px = 32 + pFacing*(1024 - 64 - self.width)
            self.height = 128
            self.py = pPyFloor - self.height
            self.drawPx = self.px
            self.drawPy = self.py
            self.facing = pFacing

            #criando frames stopped
            sFrameR = Frame.Frame('data\\imgs\\ChocolateJack\\IdleRight\\stpJackFR1.png')
            sFrameR.addCollision(9,0,64,128)
            sFrameL = Frame.Frame('data\\imgs\\ChocolateJack\\IdleLeft\\stpJackFL1.png')
            sFrameL.addCollision(22,0,64,128)

            #atribuindo frames
            self.stopFrames = [sFrameR, sFrameL]

            #criando frames de movimento
            mvFrameR1 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR1.png')
            mvFrameR1.addCollision(10,0,64,128)

            mvFrameR2 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR2.png')
            mvFrameR2.addCollision(6,0,64,128)

            mvFrameR3 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR3.png')
            mvFrameR3.addCollision(6,0,64,128)

            mvFrameR4 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR4.png')
            mvFrameR4.addCollision(6,0,64,128)

            mvFrameR5 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR5.png')
            mvFrameR5.addCollision(6,0,64,128)

            mvFrameR6 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR6.png')
            mvFrameR6.addCollision(6,0,64,128)

            mvFrameR7 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR7.png')
            mvFrameR7.addCollision(6,0,64,128)

            mvFrameR8 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR8.png')
            mvFrameR8.addCollision(6,0,64,128)

            mvFrameR9 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR9.png')
            mvFrameR9.addCollision(6,0,64,128)

            mvFrameR10 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR10.png')
            mvFrameR10.addCollision(6,0,64,128)

            mvFrameR11 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR11.png')
            mvFrameR11.addCollision(6,0,64,128)

            mvFrameR12 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR12.png')
            mvFrameR12.addCollision(6,0,64,128)

            mvFrameR13 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR13.png')
            mvFrameR13.addCollision(6,0,64,128)

            mvFrameR14 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR14.png')
            mvFrameR14.addCollision(6,0,64,128)

            mvFrameR15 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR15.png')
            mvFrameR15.addCollision(6,0,64,128)

            mvFrameR16 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveRight\\mvJackFR16.png')
            mvFrameR16.addCollision(6,0,64,128)

            mvFrameL1 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL1.png')
            mvFrameL1.addCollision(12,0,64,128)

            mvFrameL2 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL2.png')
            mvFrameL2.addCollision(18,0,64,128)

            mvFrameL3 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL3.png')
            mvFrameL3.addCollision(18,0,64,128)

            mvFrameL4 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL4.png')
            mvFrameL4.addCollision(18,0,64,128)

            mvFrameL5 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL5.png')
            mvFrameL5.addCollision(18,0,64,128)

            mvFrameL6 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL6.png')
            mvFrameL6.addCollision(18,0,64,128)

            mvFrameL7 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL7.png')
            mvFrameL7.addCollision(18,0,64,128)

            mvFrameL8 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL8.png')
            mvFrameL8.addCollision(18,0,64,128)

            mvFrameL9 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL9.png')
            mvFrameL9.addCollision(18,0,64,128)

            mvFrameL10 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL10.png')
            mvFrameL10.addCollision(18,0,64,128)

            mvFrameL11 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL11.png')
            mvFrameL11.addCollision(18,0,64,128)

            mvFrameL12 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL12.png')
            mvFrameL12.addCollision(18,0,64,128)

            mvFrameL13 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL13.png')
            mvFrameL13.addCollision(18,0,64,128)

            mvFrameL14 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL14.png')
            mvFrameL14.addCollision(18,0,64,128)

            mvFrameL15 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL15.png')
            mvFrameL15.addCollision(18,0,64,128)

            mvFrameL16 = Frame.Frame('data\\imgs\\ChocolateJack\\MoveLeft\\mvJackFL16.png')
            mvFrameL16.addCollision(18,0,64,128)

            #atribuindo frames
            self.movFrames = [mvFrameR1,mvFrameR2,mvFrameR3,mvFrameR4,mvFrameR5 \
                ,mvFrameR6,mvFrameR7,mvFrameR8,mvFrameR9,mvFrameR10 \
                ,mvFrameR11,mvFrameR12,mvFrameR13,mvFrameR14,mvFrameR15,mvFrameR16 \
                ,mvFrameL1,mvFrameL2,mvFrameL3,mvFrameL4,mvFrameL5 \
                ,mvFrameL6,mvFrameL7,mvFrameL8,mvFrameL9,mvFrameL10 \
                ,mvFrameL11,mvFrameL12,mvFrameL13,mvFrameL14,mvFrameL15,mvFrameL16 ]

            #criando frames de soco
            pcFrameR1 = Frame.Frame('data\\imgs\\ChocolateJack\\PunchRight\\pc2JackFR1.png')
            pcFrameR1.addCollision(9,0,64,128) #corpo
            pcFrameR1.addCollision(92,54,34,32) #punho

            pcFrameR2= Frame.Frame('data\\imgs\\ChocolateJack\\PunchRight\\pc2JackFR2.png')
            pcFrameR2.addCollision(9,0,64,128) #corpo
            pcFrameR2.addCollision(92,54,34,32) #punho

            pcFrameL1 = Frame.Frame('data\\imgs\\ChocolateJack\\PunchLeft\\pc2JackFL1.png')
            pcFrameL1.addCollision(29,0,64,128) #corpo
            pcFrameL1.addCollision(0,53,34,32) #punho

            pcFrameL2 = Frame.Frame('data\\imgs\\ChocolateJack\\PunchLeft\\pc2JackFL2.png')
            pcFrameL2.addCollision(29,0,64,128) #corpo
            pcFrameL2.addCollision(0,53,34,32) #punho

            #atribuindo frames
            self.pcFrames = [pcFrameR1,pcFrameR2,pcFrameR1,pcFrameL1,pcFrameL2,pcFrameL1]

            #criando frames de chute
            kcFrameR1 = Frame.Frame('data\\imgs\\ChocolateJack\\KickRight\\kcJackFR1.png')
            kcFrameR1.addCollision(10,0,64,128) #corpo
            kcFrameR1.addCollision(62,106,20,20) #pe

            kcFrameR2 = Frame.Frame('data\\imgs\\ChocolateJack\\KickRight\\kcJackFR2.png')
            kcFrameR2.addCollision(10,0,64,128) #corpo
            kcFrameR2.addCollision(68,98,20,20) #pe

            kcFrameR3 = Frame.Frame('data\\imgs\\ChocolateJack\\KickRight\\kcJackFR3.png')
            kcFrameR3.addCollision(10,0,64,128) #corpo
            kcFrameR3.addCollision(62,106,20,20) #pe

            kcFrameR4 = Frame.Frame('data\\imgs\\ChocolateJack\\KickRight\\kcJackFR4.png')
            kcFrameR4.addCollision(10,0,64,128) #corpo
            kcFrameR4.addCollision(68,98,20,20) #pe

            kcFrameR5 = Frame.Frame('data\\imgs\\ChocolateJack\\KickRight\\kcJackFR5.png')
            kcFrameR5.addCollision(10,0,64,128) #corpo
            kcFrameR5.addCollision(68,98,20,20) #pe            

            kcFrameL1 = Frame.Frame('data\\imgs\\ChocolateJack\\KickLeft\\kcJackFL1.png')
            kcFrameL1.addCollision(22,0,64,128) #corpo
            kcFrameL1.addCollision(13,106,20,20) #pe

            kcFrameL2 = Frame.Frame('data\\imgs\\ChocolateJack\\KickLeft\\kcJackFL2.png')
            kcFrameL2.addCollision(22,0,64,128) #corpo
            kcFrameL2.addCollision(6,98,20,20) #pe

            kcFrameL3 = Frame.Frame('data\\imgs\\ChocolateJack\\KickLeft\\kcJackFL3.png')
            kcFrameL3.addCollision(10,0,64,128) #corpo
            kcFrameL3.addCollision(62,106,20,20) #pe

            kcFrameL4 = Frame.Frame('data\\imgs\\ChocolateJack\\KickLeft\\kcJackFL4.png')
            kcFrameL4.addCollision(10,0,64,128) #corpo
            kcFrameL4.addCollision(68,98,20,20) #pe

            kcFrameL5 = Frame.Frame('data\\imgs\\ChocolateJack\\KickLeft\\kcJackFL5.png')
            kcFrameL5.addCollision(10,0,64,128) #corpo
            kcFrameL5.addCollision(68,98,20,20) #pe            

            #atribuindo frames
            self.kcFrames = [kcFrameR1, kcFrameR2, kcFrameR3, kcFrameR4, kcFrameR5,
                             kcFrameL1, kcFrameL2, kcFrameL3, kcFrameL4, kcFrameL5]


            #criando frames do pulo
            jpFrameR1 = Frame.Frame('data\\imgs\\ChocolateJack\\JumpRight\\jpJackFR1.png')

            jpFrameL1 = Frame.Frame('data\\imgs\\ChocolateJack\\JumpLeft\\jpJackFL1.png')


            #atribuindo frames
            self.jpFrames = [jpFrameR1, jpFrameL1]

            self.mvInc = 8
            self.pcDist = 8
            self.mvMaxCooldown = 3
            self.mvCooldown = 0
            self.pcMaxCooldown = 0
            self.pcCooldown = 0
            self.kcDist = 0
            self.kcMaxCooldown = 0
            self.kcCooldown = 0

            self.moviment.mvInc = 12;

            self.moviment.jumping = False

            self.states.add('*','null','f_stopped',
                            self.stopFrames)

            self.states.addM('f_stopped','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_stopped','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.add('f_stopped','mvUKeyPressed','f_jumping_stopped',
                            self.jpFrames)
            self.states.addM('f_stopped','pcKeyPressed','f_punching',
                            self.pcFrames)
            self.states.addM('f_stopped','kcKeyPressed','f_kicking',
                            self.kcFrames)

            self.states.addM('f_moving','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_moving','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.add('f_moving','mvUKeyPressed','f_jumping_moving',
                            self.movFrames)
            self.states.add('f_moving','pcKeyPressed','f_punching',
                            self.movFrames)
            self.states.add('f_moving','kcKeyPressed','f_kicking',
                            self.movFrames)


            self.states.addM('f_punching','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_punching','mvLKeyPressed','f_moving',
                            self.movFrames, 1)

            self.states.addM('f_kicking','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_kicking','mvRKeyPressed','f_moving',
                            self.movFrames, 0)


            self.states.add('f_jumping_moving','*','f_moving',
                            self.movFrames)

            self.states.add('f_jumping_stopped','*','f_stopped',
                            self.stopFrames)

            #combos
            self.states.add('f_punching','pcKeyPressed','f_punching_2',
                            self.pcFrames)
            self.states.add('f_punching_2','pcKeyPressed','f_punching_3',
                            self.pcFrames)
            self.states.add('f_punching_3','null','f_stopped',
                            self.stopFrames)




            self.curState = States.States.f_stopped()
            self.curState.Enter(self, self.stopFrames)
            self.curFrame = self.stopFrames[0]


        def getForceJump(self):
            #print(self.forceJump)
            return self.forceJump

    class BrocolisNinja(Fighter):
        def __init__(self, pPyFloor=0, pFacing=0, pPlayer = 1):
            Fighter.__init__(self)
            #player
            self.player = pPlayer

            #atributos/habilidades
            self.hp = 320
            self.maxHp = 320
            self.mp = 0
            self.maxMP = 0
            self.attack = 1
            self.defense = 0
            self.sp1DMG = 0
            self.sp2DMG = 0
            self.spUltDMG = 0
            self.sp1Cost = 0
            self.sp2Cost = 0
            self.setpUltCost = 0
            self.forceJump = 100

            #outros
            self.debugTrue = 0
            self.soco = 0
            self.chute = 0

            self.height = 148
            self.width = 195
            self.px = 32 + pFacing*(1024 - 64 - self.width)
            self.py = pPyFloor - self.height + 18
            self.drawPx = self.px
            self.drawPy = self.py
            self.facing = pFacing

            self.moviment.mvInc = 12;


            #criando frames stopped
            sFrameR = Frame.Frame('data\\imgs\\BrocolisNinja\\IdleRight\\idle.png')
            sFrameR.addCollision(77,41, 48,99)
            sFrameL = Frame.Frame('data\\imgs\\BrocolisNinja\\IdleLeft\\idle.png')
            sFrameL.addCollision(77,41, 48,99)

            #atribuindo frames            
            self.stopFrames = [sFrameR, sFrameL]

            #criando frames movimento
            mvFrameR1 = Frame.Frame('data\\imgs\\BrocolisNinja\\WalkRight\\walk1right.png')
            mvFrameR2 = Frame.Frame('data\\imgs\\BrocolisNinja\\WalkRight\\walk2right.png')
            mvFrameL1 = Frame.Frame('data\\imgs\\BrocolisNinja\\WalkLeft\\walk1left.png')
            mvFrameL2 = Frame.Frame('data\\imgs\\BrocolisNinja\\WalkLeft\\walk2left.png')

            #atribuindo frames 
            self.movFrames = [mvFrameR1,mvFrameR2, mvFrameL1, mvFrameL2]

            #criando frames de attack1
            pcFrameR1 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackRight\\hpRight1.png')
            pcFrameR1.addCollision(9,0,64,128) #corpo
            #TODO arrumar caixa de colisão da espada, cada linha deve ter a
            # caixa de uma parte da espada
            pcFrameR1.addCollision(92,54,34,32) #espada
            pcFrameR1.addCollision(92,54,34,32) #espada
            pcFrameR1.addCollision(92,54,34,32) #espada

            pcFrameR2 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackRight\\hpRight2.png')
            pcFrameR2.addCollision(9,0,64,128) #corpo
            #TODO arrumar caixa de colisão da espada, cada linha deve ter a
            # caixa de uma parte da espada
            pcFrameR2.addCollision(92,54,34,32) #espada
            pcFrameR2.addCollision(92,54,34,32) #espada
            pcFrameR2.addCollision(92,54,34,32) #espada

            pcFrameR3 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackRight\\hpRight3.png')
            pcFrameR3.addCollision(9,0,64,128) #corpo
            pcFrameR3.addCollision(92,54,34,32) #espada
            pcFrameR3.addCollision(92,54,34,32) #espada
            pcFrameR3.addCollision(92,54,34,32) #espada

            pcFrameR4 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackRight\\hpRight4.png')
            pcFrameR4.addCollision(9,0,64,128) #corpo
            pcFrameR4.addCollision(92,54,34,32) #espada
            pcFrameR4.addCollision(92,54,34,32) #espada
            pcFrameR4.addCollision(92,54,34,32) #espada

            pcFrameL1 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackLeft\\hpLeft1.png')
            pcFrameL1.addCollision(9,0,64,128) #corpo
            #TODO arrumar caixa de colisão da espada, cada linha deve ter a
            # caixa de uma parte da espada
            pcFrameL1.addCollision(92,54,34,32) #espada
            pcFrameL1.addCollision(92,54,34,32) #espada
            pcFrameL1.addCollision(92,54,34,32) #espada

            pcFrameL2 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackLeft\\hpLeft2.png')
            pcFrameL2.addCollision(9,0,64,128) #corpo
            #TODO arrumar caixa de colisão da espada, cada linha deve ter a
            # caixa de uma parte da espada
            pcFrameL2.addCollision(92,54,34,32) #espada
            pcFrameL2.addCollision(92,54,34,32) #espada
            pcFrameL2.addCollision(92,54,34,32) #espada

            pcFrameL3 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackLeft\\hpLeft3.png')
            pcFrameL3.addCollision(9,0,64,128) #corpo
            #TODO arrumar caixa de colisão da espada, cada linha deve ter a
            # caixa de uma parte da espada
            pcFrameL3.addCollision(92,54,34,32) #espada
            pcFrameL3.addCollision(92,54,34,32) #espada
            pcFrameL3.addCollision(92,54,34,32) #espada

            pcFrameL4 = Frame.Frame('data\\imgs\\BrocolisNinja\\AttackLeft\\hpLeft4.png')
            pcFrameL4.addCollision(9,0,64,128) #corpo
            #TODO arrumar caixa de colisão da espada, cada linha deve ter a
            # caixa de uma parte da espada
            pcFrameL4.addCollision(92,54,34,32) #espada
            pcFrameL4.addCollision(92,54,34,32) #espada
            pcFrameL4.addCollision(92,54,34,32) #espada

            #atribuindo frames attack1
            self.pcFrames = [pcFrameR1,pcFrameR2, pcFrameR3, pcFrameR4, pcFrameL1, pcFrameL2, pcFrameL3, pcFrameL4]
            self.kcFrames = [pcFrameR1,pcFrameR2, pcFrameR3, pcFrameR4, pcFrameL1, pcFrameL2, pcFrameL3, pcFrameL4]
            self.jpFrames = [sFrameR,sFrameL]

            self.mvInc = 8
            self.pcDist = 8
            self.mvMaxCooldown = 5
            self.mvCooldown = 0
            self.pcMaxCooldown = 0
            self.pcCooldown = 0
            self.kcDist = 0
            self.kcMaxCooldown = 0
            self.kcCooldown = 0

            self.jumping = False


            self.curState = States.States.f_stopped()
            self.curState.Enter(self, self.stopFrames)
            self.curFrame = self.stopFrames[0]

            self.states.add('*','null','f_stopped',
                            self.stopFrames)

            self.states.addM('f_stopped','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_moving','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_moving','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_punching','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_kicking','mvLKeyPressed','f_moving',
                            self.movFrames, 1)

            self.states.addM('f_stopped','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_moving','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_moving','mvLKeyPressed','f_moving',
                            self.movFrames, 1)
            self.states.addM('f_punching','mvRKeyPressed','f_moving',
                            self.movFrames, 0)
            self.states.addM('f_kicking','mvRKeyPressed','f_moving',
                            self.movFrames, 0)

            self.states.add('f_moving','mvUKeyPressed','f_jumping_moving',
                            self.movFrames)
            self.states.add('f_jumping_moving','*','f_moving',
                            self.movFrames)
            self.states.add('f_stopped','mvUKeyPressed','f_jumping_stopped',
                            self.jpFrames)
            self.states.add('f_jumping_stopped','*','f_stopped',
                            self.stopFrames)

            self.states.add('f_stopped','pcKeyPressed','f_punching',
                            self.pcFrames)
            self.states.add('f_punching','pcKeyPressed','f_punching_2',
                            self.pcFrames)
            self.states.add('f_punching_2','pcKeyPressed','f_punching_3',
                            self.pcFrames)
            self.states.add('f_punching_3','null','f_stopped',
                            self.stopFrames)

            self.states.add('f_stopped','kcKeyPressed','f_kicking',
                            self.kcFrames)
            self.states.add('f_punching','kcKeyPressed','f_kicking',
                            self.kcFrames)

        def getForceJump(self):
            #print(self.forceJump)
            return self.forceJump
