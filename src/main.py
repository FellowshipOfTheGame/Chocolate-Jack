#coding: utf-8
import pygame
import sys
import globals
from Control import *
import globals
###
#   Main
###

def main():
    pygame.init()
    resolucao = (1024,720)

    globals.tela = pygame.display.set_mode(resolucao)

    controller = ScreenController(globals.tela)
    clock = pygame.time.Clock()
    readConfig()
    while controller.execute():
        pygame.display.flip()
        globals.tela.fill((0,0,0))
        clock.tick(120)

    pygame.quit()

if __name__ == '__main__':
    main()
