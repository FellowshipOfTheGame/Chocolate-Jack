#coding: utf-8

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
