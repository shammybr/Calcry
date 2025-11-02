from PPlay.window import *
from PPlay.sprite import *
import Sprites
import Data
import Input
import Mapa
import math
import HUD
import Luta


class Jogo():
    def __init__(self, janela):
        self.janela = janela
        self.jogadorHUD = HUD.CriarHUD(janela)
        self.luta = Luta.Luta()
        self.lutaHUD = self.luta.CriarLutaHUD(janela)
        self.alvoLuta = 0
        self.alvoLutaAnimacao = 0
        self.estadoJogo = Data.EEstado.ANDANDO

        self.inimigosNaLuta = []
        self.botoesLuta = [self.lutaHUD.bItem, self.lutaHUD.bAtacar, self.lutaHUD.bHabilidade, self.lutaHUD.bFugir]
        self.posicoesBotoesLuta = [ (janela.width * 0.075, janela.height - (7 * janela.height / 30)), (janela.width * 0.03, janela.height - (3 * janela.height / 10)),  (janela.width * 0.01, janela.height - (janela.height / 10)), (janela.width * 0.03, janela.height - (janela.height / 6)),]
        self.botaoSelecionadoLuta = Data.ELuta.ATACAR
        self.botaoAntigo = Data.ELuta.ATACAR
        self.ultimoMovimentoBotao = time.time()
        self.botaoSolto = True
        self.objetosADesenhar = []

        self.tempoAgora = time.time()
        self.tempoUltimoFrame = time.time()

        self.ultimoMovimento = time.time()
        self.ultimaRotacao = time.time()

        self.deltaTime = 0
        self.ultimoDraw = 0
        self.numeroFrames = 0
        self.segundo = 0

        self.velRotacao = 3
        self.ultimaDirecaoX = 0
        self.ultimaDirecaoY = 0
        self.isRodando = False
        self.rodandoDirecao = 0
        self.cooldownRodar = 0.1

        self.isAndando = False
        self.cooldownAndar = 0.1
        self.andandoDestino = [0,0]
        self.andarVelocidade = 10
        self.inicioJogador = [0,0]

        self.jogador = Data.Jogador(21.5 , 9.5, 0, Data.direcao["O"], 110)
        self.teclado = Window.get_keyboard()
        self.mapaAtual = Mapa.GerarMapa(0)



        self.GAME_WIDTH = 200  
        self.GAME_HEIGHT = 200 
        self.janelaMenor = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))


