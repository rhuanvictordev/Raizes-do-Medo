import pygame
from classes.game import Jogo

# Inicialização
pygame.init()
pygame.display.set_caption("Raízes do medo")
FONTE = pygame.font.SysFont('calibri', 28)
clock = pygame.time.Clock()


# ------------------- Execução -------------------
if __name__ == "__main__":
    jogo = Jogo()
    while True:
        jogo.processar_eventos()
        jogo.atualizar_tela()
        pygame.display.flip()
        clock.tick(260)
