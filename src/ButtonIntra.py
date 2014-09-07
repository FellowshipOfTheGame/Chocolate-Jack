#coding: utf-8
import pygame
import threading
import time
import math
from Button import *
import globals

class ButtonIntra(Button):
    def __init__(self, x = 0, y = 0, lx = 0, ly = 0, char = 0, text=None):
        super().__init__(x, y, lx, ly, 0, text)
        self.px = x
        self.py = y
        self.lx = lx
        self.ly = ly
        self.char = char

    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.Bleft,self.Bmiddle, self.Bright =  pygame.mouse.get_pressed()
            return None
        if evento.type == pygame.MOUSEBUTTONUP:
            px , py = pygame.mouse.get_pos()
            if self.Bleft == True:
                self.Bleft == False
                if ((px>= self.px)and (px<=self.px+self.lx)) and ((py>= self.py)and (py<=self.py+self.ly)):
                    return self.char
        return None
    def getType(self):
        return self.char
