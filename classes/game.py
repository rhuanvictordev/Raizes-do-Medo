from classes.screen import *
from classes.soundManagement import *
from classes.states import *
from pathlib import Path

class Jogo:
    def __init__(self):
        root_path = Path(__file__).resolve().parent.parent

        self.ultimaCena = "menu"

        self.sons = GerenciadorDeSom()
        self.telas = {
             
             ## MENU
            "menu": Tela(root_path / "assets/images/menu/menu.png", "menu"),
            "config": Tela(root_path / "assets/images/menu/config.png", "config"),
            "continuar": Tela(root_path / "assets/images/menu/novo_jogo.png", ""),
            "creditos": Tela(root_path / "assets/images/menu/creditos.png", "som_creditos"),
            "pausa": Tela(root_path / "assets/images/menu/pausa.png", "pausa"),
            "config_audio": Tela(root_path / "assets/images/menu/config_audio.png", "config_audio"),
            "config_controle": Tela(root_path / "assets/images/menu/config_controle.png", "config_controle"),
            "config_controle_tecla1": Tela(root_path / "assets/images/menu/config_controle1.png", "config_controle_tecla1"),
            "config_controle_tecla2": Tela(root_path / "assets/images/menu/config_controle2.png", "config_controle_tecla2"),

            ## CENAS
            "NOVO_JOGO": Tela(root_path / "assets/images/menu/C_INICIAL.png", "NOVO_JOGO"),
            "C_ACORDAR": Tela(root_path / "assets/images/menu/C_ACORDAR.png", "C_ACORDAR"),

            "C1": Tela(root_path / "assets/images/cenas/C1.png", "C1"),
            "A": Tela(root_path / "assets/images/cenas/A.png", "A"),
            "B": Tela(root_path / "assets/images/cenas/B.png", "B"),
            
        }
        self.estados = {

            ## MENU
            "menu": EstadoMenu(self),
            "NOVO_JOGO": EstadoNovoJogo(self),
            "C_ACORDAR": C_ACORDAR(self),
            "continuar": EstadoContinuar(self),
            "creditos": EstadoCreditos(self),
            "config": EstadoConfig(self),
            "config_audio": EstadoConfigAudio(self),
            "config_controle": EstadoConfigControle(self),
            "config_controle_tecla1": EstadoConfigControleTecla1(self),
            "config_controle_tecla2": EstadoConfigControleTecla2(self),
            "pausa": EstadoPausa(self),

            ## CENAS
            "C1": C1(self),
            "A": A(self),
            "B": B(self),
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
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
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
            pygame.time.delay(1)
        self.telas[para_estado].resetar_som()
        for alpha in range(255, 0, -10):
            self.telas[para_estado].exibir(self.sons)
            fade.set_alpha(alpha)
            TELA.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)