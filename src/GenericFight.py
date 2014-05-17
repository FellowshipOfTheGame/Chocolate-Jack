#coding: utf-8
import pygame
import sys
import States
import Fighters
import Scenarios
import Frame
import random
import copy
from Button import *
from ButtonInter import *
import Fights
###
#   Main
###

from Screen import *
from Config import *
class GenericFight(Screen):
    def __init__(self, controller, tela):
        self.keys = readConfig()
        self.tela = tela
        self.control=controller
        self.messageScene = 'null'
        self.messageself1 = 'null'
        self.messageself2 = 'null'
        self.fundo = Scenarios.Training()   

        self.f1 = None
        self.f2 = None

        self.f1_victory = 0
        self.f2_victory = 0
        self.pause = False
        self.buttons = []
        self.buttons.append(ButtonInter(500, 300, 400, 73, None, "Pausado"))
        self.buttons.append(ButtonInter(500, 500, 400, 73, 0, "Sair"))
    
    def setFighters(self, f1, f2):
        self.f1 = f1(self.fundo.floorPy, 0, 1)
        self.f2 = f2(self.fundo.floorPy, 1, 2)
        
        self.hp1 = pygame.Rect(32, 32, 420, 32)
        self.hp1Atual = pygame.Rect(34, 34, 416, 28)
        self.hp1Rate = 416/self.f1.maxHp
        self.hp2 = pygame.Rect(582, 32, 420, 32)
        self.hp2Atual = pygame.Rect(584, 34, 416, 28)
        self.hp2Rate = 416/self.f2.maxHp
        
        self.f1.setEnemy(self.f2)
        self.f2.setEnemy(self.f1)
    
    def setVictorys(self, vitorias):
        self.f1_victory = vitorias[0]
        self.f2_victory = vitorias[1]
    
    def execute(self):
        if (self.f1 == None or self.f2 == None):
            print("É preciso informar os combatentes")
            exit(0)
        
        if (self.f1.hp <=0):
            self.f2_victory +=1
        if (self.f2.hp <=0):
            self.f1_victory +=1
        if ((self.f1.hp <=0) or (self.f2.hp <=0)):
            if (self.f1_victory < 2 and self.f2_victory < 2):
                self.control.setCurrentScreen(getattr(Fights.Fights,self.__class__.__name__))
                self.control.getCurrentScreen().setVictorys([self.f1_victory, self.f2_victory])
            else:
                self.control.changeScreen(0)
        #clock = pygame.time.Clock()
        #while True:
        self.fundo.draw(self.tela)
        
        pygame.draw.rect(self.tela, pygame.Color(255,0,0,128), self.hp1, 0)
        pygame.draw.rect(self.tela, pygame.Color(255,0,0,128), self.hp2, 0)
        
        self.hp1Atual.width = self.hp1Rate*self.f1.hp
        if(self.hp1Atual.width < 0):
            self.hp1Atual.width = 0
        self.hp2Atual.width = self.hp2Rate*self.f2.hp
        if(self.hp2Atual.width < 0):
            self.hp2Atual.width = 0
        self.hp2Atual.x = 584 + (416-self.hp2Atual.width)

        pygame.draw.rect(self.tela, pygame.Color(255,255,0,128), self.hp1Atual, 0)
        pygame.draw.rect(self.tela, pygame.Color(255,255,0,128), self.hp2Atual, 0)
        
        self.victorys(self.hp1, self.f1_victory)
        self.victorys(self.hp2, self.f2_victory)
        
        self.f2.draw(self.tela)
        self.f1.draw(self.tela)
        
        if (self.pause):
            for i in self.buttons:
                i.desenha(self.tela)
    
    def victorys(self, pos, victorys):
        newpos = copy.copy(pos)
        newpos.y += 60
        newpos.x += 60
        for i in range(victorys):
            pygame.draw.circle(self.tela, pygame.Color(255,255,0,128), (newpos.x, newpos.y), 10)
            newpos.x += 50
