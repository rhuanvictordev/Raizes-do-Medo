import pygame
from classes.soundManagement import MapeamentoDeSons
import random
import service.prop as arquivo

pygame.init()
info = pygame.display.Info()
#LARGURA, ALTURA = info.current_w, info.current_h
#TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)

LARGURA, ALTURA = 1280, 720
TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Raízes do medo")
pygame.event.set_grab(False)   # trava o mouse dentro da janela
pygame.mouse.set_visible(True)  # esconde ou exibe o cursor

class Tela:
    def __init__(self, caminho_img, som_nome=None):
        self.fundo = pygame.transform.scale(pygame.image.load(caminho_img).convert(),(LARGURA, ALTURA))
        self.som_nome = som_nome
        self.som_tocou = False
        self.botoes = []

    def exibir(self, sons: MapeamentoDeSons):
        TELA.blit(self.fundo, (0, 0))
        narradorAtivado = (arquivo.getConfig("narradorativo") == "true")
        if narradorAtivado:
            if self.som_nome and not self.som_tocou:
                sons.tocar(self.som_nome, "narrador", False)
            self.som_tocou = True

    def resetar_som(self):
        self.som_tocou = False

    def carregarBotoes(self, botoes_info):
        self.botoes = []
        pos_mouse = pygame.mouse.get_pos()
        fonte = pygame.font.SysFont("arial", int(ALTURA/25), bold=True)
        cursor_hover = False

        for (percentualDaEsquerda, percentualDaDireita, percentualLargura, percentualAltura, texto) in botoes_info:
            rect = pygame.Rect(percentualDaEsquerda * LARGURA, percentualDaDireita * ALTURA, percentualLargura* LARGURA, percentualAltura * ALTURA)
            if rect.collidepoint(pos_mouse):
                cursor_hover = True
                cor = (200, 200, 200, 200) # debug (200, 200, 200, 200) nao debug (0, 0, 0, 100)
            else:
                cor = (100, 100, 100, 100) # debug (100, 100, 100, 100) nao debug (0, 0, 0, 0)

            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            overlay.fill(cor)
            TELA.blit(overlay, rect.topleft)

            txt = fonte.render(texto, True, (0, 0, 0))
            TELA.blit(txt, txt.get_rect(center=rect.center))
            self.botoes.append(rect)

        if cursor_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    def verificar_clique(self, pos_mouse):
        for valorBotaoClicado, rect in enumerate(self.botoes):
            if rect.collidepoint(pos_mouse):
                return valorBotaoClicado
        return None
