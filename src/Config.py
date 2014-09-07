#coding: utf-8
# -*- coding: iso-8859-15 -*-

import pygame
import sys
import Scenarios

from Screen import *
from Button import *
from ButtonInter import *
from ButtonIntra import *
import globals

class setConfig():
    def __init__(self, controller, screen):
        self.buttons = []
        self.currentCmd = 0
        self.screen = screen
        self.flag = False
        self.control=controller
        self.buttons.append(ButtonIntra(100, 220, 95, 50, 1, "Jump"))
        self.buttons.append(ButtonIntra(150, 280, 95, 50, 2, "Right"))
        self.buttons.append(ButtonIntra(50, 280, 95, 50, 3, "Left"))
        self.buttons.append(ButtonIntra(50, 360, 120, 50, 4, "Attack1"))
        self.buttons.append(ButtonIntra(170, 360, 120, 50, 5, "Attack2"))
        self.buttons.append(ButtonIntra(500, 220, 95, 50, 6, "Jump P2"))
        self.buttons.append(ButtonIntra(550, 280, 95, 50, 7, "Right P2"))
        self.buttons.append(ButtonIntra(450, 280, 95, 50, 8, "Left P2"))
        self.buttons.append(ButtonIntra(400, 360, 120, 50, 9, "Attack1 P2"))
        self.buttons.append(ButtonIntra(600, 360, 120, 50, 10, "Attack2 P2"))
        self.buttons.append(ButtonInter(700, 600, 290, 73, 0, "Voltar"))
        self.background = Scenarios.Config()
        self.up = None
        self.right = None
        self.left = None
        self.attack1 = None
        self.attack2 = None
        self.upp2 = None
        self.rightp2 = None
        self.leftp2 = None
        self.attackp2 = None
        self.attack2p2 = None
        
    #def setControl(self, command,  value):
    def setControl(self):
        ###como faz switch case?
        if(command == 1):#Jump P1
                self.up = value
        elif(command == 2):#Right P1
                self.right = value
        elif(command == 3):#Left P1
                self.left = value
        elif(command == 4):#Attack1 P1
                self.attack1 = value
        elif(command == 5):#Attack2 P1
                self.attack2 = value
        elif(command == 6):#Jump P2
                self.upp2 = value
        elif(command == 7):#Right P2
                self.rightp2 = value
        elif(command == 8):#Left P2
                self.leftp2 = value
        elif(command == 9):#Attack1 P2
                self.attack1p2 = value
        elif(command == 10):#Attack2 P2
                self.attack2p2 = value
    
    def execute(self):
        notPressed = True
        self.background.draw(self.screen)
        for evento in pygame.event.get():
            if (self.flag == False):
                for i in self.buttons:
                    resp = i.click(evento)
                    if(isinstance(i, ButtonInter) and resp!=None):
                        self.control.changeScreen(resp)
                    elif(isinstance(i, ButtonIntra) and resp!= None):
                        cont = 0
                        self.currentCmd = i.getType()
                        self.flag = True
                        '''if i.getType() == 1:
                            self.currentCmd = 1
                            self.flag = True
                            print ('Catching jump')
                            break;
                        elif i.getType() == 2:
                            self.flag = True
                            self.currentCmd = 2
                            print ('Catching right')
                            break;
                        elif i.getType() == 3:
                            self.currentCmd = 3
                            self.flag = True
                            print ('Catching left')
                            break;
                        '''
            elif (self.flag == True):
                if evento.type is pygame.KEYDOWN:
                    keyname = pygame.key.name(evento.key)
                    if(evento.key != None and self.currentCmd != 0):
                        self.readData()
                        if(self.currentCmd == 1):#Jump P1
                            self.up = evento.key
                        elif(self.currentCmd == 2):#Right P1
                            self.right = evento.key
                        elif(self.currentCmd == 3):#Left P1
                            self.left = evento.key
                        elif(self.currentCmd == 4):#Attack1 P1
                            self.attack1 = evento.key
                        elif(self.currentCmd == 5):#Attack2 P2
                            self.attack2 = evento.key
                        elif(self.currentCmd == 6):#Jump P1
                            self.upp2 = evento.key
                        elif(self.currentCmd == 7):#Right P1
                            self.rightp2 = evento.key
                        elif(self.currentCmd == 8):#Left P1
                            self.leftp2 = evento.key
                        elif(self.currentCmd == 9):#Attack1 P1
                            self.attack1p2 = evento.key
                        elif(self.currentCmd == 10):#Attack2 P2
                            self.attack2p2 = evento.key
                        self.saveData();
                        self.currentCmd = 0
                        print(evento.key)
                    self.flag = False
            if evento.type == pygame.QUIT:
                sys.exit(0)
        for i in self.buttons:
            i.desenha(self.screen)
            
    def readData(self):
        f = open('data\\config.cjk', 'r')
        text, code = f.readline().split('#', 2)
        self.up = int(code)
        text, code = f.readline().split('#', 2)
        self.right = int(code)
        text, code = f.readline().split('#', 2)
        self.left = int(code)
        text, code = f.readline().split('#', 2)
        self.attack1 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack2 = int(code)
        text, code = f.readline().split('#', 2)
        self.upp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.rightp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.leftp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack1p2 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack2p2 = int(code)
        f.close()
        
    def saveData(self):
        file = open('data\\config.cjk', 'w')
        aux = 'up#' + str(self.up)+'\n'
        file.write(aux)
        aux = 'right#' + str(self.right)+'\n'
        file.write(aux)
        aux = 'left#' + str(self.left)+'\n'
        file.write(aux)
        aux = 'attack1#' + str(self.attack1)+'\n'
        file.write(aux)
        aux = 'attack2#' + str(self.attack2)+'\n'
        file.write(aux)
        aux = 'upp2#' + str(self.upp2)+'\n'
        file.write(aux)
        aux = 'rightp2#' + str(self.rightp2)+'\n'
        file.write(aux)
        aux = 'leftp2#' + str(self.leftp2)+'\n'
        file.write(aux)
        aux = 'attack1p2#' + str(self.attack1p2)+'\n'
        file.write(aux)
        aux = 'attack2p2#' + str(self.attack2p2)+'\n'
        file.write(aux)
        file.truncate()
        file.close()
        
        
class readConfig():
    def __init__(self):
        f = open('data\\config.cjk', 'r')
        text, code = f.readline().split('#', 2)
        self.up = int(code)
        text, code = f.readline().split('#', 2)
        self.right = int(code)
        text, code = f.readline().split('#', 2)
        self.left = int(code)
        text, code = f.readline().split('#', 2)
        self.attack1 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack2 = int(code)
        text, code = f.readline().split('#', 2)
        self.upp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.rightp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.leftp2 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack1p2 = int(code)
        text, code = f.readline().split('#', 2)
        self.attack2p2 = int(code)
        f.close()
    def getUpControl(self):
        return self.up
    def getRightControl(self):
        return self.right
    def getLeftControl(self):
        return self.left
    def getAttack1Control(self):
        return self.attack1
    def getAttack2Control(self):
        return self.attack2
    def getUpControlP2(self):
        return self.upp2
    def getRightControlP2(self):
        return self.rightp2
    def getLeftControlP2(self):
        return self.leftp2
    def getAttack1ControlP2(self):
        return self.attack1p2
    def getAttack2ControlP2(self):
        return self.attack2p2
