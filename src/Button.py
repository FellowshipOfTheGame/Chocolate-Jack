#coding: utf-8
import pygame
import threading
import time
import math
from utils import safe_load
class names:
    Start, Config= range(2)

class Button:
    def __init__ (self, x=0, y=0, lx=0, ly=0, screenCod=0, text=None):
        self.control = 0
        self.text = text
        self.Franchise_36 = pygame.font.Font("data/fontes/Franchise-Bold-hinted.ttf", 36)
        self.image = pygame.transform.scale(safe_load(pygame.image.load, "data/buttons/botao2.jpg"), (lx,ly))
        self.screenCod = screenCod
        tamXY = self.Franchise_36.size(str(self.text))
        self.lx = lx
        self.ly = ly
        self.px = x
        self.py = y
        self.posTX = (x + (lx/2) - (tamXY[0]/2))
        self.posTY = (y + (ly/2) - (tamXY[1]/2))
        self.renderText = self.Franchise_36.render(str(self.text), True, (255, 0, 0))

    def getState(self):
        if self.control==1:
            self.control=0
            return True
        else:
            return False

    def desenha(self, tela):
        tela.blit(self.image, (self.px, self.py))
        tela.blit(self.renderText, (self.posTX, self.posTY))

    def click(self, evento):#retorna 1 caso o botao esteja pressionado, 0 caso contrario
        pass
    def getScreenCode(self):
        return self.screenCod
