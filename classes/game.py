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
            "menu": Tela(root_path / "assets/images/menu.png", "menu"),
            "config": Tela(root_path / "assets/images/config.png", "config"),
            "novo_jogo": Tela(root_path / "assets/images/novo_jogo.png", "novo_jogo"),
            "continuar": Tela(root_path / "assets/images/novo_jogo.png", ""),
            "creditos": Tela(root_path / "assets/images/creditos.png", "som_creditos"),
            "pausa": Tela(root_path / "assets/images/pausa.png", "pausa"),
            "config_audio": Tela(root_path / "assets/images/config_audio.png", "config_audio"),
            "config_controle": Tela(root_path / "assets/images/config_controle.png", "config_controle"),
            "cena01": Tela(root_path / "assets/images/cena01.png", "cena01"),
            "cena02": Tela(root_path / "assets/images/cena02.png", "cena02"),
            "cena03": Tela(root_path / "assets/images/cena03.png", "cena03"),
            "cena04": Tela(root_path / "assets/images/cena04.png", "cena04"),
            "cena05": Tela(root_path / "assets/images/cena05.png", "cena05"),
            "cena06": Tela(root_path / "assets/images/cena06.png", "cena06")
        }
        self.estados = {
            "menu": EstadoMenu(self),
            "novo_jogo": EstadoNovoJogo(self),
            "continuar": EstadoContinuar(self),
            "creditos": EstadoCreditos(self),
            "config": EstadoConfig(self),
            "config_audio": EstadoConfigAudio(self),
            "config_controle": EstadoConfigControle(self),
            "pausa": EstadoPausa(self),
            "cena01": Cena01(self),
            "cena02": Cena02(self),
            "cena03": Cena03(self),
            "cena04": Cena04(self),
            "cena05": Cena05(self),
            "cena06": Cena06(self)
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
            pygame.time.delay(1)
        self.telas[para_estado].resetar_som()
        for alpha in range(255, 0, -10):
            self.telas[para_estado].exibir(self.sons)
            fade.set_alpha(alpha)
            TELA.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)

    