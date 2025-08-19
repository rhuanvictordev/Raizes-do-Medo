import pygame
import sys
import service.prop as arquivoConfig


# ------------------- Estado Base -------------------
class Estado:
    def __init__(self, jogo):
        self.jogo = jogo

# ------------------- Estados -------------------

class EstadoMenu(Estado):
    def exibir(self):
        self.jogo.telas["menu"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.key == pygame.K_LCTRL:
            self.jogo.sons.tocar("menu", "narrador")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.parar_musica()
            self.jogo.mudar_estado("cena01")

        elif event.key == pygame.K_2:
            self.jogo.mudar_estado(arquivoConfig.getSave("tela")) # continua o jogo do ponto que parou
            
        elif event.key == pygame.K_3:
            self.jogo.mudar_estado("config")
        elif event.key == pygame.K_4:
            self.jogo.mudar_estado("creditos")
        elif event.key == pygame.K_ESCAPE:
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
        self.jogo.sons.tocar("musica", "musica", True)

    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.parar_musica()
            self.jogo.telas["pausa"].resetar_som()
            self.jogo.mudar_estado(self.jogo.ultimaCena)
            

        elif event.key == pygame.K_LCTRL:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("pausa", "narrador")

    def resetar_som(self):
        self.jogo.telas["pausa"].resetar_som()

class EstadoContinuar(Estado):
    pass

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
            narrador_vol = self.jogo.sons.ajustar_volume("narrador", -0.1)
            arquivoConfig.setConfig("narrador", narrador_vol)
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_n_mais", "narrador")
            narrador_vol = self.jogo.sons.ajustar_volume("narrador", 0.1)
            arquivoConfig.setConfig("narrador", narrador_vol)
        elif event.key == pygame.K_3:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_m_menos", "narrador")
            musica_vol = self.jogo.sons.ajustar_volume("musica", -0.1)
            arquivoConfig.setConfig("musica", musica_vol)
        elif event.key == pygame.K_4:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("som_m_mais", "narrador")
            musica_vol = self.jogo.sons.ajustar_volume("musica", 0.1)
            arquivoConfig.setConfig("musica", musica_vol)

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

class Cena01(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena01"].exibir(self.jogo.sons)
        arquivoConfig.setSave("tela", "cena01")
        self.jogo.ultimaCena = "cena01"
    
    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena02")
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena02")
        elif event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("pausa")

    def resetar_som(self):
        self.jogo.telas["cena01"].resetar_som()

class Cena02(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena02"].exibir(self.jogo.sons)
        arquivoConfig.setSave("tela", "cena02")
        self.jogo.ultimaCena = "cena02"
    
    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena03")
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena03")
        elif event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("pausa")

    def resetar_som(self):
        self.jogo.telas["cena02"].resetar_som()


class Cena03(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena03"].exibir(self.jogo.sons)
        arquivoConfig.setSave("tela", "cena03")
        self.jogo.ultimaCena = "cena03"
    
    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena04")
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena04")
        elif event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("pausa")

    def resetar_som(self):
        self.jogo.telas["cena03"].resetar_som()


class Cena04(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena04"].exibir(self.jogo.sons)
        arquivoConfig.setSave("tela", "cena04")
        self.jogo.ultimaCena = "cena04"
    
    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena05")
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena05")
        elif event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("pausa")

    def resetar_som(self):
        self.jogo.telas["cena04"].resetar_som()

class Cena05(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena05"].exibir(self.jogo.sons)
        arquivoConfig.setSave("tela", "cena05")
        self.jogo.ultimaCena = "cena05"
    
    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena06")
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena06")
        elif event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("pausa")

    def resetar_som(self):
        self.jogo.telas["cena05"].resetar_som()

class Cena06(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena06"].exibir(self.jogo.sons)
        arquivoConfig.setSave("tela", "cena06")
        self.jogo.ultimaCena = "cena06"
    
    def processar_eventos(self, event):
        if event.key == pygame.K_ESCAPE:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("menu")
        elif event.key == pygame.K_1:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena01")
        elif event.key == pygame.K_2:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("cena01")
        elif event.key == pygame.K_p:
            self.jogo.sons.parar_narrador()
            self.jogo.mudar_estado("pausa")

    def resetar_som(self):
        self.jogo.telas["cena06"].resetar_som()
