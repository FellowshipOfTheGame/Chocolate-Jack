#coding: utf-8
import pygame
import threading
import time
import math
from Button import *
class ButtonIntra(Button):
    def __init__(self, x=0, y=0, screenCod =0, text=None):
        super().__init__(x, y, screenCod, text)
        self.px = x
        self.py = y
        self.screenCod = screenCod

    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.Bleft,self.Bmiddle, self.Bright =  pygame.mouse.get_pressed()
            return None
        if evento.type == pygame.MOUSEBUTTONUP:
            px , py = pygame.mouse.get_pos()
            if self.Bleft == True:#todo: tornar hitbox dinamica
                self.Bleft == False
                if ((px>= self.px)and (px<=self.px+200)) and ((py>= self.py)and (py<=self.py+50)):
                    return 1
        return None
