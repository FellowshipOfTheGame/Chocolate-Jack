#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 14/09/2013

@author: Eldhelion
'''
import pygame
import sys
import Scenarios

from Screen import *
from Button import *
from ButtonInter import *
from ButtonIntra import *

class Menu(Screen):
    def __init__(self, controller, screen):
        self.buttons = []
        self.screen = screen
        self.control=controller
#        self.buttons.append(ButtonInter(248, 400, 290, 73, 3, "Comecar PVC", 0))
#        self.buttons.append(ButtonInter(544, 400, 290, 73, 2, "Comecar PVP", 1))
#        self.buttons.append(ButtonInter(368, 515, 290, 73, 1, "Configuracoes", 2))
        self.buttons.append(ButtonInter(248, 400, 290, 73, 3, " ", 0))
        self.buttons.append(ButtonInter(544, 400, 290, 73, 2, " ", 1))
        self.buttons.append(ButtonInter(368, 515, 290, 73, 1, " ", 2))
        self.ok = self.buttons[0]
        self.config = self.buttons[1]
        self.Bleft = self.Bright = self.Bmiddle = False
        self.background = Scenarios.Menu()

    def execute(self):

        self.background.draw(self.screen)

        for evento in pygame.event.get():
            for i in self.buttons:
                resp = i.click(evento)
                if(isinstance(i, ButtonInter) and resp!=None):
                    self.control.changeScreen(resp)
                elif(isinstance(i, ButtonIntra) and resp!=None):
                    pass
                if evento.type == pygame.QUIT:
                    sys.exit(0)
        for i in self.buttons:
            i.desenha(self.screen)
        if (self.ok.getState()):
            self.control.changeScreen(2)
        if (self.config.getState()):
            sys.exit(0)
