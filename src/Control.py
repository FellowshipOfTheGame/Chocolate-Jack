#coding: utf-8
#todo: fazer os enums dos estados das telas

from Screen import *
from Fight import *
from FightPC import *
from Menu import *
from ChoiseMenu import *
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
            pass
            #self.currentScreen = Escolha(control, self.tela)
        elif (tipo ==2):
            #self.currentScreen = Fight(control, self.tela)
            self.currentScreen = ChoiseMenu(control, self.tela, 2)
        elif (tipo ==3):
            self.currentScreen = FightPC(control, self.tela)
        #self.currentScreen = Settings(control, self.tela)

    def execute (self):
        self.currentScreen.execute()
        return self.status
