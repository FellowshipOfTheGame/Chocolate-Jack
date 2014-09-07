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

    globals.globTela = pygame.display.set_mode(resolucao)

    controller = ScreenController(globals.globTela)
    clock = pygame.time.Clock()
    readConfig()
    while controller.execute():
        pygame.display.flip()
        globals.globTela.fill((0,0,0))
        clock.tick(120)

    pygame.quit()

if __name__ == '__main__':
    main()
