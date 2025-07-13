import pygame
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 640, 480
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Raízes do medo")
FONTE = pygame.font.SysFont('calibri', 28)
clock = pygame.time.Clock()

# ------------------- Gerenciador de Som -------------------
class GerenciadorDeSom:
    def __init__(self):
        self.sons = {
            "musica": pygame.mixer.Sound("s_musica.mp3"),
            "menu": pygame.mixer.Sound("s_n_menu.mp3"),
            "config": pygame.mixer.Sound("s_n_configuracoes.mp3"),
            "pausa": pygame.mixer.Sound("s_n_pausa.mp3"),
            "novo_jogo": pygame.mixer.Sound("s_n_novo_jogo.mp3"),
            "config_audio": pygame.mixer.Sound("s_n_c_audio.mp3"),
            "config_controle": pygame.mixer.Sound("s_n_c_controles.mp3"),
            "som_creditos": pygame.mixer.Sound("s_n_creditos.mp3"),
            "som_n_menos": pygame.mixer.Sound("s_n_menos.mp3"),
            "som_n_mais": pygame.mixer.Sound("s_n_mais.mp3"),
            "som_m_menos": pygame.mixer.Sound("s_n_musica_menos.mp3"),
            "som_m_mais": pygame.mixer.Sound("s_n_musica_mais.mp3"),
            "som_sair": pygame.mixer.Sound("s_n_sair.mp3")
        }

        self.canais = {
            "musica": pygame.mixer.Channel(0),
            "narrador": pygame.mixer.Channel(1)
        }

        self.volumes = {
            "musica": 0.6,
            "narrador": 0.4
        }

    def tocar(self, nome_som, canal, loop=False):
        if not self.canais[canal].get_busy():
            loops = -1 if loop else 0
            self.canais[canal].play(self.sons[nome_som], loops=loops)
            vol = self.volumes.get(canal, 1.0)
            self.canais[canal].set_volume(vol)

    def ajustar_volume(self, canal, delta):
        if canal in self.canais and canal in self.volumes:
            novo_volume = self.volumes[canal] + delta
            novo_volume = max(0.0, min(1.0, novo_volume))
            self.volumes[canal] = novo_volume
            self.canais[canal].set_volume(novo_volume)
            print(f"Volume de '{canal}' ajustado para {novo_volume:.2f}")

    def parar_musica(self):
        self.canais["musica"].stop()

    def parar_narrador(self):
        self.canais["narrador"].stop()

# ------------------- Classe de Tela -------------------
class Tela:
    def __init__(self, caminho_img, som_nome=None):
        self.fundo = pygame.transform.scale(pygame.image.load(caminho_img).convert(), (LARGURA, ALTURA))
        self.som_nome = som_nome
        self.som_tocou = False

    def exibir(self, sons: GerenciadorDeSom):
        TELA.blit(self.fundo, (0, 0))
        if self.som_nome and not self.som_tocou:
            sons.tocar(self.som_nome, "narrador")
            self.som_tocou = True

    def resetar_som(self):
        self.som_tocou = False

# ------------------- Estado Base -------------------
class Estado:
    def __init__(self, jogo):
        self.jogo = jogo

    def exibir(self):
        pass

    def processar_eventos(self, event):
        pass

    def resetar_som(self):
        pass

