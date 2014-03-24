#coding: utf-8
import pygame
import sys

from Control import *
###
#   Main
###
def main():
    pygame.init()
    resolucao = (1024,720)
    tela = pygame.display.set_mode(resolucao)

    controller = ScreenController(tela)
    clock = pygame.time.Clock()

    while controller.execute():
        pygame.display.flip()
        tela.fill((0,0,0))
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
