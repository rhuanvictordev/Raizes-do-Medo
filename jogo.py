import pygame
from pygame.locals import *
from sys import exit

pygame.init()

altura = 640
largura = 480

tela = pygame.display.set_mode((altura, largura))
pygame.display.set_caption('JOGO')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    pygame.display.update()