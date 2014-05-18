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
        self.count = 0
        self.pdx = 200
        self.buttons.append(ButtonInter(700, 600, 290, 73, 4, "Comecar"))
        self.buttons.append(ButtonInter(100, 600, 290, 73, 0, "Voltar"))
        self.buttons.append(ButtonIntra(self.pdx*0 + 10, 400, 100, 30, 0, 0, "Escolher"))
        self.buttons.append(ButtonIntra(self.pdx*1 + 10, 400, 100, 30, 0, 1, "Escolher"))
        self.buttons.append(ButtonIntra(self.pdx*2 + 10, 400, 100, 30, 0, 2, "Escolher"))
        self.chars.append(Fighters.ChocoJack(300))
        self.chars.append(Fighters.ChocoJack(400))
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
                    if i.getScreenCode() == 4 and len(self.fighters) == 2:
                        #self.control.changeScreen(self.nextS)
                        self.control.changeScreen(resp)
                        self.control.getCurrentScreen().setFighters(getattr(Fighters, self.fighters[0]),getattr(Fighters, self.fighters[1]));
                    elif i.getScreenCode() == 4 and len(self.fighters) != 2:
                       print('Escolha 2 personagens')
                    else:
                        self.control.changeScreen(resp)
                elif(isinstance(i, ButtonIntra) and resp!=None and len(self.fighters) < 2):
                    self.fighters.append(self.chars[i.getType()].getName())
                if evento.type == pygame.QUIT:
                    sys.exit(0)
        for i in self.buttons:
            i.desenha(self.screen)
        self.count = 0
        for i in self.chars:
            i.drawChoise(self.screen, 50 +(self.count*150), 250)
            self.count = self.count+1
