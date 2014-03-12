#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 14/09/2013

@author: Eldhelion
'''
import pygame
import sys
from Screen import *
from Button import *
from ButtonInter import *
from ButtonIntra import *
class Menu(Screen):
    def __init__(self, controller, tela):
        self.buttons = []
        self.tela = tela
        self.control=controller
        self.buttons.append(ButtonInter(0, 0, 2, "Começar"))
        self.buttons.append(ButtonInter(0, 300, 1, "Configurações"))
        self.ok = self.buttons[0]
        self.config = self.buttons[1]
        self.Bleft = self.Bright = self.Bmiddle = False

    def execute(self):
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
            i.desenha(self.tela)
        if (self.ok.getState()):
            self.control.changeScreen(2)
        if (self.config.getState()):
            sys.exit(0)
