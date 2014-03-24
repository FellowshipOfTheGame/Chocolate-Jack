#coding: utf-8
import pygame
import threading
import time
import math
from utils import safe_load
class names:
    Start, Config= range(2)

class Button:
    def __init__ (self, x=0, y=0, screenCod=0, text=None):
        self.control = 0
        self.text = text
        self.Carolingia_20 = pygame.font.Font("data/fontes/Carolingia.ttf", 20)
        self.image = safe_load(pygame.image.load, "data/buttons/botao.jpg")
        self.screenCod = screenCod
        self.px = x
        self.py = y
        self.renderText = self.Carolingia_20.render(str(self.text), True, (255, 0, 0))
    def getState(self):
        if self.control==1:
            self.control=0
            return True
        else:
            return False
    def desenha(self, tela):
        tela.blit(self.image, (self.px, self.py))
        tela.blit(self.renderText, (self.px, self.py))

    def click(self, evento):#retorna 1 caso o botao esteja pressionado, 0 caso contrario
        pass
