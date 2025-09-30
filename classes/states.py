import pygame
import sys
import service.prop as arquivo
import time

# ------------------- ESTADO BASE -------------------
class Estado:
    def __init__(self, jogo):
        self.jogo = jogo
        
# ----------------- ESTADO BASE DAS CENAS -- HERDA DO ESTADO BASE ---------------

class CenaBase(Estado):
    cena = None; cenaescolha1 = None; cenaescolha2 = None

    def exibir(self):
        botoes = [(0.026, 0.840, 0.314, 0.066, ""),(0.026, 0.923, 0.314, 0.066, ""),(0.360, 0.832, 0.625, 0.074, ""),(0.360, 0.915, 0.625, 0.074, "")]
        self.jogo.sons.parar_musica(); self.jogo.telas[self.cena].exibir(self.jogo.sons); self.jogo.sons.tocar_ruido(); self.jogo.telas[self.cena].tocar_cena(self.jogo.sons)
        self.jogo.telas[self.cena].carregarBotoes(botoes)
        arquivo.setSave("tela", self.cena)
        self.jogo.ultimaCena = self.cena

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado("menu")
            if event.key == pygame.K_p: self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado("pausa")
            
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.parar_narrador()
                self.jogo.sons.parar_cena()
                narradorAtivado = (arquivo.getConfig("narradorativo") == "true")
                if narradorAtivado:
                    self.jogo.sons.tocar(self.cena,"narrador")
                else:
                    self.jogo.sons.tocar(self.cena,"cena")
            
            elif event.key == int(arquivo.getConfig("tecla1", "49")): self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado(self.cenaescolha1)
            elif event.key == int(arquivo.getConfig("tecla2", "50")): self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado(self.cenaescolha2)

        elif event.type == pygame.MOUSEMOTION:
            narradorAtivado = (arquivo.getConfig("narradorativo") == "true")
            if narradorAtivado:
                pos_mouse = pygame.mouse.get_pos()
                botao = self.jogo.telas[self.cena].verificar_clique(pos_mouse)
                if botao == 0: self.jogo.sons.parar_narrador();  self.jogo.sons.tocar("pausar", "narrador")
                elif botao == 1: self.jogo.sons.parar_narrador();  self.jogo.sons.tocar("acessar_menu_principal", "narrador")
                elif botao == 2: self.jogo.sons.parar_narrador();  self.jogo.sons.tocar("escolha1", "narrador")
                elif botao == 3: self.jogo.sons.parar_narrador();  self.jogo.sons.tocar("escolha2", "narrador")
            
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas[self.cena].verificar_clique(pos_mouse)
            if botao == 0: self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado("pausa")
            elif botao == 1: self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado("menu")
            elif botao == 2: self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado(self.cenaescolha1)
            elif botao == 3: self.jogo.sons.parar_narrador(); self.jogo.sons.parar_cena(); self.jogo.mudar_estado(self.cenaescolha2)

    def resetar_som(self):
        self.jogo.telas[self.cena].resetar_som()

