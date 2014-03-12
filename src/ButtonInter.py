#coding: utf-8

import pygame
import threading
import time
import math
from Button import *
class ButtonInter(Button):
    def __init__(self, x=0, y=0, screenCod=0, text=None, screen=None):
        super().__init__(x, y, screenCod, text)
        self.control = 0
        self.px = x
        self.py = y
        self.screen = screen
        self.screenCod = screenCod

    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.Bleft, self.Bmiddle, self.Bright =  pygame.mouse.get_pressed()
            return None
        if evento.type == pygame.MOUSEBUTTONUP:
            px , py = pygame.mouse.get_pos()
            print (px, self.px, py, self.py)
            if self.Bleft == True:#todo: tornar hitbox dinamica
                self.Bleft == False
                if ((px>= self.px)and (px<=self.px+200)) and ((py>= self.py)and (py<=self.py+50)):
                    return self.screenCod
                return None
