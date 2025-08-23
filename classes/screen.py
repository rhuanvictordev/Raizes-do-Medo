import pygame
from classes.soundManagement import GerenciadorDeSom

# precisa inicializar primeiro pra conseguir colocar em tela cheia
pygame.init()

info = pygame.display.Info()

## para ajustar em tela cheia: LARGURA, ALTURA = info.current_w, info.current_h
## para ajustar em tela cheia: TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)


LARGURA, ALTURA = info.current_w, info.current_h
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)

pygame.event.set_grab(True)   # trava ou nao o mouse dentro da janela
pygame.mouse.set_visible(True)  # esconde ou exibe o cursor

pygame.display.set_caption("Raízes do medo")
class Tela:
    def __init__(self, caminho_img, som_nome=None):
        self.fundo = pygame.transform.scale(pygame.image.load(caminho_img).convert(), (LARGURA, ALTURA))
        self.som_nome = som_nome
        self.som_tocou = False

    def exibir(self, sons: GerenciadorDeSom):
        TELA.blit(self.fundo, (0, 0))
        if self.som_nome and not self.som_tocou:
            sons.tocar(self.som_nome, "narrador", False)
            self.som_tocou = True

    def resetar_som(self):
        self.som_tocou = False
        