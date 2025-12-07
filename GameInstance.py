import pickle
from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
import Sprites
import Data
import Input
import Mapa
import math
import HUD
import Luta
import MainMenu
import Sounds

class Jogo():
    def __init__(self, janela):
        self.janela = janela
        self.jogadorHUD = HUD.CriarHUD(janela)
        self.luta = Luta.Luta()
        self.lutaHUD = self.luta.CriarLutaHUD(janela)
        self.alvoLuta = 0
        self.alvoLutaAnimacao = 0
        self.estadoJogo = Data.EEstado.MAINMENU
        self.ultimoEstadoJogo = Data.EEstado.MAINMENU
        self.animacao = Data.EANIMACAOOVERWORLD.NADA
        self.escolhas = []
        self.inimigosNaLuta = []
        self.botoesLuta = [self.lutaHUD.bItem, self.lutaHUD.bAtacar, self.lutaHUD.bHabilidade, self.lutaHUD.bFugir]
        self.posicoesBotoesLuta = [ (janela.width * 0.075, janela.height - (7 * janela.height / 30)), (janela.width * 0.03, janela.height - (3 * janela.height / 10)),  (janela.width * 0.01, janela.height - (janela.height / 10)), (janela.width * 0.03, janela.height - (janela.height / 6)),]
        self.botaoSelecionadoLuta = Data.ELuta.ATACAR
        self.botaoAntigo = Data.ELuta.ATACAR
        self.ultimoMovimentoBotao = time.time()
        self.botaoSolto = True
        self.objetosADesenhar = []
        self.escolhaSelecionada = 0
        self.tempoAgora = time.time()
        self.tempoUltimoFrame = time.time()
        self.ultimoInput = 0
        self.ultimoInputAnterior = 0
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

        self.jogador = Data.Jogador(23.5 , 8.5, 0, Data.direcao["L"], 110)
        self.teclado = Window.get_keyboard()
        self.mouse = Window.get_mouse()
        self.mapaAtual = Mapa.GerarMapa(1, self)
        self.dialogoMensagens = []


        self.GAME_WIDTH = 200  
        self.GAME_HEIGHT = 200 
        self.janelaMenor = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))

        self.fade = Sprites.FadeSprite(janela.width, janela.height)

        self.MainMenu = MainMenu.MainMenu()
        self.SubMenu = MainMenu.SubMenu()
        self.Musica = Sounds.musica(Sounds.criar_lista_musicas())
        self.ultimaLuta = False    


    def SalvarJogo(self):
        habilidades = []

        for habilidade in self.jogador.habilidades:
            habilidades.append(habilidade.ID)

        items = []

        for item in self.jogador.items:
            items.append([item.ID, item.quantidade])

        save = {
            "jogadorPos": [self.jogador.x, self.jogador.y],
            "jogadorRot": [self.jogador.dirX, self.jogador.dirY, self.jogador.planeX, self.jogador.planeY, self.jogador.direcao],
            "jogadorLevel": self.jogador.level,
            "jogadorXp": self.jogador.xp,
            "jogadorHabilidades": habilidades,
            "jogadorEngrenagens": self.jogador.engrenagems,
            "jogadorItems":  items,
            "jogadorHp": self.jogador.vida,
            "jogadorHpMax": self.jogador.vidaMaxima,
            "jogadorEnergia": self.jogador.energia,
            "jogadorEnergiaMax": self.jogador.energiaMaxima,
            "andar": self.jogador.andar,
            "quests": self.jogador.quests,
            "provas" : self.jogador.provas,
            "aulas" : self.jogador.aulas,
            "itemPego": self.jogador.itemPego
        }

        with open("save.pkl", "wb") as f:
            pickle.dump(save, f)

    def CarregarJogo(self, save):

        self.jogador.x =      save["jogadorPos"][0]
        self.jogador.y  =     save["jogadorPos"][1]
        self.jogador.dirX =   save["jogadorRot"][0]
        self.jogador.dirY =   save["jogadorRot"][1]
        self.jogador.planeX = save["jogadorRot"][2]
        self.jogador.planeY = save["jogadorRot"][3]
        self.jogador.direcao = save["jogadorRot"][4]
        self.jogador.level =  save["jogadorLevel"]
        self.jogador.xp =     save["jogadorXp"]
        self.jogador.engrenagems = save["jogadorEngrenagens"]
        self.jogador.quests = save["quests"]
        self.jogador.provas = save["provas"]
        self.jogador.aulas = save["aulas"]

        for habilidade in save["jogadorHabilidades"]:     
            self.jogador.AprenderHabilidade(Data.habilidadeBD[habilidade-1])

        for item in save["jogadorItems"]:
            for i in range(0, item[1]):
                self.jogador.ObterItem(Data.itemBD[item[0] - 1])


        self.jogador.vida = save["jogadorHp"]
        self.jogador.vidaMaxima = save["jogadorHpMax"]
        self.jogador.energia = save["jogadorEnergia"]
        self.jogador.energiaMaxima = save["jogadorEnergiaMax"]
        self.jogador.andar = save["andar"]
        self.jogador.itemPego = save["itemPego"]