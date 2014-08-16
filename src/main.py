#coding: utf-8
import pygame
import sys

from Control import *
###
#   Main
###
tela = None
def main():
    pygame.init()
    resolucao = (1024,720)
    global tela
    tela = pygame.display.set_mode(resolucao)

    controller = ScreenController(tela)
    clock = pygame.time.Clock()
    readConfig()
    while controller.execute():
        pygame.display.flip()
        tela.fill((0,0,0))
        clock.tick(120)

    pygame.quit()

if __name__ == '__main__':
    main()
