#coding: utf-8
import pygame
import States
import sys
import Frame
from utils import safe_load

###
#   Fighters
###
class Fighter:
    #Define qual eh o jogador, player 1 ou player 2
    player = None


    #atributos/habilidades
    hp = None
    maxHp = None
    mp = None
    maxMP = None
    attack = None
    defense = None
    sp1DMG = None #
    sp2DMG = None # dano dos especiais
    spUltDMG = None #
    sp1Cost = None #
    sp2Cost = None # Custo dos especiais, preferencialmente spUlt custarah todo o MP
    spUltCost = None #

    #indica se deve mostrar palavra de colisao ou nao, 0 = nao
    soco = None
    chute = None

    #ponteiro para oponente
    enemy = None
	
    #debugg
    debugTrue = None #qdo 1 ativa modo debugg do fighter
	
    #dimensoes
    height = None
    weight = None

    #pose
    px, py = None, None
    pcPx, pcPy = None, None #posicao qdo soca, sera alterada caso de socos para a esquerda.
    kcPx, kcPy = None, None #posicao qdo chuta.
    drawPx, drawPy = None, None
    facing = None # 0 right 1 left

    #Image Stuff
    curFrame = None #tipo Frame
    frameNum = None #valor de 0 a X-1, indicando o frame do cinj de imagens q o fighter estah
	
    #array com os 'frames' usados em cada estado, segue a seguinte forma
    #array[idx] = o endereco da imagem; idx e um inteirro da forma facing*frameOrder
    #ex: o segundo passo de um movimento olhando para a direita 2 : 'mvRImg.png'
    movFrames = None
    pcFrames = None
    kcFrames = None
    stopFrames = None

    #Parametros
    mvInc = None #distancia percorrida a cada passo.
    mvDir = None #0 = indo para dir, 1 = indo para esq.
    mvMaxCooldown = None #cooldown maximo para troca de img de movimento
    mvCooldown = None #cooldown atual para movimento.

    pcDist = None #indica a distancia para soco, usado para posicionar o fighter quando ele soca para a esquerda
    pcMaxCooldown = None
    pcCooldown = None

    kcDist = None
    kcMaxCooldown = None
    kcCooldown = None


    machine = None
    #State
    curState = None
	
    jumping = None
    #Contrutor
    def __init__(self, pPyFloor = 0, pFacing=0, pPlayer = 1):
        self.player = pPlayer
		
        #atributos/habilidades
        self.hp = 1
        self.maxHp = 1
        self.mp = 0
        self.maxMP = 0
        self.attack = 0
        self.defense = 0
        self.sp1DG = 0
        self.sp2DMG = 0
        self.spUltDMG = 0
        self.sp1Cost = 0
        self.sp2Cost = 0
        self.setpUltCost = 0
		
        #outros
        self.soco = 0
        self.chute = 0
        self.enemy = None
        self.px = 32 + pFacing*992
        self.py = pPyFloor - self.heigth
        self.facing = pFacing
        self.curState = States.f_jumping_stopped(self)
        self.curState.Enter(self)
        self.curFrame = None

        self.debugTrue = 0
        self.height = 0
        self.width = 0

        self.drawPx = self.px
        self.drawPy = self.py

        self.frameNum = 0
        self.movFrames = []
        self.pcFrames = []
        self.stopFrames = []
        self.kcFrames = []

        self.mvInc = 0
        self.mvDir = 0
        self.mvMaxCooldown = 0
        self.mvCooldown = 0

        self.pcDist = 0
        self.pcMaxCooldown = 0
        self.pcCooldown = 0

        self.kcDist = 0
        self.kcMaxCooldown = 0
        self.kcCooldown = 0
        
        self.jumping = False
        
        self.machine = States.StateMachine()
		

    #troca de estado
    def changeState(self, pNewState):
        self.curState.Exit(self)
        self.curState = pNewState
        self.curState.Enter(self)

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
        self.machine.execute(message)
        self.facingUpdate()
        self.curState.Execute(self, self.machine)


    #draw
    def draw(self, tela):
        img = safe_load(pygame.image.load, self.curFrame.img).convert_alpha()
        tela.blit(img, (self.drawPx, self.drawPy))


        if(self.soco > 0):
            self.soco = self.soco + 1
            socoImg = safe_load(pygame.image.load,'data\\imgs\\soco2.png').convert_alpha()
            tela.blit(socoImg, (self.drawPx + self.width - self.facing*int(3*self.width/2), self.drawPy + int(self.height/4)))

            if(self.soco > 10):
                self.soco = 0

            if(self.chute > 0):
                self.chute = self.chute + 1
                chuteImg = safe_load(pygame.image.load, 'data\\imgs\\chute.png').convert_alpha()
                tela.blit(chuteImg, (self.drawPx + self.width - self.facing*int(3*self.width/2), self.drawPy + int(2*self.height/3)))

            if(self.chute > 10):
                self.chute = 0

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

