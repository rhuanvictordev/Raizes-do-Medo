import pygame
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 640, 480
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com Fade")
FONTE = pygame.font.SysFont('calibri', 28)
clock = pygame.time.Clock()


# ------------------- Gerenciador de Som -------------------
class GerenciadorDeSom:
    def __init__(self):
        self.sons = {
            "musica": pygame.mixer.Sound("som_fundo.mp3"),
            "menu": pygame.mixer.Sound("som_narrador_menu.mp3"),
            "config": pygame.mixer.Sound("som_config.mp3"),
            "pausa": pygame.mixer.Sound("som_narrador_pausa.mp3"),
            "novo_jogo": pygame.mixer.Sound("som_narrador_novo_jogo.mp3"),
            "config_audio": pygame.mixer.Sound("som_narrador_config_audio.mp3"),
            "config_controle": pygame.mixer.Sound("som_narrador_config_controle.mp3"),
            "som_creditos": pygame.mixer.Sound("som_narrador_creditos.mp3"),
            "som_n_menos": pygame.mixer.Sound("som_narrador_menos.mp3"),
            "som_n_mais": pygame.mixer.Sound("som_narrador_mais.mp3"),
            "som_m_menos": pygame.mixer.Sound("som_narrador_musica_menos.mp3"),
            "som_m_mais": pygame.mixer.Sound("som_narrador_musica_mais.mp3"),
            "som_sair": pygame.mixer.Sound("som_narrador_sair.mp3")
        }

        self.canais = {
            "musica": pygame.mixer.Channel(0),
            "narrador": pygame.mixer.Channel(1)
        }

        self.volumes = {
            "musica": 0.6,
            "narrador": 0.4
        }


    def tocar(self, nome_som, canal, loop=False):
        if not self.canais[canal].get_busy():  # só toca se o canal estiver livre
            loops = -1 if loop else 0
            self.canais[canal].play(self.sons[nome_som], loops=loops)
            vol = self.volumes.get(canal, 1.0)
            self.canais[canal].set_volume(vol)


    def ajustar_volume(self, canal, delta):
        if canal in self.canais and canal in self.volumes:
            novo_volume = self.volumes[canal] + delta
            # Garante que o volume fique entre 0.0 e 1.0
            novo_volume = max(0.0, min(1.0, novo_volume))
            self.volumes[canal] = novo_volume
            self.canais[canal].set_volume(novo_volume)
            print(f"Volume de '{canal}' ajustado para {novo_volume:.2f}")



    def parar_musica(self):
        self.canais["musica"].stop()
    
    def parar_narrador(self):
        self.canais["narrador"].stop()


# ------------------- Classe de Tela -------------------
class Tela:
    def __init__(self, caminho_img, som_nome=None):
        self.fundo = pygame.transform.scale(pygame.image.load(caminho_img).convert(), (LARGURA, ALTURA))
        self.som_nome = som_nome
        self.som_tocou = False

    def exibir(self, sons: GerenciadorDeSom):
        TELA.blit(self.fundo, (0, 0))
        if self.som_nome and not self.som_tocou:
            sons.tocar(self.som_nome, "narrador")
            self.som_tocou = True

    def resetar_som(self):
        self.som_tocou = False