# ------------------- Estados -------------------
class EstadoMenu(Estado):
    def exibir(self):
        self.jogo.telas["menu"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_LCTRL:
            self.jogo.sons.tocar("menu", "narrador")
        elif event.key == pygame.K_1:
            self.jogo.mudar_estado("novo_jogo")
        elif event.key == pygame.K_2:
            self.jogo.mudar_estado("continuar")
        elif event.key == pygame.K_3:
            self.jogo.mudar_estado("config")
        elif event.key == pygame.K_4:
            self.jogo.mudar_estado("creditos")
        elif event.key == pygame.K_5:
            self.jogo.sons.tocar("som_sair", "narrador")
            pygame.time.delay(int(self.jogo.sons.sons["som_sair"].get_length() * 1000))
            pygame.quit()
            sys.exit()

    def resetar_som(self):
        self.jogo.telas["menu"].resetar_som()

class EstadoNovoJogo(Estado):
    def exibir(self):
        self.jogo.telas["novo_jogo"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("pausa")
        elif event.key == pygame.K_LCTRL:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("novo_jogo", "narrador")

    def resetar_som(self):
        self.jogo.telas["novo_jogo"].resetar_som()

class EstadoPausa(Estado):
    def exibir(self):
        self.jogo.telas["pausa"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")  # Basta passar a string
            self.jogo.telas["pausa"].resetar_som()
        elif event.key == pygame.K_LCTRL:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("pausa", "narrador")

        elif event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            if self.jogo.estado_anterior_nome:
                self.jogo.mudar_estado(self.jogo.estado_anterior_nome)
                self.jogo.telas["pausa"].resetar_som()

    def resetar_som(self):
        self.jogo.telas["pausa"].resetar_som()

class EstadoContinuar(Estado):
    def exibir(self):
        self.jogo.telas["continuar"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.mudar_estado("menu")

    def resetar_som(self):
        self.jogo.telas["continuar"].resetar_som()

class EstadoCreditos(Estado):
    def exibir(self):
        self.jogo.telas["creditos"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_LCTRL:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_creditos", "narrador")

    def resetar_som(self):
        self.jogo.telas["creditos"].resetar_som()

class EstadoConfig(Estado):
    def exibir(self):
        self.jogo.telas["config"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.key == pygame.K_ESCAPE:
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_1:
            self.jogo.mudar_estado("config_audio")
        elif event.key == pygame.K_2:
            self.jogo.mudar_estado("config_controle")
        elif event.key == pygame.K_LCTRL:
            self.jogo.sons.tocar("config", "narrador")

    def resetar_som(self):
        self.jogo.telas["config"].resetar_som()

class EstadoConfigAudio(Estado):
    def exibir(self):
        self.jogo.telas["config_audio"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("config")
        elif event.key == pygame.K_LCTRL:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("config_audio", "narrador")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_n_menos", "narrador")
            self.jogo.sons.ajustar_volume("narrador", -0.1)
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_n_mais", "narrador")
            self.jogo.sons.ajustar_volume("narrador", 0.1)
        elif event.key == pygame.K_3:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_m_menos", "narrador")
            self.jogo.sons.ajustar_volume("musica", -0.1)
        elif event.key == pygame.K_4:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_m_mais", "narrador")
            self.jogo.sons.ajustar_volume("musica", 0.1)

    def resetar_som(self):
        self.jogo.telas["config_audio"].resetar_som()

class EstadoConfigControle(Estado):
    def exibir(self):
        self.jogo.telas["config_controle"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("config")
        elif event.key == pygame.K_LCTRL:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("config_controle", "narrador")
        elif event.key == pygame.K_1:
            print("controle 1")
        elif event.key == pygame.K_2:
            print("controle 2")

    def resetar_som(self):
        self.jogo.telas["config_controle"].resetar_som()

# ------------------- Jogo Principal -------------------
class Jogo:
    def __init__(self):
        self.sons = GerenciadorDeSom()
        self.telas = {
            "menu": Tela("menu.png", "menu"),
            "config": Tela("config.png", "config"),
            "novo_jogo": Tela("novo_jogo.png", "novo_jogo"),
            "continuar": Tela("novo_jogo.png", ""),
            "creditos": Tela("creditos.png", "som_creditos"),
            "pausa": Tela("pausa.png", "pausa"),
            "config_audio": Tela("config_audio.png", "config_audio"),
            "config_controle": Tela("config_controle.png", "config_controle")
        }
        self.estados = {
            "menu": EstadoMenu(self),
            "novo_jogo": EstadoNovoJogo(self),
            "continuar": EstadoContinuar(self),
            "creditos": EstadoCreditos(self),
            "config": EstadoConfig(self),
            "config_audio": EstadoConfigAudio(self),
            "config_controle": EstadoConfigControle(self),
            "pausa": EstadoPausa(self)
        }

        self.estado_atual_nome = "menu"
        self.estado_anterior_nome = None
        self.estado = self.estados[self.estado_atual_nome]

    def mudar_estado(self, estadoNovo):
        if estadoNovo == 'pausa':
            if self.estado != self.estados['pausa']:
                self.estado_anterior_nome = self.estado_atual_nome
            self.estado = self.estados['pausa']

        elif estadoNovo in self.estados:
            self.transicao_com_fade(self.estado_atual_nome, estadoNovo)
            self.estado_anterior_nome = self.estado_atual_nome
            self.estado_atual_nome = estadoNovo
            self.estado = self.estados[estadoNovo]
            self.estado.resetar_som()

    def atualizar_tela(self):
        self.estado.exibir()

    def processar_eventos(self):
        for event in pygame.event.get():
            if not self.sons.canais["musica"].get_busy():
                self.sons.tocar("musica", "musica", True)
            if event.type == pygame.QUIT:
                self.sons.parar_narrador()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.estado.processar_eventos(event)

    def transicao_com_fade(self, de_estado, para_estado):
        if de_estado not in self.telas or para_estado not in self.telas:
            return
        fade = pygame.Surface((LARGURA, ALTURA))
        fade.fill((0, 0, 0))
        for alpha in range(0, 255, 10):
            self.telas[de_estado].exibir(self.sons)
            fade.set_alpha(alpha)
            TELA.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(15)
        self.telas[para_estado].resetar_som()
        for alpha in range(255, 0, -10):
            self.telas[para_estado].exibir(self.sons)
            fade.set_alpha(alpha)
            TELA.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(15)

# ------------------- Execução -------------------
if __name__ == "__main__":
    jogo = Jogo()
    while True:
        jogo.processar_eventos()
        jogo.atualizar_tela()
        pygame.display.flip()
        clock.tick(60)
