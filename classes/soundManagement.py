from pathlib import Path
import pygame
import service.prop as arquivoConfig


class GerenciadorDeSom:
    def __init__(self):
        root_path = Path(__file__).resolve().parent.parent

        self.sons = {
            "ruido": pygame.mixer.Sound(root_path / "assets/sounds/menu/ruido.mp3"),
            "musica": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_musica.mp3"),
            "menu": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_menu.mp3"),
            "config": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_configuracoes.mp3"),
            "pausa": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_pausa.mp3"),
            "config_audio": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_c_audio.mp3"),
            "config_controle": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_c_controles.mp3"),
            "config_controle_alterado": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_c_alterado.mp3"),
            "config_controle_usada": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_c_tecla_usada.mp3"),
            "config_controle_tecla1": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_c_c_primeira.mp3"),
            "config_controle_tecla2": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_c_c_segunda.mp3"),
            "som_creditos": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_creditos.mp3"),
            "som_n_menos": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_menos.mp3"),
            "som_n_mais": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_mais.mp3"),
            "som_m_menos": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_musica_menos.mp3"),
            "som_m_mais": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_musica_mais.mp3"),
            "som_sair": pygame.mixer.Sound(root_path / "assets/sounds/menu/s_n_sair.mp3"),

            "NOVO_JOGO": pygame.mixer.Sound(root_path / "assets/sounds/menu/C_INICIAL.mp3"), # INICIANDO UM NOVO JOGO -> VOCE SE CHAMA JOAO
            "C_ACORDAR": pygame.mixer.Sound(root_path / "assets/sounds/menu/C_ACORDAR.mp3"), # VOCE ACORDA EM SUA CASA
            
            # PRIMEIRA CENA:
            "C1": pygame.mixer.Sound(root_path / "assets/sounds/cenas/C1.mp3"), # ELIAS: -OPA JOAO TUDO CERTO?
            "A": pygame.mixer.Sound(root_path / "assets/sounds/cenas/A.mp3"),
            "B": pygame.mixer.Sound(root_path / "assets/sounds/cenas/B.mp3"),
        }

        self.canais = {
            "musica": pygame.mixer.Channel(0),
            "narrador": pygame.mixer.Channel(1),
            "ruido": pygame.mixer.Channel(2)
        }

        self.volumes = {
            "musica": float(arquivoConfig.getConfig("musica")),
            "narrador": float(arquivoConfig.getConfig("narrador"))
        }


    def tocar(self, nome_som, canal, loop=False):
        if not self.canais[canal].get_busy():
            loops = -1 if loop else 0
            self.canais[canal].play(self.sons[nome_som], loops=loops)
            vol = self.volumes.get(canal, 1.0)
            self.canais[canal].set_volume(vol)

    def tocar_ruido(self, loop=True):
        if not self.canais["ruido"].get_busy():
            loops = -1 if loop else 0
            self.canais["ruido"].play(self.sons["ruido"], loops=loops)
            self.canais["ruido"].set_volume(0.10)

    def ajustar_volume(self, canal, delta):
        if canal in self.canais and canal in self.volumes:
            novo_volume = self.volumes[canal] + delta
            novo_volume = max(0.0, min(1.0, novo_volume))
            self.volumes[canal] = novo_volume
            self.canais[canal].set_volume(novo_volume)
            arquivoConfig.setConfig(canal, novo_volume)

    def parar_musica(self):
        self.canais["musica"].stop()

    def parar_narrador(self):
        self.canais["narrador"].stop()

    def parar_ruido(self):
        self.canais["ruido"].stop()