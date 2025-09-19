import pygame
from classes.soundManagement import GerenciadorDeSom
import random
import service.prop as arquivo

# precisa inicializar primeiro pra conseguir colocar em tela cheia
pygame.init()
info = pygame.display.Info()

#LARGURA, ALTURA = info.current_w, info.current_h
#TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)

LARGURA, ALTURA = 1366, 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.event.set_grab(True)   # trava ou nao o mouse dentro da janela
pygame.mouse.set_visible(True)  # esconde ou exibe o cursor

pygame.display.set_caption("Raízes do medo")

class Tela:
    def __init__(self, caminho_img, som_nome=None):
        self.fundo = pygame.transform.scale(
            pygame.image.load(caminho_img).convert(),
            (LARGURA, ALTURA)
        )
        self.som_nome = som_nome
        self.som_tocou = False
        self.botoes = []  # lista de rects desenhados

    def exibir(self, sons: GerenciadorDeSom):
        TELA.blit(self.fundo, (0, 0))
        if self.som_nome and not self.som_tocou:
            if(arquivo.getConfig("narradorativo") == "true"):
                sons.tocar(self.som_nome, "narrador", False)
            self.som_tocou = True

    def resetar_som(self):
        self.som_tocou = False

    def carregarBotoes(self, botoes_info):
        """
        botoes_info: lista de tuplas [(x_rel, y_rel, w_rel, h_rel, texto), ...]
        onde valores *_rel são frações da tela (ex: 0.4 = 40%)
        """
        self.botoes = []
        pos_mouse = pygame.mouse.get_pos()
        fonte = pygame.font.SysFont("arial", int(ALTURA/25), bold=True)
        cursor_hover = False

        for (x_rel, y_rel, w_rel, h_rel, texto) in botoes_info:
            rect = pygame.Rect(
                x_rel * LARGURA,
                y_rel * ALTURA,
                w_rel * LARGURA,
                h_rel * ALTURA
            )

            if rect.collidepoint(pos_mouse):
                cursor_hover = True
                cor = (0, 0, 0, 150)
            else:
                cor = (0, 0, 0, 0)

            # cria surface com alpha
            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            overlay.fill(cor)
            TELA.blit(overlay, rect.topleft)

            # desenha texto centralizado
            txt = fonte.render(texto, True, (0, 0, 0))  # texto preto
            TELA.blit(txt, txt.get_rect(center=rect.center))

            self.botoes.append(rect)

        # troca o cursor
        if cursor_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    def verificar_clique(self, pos_mouse):
        """Retorna o índice do botão clicado ou None"""
        for i, rect in enumerate(self.botoes):
            if rect.collidepoint(pos_mouse):
                return i
        return None
