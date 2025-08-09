import pygame
import sys


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