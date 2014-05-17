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

        self.buttons.append(ButtonInter(700, 600, 290, 73, 4, "Comecar"))
        self.buttons.append(ButtonIntra(10, 400, 50, 25, 0, 0, "Escolher"))
        self.buttons.append(ButtonIntra(70, 400, 50, 25, 0, 1, "Escolher"))
        self.chars.append(Fighters.ChocoJack(300))
        self.chars.append(Fighters.BrocolisNinja(400))
        self.ok = self.buttons[0]
        self.Bleft = self.Bright = self.Bmiddle = False
        self.background = Scenarios.ChoiseMenu()
        self.count = 0
        self.p1 = None
        self.p2 = None
        self.fighters = []
        
    def execute(self):

        self.background.draw(self.screen)

        for evento in pygame.event.get():
            for i in self.buttons:
                resp = i.click(evento)
                if(isinstance(i, ButtonInter) and resp!=None):
                    if len(self.fighters) == 2:
                        self.control.changeScreen(resp)
                    else:
                       print('Escolha 2 personagens')
                elif(isinstance(i, ButtonIntra) and resp!=None and len(self.fighters) < 2):
                    self.fighters.append(self.chars[i.getType()].getName())
                if evento.type == pygame.QUIT:
                    sys.exit(0)
        for i in self.buttons:
            i.desenha(self.screen)
        if (self.ok.getState()):
            self.control.changeScreen(self.next)
            self.control.getCurrentScreen().setFighters(getattr(Fighters, self.fighters[0]), getattr(Fighters, self.fighters[1]))
        count = 0
        for i in self.chars:
            i.drawChoise(self.screen, 50 +(count*200), 250)
            count = count+1
