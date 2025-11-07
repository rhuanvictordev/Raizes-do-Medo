from classes.screen import *
from classes.soundManagement import *
from classes.states import *
from pathlib import Path

class Jogo:
    def __init__(self):
        caminho = Path(__file__).resolve().parent.parent

        self.ultimaCena = "menu"

        self.sons = MapeamentoDeSons()
        self.telas = {
             
            ## MENU
            "menu": Tela(caminho / "assets/images/menu/menu.png", "menu"),
            "config": Tela(caminho / "assets/images/menu/config.png", "config"),
            "continuar": Tela(caminho / "assets/images/menu/novo_jogo.png", ""),
            "creditos": Tela(caminho / "assets/images/menu/creditos.png", "som_creditos"),
            "pausa": Tela(caminho / "assets/images/menu/pausa.png", "pausa"),
            "config_audio": Tela(caminho / "assets/images/menu/config_audio.png", "config_audio"),
            "config_controle": Tela(caminho / "assets/images/menu/config_controle.png", "config_controle"),
            "config_controle_tecla1": Tela(caminho / "assets/images/menu/config_controle1.png", "config_controle_tecla1"),
            "config_controle_tecla2": Tela(caminho / "assets/images/menu/config_controle2.png", "config_controle_tecla2"),

            ## CENAS
            "NOVO_JOGO": Tela(caminho / "assets/images/menu/C_INICIAL.png", "NOVO_JOGO"),
            "C_ACORDAR": Tela(caminho / "assets/images/menu/C_ACORDAR.png", "C_ACORDAR"),

            "C1": Tela(caminho / "assets/images/cenas/C1.png", "C1"),
            "A": Tela(caminho / "assets/images/cenas/A.png", "A"),
            "B": Tela(caminho / "assets/images/cenas/B.png", "B"),
            "A2": Tela(caminho / "assets/images/cenas/A2.png", "A2"),
            "AB": Tela(caminho / "assets/images/cenas/AB.png", "AB"),
            "BA": Tela(caminho / "assets/images/cenas/BA.png", "BA"),
            "B2": Tela(caminho / "assets/images/cenas/B2.png", "B2"),
            "A3": Tela(caminho / "assets/images/cenas/A3.png", "A3"),
            "A2B": Tela(caminho / "assets/images/cenas/A2B.png", "A2B"),
            "ABA": Tela(caminho / "assets/images/cenas/ABA.png", "ABA"),
            "B2A": Tela(caminho / "assets/images/cenas/B2A.png", "B2A"),
            "B3": Tela(caminho / "assets/images/cenas/B3.png", "B3"),
            "A3B": Tela(caminho / "assets/images/cenas/A3B.png", "A3B"),
            "A4": Tela(caminho / "assets/images/cenas/A4.png", "A4"),
            "A4B": Tela(caminho / "assets/images/cenas/A4B.png", "A4B"),
            "A5": Tela(caminho / "assets/images/cenas/A5.png", "A5"),
            "A6": Tela(caminho / "assets/images/cenas/A6.png", "A6"),
            "BA2": Tela(caminho / "assets/images/cenas/BA2.png", "BA2"),
            "BA3": Tela(caminho / "assets/images/cenas/BA3.png", "BA3"),
            "B2A2": Tela(caminho / "assets/images/cenas/B2A2.png", "B2A2"),
            "B2A3": Tela(caminho / "assets/images/cenas/B2A3.png", "B2A3"),
            "B2A2B": Tela(caminho / "assets/images/cenas/B2A2B.png", "B2A2B"),
            "B3A": Tela(caminho / "assets/images/cenas/B3A.png", "B3A"),
            "B2A2BA": Tela(caminho / "assets/images/cenas/B2A2BA.png", "B2A2BA"),
            "B2A2BAB": Tela(caminho / "assets/images/cenas/B2A2BAB.png", "B2A2BAB"),
            "B2A2BABA": Tela(caminho / "assets/images/cenas/B2A2BABA.png", "B2A2BABA"),
            "B2A2BAB2": Tela(caminho / "assets/images/cenas/B2A2BAB2.png", "B2A2BAB2"),
            "A4BA": Tela(caminho / "assets/images/cenas/A4BA.png", "A4BA"),
            "A4BA2": Tela(caminho / "assets/images/cenas/A4BA2.png", "A4BA2"),
            "A4BAB": Tela(caminho / "assets/images/cenas/A4BAB.png", "A4BAB"),
            "A4BAB2": Tela(caminho / "assets/images/cenas/A4BAB2.png", "A4BAB2"),
            "GAME_OVER_1": Tela(caminho / "assets/images/cenas/GAME_OVER_1.png", "GAME_OVER_1"),
            "GAME_OVER_2": Tela(caminho / "assets/images/cenas/GAME_OVER_2.png", "GAME_OVER_2"),
            "GAME_OVER_6": Tela(caminho / "assets/images/cenas/GAME_OVER_6.png", "GAME_OVER_6"),
            "MORREU": Tela(caminho / "assets/images/cenas/MORREU.png", "MORREU"),
            "A4B2": Tela(caminho / "assets/images/cenas/A4B2.png", "A4B2"),
            "A4B2A": Tela(caminho / "assets/images/cenas/A4B2A.png", "A4B2A"),
            "A4B3": Tela(caminho / "assets/images/cenas/A4B3.png", "A4B3"),
            "A4B2A2": Tela(caminho / "assets/images/cenas/A4B2A2.png", "A4B2A2"),
            "A4B2AB": Tela(caminho / "assets/images/cenas/A4B2AB.png", "A4B2AB"),
            "GAME_OVER_4": Tela(caminho / "assets/images/cenas/GAME_OVER_4.png", "GAME_OVER_4"),
            "A4B4": Tela(caminho / "assets/images/cenas/A4B4.png", "A4B4"),
            "A4B2A3": Tela(caminho / "assets/images/cenas/A4B2A3.png", "A4B2A3"),
            "GAME_OVER_3": Tela(caminho / "assets/images/cenas/GAME_OVER_3.png", "GAME_OVER_3"),
            "A4B4A": Tela(caminho / "assets/images/cenas/A4B4A.png", "A4B4A"),
            "GAME_OVER_5": Tela(caminho / "assets/images/cenas/GAME_OVER_5.png", "GAME_OVER_5"),

            "A4B2A3B": Tela(caminho / "assets/images/cenas/A4B2A3B.png", "A4B2A3B"),
            "A4B2A3BA": Tela(caminho / "assets/images/cenas/A4B2A3BA.png", "A4B2A3BA"),
            "GAME_OVER_7": Tela(caminho / "assets/images/cenas/GAME_OVER_7.png", "GAME_OVER_7"),
        }

        self.estado_atual_nome = "menu"

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
            "A2": A2(self),
            "AB": AB(self),
            "BA": BA(self),
            "B2": B2(self),
            "A3": A3(self),
            "A2B": A2B(self),
            "ABA": ABA(self),
            "B2A": B2A(self),
            "B3": B3(self),
            "A3B": A3B(self),
            "A4": A4(self),
            "A4B": A4B(self),
            "A5": A5(self),
            "A6": A6(self),
            "BA2": BA2(self),
            "BA3": BA3(self),
            "B2A2": B2A2(self),
            "B2A3": B2A3(self),
            "B2A2B": B2A2B(self),
            "B3A": B3A(self),
            "B2A2BA": B2A2BA(self),
            "B2A2BAB": B2A2BAB(self),
            "B2A2BABA": B2A2BABA(self),
            "B2A2BAB2": B2A2BAB2(self),
            "A4BA": A4BA(self),
            "A4BA2": A4BA2(self),
            "A4BAB": A4BAB(self),
            "A4BAB2": A4BAB2(self),
            "GAME_OVER_1": GAME_OVER_1(self),
            "GAME_OVER_2": GAME_OVER_2(self),
            "GAME_OVER_6": GAME_OVER_6(self),
            "MORREU": MORREU(self),
            "A4B2": A4B2(self),
            "A4B2A": A4B2A(self),
            "A4B3": A4B3(self),
            "A4B2A2": A4B2A2(self),
            "A4B2AB": A4B2AB(self),
            "GAME_OVER_4": GAME_OVER_4(self),
            "A4B4": A4B4(self),
            "A4B2A3": A4B2A3(self),
            "GAME_OVER_3": GAME_OVER_3(self),
            "A4B4A": A4B4A(self),
            "GAME_OVER_5": GAME_OVER_5(self),

            "A4B2A3B": A4B2A3B(self),
            "A4B2A3BA": A4B2A3BA(self),
            "GAME_OVER_7": GAME_OVER_7(self),
        }
        
        
        self.estado_antes_da_pausa = None
        self.estado = self.estados[self.estado_atual_nome]

    def mudar_estado(self, novoEstado, tempo=1):
        if novoEstado == 'pausa':
            if self.estado != self.estados['pausa']:
                self.estado_anterior_nome = self.estado_atual_nome
            self.estado = self.estados['pausa']

        elif novoEstado in self.estados:
            self.transicao_com_fade(self.estado_atual_nome, novoEstado, tempo=1)
            self.estado_anterior_nome = self.estado_atual_nome
            self.estado_atual_nome = novoEstado
            self.estado = self.estados[novoEstado]
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


    def transicao_com_fade(self, estadoAgora, estadoNovo, tempo):
        tamanhoTela = pygame.Surface((LARGURA, ALTURA))
        
        for alpha in range(0, 255, 100):
            self.telas[estadoAgora].exibir(self.sons)
            tamanhoTela.set_alpha(alpha)
            TELA.blit(tamanhoTela, (0, 0))
            pygame.display.update()
            pygame.time.delay(tempo)
        self.telas[estadoNovo].resetar_som()
        
        for alpha in range(255, 0, -100):
            self.telas[estadoNovo].exibir(self.sons)
            tamanhoTela.set_alpha(alpha)
            TELA.blit(tamanhoTela, (0, 0))
            pygame.display.update()
            pygame.time.delay(tempo)