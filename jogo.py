import pygame
import sys

# Inicialização
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("jogo")
font = pygame.font.SysFont('calibri', 28)
clock = pygame.time.Clock()

# Som de fundo
som_fundo = pygame.mixer.Sound('som_fundo.mp3')

# Cores
BRANCO = (255, 255, 255)
FUNDO_OPCAO = (50, 50, 50)

# Fundo do menu
fundo_menu = pygame.image.load("f.png").convert()
fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))

fundo_pausa = pygame.image.load("p.png").convert()
fundo_pausa = pygame.transform.scale(fundo_pausa, (largura, altura))

fundo_creditos = pygame.image.load("c.png").convert()
fundo_creditos = pygame.transform.scale(fundo_creditos, (largura, altura))

fundo_menu = pygame.image.load("m.png").convert()
fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))

# Estado e variáveis
estado = "menu_principal"
estado_anterior = None
volume = 0.5
som_tocando = False
som_fundo.set_volume(volume)

# ---------- Funções das Telas ----------

def tela_menu_principal():
    tela.blit(fundo_menu, (0, 0))  # agora usa a imagem de fundo

def tela_configuracoes():
    opcoes = ["[1] ÁUDIO", "[2] CONTROLE"]
    desenhar_tela_com_opcoes("SETTINGS", opcoes)

def tela_audio():
    tela.blit(fundo_menu, (0, 0))

    titulo = font.render("ÁUDIO", True, BRANCO)
    tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 6))

    texto_volume = font.render(f"Volume: {int(volume * 100)}%", True, BRANCO)
    barra_largura = 300
    barra_altura = 20
    barra_x = largura // 2 - barra_largura // 2
    barra_y = altura // 2

    pygame.draw.rect(tela, (100, 100, 100), (barra_x, barra_y, barra_largura, barra_altura), border_radius=10)
    pygame.draw.rect(tela, (0, 200, 100), (barra_x, barra_y, barra_largura * volume, barra_altura), border_radius=10)

    tela.blit(texto_volume, (largura // 2 - texto_volume.get_width() // 2, barra_y - 50))

    esc = font.render("ESC para voltar", True, BRANCO)
    esc_rect = esc.get_rect(bottomright=(largura - 20, altura - 20))
    tela.blit(esc, esc_rect)

def tela_controle():
    tela.blit(fundo_menu, (0, 0))
    titulo = font.render("CONTROLE", True, BRANCO)
    tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 4))

    instrucoes = [
        "Seta Esquerda: Diminuir Volume",
        "Seta Direita: Aumentar Volume",
        "ESC: Voltar"
    ]
    for i, texto in enumerate(instrucoes):
        txt = font.render(texto, True, BRANCO)
        tela.blit(txt, (largura // 2 - txt.get_width() // 2, altura // 2 + i * 40))

def tela_creditos():
    tela.blit(fundo_creditos, (0, 0))  # agora usa a imagem de fundo

def tela_iniciar():
    tela.blit(fundo_menu, (0, 0))
    texto = font.render("Iniciando jogo...", True, BRANCO)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2))

def tela_continuar():
    tela.blit(fundo_menu, (0, 0))
    texto = font.render("Continuando jogo...", True, BRANCO)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2))

def tela_pausa():
    tela.blit(fundo_pausa, (0, 0))  # agora usa a imagem de fundo
    texto = font.render("JOGO PAUSADO", True, BRANCO)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2))

    dica = font.render("Pressione P para continuar", True, BRANCO)
    tela.blit(dica, (largura // 2 - dica.get_width() // 2, altura // 2 + 40))

# ---------- Função Utilitária ----------
def desenhar_tela_com_opcoes(titulo, opcoes):
    tela.blit(fundo_menu, (0, 0))
    titulo_render = font.render(titulo, True, BRANCO)
    #tela.blit(titulo_render, (largura // 2 - titulo_render.get_width() // 2, altura // 7))

    padding = 10
    for i, texto in enumerate(opcoes):
        label = font.render(texto, True, BRANCO)
        label_rect = label.get_rect()
        pos_x = largura / 2 - 0.6 * label.get_width()
        pos_y = altura / 2 + i * 60
        label_rect.topleft = (pos_x, pos_y)

        fundo_rect = pygame.Rect(
            label_rect.left - padding,
            label_rect.top - padding,
            label_rect.width + padding * 2,
            label_rect.height + padding * 2
        )
        pygame.draw.rect(tela, FUNDO_OPCAO, fundo_rect, border_radius=8)
        tela.blit(label, label_rect)

    if estado != "menu_principal":
        esc = font.render("ESC para voltar", True, BRANCO)
        esc_rect = esc.get_rect(bottomright=(largura - 20, altura - 20))
        tela.blit(esc, esc_rect)

# ---------- Loop Principal ----------
while True:
    for event in pygame.event.get():
        if not som_tocando:
                        som_fundo.play(loops=-1)
                        som_fundo.set_volume(volume)
                        som_tocando = True
        if event.type == pygame.QUIT:
            som_fundo.stop()
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # PAUSAR
            if event.key == pygame.K_p:
                if estado != "pausado":
                    estado_anterior = estado
                    estado = "pausado"
                else:
                    estado = estado_anterior

            # ESC para voltar
            if event.key == pygame.K_ESCAPE:
                if estado in ["menu_config_audio", "menu_config_controle"]:
                    estado = "menu_config"
                elif estado != "menu_principal":
                    estado = "menu_principal"

            if estado == "menu_principal":
                if event.key == pygame.K_1:
                    estado = "iniciar"
                elif event.key == pygame.K_2:
                    estado = "continuar"
                elif event.key == pygame.K_3:
                    estado = "menu_config"
                elif event.key == pygame.K_4:
                    estado = "creditos"
                elif event.key == pygame.K_5:
                    som_fundo.stop()
                    pygame.quit()
                    sys.exit()

            elif estado == "menu_config":
                if event.key == pygame.K_1:
                    estado = "menu_config_audio"
                elif event.key == pygame.K_2:
                    estado = "menu_config_controle"

            elif estado == "menu_config_audio":
                if event.key == pygame.K_LEFT:
                    volume = max(0.0, volume - 0.05)
                    som_fundo.set_volume(volume)
                elif event.key == pygame.K_RIGHT:
                    volume = min(1.0, volume + 0.05)
                    som_fundo.set_volume(volume)

    # Desenhar a tela atual
    if estado == "menu_principal":
        tela_menu_principal()
    elif estado == "menu_config":
        tela_configuracoes()
    elif estado == "menu_config_audio":
        tela_audio()
    elif estado == "menu_config_controle":
        tela_controle()
    elif estado == "creditos":
        tela_creditos()
    elif estado == "iniciar":
        tela_iniciar()
    elif estado == "continuar":
        tela_continuar()
    elif estado == "pausado":
        tela_pausa()

    pygame.display.flip()
    clock.tick(60)
