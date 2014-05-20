#coding: utf-8
# -*- coding: iso-8859-15 -*-

import pygame
import sys
import Scenarios

from Screen import *
from Button import *
from ButtonInter import *
from ButtonIntra import *

class setConfig():
    def __init__(self, controller, screen):
        self.buttons = []
        self.screen = screen
        self.control=controller
        self.buttons.append(ButtonIntra(100, 200, 50, 50, 1, "Jump"))
        self.buttons.append(ButtonIntra(150, 260, 50, 50, 2, "Right"))
        self.buttons.append(ButtonIntra(50, 260, 50, 50, 3, "Left"))
        self.buttons.append(ButtonInter(700, 600, 290, 73, 0, "Voltar"))
        self.background = Scenarios.Config()
        
    def execute(self):
        self.background.draw(self.screen)
        for evento in pygame.event.get():
            for i in self.buttons:
                resp = i.click(evento)
                if(isinstance(i, ButtonInter) and resp!=None):
                    self.control.changeScreen(resp)
                if evento.type == pygame.QUIT:
                    sys.exit(0)
        for i in self.buttons:
            i.desenha(self.screen)

                            
class readConfig():
    def __init__(self):
        f = open('data\\config.cjk', 'r')
        text, code = f.readline().split('#', 2)
        self.up = int(code)
        text, code = f.readline().split('#', 2)
        self.right = int(code)
        text, code = f.readline().split('#', 2)
        self.left = int(code)
        text, code = f.readline().split('#', 2)
        self.attack1 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack2 = int(code)
        text, code = f.readline().split('#', 2)
        self.upp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.rightp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.leftp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack1p2 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack2p2 = int(code) 
    def getUpControl(self):
        return self.up
    def getRightControl(self):
        return self.right
    def getLeftControl(self):
        return self.left
    def getAttack1Control(self):
        return self.attack1
    def getAttack2Control(self):
        return self.attack2
    def getUpControlP2(self):
        return self.upp2
    def getRightControlP2(self):
        return self.rightp2
    def getLeftControlP2(self):
        return self.leftp2
    def getAttack1ControlP2(self):
        return self.attack1p2
    def getAttack2ControlP2(self):
        return self.attack2p2
