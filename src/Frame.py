import sys
import pygame

#classe que terah uma imagem e a lista de areas de colisao
class Frame:
    img = None
    collision = None

    #pImg deve ser na forma de string indicando o endereco da imagem.
    #as colisoes serao adicionadas uma a uma, com o metodo addColision()
    def __init__(self, pImg):
        self.img = pImg
        self.collision = []          

    def addCollision(self, pPx, pPy, pWidth, pHeight):
        newCollision = (pPx, pPy, pWidth, pHeight)
        self.collision.append(newCollision)

    def getCollisions(self):
        return self.collision

    #essa funcao passa os rects ajustados pela posicao passada por parametro
    def getCollisionsRect(self, pPx, pPy):
        rectRet = []
        for coll in self.collision:
            rect = pygame.Rect(coll[0]+pPx, coll[1] + pPy, coll[2], coll[3])
            #print('SELF = ',self,'getting = ',rect)
            rectRet.append(rect)

        return rectRet
