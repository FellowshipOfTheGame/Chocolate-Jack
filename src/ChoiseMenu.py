#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import pygame
import sys
import Scenarios

from Screen import *
from Button import *
from ButtonInter import *
from ButtonIntra import *
from Fighters import *
class ChoiseMenu(Screen):
    def __init__(self, controller, screen, nextS):
        self.buttons = []
        self.chars = []
        self.screen = screen
        self.control=controller
        self.buttons.append(ButtonInter(700, 500, 290, 73, 3, "Comecar"))
        self.chars.append(ChocoJack(300))
        self.chars.append(Alvo2(400))
        self.chars.append(Alvo(500))
        self.chars.append(Tank(600))
        self.ok = self.buttons[0]
        self.Bleft = self.Bright = self.Bmiddle = False
        self.background = Scenarios.ChoiseMenu()
        self.count = 0
        self.p1 = None
        self.p2 = None

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
            self.control.changeScreen(self.nextS)
        count = 0
        for i in self.chars:
            i.drawChoise(self.screen, 50 +(count*200), 250)
            count = count+1
