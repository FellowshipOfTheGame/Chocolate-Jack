#coding: utf-8
#todo: fazer os enums dos estados das telas

from Screen import *
from Fights import *
from Menu import *
from ChoiseMenu import *
from Fighters import *
import globals

class Materials:
    Menu, Escolha, Fight, Settings = range(4)

class ScreenController():
    def __init__(self, tela):
        self.tela = tela
        self.status =True
        control = self
        self.currentScreen = Menu(control, self.tela)

    def changeScreen(self, tipo=0):
        control = self
        if (tipo==0):
            self.currentScreen = Menu(control, self.tela)
        elif (tipo ==1):
            self.currentScreen = setConfig(control, self.tela)
        elif (tipo ==2):
            #self.currentScreen = Fight(control, self.tela)
            self.currentScreen = ChoiseMenu(control, self.tela, 2)
        elif (tipo ==3):
            self.currentScreen = Fights.FightPC(control, self.tela)
            self.currentScreen.setFighters(getattr(Fighters, 'ChocoJack'), getattr(Fighters, 'ChocoJack'))
        elif (tipo ==4):
            self.currentScreen = Fights.Fight(control, self.tela)
            self.currentScreen.setFighters(getattr(Fighters, 'ChocoJack'), getattr(Fighters, 'ChocoJack'))
        #self.currentScreen = Settings(control, self.tela)

    def execute (self):
        self.currentScreen.execute()
        return self.status
    
    def getCurrentScreen(self):
        return self.currentScreen
    
    def setCurrentScreen(self, screen):
        newScreen = screen(self, self.tela) #Instancia nova tela
        newScreen.setFighters(getattr(Fighters, self.currentScreen.f1.getName()), getattr(Fighters, self.currentScreen.f2.getName()))
        self.currentScreen = newScreen
        
