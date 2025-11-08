import pygame
from classes.game import Jogo, arquivoConfig

pygame.init()
pygame.display.set_caption("Raízes do medo")
FONTE = pygame.font.SysFont('calibri', 28)
clock = pygame.time.Clock()

volumeNarrador = arquivoConfig.getConfig("narrador")
arquivoConfig.setConfig("narradorativo", "true")

if volumeNarrador == None or volumeNarrador == "0.0":
    arquivoConfig.setConfig("narrador", "0.1")
    arquivoConfig.setConfig("narradorativo", "true")

if __name__ == "__main__":
    jogo = Jogo()
    while True:
        jogo.processar_eventos()
        jogo.atualizar_tela()
        pygame.display.flip()
        clock.tick(60)

