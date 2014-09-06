#coding: utf-8
import pygame
import threading
import time
import math
from utils import safe_load
import globals

class GenericAnimation:
    def __init__(self, tela, duration= 0, origin=None, destiny=None):
        self.tela = tela
        self.image = None
        self.lifetime = duration
        self.origin = origin
        self.current = self.origin
        self.moviment = destiny
    def execute(self, decrementa):
        if (self.lifetime > 0):
            self.lifetime = self.lifetime -1*decrementa
        self.current[0] = self.current[0] + self.moviment[0]
        self.current[1] = self.current[1] + self.moviment[1]
    def isAlive(self):
        return (self.lifetime > 0 or self.lifetime == -1)
    def desenha(self):
        self.tela.blit(self.image, self.current)
class Animations:
    class TextAnimation(GenericAnimation):
        def __init__(self, tela, text = '', duration= 0, origin=None, destiny=None):
            GenericAnimation.__init__(
                self,
                duration,
                origin,
                destiny
                )
            self.image = self.Franchise_36.render(str(text), True, (255, 0, 0))
    class Animation1(GenericAnimation):
        def __init__(self):
            GenericAnimation.__init__(self)
            pass
    class StartAnimation(GenericAnimation):
        def __init__(self, tela):
            GenericAnimation.__init__(
                self,
                tela,
                30,
                [400,100],
                [0,0]
                )
            self.index = 4;
            self.tela = tela
            self.image = safe_load(pygame.image.load,
                                   "data/imgs/Screen/3.png")
        def execute(self, decrementa):
            super().execute(decrementa)
            if (self.lifetime < 1 and self.index > 1):
                self.lifetime = 30
                self.change()

        def change(self):
            self.index = self.index - 1
            if (self.index == 3):
                self.image = safe_load(pygame.image.load,
                                   "data/imgs/Screen/2.png")
            elif (self.index == 2):
                self.image = safe_load(pygame.image.load,
                                   "data/imgs/Screen/1.png")
            elif (self.index == 1):
                self.image = safe_load(pygame.image.load,
                                   "data/imgs/Screen/fight.png")
    class StartChocoPunchAnimation(GenericAnimation):
        def __init__(self, tela,origin, player):
            self.player = player
            GenericAnimation.__init__(
                self,
                tela,
                30,
                origin,
                [0,0]
                )
            self.index = 4;
            self.tela = tela
            self.image = safe_load(pygame.image.load, "data/imgs/ChocolateJack/ChocoDrop.png")
        def execute(self, decrementa):
            super().execute(decrementa)
            if (self.lifetime < 1 and self.index > 1):
                self.lifetime = 30
                self.change()

        def change(self):
            self.index = self.index - 1
            if (self.index == 3):
                self.image = safe_load(pygame.image.load, "data/imgs/Screen/2.png")
            elif (self.index == 2):
                self.image = safe_load(pygame.image.load, "data/imgs/Screen/1.png")
            elif (self.index == 1):
                self.image = safe_load(pygame.image.load, "data/imgs/Screen/fight.png")

