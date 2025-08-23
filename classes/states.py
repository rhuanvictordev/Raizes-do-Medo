import pygame
import sys
import service.prop as arquivo


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
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.tocar("menu", "narrador")
            elif event.key == pygame.K_1:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.parar_musica()
                self.jogo.mudar_estado("cena01")
            elif event.key == pygame.K_2:
                self.jogo.mudar_estado(arquivo.getSave("tela")) # continua o jogo do ponto que parou
            elif event.key == pygame.K_3:
                self.jogo.mudar_estado("config")
            elif event.key == pygame.K_4:
                self.jogo.mudar_estado("creditos")
            elif event.key == pygame.K_ESCAPE:
                self.jogo.sons.tocar("som_sair", "narrador")
                pygame.time.delay(int(self.jogo.sons.sons["som_sair"].get_length() * 1000))
                pygame.quit()
                sys.exit()
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("menu", "narrador")

    def resetar_som(self):
        self.jogo.telas["menu"].resetar_som()

class EstadoNovoJogo(Estado):
    def exibir(self):
        self.jogo.telas["cena01"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("novo_jogo", "narrador")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                self.jogo.sons.tocar("menu", "narrador")

    def resetar_som(self):
        self.jogo.telas["novo_jogo"].resetar_som()

class EstadoPausa(Estado):
    def exibir(self):
        self.jogo.telas["pausa"].exibir(self.jogo.sons)
        self.jogo.sons.tocar("musica", "musica", True)

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.parar_musica()
                self.jogo.telas["pausa"].resetar_som()
                self.jogo.mudar_estado(self.jogo.ultimaCena)
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("pausa", "narrador")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("pausa", "narrador")

    def resetar_som(self):
        self.jogo.telas["pausa"].resetar_som()

class EstadoContinuar(Estado):
    pass

class EstadoCreditos(Estado):
    def exibir(self):
        self.jogo.telas["creditos"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("som_creditos", "narrador")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("som_creditos", "narrador")

    def resetar_som(self):
        self.jogo.telas["creditos"].resetar_som()

class EstadoConfig(Estado):
    def exibir(self):
        self.jogo.telas["config"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.mudar_estado("menu")
            elif event.key == pygame.K_1:
                self.jogo.mudar_estado("config_audio")
            elif event.key == pygame.K_2:
                self.jogo.mudar_estado("config_controle")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.tocar("config", "narrador")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("config", "narrador")

    def resetar_som(self):
        self.jogo.telas["config"].resetar_som()

class EstadoConfigAudio(Estado):
    def exibir(self):
        self.jogo.telas["config_audio"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.mudar_estado("config")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.tocar("config_audio", "narrador")
            elif event.key == pygame.K_1:
                self.jogo.sons.tocar("som_n_menos", "narrador")
                self.jogo.sons.ajustar_volume("narrador", -0.1)
                
            elif event.key == pygame.K_2:
                self.jogo.sons.tocar("som_n_mais", "narrador")
                self.jogo.sons.ajustar_volume("narrador", 0.1)
                
            elif event.key == pygame.K_3:
                self.jogo.sons.tocar("som_m_menos", "narrador")
                self.jogo.sons.ajustar_volume("musica", -0.1)
                
            elif event.key == pygame.K_4:
                self.jogo.sons.tocar("som_m_mais", "narrador")
                self.jogo.sons.ajustar_volume("musica", 0.1)
                
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("config_audio", "narrador")
        

    def resetar_som(self):
        self.jogo.telas["config_audio"].resetar_som()

class EstadoConfigControle(Estado):
    def exibir(self):
        self.jogo.telas["config_controle"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.mudar_estado("config")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.tocar("config_controle", "narrador")
            elif event.key == pygame.K_1:
                self.jogo.mudar_estado("config_controle_tecla1")
            elif event.key == pygame.K_2:
                self.jogo.mudar_estado("config_controle_tecla2")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("config_controle", "narrador")

    def resetar_som(self):
        self.jogo.telas["config_controle"].resetar_som()

class EstadoConfigControleTecla1(Estado):
    def exibir(self):
        self.jogo.telas["config_controle_tecla1"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            self.jogo.sons.parar_narrador()
            if event.key == pygame.K_ESCAPE:
                self.jogo.mudar_estado("config_controle")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.tocar("config_controle_tecla1", "narrador")
    # qualquer outra tecla que nao seja ESC ou CTRL e seja diferente de outro controle, será salva no arquivo de config controles
            else:
                tecla1Salva = int(arquivo.getConfig("tecla1", "0"))
                tecla2Salva = int(arquivo.getConfig("tecla2", "0"))
                print("Tecla1Salva:", tecla1Salva, "Tecla2Salva:", tecla2Salva, "Tecla pressionada:", event.key)
                if tecla1Salva != event.key and tecla2Salva != event.key:
                    arquivo.setConfig("tecla1", event.key)
                    self.jogo.sons.tocar("config_controle_alterado", "narrador")
                    self.jogo.mudar_estado("config_controle")
                else:
                    self.jogo.sons.tocar("config_controle_usada", "narrador")

        elif event.type == pygame.MOUSEMOTION:
            pass


    def resetar_som(self):
        self.jogo.telas["config_controle"].resetar_som()

class EstadoConfigControleTecla2(Estado):
    def exibir(self):
        self.jogo.telas["config_controle_tecla2"].exibir(self.jogo.sons)

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            self.jogo.sons.parar_narrador()
            if event.key == pygame.K_ESCAPE:
                self.jogo.mudar_estado("config_controle")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.tocar("config_controle_tecla2", "narrador")
    # qualquer outra tecla que nao seja ESC ou CTRL e seja diferente de outro controle, será salva no arquivo de config controles
            else:
                tecla1Salva = int(arquivo.getConfig("tecla1", "0"))
                tecla2Salva = int(arquivo.getConfig("tecla2", "0"))
                print("Tecla1Salva:", tecla1Salva, "Tecla2Salva:", tecla2Salva, "Tecla pressionada:", event.key)
                if tecla1Salva != event.key and tecla2Salva != event.key:
                    arquivo.setConfig("tecla2", event.key)
                    self.jogo.sons.tocar("config_controle_alterado", "narrador")
                    self.jogo.mudar_estado("config_controle")
                else:
                    self.jogo.sons.tocar("config_controle_usada", "narrador")

        elif event.type == pygame.MOUSEMOTION:
            pass

    def resetar_som(self):
        self.jogo.telas["config_controle_tecla2"].resetar_som()

class Cena01(Estado):

    def exibir(self):
        self.jogo.telas["cena01"].exibir(self.jogo.sons)
        self.jogo.sons.parar_musica()
        self.jogo.sons.tocar_ruido()
        arquivo.setSave("tela", "cena01")
        self.jogo.ultimaCena = "cena01"
    
    def processar_eventos(self, event):
    # eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena02")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena02")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                print("CTRL pressionado")

            # eventos de mouse
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("cena01", "narrador")

    def resetar_som(self):
        self.jogo.telas["cena01"].resetar_som()

class Cena02(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena02"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "cena02")
        self.jogo.ultimaCena = "cena02"
    
    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena03")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena03")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("cena02", "narrador")


    def resetar_som(self):
        self.jogo.telas["cena02"].resetar_som()

class Cena03(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena03"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "cena03")
        self.jogo.ultimaCena = "cena03"
    
    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena04")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena04")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("cena03", "narrador")

    def resetar_som(self):
        self.jogo.telas["cena03"].resetar_som()

class Cena04(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena04"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "cena04")
        self.jogo.ultimaCena = "cena04"
    
    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena05")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena05")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("cena04", "narrador")

    def resetar_som(self):
        self.jogo.telas["cena04"].resetar_som()

class Cena05(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena05"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "cena05")
        self.jogo.ultimaCena = "cena05"
    
    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena06")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena06")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("cena05", "narrador")

    def resetar_som(self):
        self.jogo.telas["cena05"].resetar_som()

class Cena06(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        self.jogo.telas["cena06"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "cena06")
        self.jogo.ultimaCena = "cena06"
    
    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena01")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("cena01")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.jogo.sons.tocar("cena06", "narrador")

    def resetar_som(self):
        self.jogo.telas["cena06"].resetar_som()
