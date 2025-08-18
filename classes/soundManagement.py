from pathlib import Path
import pygame
import service.prop as arquivoConfig


class GerenciadorDeSom:
    def __init__(self):
        root_path = Path(__file__).resolve().parent.parent

        self.sons = {
            "musica": pygame.mixer.Sound(root_path / "assets/sounds/s_musica.mp3"),
            "menu": pygame.mixer.Sound(root_path / "assets/sounds/s_n_menu.mp3"),
            "config": pygame.mixer.Sound(root_path / "assets/sounds/s_n_configuracoes.mp3"),
            "pausa": pygame.mixer.Sound(root_path / "assets/sounds/s_n_pausa.mp3"),
            "novo_jogo": pygame.mixer.Sound(root_path / "assets/sounds/cena01.mp3"),
            "config_audio": pygame.mixer.Sound(root_path / "assets/sounds/s_n_c_audio.mp3"),
            "config_controle": pygame.mixer.Sound(root_path / "assets/sounds/s_n_c_controles.mp3"),
            "som_creditos": pygame.mixer.Sound(root_path / "assets/sounds/s_n_creditos.mp3"),
            "som_n_menos": pygame.mixer.Sound(root_path / "assets/sounds/s_n_menos.mp3"),
            "som_n_mais": pygame.mixer.Sound(root_path / "assets/sounds/s_n_mais.mp3"),
            "som_m_menos": pygame.mixer.Sound(root_path / "assets/sounds/s_n_musica_menos.mp3"),
            "som_m_mais": pygame.mixer.Sound(root_path / "assets/sounds/s_n_musica_mais.mp3"),
            "som_sair": pygame.mixer.Sound(root_path / "assets/sounds/s_n_sair.mp3"),
            "cena01": pygame.mixer.Sound(root_path / "assets/sounds/cena01.mp3"),
            "cena02": pygame.mixer.Sound(root_path / "assets/sounds/cena02.mp3")
        }

        self.canais = {
            "musica": pygame.mixer.Channel(0),
            "narrador": pygame.mixer.Channel(1)
        }

        self.volumes = {
            "musica": float(arquivoConfig.get("musica")),
            "narrador": float(arquivoConfig.get("narrador"))
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
            return (f"{novo_volume:.2f}")
            print(f"Volume de '{canal}' ajustado para {novo_volume:.2f}")

    def parar_musica(self):
        self.canais["musica"].stop()

    def parar_narrador(self):
        self.canais["narrador"].stop()