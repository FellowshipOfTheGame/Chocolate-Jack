#coding: utf-8

import pygame
import threading
import time
import math
from Button import *
class ButtonInter(Button):
    def __init__(self, x=0, y=0, lx=0, ly=0, screenCod=0, text=None, screen=None):
        super().__init__(x, y, lx, ly, screenCod, text)
        self.control = 0

    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.Bleft, self.Bmiddle, self.Bright =  pygame.mouse.get_pressed()
            return None
        if evento.type == pygame.MOUSEBUTTONUP:
            px , py = pygame.mouse.get_pos()
            print (px, self.px, py, self.py)
            if self.Bleft == True:
                self.Bleft == False
                if ((px>= self.px)and (px<=self.px+self.lx)) and ((py>= self.py)and (py<=self.py+self.ly)):
                    return self.screenCod
                return None
