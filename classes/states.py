import pygame
import sys
import service.prop as arquivo
import time




# ------------------- Estado Base -------------------
class Estado:
    def __init__(self, jogo):
        self.jogo = jogo

# ------------------- Estados -------------------

class EstadoMenu(Estado):
    def exibir(self):
        botoes = [
            (0.388, 0.600, 0.410, 0.062, ""),
            (0.378, 0.672, 0.410, 0.062, ""),
            (0.380, 0.742, 0.410, 0.063, ""),
            (0.409, 0.815, 0.360, 0.064, ""),
            (0.427, 0.886, 0.285, 0.060, ""),
        ]
        self.jogo.telas["menu"].exibir(self.jogo.sons)
        self.jogo.telas["menu"].carregarBotoes(botoes)
        self.jogo.sons.parar_ruido()

    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.tocar("menu", "narrador")
            elif event.key == pygame.K_1:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.parar_musica()
                self.jogo.mudar_estado("NOVO_JOGO")
            elif event.key == pygame.K_2:
                self.jogo.sons.tocar_ruido()
                self.jogo.mudar_estado(arquivo.getSave("tela")) # continua o jogo do ponto que parou
                self.jogo.sons.tocar_ruido()
            elif event.key == pygame.K_3:
                self.jogo.mudar_estado("config")
            elif event.key == pygame.K_4:
                self.jogo.mudar_estado("creditos")
            elif event.key == pygame.K_ESCAPE:
                self.jogo.sons.tocar("som_sair", "narrador")
                pygame.time.delay(int(self.jogo.sons.sons["som_sair"].get_length() * 1000))
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            self.jogo.sons.tocar("menu", "narrador")
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["menu"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("novo", "narrador")
            elif botao == 1:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("continuar", "narrador")
            elif botao == 2:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("configuracoes", "narrador")
            elif botao == 3:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("creditos", "narrador")
            elif botao == 4:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("sair", "narrador")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["menu"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.mudar_estado("NOVO_JOGO")
            elif botao == 1:
                self.jogo.mudar_estado(arquivo.getSave("tela"))
            elif botao == 2:
                self.jogo.mudar_estado("config")
            elif botao == 3:
                self.jogo.mudar_estado("creditos")
            elif botao == 4:
                self.jogo.sons.tocar("som_sair", "narrador")
                pygame.time.delay(int(self.jogo.sons.sons["som_sair"].get_length() * 1000))
                pygame.quit()
                sys.exit()

    def resetar_som(self):
        self.jogo.telas["menu"].resetar_som()

class EstadoNovoJogo(Estado):
    def exibir(self):
        self.jogo.sons.tocar_ruido()
        self.jogo.telas["NOVO_JOGO"].exibir(self.jogo.sons)
        self.jogo.sons.parar_musica()

        # mantém a cena visível por 18s
        inicio = time.time()
        while time.time() - inicio < 18:
            pygame.event.pump()      # mantém pygame vivo
            pygame.event.clear()     # esvazia fila (ignora teclas/cliques)
            time.sleep(0.02)         # espera em pequenos passos
        self.jogo.sons.parar_narrador()
        self.jogo.mudar_estado("C_ACORDAR")

    def resetar_som(self):
        self.jogo.telas["NOVO_JOGO"].resetar_som()

    def processar_eventos(self, event):
        pass

class C_ACORDAR(Estado):

    def exibir(self):
        #self.jogo.sons.tocar_ruido()
        self.jogo.telas["C_ACORDAR"].exibir(self.jogo.sons)
        self.jogo.sons.parar_musica()

        # mantém a cena visível por 20s
        inicio = time.time()
        while time.time() - inicio < 20:
            pygame.event.pump()      # mantém pygame vivo
            pygame.event.clear()     # esvazia fila (ignora teclas/cliques)
            time.sleep(0.02)         # espera em pequenos passos
        self.jogo.sons.parar_narrador()
        self.jogo.mudar_estado("C1")

    def resetar_som(self):
        self.jogo.telas["C_ACORDAR"].resetar_som()

    def processar_eventos(self, event):
        pass

class EstadoPausa(Estado):
    def exibir(self):
        self.jogo.sons.parar_ruido()
        botoes = [
            (0.320, 0.200, 0.370, 0.180, "")
        ]
        self.jogo.telas["pausa"].exibir(self.jogo.sons)
        self.jogo.telas["pausa"].carregarBotoes(botoes)
        self.jogo.sons.tocar("musica", "musica", True)

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.parar_musica()
                self.jogo.telas["pausa"].resetar_som()
                self.jogo.mudar_estado(self.jogo.ultimaCena)
                self.jogo.sons.tocar_ruido()
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("pausa", "narrador")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.parar_musica()
            self.jogo.telas["pausa"].resetar_som()
            self.jogo.mudar_estado(self.jogo.ultimaCena)
            self.jogo.sons.tocar_ruido()
    def resetar_som(self):
        self.jogo.telas["pausa"].resetar_som()

class EstadoContinuar(Estado):
    def exibir(self):
        self.jogo.sons.tocar_ruido()
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
        botoes = [
            (0.400, 0.595, 0.210, 0.080, ""),
            (0.400, 0.685, 0.210, 0.080, ""),
            (0.400, 0.765, 0.210, 0.080, ""),
        ]
        self.jogo.telas["config"].exibir(self.jogo.sons)
        self.jogo.telas["config"].carregarBotoes(botoes)

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
        
        elif event.type == pygame.MOUSEMOTION:
            self.jogo.sons.tocar("config", "narrador")
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("config_audio_rapido", "narrador")
            elif botao == 1:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("config_controles", "narrador")
            elif botao == 2:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("voltar", "narrador")
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.mudar_estado("config_audio")
            elif botao == 1:
                self.jogo.mudar_estado("config_controle")
            elif botao == 2:
                self.jogo.mudar_estado("menu")
            

    def resetar_som(self):
        self.jogo.telas["config"].resetar_som()

class EstadoConfigAudio(Estado):
    def exibir(self):
        botoes = [
            (0.110, 0.755, 0.070, 0.113, ""),
            (0.234, 0.760, 0.070, 0.113, ""),
            (0.690, 0.757, 0.070, 0.113, ""),
            (0.800, 0.757, 0.070, 0.113, ""),
            (0.469, 0.756, 0.070, 0.113, ""),
        ]
        self.jogo.telas["config_audio"].exibir(self.jogo.sons)
        self.jogo.telas["config_audio"].carregarBotoes(botoes)

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
            elif event.key == pygame.K_5:
                self.alternarNarrador()
            
        elif event.type == pygame.MOUSEMOTION:
            self.jogo.sons.tocar("config_audio", "narrador")
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_audio"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("diminuir_narrador", "narrador")
            elif botao == 1:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("aumentar_narrador", "narrador")
            elif botao == 2:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("diminuir_musica", "narrador")
            elif botao == 3:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("aumentar_musica", "narrador")
            elif botao == 4:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("ativar_desativar_narrador", "narrador")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_audio"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.tocar("som_n_menos", "narrador")
                self.jogo.sons.ajustar_volume("narrador", -0.1)
            elif botao == 1:
                self.jogo.sons.tocar("som_n_mais", "narrador")
                self.jogo.sons.ajustar_volume("narrador", 0.1)
            elif botao == 2:
                self.jogo.sons.tocar("som_m_menos", "narrador")
                self.jogo.sons.ajustar_volume("musica", -0.1)
            elif botao == 3:
                self.jogo.sons.tocar("som_m_mais", "narrador")
                self.jogo.sons.ajustar_volume("musica", 0.1)
            elif botao == 4:
                self.alternarNarrador()

    ################## ATIVAR / DESATIVAR NARRADOR
    def alternarNarrador(self):
        narradorAtivo = (arquivo.getConfig("narradorativo"))
        if narradorAtivo == "true":
            self.jogo.sons.tocar("narrador_desativado", "narrador")
            arquivo.setConfig("narradorativo", "false")
        else:
            arquivo.setConfig("narradorativo", "true")
            self.jogo.sons.tocar("narrador_ativado", "narrador")        
    ################### ATIVAR / DESATIVAR NARRADOR

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

class C1(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        time.sleep(1) # esse sleep garante que a cena seja iniciada com o som dela
        self.jogo.telas["C1"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "C1")
        self.jogo.ultimaCena = "C1"
    
    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("A")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("B")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.jogo.sons.tocar("C1", "narrador")

    def resetar_som(self):
        self.jogo.telas["C1"].resetar_som()

class A(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        time.sleep(1) # esse sleep garante que a cena seja iniciada com o som dela
        self.jogo.telas["A"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "A")
        self.jogo.ultimaCena = "A"
    
    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("A2")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("AB")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.jogo.sons.tocar("A", "narrador")

    def resetar_som(self):
        self.jogo.telas["A"].resetar_som()

class B(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        time.sleep(1) # esse sleep garante que a cena seja iniciada com o som dela
        self.jogo.telas["B"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "B")
        self.jogo.ultimaCena = "B"
    
    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("BA")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("B2")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.jogo.sons.tocar("B", "narrador")

    def resetar_som(self):
        self.jogo.telas["B"].resetar_som()

class A2(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        time.sleep(1) # esse sleep garante que a cena seja iniciada com o som dela
        self.jogo.telas["A2"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "A2")
        self.jogo.ultimaCena = "A2"
    
    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.jogo.sons.tocar("A2", "narrador")

    def resetar_som(self):
        self.jogo.telas["A2"].resetar_som()

class AB(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        time.sleep(1) # esse sleep garante que a cena seja iniciada com o som dela
        self.jogo.telas["AB"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "AB")
        self.jogo.ultimaCena = "AB"
    
    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.jogo.sons.tocar("AB", "narrador")

    def resetar_som(self):
        self.jogo.telas["AB"].resetar_som()

class BA(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        time.sleep(1) # esse sleep garante que a cena seja iniciada com o som dela
        self.jogo.telas["BA"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "BA")
        self.jogo.ultimaCena = "BA"
    
    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.jogo.sons.tocar("BA", "narrador")

    def resetar_som(self):
        self.jogo.telas["BA"].resetar_som()

class B2(Estado):

    def exibir(self):
        self.jogo.sons.parar_musica()
        time.sleep(1) # esse sleep garante que a cena seja iniciada com o som dela
        self.jogo.telas["B2"].exibir(self.jogo.sons)
        arquivo.setSave("tela", "B2")
        self.jogo.ultimaCena = "B2"
    
    def processar_eventos(self, event):
        self.jogo.sons.parar_narrador()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla1", "49")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == int(arquivo.getConfig("tecla2", "50")):
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key == pygame.K_p:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("pausa")
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.jogo.sons.tocar("B2", "narrador")

    def resetar_som(self):
        self.jogo.telas["B2"].resetar_som()




