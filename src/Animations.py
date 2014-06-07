#coding: utf-8
import pygame
import threading
import time
import math
from utils import safe_load

class Animations:
    class GenericAnimation:
        def __init__(self, tela, duration= 0, origin=None, destiny=None):
            self.tela = tela
            self.image = None
            self.lifetime = duration
            self.origin = origin
            self.current = self.origin
            self.moviment = destiny
        def execute(self):
            if (self.lifetime > 0):
                self.lifetime = self.lifetime -1
            self.current.x = self.current.x + self.moviment.x
            self.current.y = self.current.y + self.moviment.y
        def isAlive(self):
            return (self.lifetime > 0 or self.lifetime == -1)
        def desenha(self):
            self.tela.blit(self.image, (self.current.px, self.current.py))
    class TextAnimation(GenericAnimation):
        def __init__(self, tela, text = '', duration= 0, origin=None, destiny=None):
            Animations.GenericAnimation.__init__(
                self,
                duration,
                origin,
                destiny
                )
            self.image = self.Franchise_36.render(str(text), True, (255, 0, 0))
    class Animation1(GenericAnimation):
        def __init__(self):
            Animations.GenericAnimation.__init__(self)
            pass