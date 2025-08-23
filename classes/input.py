import pygame
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 400, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("5 Botões Verticais Translucidos")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 122, 255)

# Fonte
fonte = pygame.font.SysFont(None, 30)

# Criar 5 botões
botao_largura, botao_altura = 200, 50
espaco = 10
botoes = []
for i in range(5):
    x = LARGURA // 2 - botao_largura // 2
    y = 50 + i * (botao_altura + espaco)
    rect = pygame.Rect(x, y, botao_largura, botao_altura)
    texto = fonte.render(f"Botão {i+1}", True, BRANCO)
    texto_rect = texto.get_rect(center=rect.center)
    botoes.append({"rect": rect, "texto": texto, "texto_rect": texto_rect})

# Cursor
cursor_padrao = pygame.SYSTEM_CURSOR_ARROW
cursor_mao = pygame.SYSTEM_CURSOR_HAND

# Loop principal
rodando = True
while rodando:
    tela.fill(PRETO)
    mouse_pos = pygame.mouse.get_pos()
    cursor_atual = cursor_padrao

    for botao in botoes:
        rect = botao["rect"]
        texto = botao["texto"]
        texto_rect = botao["texto_rect"]

        # Verifica se o mouse está sobre o botão
        if rect.collidepoint(mouse_pos):
            cursor_atual = cursor_mao

            # Cria surface translúcida
            botao_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            botao_surface.fill((0, 122, 255, 150))  # RGBA, 150 = alpha (transparência)
            tela.blit(botao_surface, rect.topleft)

        # Desenha o texto por cima
        tela.blit(texto, texto_rect)

    pygame.mouse.set_cursor(cursor_atual)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, botao in enumerate(botoes):
                if botao["rect"].collidepoint(event.pos):
                    print(f"Botão {i+1} apertado!")

    pygame.display.flip()

pygame.quit()
sys.exit()