# ------------------- Jogo Principal -------------------
class Jogo:
    def __init__(self):
        self.estado = "menu"
        self.estado_anterior = None
        self.sons = GerenciadorDeSom()

        self.telas = {
            "menu": Tela("menu.png", "menu"),
            "config": Tela("config.png", "config"),
            "jogo": Tela("novo_jogo.png", "novo_jogo"),
            "continuar": Tela("menu.png"),
            "creditos": Tela("creditos.png", "som_creditos"),
            "pausa": Tela("pausa.png", "pausa"),
            "config_audio": Tela("config_audio.png", "config_audio"),
            "config_controle": Tela("config_controle.png", "config_controle")
        }

    def atualizar_tela(self):
        if self.estado != self.estado_anterior:
            self.transicao_com_fade(self.estado_anterior, self.estado)
            self.estado_anterior = self.estado

        self.telas[self.estado].exibir(self.sons)

    def transicao_com_fade(self, de_estado, para_estado):
        if de_estado not in self.telas or para_estado not in self.telas:
            return

        fade = pygame.Surface((LARGURA, ALTURA))
        fade.fill((0, 0, 0))

        # Fade out
        for alpha in range(0, 255, 10):
            self.telas[de_estado].exibir(self.sons)
            fade.set_alpha(alpha)
            TELA.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(15)

        self.telas[para_estado].resetar_som()

        # Fade in
        for alpha in range(255, 0, -10):
            self.telas[para_estado].exibir(self.sons)
            fade.set_alpha(alpha)
            TELA.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(15)

    


    def processar_eventos(self):
        
        for event in pygame.event.get():
            if not self.sons.canais["musica"].get_busy():
                self.sons.tocar("musica", "musica", True)

            if event.type == pygame.QUIT:
                self.sons.parar_narrador()
                pygame.quit()
                sys.exit()

            # ABAIXO -> EVENTOS DE CAPTURAR TECLAS EM CADA TELA
            elif event.type == pygame.KEYDOWN:

                #MENU
                if self.estado == "menu":
                    self.sons.parar_narrador()

                    if event.key == pygame.K_ESCAPE:
                        self.sons.parar_narrador()
                        self.sons.tocar("menu", "narrador")

                    elif event.key == pygame.K_1:
                        self.estado = "jogo"
                        
                    elif event.key == pygame.K_2:
                        self.estado = "continuar"
                    
                    elif event.key == pygame.K_3:
                        self.estado = "config"

                    elif event.key == pygame.K_4:
                        self.estado = "creditos"
                    
                    elif event.key == pygame.K_LCTRL:
                        self.sons.tocar('menu', 'narrador')

                    elif event.key == pygame.K_5:
                        self.sons.tocar("som_sair", "narrador")
                        duracao = self.sons.sons["som_sair"].get_length() * 1000  # capta a duracao do som de sair
                        pygame.time.delay(int(duracao))  # espera a duracao do som de sair antes de sair
                        pygame.quit()
                        sys.exit()

                #CONFIG
                elif self.estado == "config":
                    self.sons.parar_narrador()
                    
                    if event.key == pygame.K_ESCAPE:
                        self.estado = "menu"

                    if event.key == pygame.K_1:
                        self.estado = "config_audio"
                        
                    if event.key == pygame.K_2:
                        self.estado = "config_controle"

                    if event.key == pygame.K_LCTRL:
                        self.sons.tocar('config', 'narrador')

                #CREDITOS
                elif self.estado == "creditos":
                    self.sons.parar_narrador()

                    if event.key == pygame.K_ESCAPE:
                        self.sons.parar_narrador()
                        self.estado = "menu"
                        
                
                # METODOS DA TELA DE CONFIG AUDIO
                elif self.estado == "config_audio":
                    
                    if event.key == pygame.K_ESCAPE:
                        self.sons.parar_narrador()
                        self.estado = "config"

                    if event.key == pygame.K_LCTRL:
                        self.sons.tocar("config_audio", "narrador")

                    if event.key == pygame.K_1:
                        self.sons.parar_narrador()
                        self.sons.tocar("som_n_menos", "narrador")
                        self.sons.ajustar_volume("narrador", -0.1)
                    
                    if event.key == pygame.K_2:
                        self.sons.parar_narrador()
                        self.sons.tocar("som_n_mais", "narrador")
                        self.sons.ajustar_volume("narrador", +0.1)

                    if event.key == pygame.K_3:
                        self.sons.parar_narrador()
                        self.sons.tocar("som_m_menos", "narrador")
                        self.sons.ajustar_volume("musica", -0.1)
                    
                    if event.key == pygame.K_4:
                        self.sons.parar_narrador()
                        self.sons.tocar("som_m_mais", "narrador")
                        self.sons.ajustar_volume("musica", +0.1)


                # METODOS DA TELA DE CONFIG CONTROLE
                elif self.estado == "config_controle":

                    if event.key == pygame.K_ESCAPE:
                        self.sons.parar_narrador()
                        self.estado = "config"

                    if event.key == pygame.K_1:
                        print("controle 1")

                    if event.key == pygame.K_2:
                        print("controle 2")



# ------------------- Execução -------------------
if __name__ == "__main__":
    jogo = Jogo()

    while True:
        jogo.processar_eventos()
        jogo.atualizar_tela()
        pygame.display.flip()
        clock.tick(60)