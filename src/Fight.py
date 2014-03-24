#coding: utf-8
import pygame
import sys
import States
import Fighters
import Scenarios
import Frame
import random


###
#   Main
###

from Screen import *
class Fight(Screen):
    def __init__(self, controller, tela):
        self.tela = tela
        self.control=controller
        self.messageScene = 'null'
        self.messageself1 = 'null'
        self.messageself2 = 'null'
        self.fundo = Scenarios.Training()   
        self.f1 = Fighters.ChocoJack(self.fundo.floorPy, 0, 1)
        self.f2 = Fighters.ChocoJack(self.fundo.floorPy, 1, 2)
        #self.f2 = Fighters.Alvo2(self.fundo.floorPy, 0, 2)
        #self.f2 = Fighters.Alvo(self.fundo.floorPy, 0, 2)
        self.hp1 = pygame.Rect(32, 32, 420, 32)
        self.hp1Atual = pygame.Rect(34, 34, 416, 28)
        self.hp1Rate = 416/self.f1.maxHp
        self.hp2 = pygame.Rect(582, 32, 420, 32)
        self.hp2Atual = pygame.Rect(584, 34, 416, 28)
        self.hp2Rate = 416/self.f2.maxHp
        
        self.f1.setEnemy(self.f2)
        self.f2.setEnemy(self.f1)
        
        
    
    def execute(self):
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
        
        self.f2.draw(self.tela)
        self.f1.draw(self.tela)
        
        """punchTrue = random.randint(0,25)
        if(punchTrue == 0):
            self.f2.changeState(States.f_punching())"""
        
        #dps alterar as teclas por algo generico que virah do arq de conf.
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif(event.key == pygame.K_q):
                    self.f1.toogleDebug()
                    self.f2.toogleDebug()
                    self.fundo.toogleDebug()
                #player 1
                elif(event.key == pygame.K_a):
                    self.messageself1 = 'pcKeyPressed'
                elif(event.key == pygame.K_s):
                    self.messageself1 = 'kcKeyPressed'
                elif(event.key == pygame.K_LEFT):
                    self.messageself1 = 'mvLKeyPressed'
                elif(event.key == pygame.K_RIGHT):
                    self.messageself1 = 'mvRKeyPressed'
                #player2
                elif(event.key == pygame.K_y):
                    self.messageself2 = 'pcKeyPressed'
                elif(event.key == pygame.K_h):
                    self.messageself2 = 'kcKeyPressed'
                elif(event.key == pygame.K_k):
                    self.messageself2 = 'mvLKeyPressed'
                elif(event.key == pygame.K_l):
                    self.messageself2 = 'mvRKeyPressed'
                    
            elif(event.type == pygame.KEYUP):
                #player 1
                if(event.key == pygame.K_LEFT):
                    self.messageself1 = 'mvLKeyReleased'
                elif(event.key == pygame.K_RIGHT):
                    self.messageself1 = 'mvRKeyReleased'
                #player 2
                elif(event.key == pygame.K_k):
                    self.messageself2 = 'mvLKeyReleased'
                elif(event.key == pygame.K_l):
                    self.messageself2 = 'mvRKeyReleased'
                    
        self.fundo.update(self.messageScene)
        self.f1.Update(self.messageself1)
        self.f2.Update(self.messageself2)
        
        self.messageself1 = 'null'
        self.messageself2 = 'null'
        self.messageScene = 'null'