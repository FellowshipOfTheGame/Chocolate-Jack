import pygame
import sys
import os
import States
import Frame
from utils import safe_load

class Scenario:

    #debug
    debugTrue = None #sera 1 caso debbug on

    frames = None #imagens de fundo, caso animado serah mais de uma, portanto tipo array[]
    curFrame = None
    frameNum = None #indica o frame atual de 0 a X-1
    floorPy = None #indica a altura onde os personagens vao pisar (vulgo chao)
    curState = None
    frameCooldown = None # taxa de atualizacao de frames
    cooldown = None # quantidade que falta para atualizar os frames

    def __init__(self):
        self.debugTrue = 0
        self.frames = None
        self.frameNum = 0
        self.curFrame = None
        self.floorPy = None
        self.curState = None

        self.frameCooldown = None
        self.cooldown = None


    def draw(self, tela):
        img = safe_load(pygame.image.load, self.curFrame.img).convert_alpha()
        tela.blit(img, (0,0))

    #troca de estado
    def Change_state(self, pNewState):
        self.curState.Exit(self)
        self.curState = pNewState
        self.curState.Enter(self)

    def update(self, message):
        self.curState.Execute(self, message)

    def toogleDebug(self):
        self.debugTrue = (self.debugTrue + 1)%2 #farah com que troque de 0 para 1 e vice-versa
        

class Praia(Scenario):

    def __init__(self):
        self.debugTrue = 0
        self.frameNum = 0
        self.cooldown = 0
        
        frame1 = Frame.Frame(os.path.join('data\\imgs\\praia.png'))
        frame2 = Frame.Frame('data\\imgs\\praia2.png')
        self.frames = [frame1,frame2]
        self.curFrame = self.frames[self.frameNum]
        self.floorPy = 611
        self.curState = States.s_default()
        self.frameCooldown = 45

class Training(Scenario):

    def __init__(self):
        self.debugTrue = 0
        self.frameNum = 0
        self.cooldown = 0
        
        frame1 = Frame.Frame('data\\imgs\\trainingRoom.png')
        frame2 = Frame.Frame('data\\imgs\\trainingRoom2.png')
        self.frames = [frame1, frame2]
        self.curFrame = self.frames[self.frameNum]
        self.floorPy = 675
        self.curState = States.s_default()
        self.frameCooldown = 25
        
##Tudo novo a partir daqui
class Menu(Scenario):
    def __init__(self):
        self.debugTrue = 0
        self.frameNum = 0
        self.cooldown = 0;
        
        frame1 = Frame.Frame('data\\imgs\\Menu\\ChocolateMenu.png')
        frame2 = Frame.Frame('data\\imgs\\Menu\\ChocolateMenu.png')

        self.frames = [frame1, frame2]
        self.curFrame = self.frames[self.frameNum]
        self.curState = States.s_default()
        self.frameCooldown = 25
class Config(Scenario):
    def __init__(self):
        self.debugTrue = 0
        self.frameNum = 0
        self.cooldown = 0

        print("nada")