class EstadoMenu(Estado):
    def exibir(self):
        botoes = [
            (0.388, 0.600, 0.220, 0.062, ""),
            (0.378, 0.672, 0.240, 0.062, ""),
            (0.380, 0.742, 0.230, 0.063, ""),
            (0.409, 0.815, 0.200, 0.064, ""),
            (0.427, 0.886, 0.155, 0.060, ""),
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
                self.jogo.sons.tocar("novo", "narrador")
                time.sleep(2); pygame.event.clear()
                self.jogo.sons.parar_narrador()
                self.jogo.sons.parar_musica()
                self.jogo.sons.tocar("musica2", "musica")
                self.jogo.mudar_estado("NOVO_JOGO", 20)
            elif event.key == pygame.K_2:
                self.jogo.sons.tocar_ruido()
                self.jogo.mudar_estado(arquivo.getSave("tela")) # continua o jogo do ponto que parou
                self.jogo.sons.parar_musica()
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
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["menu"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.tocar("novo", "narrador")
                time.sleep(2); pygame.event.clear()
                self.jogo.sons.parar_narrador()
                self.jogo.sons.parar_musica()
                self.jogo.sons.tocar("musica2", "musica")
                self.jogo.mudar_estado("NOVO_JOGO", 20)
            elif botao == 1:
                self.jogo.sons.parar_musica()
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
        self.jogo.telas["NOVO_JOGO"].exibir(self.jogo.sons)
        # 83
        #time.sleep(4)
        #pygame.event.clear()
        #self.jogo.sons.parar_narrador()
        #self.jogo.mudar_estado("C_ACORDAR")

    def resetar_som(self):
        self.jogo.telas["NOVO_JOGO"].resetar_som()

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("C_ACORDAR")

class C_ACORDAR(Estado):

    def exibir(self):
        self.jogo.telas["C_ACORDAR"].exibir(self.jogo.sons)
        self.jogo.sons.tocar_ruido()
        # 43
        #time.sleep(4)
        #pygame.event.clear()
        #self.jogo.sons.parar_narrador()
        #self.jogo.mudar_estado("C1")

    def resetar_som(self):
        self.jogo.telas["C_ACORDAR"].resetar_som()

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("C1")

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
        elif event.type == pygame.MOUSEBUTTONUP:
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
        botoes = [
            (0.404, 0.830, 0.190, 0.112, ""),
        ]
        self.jogo.telas["creditos"].exibir(self.jogo.sons)
        self.jogo.telas["creditos"].carregarBotoes(botoes)

    def processar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.jogo.sons.parar_narrador()
                self.jogo.mudar_estado("menu")
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("som_creditos", "narrador")
        elif event.type == pygame.MOUSEMOTION:
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("creditos", "narrador")
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["creditos"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("voltar", "narrador")
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["creditos"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.mudar_estado("menu")

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
        
        elif event.type == pygame.MOUSEBUTTONUP:
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
            (0.110, 0.755, 0.070, 0.113, ""), # NARRADOR  -
            (0.234, 0.750, 0.070, 0.113, ""), # NARRADOR +
            (0.690, 0.757, 0.070, 0.113, ""), # MUSICA - 
            (0.800, 0.757, 0.070, 0.113, ""), # MUSICA +
            (0.469, 0.689, 0.070, 0.122, ""), # ATIVAR / DESATIVAR NARRADOR
            (0.419, 0.846, 0.170, 0.070, ""), # VOLTAR
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
            elif botao == 5:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("voltar", "narrador")

        elif event.type == pygame.MOUSEBUTTONUP:
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
            elif botao == 5:
                self.jogo.mudar_estado("config")

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
        botoes = [
            (0.816, 0.366, 0.070, 0.118, ""), # TECLA 1
            (0.816, 0.494, 0.070, 0.118, ""), # TECLA 2
            (0.400, 0.827, 0.230, 0.100, ""), # VOLTAR
        ]
        self.jogo.telas["config_controle"].exibir(self.jogo.sons)
        self.jogo.telas["config_controle"].carregarBotoes(botoes)

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
        elif event.type == pygame.MOUSEMOTION:
            self.jogo.sons.tocar("config_controle", "narrador")
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_controle"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("mudar_tecla1", "narrador")
            elif botao == 1:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("mudar_tecla2", "narrador")
            elif botao == 2:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("voltar", "narrador")
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_controle"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.mudar_estado("config_controle_tecla1")
            elif botao == 1:
                self.jogo.mudar_estado("config_controle_tecla2")
            elif botao == 2:
                self.jogo.mudar_estado("config")
            
    def resetar_som(self):
        self.jogo.telas["config_controle"].resetar_som()

class EstadoConfigControleTecla1(Estado):
    def exibir(self):
        botoes = [
            (0.404, 0.830, 0.220, 0.112, ""),
        ]
        self.jogo.telas["config_controle_tecla1"].exibir(self.jogo.sons)
        self.jogo.telas["config_controle_tecla1"].carregarBotoes(botoes)

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
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("config_controle_tecla1", "narrador")
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_controle_tecla1"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("voltar", "narrador")
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_controle_tecla1"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.mudar_estado("config_controle")


    def resetar_som(self):
        self.jogo.telas["config_controle"].resetar_som()

class EstadoConfigControleTecla2(Estado):
    def exibir(self):
        botoes = [
            (0.404, 0.830, 0.220, 0.112, ""),
        ]
        self.jogo.telas["config_controle_tecla2"].exibir(self.jogo.sons)
        self.jogo.telas["config_controle_tecla2"].carregarBotoes(botoes)

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
            self.jogo.sons.parar_narrador()
            self.jogo.sons.tocar("config_controle_tecla2", "narrador")
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_controle_tecla2"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.sons.parar_narrador()
                self.jogo.sons.tocar("voltar", "narrador")
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_mouse = pygame.mouse.get_pos()
            botao = self.jogo.telas["config_controle_tecla2"].verificar_clique(pos_mouse)
            if botao == 0:
                self.jogo.mudar_estado("config_controle")

    def resetar_som(self):
        self.jogo.telas["config_controle_tecla2"].resetar_som()

class C1(CenaBase): cena = "C1"; cenaescolha1 = "A"; cenaescolha2 = "B" # OK
class A(CenaBase): cena = "A"; cenaescolha1 = "A2"; cenaescolha2 = "AB" # OK
class B(CenaBase): cena = "B"; cenaescolha1 = "BA"; cenaescolha2 = "B2" # OK
class A2(CenaBase): cena = "A2"; cenaescolha1 = "A3"; cenaescolha2 = "A2B" # OK
class AB(CenaBase): cena = "AB"; cenaescolha1 = "ABA"; cenaescolha2 = "A2B" # OK
class BA(CenaBase): cena = "BA"; cenaescolha1 = "BA2"; cenaescolha2 = "ABA" # OK
class B2(CenaBase): cena = "B2"; cenaescolha1 = "B2A"; cenaescolha2 = "B3" # OK
class A3(CenaBase): cena = "A3"; cenaescolha1 = "A4"; cenaescolha2 = "A3B" # OK
class A4(CenaBase): cena = "A4"; cenaescolha1 = "A5"; cenaescolha2 = "A4B" # OK
class A3B(CenaBase): cena = "A3B"; cenaescolha1 = "A5"; cenaescolha2 = "A4B" # OK
class A4B(CenaBase): cena = "A4B"; cenaescolha1 = "A4BA"; cenaescolha2 = "A4B2" # OK
class A5(CenaBase): cena = "A5"; cenaescolha1 = "A6"; cenaescolha2 = "A4B2" # OK
class A6(CenaBase): cena = "A6"; cenaescolha1 = "A4BA"; cenaescolha2 = "BA" # OK
class BA2(CenaBase): cena = "BA2"; cenaescolha1 = "BA3"; cenaescolha2 = "B2" # OK
class BA3(CenaBase): cena = "BA3"; cenaescolha1 = "A5"; cenaescolha2 = "A4B" # OK
class A2B(CenaBase): cena = "A2B"; cenaescolha1 = "BA"; cenaescolha2 = "A4BA" # OK
class ABA(CenaBase): cena = "ABA"; cenaescolha1 = "A4BA"; cenaescolha2 = "BA" # OK
class B2A(CenaBase): cena = "B2A"; cenaescolha1 = "B2A2"; cenaescolha2 = "A4BA" # OK
class B3(CenaBase): cena = "B3"; cenaescolha1 = "B3A"; cenaescolha2 = "B2A2" # OK
class B2A2(CenaBase): cena = "B2A2"; cenaescolha1 = "B2A3"; cenaescolha2 = "B2A2B" # OK
class B2A3(CenaBase): cena = "B2A3"; cenaescolha1 = "B2A2BA"; cenaescolha2 = "A4BA" # OK
class B2A2B(CenaBase): cena = "B2A2B"; cenaescolha1 = "A4BA"; cenaescolha2 = "B2A2BA" # OK
class B3A(CenaBase): cena = "B3A"; cenaescolha1 = "A5"; cenaescolha2 = "B2A2" # OK
class B2A2BA(CenaBase): cena = "B2A2BA"; cenaescolha1 = "A4BA"; cenaescolha2 = "B2A2BAB" # OK
class B2A2BAB(CenaBase): cena = "B2A2BAB"; cenaescolha1 = "B2A2BABA"; cenaescolha2 = "B2A2BAB2" # OK


class B2A2BABA(CenaBase): cena = "B2A2BABA"; cenaescolha1 = "creditos"; cenaescolha2 = "creditos"
class B2A2BAB2(CenaBase): cena = "B2A2BAB2"; cenaescolha1 = "creditos"; cenaescolha2 = "creditos"








