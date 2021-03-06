#coding: utf-8
import pygame
import sys
import States
import Fighters
import Scenarios
import Frame
import random
import copy
from GenericFight import *
from Button import *
from ButtonInter import *
from Screen import *
from Config import *
import globals
###
#   Main
###
class Fights:
    class Fight(GenericFight):
        def __init__(self, controller, tela):
            GenericFight.__init__(self, controller, tela)
        
        def execute(self):
            GenericFight.execute(self) #realiza o desenho dos combatentes e da tela
            
            for event in pygame.event.get():
                if (self.pause):
                    for i in self.buttons:
                        resp = i.click(event)
                        if(isinstance(i, ButtonInter) and resp!=None):
                            self.control.changeScreen(resp)
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_ESCAPE):
                        self.pause = not self.pause
                   
                    if (not self.pause):
                        if(event.key == pygame.K_q):
                            self.f1.toogleDebug()
                            self.f2.toogleDebug()
                            self.fundo.toogleDebug()
                        #player 1
                        elif(event.key == self.keys.getAttack1Control()):
                            self.messageself1 = 'pcKeyPressed'
                        elif(event.key == self.keys.getAttack2Control()):
                            self.messageself1 = 'kcKeyPressed'
                        elif(event.key == self.keys.getLeftControl()):
                            self.messageself1 = 'mvLKeyPressed'
                        elif(event.key == self.keys.getRightControl()):
                            self.messageself1 = 'mvRKeyPressed'
                        elif(event.key == self.keys.getUpControl()):
                            self.messageself1 = 'mvUKeyPressed'
                        #player2
                        elif(event.key == self.keys.getAttack1ControlP2()):
                            self.messageself2 = 'pcKeyPressed'
                        elif(event.key == self.keys.getAttack2ControlP2()):
                            self.messageself2 = 'kcKeyPressed'
                        elif(event.key == self.keys.getLeftControlP2()):
                            self.messageself2 = 'mvLKeyPressed'
                        elif(event.key == self.keys.getRightControlP2()):
                            self.messageself2 = 'mvRKeyPressed'
                        elif(event.key == self.keys.getUpControlP2()):
                            self.messageself2 = 'mvUKeyPressed'
                        
                elif(event.type == pygame.KEYUP):
                    #player 1
                    if(event.key == self.keys.getLeftControl()):
                        self.messageself1 = 'mvLKeyReleased'
                    elif(event.key == self.keys.getRightControl()):
                        self.messageself1 = 'mvRKeyReleased'
                    #player 2
                    elif(event.key == self.keys.getLeftControlP2()):
                        self.messageself2 = 'mvLKeyReleased'
                    elif(event.key == self.keys.getRightControlP2()):
                        self.messageself2 = 'mvRKeyReleased'
            
            if (not self.pause and self.startAnimation == None):
                self.messageScene = 'null'
                self.fundo.update(self.messageScene)
                self.f1.Update(self.messageself1)
                self.f2.Update(self.messageself2)

                if(self.f1.px < 0):
                    self.f1.px = self.f1.px + self.f1.width
                    self.f1.Update('null')
                elif(self.f1.px > 1024):
                    self.f1.px = self.f1.px - self.f1.width
                    self.f1.Update('null')
                    
                if(self.f2.px < 0):
                    self.f2.px = self.f2.px + self.f2.width
                    self.f2.Update('null')
                elif(self.f2.px > 1024):
                    self.f2.px = self.f2.px - self.f2.width
                    self.f2.Update('null')
                self.messageself1 = 'null'
                self.messageself2 = 'null'
                self.messageScene = 'null'
    class FightPC(GenericFight):
        def __init__(self, controller, tela):
            GenericFight.__init__(self, controller, tela)
            self.messageScene = 'null'
        
        def execute(self):
            GenericFight.execute(self) #realiza o desenho dos combatentes e da tela
            ##AI
            if (not self.pause):
                if((self.f1.px < self.f2.px) and (self.f2.px - self.f1.px > 200)):
                    self.messageself2 = 'mvLKeyPressed'
                elif(self.f2.px - self.f1.px > 0):
                    self.messageself2 = 'mvLKeyReleased'
                    #self.f2.machine.punch = True
                elif(self.f2.px - self.f1.px > -200):
                    self.messageself2 = 'mvRKeyPressed'
                
            ##
            for event in pygame.event.get():
                if (self.pause):
                    for i in self.buttons:
                        resp = i.click(event)
                        if(isinstance(i, ButtonInter) and resp!=None):
                            self.control.changeScreen(resp)
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_ESCAPE):
                        self.pause = not self.pause
                        self.messageself2 = 'null'
                   
                    if (not self.pause):
                        if(event.key == pygame.K_q):
                            self.f1.toogleDebug()
                            self.f2.toogleDebug()
                            self.fundo.toogleDebug()
                        #player 1
                        elif(event.key == self.keys.getAttack1Control()):
                            self.messageself1 = 'pcKeyPressed'
                        elif(event.key == self.keys.getAttack2Control()):
                            self.messageself1 = 'kcKeyPressed'
                        elif(event.key == self.keys.getLeftControl()):
                            self.messageself1 = 'mvLKeyPressed'
                        elif(event.key == self.keys.getRightControl()):
                            self.messageself1 = 'mvRKeyPressed'
                        elif(event.key == self.keys.getUpControl()):
                            self.messageself1 = 'mvUKeyPressed'
                        
                elif(event.type == pygame.KEYUP):
                    #player 1
                    if(event.key == self.keys.getLeftControl()):
                        self.messageself1 = 'mvLKeyReleased'
                    elif(event.key == self.keys.getRightControl()):
                        self.messageself1 = 'mvRKeyReleased'
            
            if (not self.pause and self.startAnimation == None):
                self.messageScene = 'null'
                self.fundo.update(self.messageScene)
                self.f1.Update(self.messageself1)
                self.f2.Update(self.messageself2)
                
                self.messageself1 = 'null'
                self.messageself2 = 'null'