class Tank(Fighter):

    def __init__(self, pPyFloor = 0, pFacing=0, pPlayer=1):
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

        #outros
        self.debugTrue = 0
        self.soco = 0
        self.chute = 0
		
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

        #criando frames de movimento
        mvFrameR1 = Frame.Frame('data\\imgs\\tankMvFR1.png')
        mvFrameR2 = Frame.Frame('data\\imgs\\tankMvFR2.png')
        mvFrameR3 = Frame.Frame('data\\imgs\\tankMvFR3.png')
        mvFrameL1 = Frame.Frame('data\\imgs\\tankMvFL1.png')
        mvFrameL2 = Frame.Frame('data\\imgs\\tankMvFL2.png')
        mvFrameL3 = Frame.Frame('data\\imgs\\tankMvFL3.png')
		
        #atribuindo frames
        self.movFrames = (mvFrameR1,mvFrameR2,mvFrameR3,mvFrameL1,mvFrameL2,mvFrameL3)

        #criando frames de soco
        pcFrame1 = Frame.Frame('data\\imgs\\punchtankR.png')
        pcFrame2 = Frame.Frame('data\\imgs\\punchtankL.png')

        #atribuindo frames
        self.pcFrames = [pcFrame1,pcFrame2]

        self.kcDist = 0
        self.kcMaxCooldown = 0
        self.kcCooldown = 0
        self.mvInc = 64
        self.pcDist = 16
        self.mvMaxCooldown = 7 #aprox 0.25 sec
        self.mvCooldown = 0
        self.pcMaxCooldown = 5
        self.pcCooldown = 0
        self.curState = States.f_stopped()
        self.curState.Enter(self)
		

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
        self.curState = States.f_stopped()
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
        self.curState = States.f_stopped()
        self.curState.Enter(self)
        self.kcDist = 0
        self.kcMaxCooldown = 0
        self.kcCooldown = 0

class ChocoJack(Fighter):
    def __init__(self, pPyFloor=0, pFacing=0, pPlayer=1):
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
        sFrameR = Frame.Frame('data\\imgs\\ChocolateJack\\stpJackFR1.png')
        sFrameR.addCollision(9,0,64,128)
        sFrameL = Frame.Frame('data\\imgs\\ChocolateJack\\stpJackFL1.png')
        sFrameL.addCollision(22,0,64,128)
		
        #atribuindo frames
        self.stopFrames = [sFrameR, sFrameL]

        #criando frames de movimento
        mvFrameR1 = Frame.Frame('data\\imgs\\ChocolateJack\\mvJackFR1.png')
        mvFrameR1.addCollision(10,0,64,128)
		
        mvFrameR2 = Frame.Frame('data\\imgs\\ChocolateJack\\mvJackFR2.png')
        mvFrameR2.addCollision(6,0,64,128)
		
        mvFrameR3 = Frame.Frame('data\\imgs\\ChocolateJack\\mvJackFR3.png')
        mvFrameR3.addCollision(6,0,64,128)
		
        mvFrameL1 = Frame.Frame('data\\imgs\\ChocolateJack\\mvJackFL1.png')
        mvFrameL1.addCollision(12,0,64,128)
		
        mvFrameL2 = Frame.Frame('data\\imgs\\ChocolateJack\\mvJackFL2.png')
        mvFrameL2.addCollision(18,0,64,128)
		
        mvFrameL3 = Frame.Frame('data\\imgs\\ChocolateJack\\mvJackFL3.png')
        mvFrameL3.addCollision(18,0,64,128)

		
        #atribuindo frames
        self.movFrames = [mvFrameR1,mvFrameR2,mvFrameR3,mvFrameR2,mvFrameL1,mvFrameL2,mvFrameL3,mvFrameL2]

        #criando frames de soco
        pcFrameR1 = Frame.Frame('data\\imgs\\ChocolateJack\\pcJackFR1.png')
        pcFrameR1.addCollision(9,0,64,128) #corpo
        pcFrameR1.addCollision(80,60,20,20) #punho
		
        pcFrameR2= Frame.Frame('data\\imgs\\ChocolateJack\\pcJackFR2.png')
        pcFrameR2.addCollision(9,0,64,128) #corpo
        pcFrameR2.addCollision(82,64,18,25) #punho
		
        pcFrameL1 = Frame.Frame('data\\imgs\\ChocolateJack\\pcJackFL1.png')
        pcFrameL1.addCollision(29,0,64,128) #corpo
        pcFrameL1.addCollision(0,62,20,20) #punho
		
        pcFrameL2 = Frame.Frame('data\\imgs\\ChocolateJack\\pcJackFL2.png')
        pcFrameL2.addCollision(29,0,64,128) #corpo
        pcFrameL2.addCollision(4,62,18,25) #punho

        #atribuindo frames
        self.pcFrames = [pcFrameR1,pcFrameR2,pcFrameR1,pcFrameL1,pcFrameL2,pcFrameL1]

        #criando frames de chute
        kcFrameR1 = Frame.Frame('data\\imgs\\ChocolateJack\\kcJackFR1.png')
        kcFrameR1.addCollision(10,0,64,128) #corpo
        kcFrameR1.addCollision(62,106,20,20) #pe
		
        kcFrameR2 = Frame.Frame('data\\imgs\\ChocolateJack\\kcJackFR2.png')
        kcFrameR2.addCollision(10,0,64,128) #corpo
        kcFrameR2.addCollision(68,98,20,20) #pe
		
        kcFrameL1 = Frame.Frame('data\\imgs\\ChocolateJack\\kcJackFL1.png')
        kcFrameL1.addCollision(22,0,64,128) #corpo
        kcFrameL1.addCollision(13,106,20,20) #pe
		
        kcFrameL2 = Frame.Frame('data\\imgs\\ChocolateJack\\kcJackFL2.png')
        kcFrameL2.addCollision(22,0,64,128) #corpo
        kcFrameL2.addCollision(6,98,20,20) #pe

        #atribuindo frames
        self.kcFrames = [kcFrameR1, kcFrameR2, kcFrameR1, kcFrameL1, kcFrameL2, kcFrameL1]
		
        self.mvInc = 64
        self.pcDist = 8
        self.mvMaxCooldown = 3
        self.mvCooldown = 0
        self.pcMaxCooldown = 0
        self.pcCooldown = 0
        self.kcDist = 0
        self.kcMaxCooldown = 0
        self.kcCooldown = 0
		
        self.curState = States.f_stopped()
        self.curState.Enter(self)
        
        self.jumping = False
        self.machine = States.StateMachine()
