from PPlay.window import *
from PPlay.sprite import *

from Janela import CriarJanela
import Sprites
import Data
import Input
import Mapa
import math
import HUD

janela = CriarJanela()
Sprites.CarregarTexturas(janela)
jogadorHUD = HUD.CriarHUD(janela)


tempoAgora = time.time()
tempoUltimoFrame = time.time()

ultimoMovimento = time.time()
ultimaRotacao = time.time()

deltaTime = 0
ultimoDraw = 0
numeroFrames = 0
segundo = 0


velRotacao = 3
ultimaDirecaoX = 0
ultimaDirecaoY = 0
isRodando = False
rodandoDirecao = 0
cooldownRodar = 0.1

isAndando = False
cooldownAndar = 0.1
andandoDestino = [0,0]
andarVelocidade = 10
inicioJogador = [0,0]

jogador = Data.Jogador(1.5 , 6.5, 0, Data.direcao["N"])
teclado = Window.get_keyboard()
mapaAtual = Mapa.GerarMapa(0)



GAME_WIDTH = 200  
GAME_HEIGHT = 200 
janelaMenor = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))



def Update():
    global tempoAgora   
    global tempoUltimoFrame
    global deltaTime
    global ultimoDraw
    global numeroFrames
    global segundo
    global janela
    global teclado
    global coordenadaJogador
    global ultimoMovimento
    global ultimaRotacao
    global mapaAtual
    global velRotacao
    global isRodando
    global rodandoDirecao
    global ultimaDirecaoX
    global ultimaDirecaoY
    global isAndando
    global cooldownAndar
    global andandoDestino
    global inicioJogador
    global andarVelocidade

    deltaTime = time.time() - tempoUltimoFrame
    tempoUltimoFrame = time.time()

    segundo += deltaTime

    ultimoDraw += deltaTime


  

    ultimoInput = Input.LerInput(teclado, janela)



    if(time.time() - ultimaRotacao > 0.005):
        if(isRodando):
            
            VirarJogadorLoop(ultimaDirecaoX, ultimaDirecaoY)

        else:


            if(ultimoInput == 3):
                AtualizarDirecaoJogador(ultimoInput)
                rodandoDirecao = 1
                isRodando = True
                ultimaDirecaoX = jogador.dirX
                ultimaDirecaoY = jogador.dirY


            elif(ultimoInput == 4):
                AtualizarDirecaoJogador(ultimoInput)
                rodandoDirecao = 2
                isRodando = True
                ultimaDirecaoX = jogador.dirX
                ultimaDirecaoY = jogador.dirY




    if(time.time() - ultimoMovimento > 0.1):

        if(isAndando):
            AndarJogadorLoop(jogador, andandoDestino, inicioJogador, andarVelocidade)

            if(abs(andandoDestino[0] - jogador.x) < 0.05 and abs(andandoDestino[1] - jogador.y) < 0.05):
                jogador.x = andandoDestino[0]
                jogador.y = andandoDestino[1]

                isAndando = False
                ultimoMovimento = time.time()

        elif(AndarJogador(ultimoInput)):
            

            isAndando = True





    #dar update em 60 frames
    if(ultimoDraw > 0.016):

        janela.get_screen().fill((100, 100, 100)) # cinza
        janelaMenor.fill((100, 100, 100))


        Mapa.RenderizarMapa3DLowPoly(janelaMenor,GAME_HEIGHT, GAME_WIDTH, jogador)
        scaled_surface = pygame.transform.scale(janelaMenor, (janela.width, janela.height))
    

        janela.get_screen().blit(scaled_surface, (0, 0))
        Mapa.RenderizarMapa3D(janela, jogador)


        DesenharHUD()


        janela.update()




        ultimoDraw = 0
    numeroFrames += 1





    janela.update()


    if(segundo > 1):
        print(numeroFrames)
        numeroFrames = 0
        segundo -= 1




def ChecarColisao(novaPosicaoX, novaPosicaoY):
    direcao = 0

    if(novaPosicaoX - jogador.x > 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].oeste):
            return True
        
    elif(novaPosicaoX - jogador.x < 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].leste):
            return True
        
    elif(novaPosicaoY - jogador.y < 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].norte):
            return True
        
    elif(novaPosicaoY - jogador.y > 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].sul):
            return True


    return False

def AndarJogadorLoop(jogador, andandoDestino, inicioJogador, velocidade):
    
    if(andandoDestino[1] == jogador.y):
        jogador.x += (andandoDestino[0] - inicioJogador.x) * velocidade * deltaTime
    elif(andandoDestino[0] == jogador.x):
        jogador.y += (andandoDestino[1] - inicioJogador.y) * velocidade * deltaTime

def AndarJogador(ultimoInput):
    global inicioJogador
    global andandoDestino

    passo = 0

    if(ultimoInput == 1):
        passo = 1

        
    elif(ultimoInput == 2):
        passo = -1


    if(passo != 0):
        #norte
        if(jogador.dirX == 0 and jogador.dirY == 1):
            if(not ChecarColisao(jogador.x, (jogador.y + passo))):
                inicioJogador = jogador

                andandoDestino[0] = jogador.x
                andandoDestino[1] = jogador.y + passo
                return True
        #sul
        elif(jogador.dirX == 0 and jogador.dirY == -1 ):
            if(not ChecarColisao(jogador.x, (jogador.y - passo))):
                inicioJogador = jogador

                andandoDestino[0] = jogador.x
                andandoDestino[1] = jogador.y - passo
                return True
        #leste
        if(jogador.dirX == 1 and jogador.dirY == 0):
            if(not ChecarColisao(jogador.x + passo, jogador.y)):
                inicioJogador = jogador

                andandoDestino[0] = jogador.x + passo
                andandoDestino[1] = jogador.y
                return True
        #oeste
        elif(jogador.dirX == -1 and jogador.dirY == 0 ):
            if(not ChecarColisao(jogador.x - passo, jogador.y)):
                inicioJogador = jogador

                andandoDestino[0] = jogador.x - passo
                andandoDestino[1] = jogador.y
                return True


def AtualizarDirecaoJogador(input):
    global jogador

    if(input == 3):
        if(jogador.direcao == Data.direcao["O"]):
            jogador.direcao = Data.direcao["N"]
        else:
            jogador.direcao += 1
    elif(input == 4):
        if(jogador.direcao == Data.direcao["N"]):
            jogador.direcao = Data.direcao["O"]
        else:
            jogador.direcao -= 1

#virar aos poucos pra ficar bonitinho
def VirarJogadorLoop(ultimaDirecaoX, ultimaDirecaoY):
    global isRodando
    global ultimaRotacao

    # print("Ultima direção X:  " + str(ultimaDirecaoX))
    # print("jogador.dirX:  " + str(jogador.dirX))

    VirarJogador(rodandoDirecao, ultimaDirecaoX, ultimaDirecaoY)

    ultimaRotacao = time.time()
    




    




def VirarJogador(direcao, ultimaDirecaoX, ultimaDirecaoY):
    #direita
    global isRodando
    global ultimaRotacao
    
    if(direcao == 1):
       
        oldDirX = jogador.dirX


        jogador.dirX = jogador.dirX * math.cos(-velRotacao * min(0.1, deltaTime)) - jogador.dirY * math.sin(-velRotacao * min(0.1, deltaTime))
        jogador.dirY = oldDirX * math.sin(-velRotacao * min(0.1, deltaTime)) + jogador.dirY * math.cos(-velRotacao * min(0.1, deltaTime))

        oldPlaneX = jogador.planeX
        jogador.planeX = jogador.planeX * math.cos(-velRotacao * min(0.1, deltaTime)) - jogador.planeY * math.sin(-velRotacao * min(0.1, deltaTime))
        jogador.planeY = oldPlaneX * math.sin(-velRotacao * min(0.1, deltaTime)) + jogador.planeY * math.cos(-velRotacao * min(0.1, deltaTime))







    elif(direcao == 2):


        oldDirX = jogador.dirX
        jogador.dirX = jogador.dirX * math.cos(velRotacao * min(0.1, deltaTime)) - jogador.dirY * math.sin(velRotacao * min(0.1, deltaTime))
        jogador.dirY = oldDirX * math.sin(velRotacao * min(0.1, deltaTime)) + jogador.dirY * math.cos(velRotacao * min(0.1, deltaTime))

        oldPlaneX = jogador.planeX
        jogador.planeX = jogador.planeX * math.cos(velRotacao * min(0.1, deltaTime)) - jogador.planeY * math.sin(velRotacao * min(0.1, deltaTime))
        jogador.planeY = oldPlaneX * math.sin(velRotacao * min(0.1, deltaTime)) + jogador.planeY * math.cos(velRotacao * min(0.1, deltaTime))

    
    if(abs(ultimaDirecaoX - jogador.dirX) >= 1):
        jogador.dirX = 0
        
        #norte
        if(jogador.dirY > 0):
            jogador.dirY = 1
            jogador.planeX = 0.66
            jogador.planeY = 0.0

        #sul
        else:
            jogador.dirY = -1
            jogador.planeX = -0.66
            jogador.planeY = 0.0

        isRodando = False
        ultimaRotacao = time.time() + cooldownRodar

    elif(abs(ultimaDirecaoY - jogador.dirY) >= 1):
        jogador.dirY = 0
        
        #leste
        if(jogador.dirX > 0):
            jogador.dirX = 1
            jogador.planeX = 0
            jogador.planeY = -0.66

        #oeste
        else:
            jogador.dirX = -1
            jogador.planeX = 0.0
            jogador.planeY = 0.66

        isRodando = False
        ultimaRotacao = time.time() + cooldownRodar



def DesenharHUD():
    jogadorHUD.background.draw()
    jogadorHUD.barraHPBackground.draw()
    jogadorHUD.barraHP.Transformar((janela.width * 0.25) * max(1, (jogador.vida / jogador.vidaMaxima)), janela.height* 0.04)
    jogadorHUD.barraHP.draw()

    jogadorHUD.barraEnergiaBackground.draw()
    jogadorHUD.barraHP.Transformar((janela.width * 0.25) * max(1, (jogador.energia / jogador.energiaMaxima)), janela.height* 0.04)
    jogadorHUD.barraEnergia.draw()


    janela.draw_text("Vida:", janela.width * 0.17, janela.height * 0.8, "Sprites/HUD/PressStart2P-Regular.ttf", 20 * int((1280/janela.width)), (255,255,255), )
    janela.draw_text("Energia:", janela.width * 0.17, janela.height * 0.89, "Sprites/HUD/PressStart2P-Regular.ttf", 20 * int((1280/janela.width)), (255,255,255), )

#não usado
def UpdateTest():
    janela.get_screen().fill((100, 100, 100)) # Gray floor
    paredes = []
    paredes.append(Data.Parede(1,0, Data.direcao["L"]))
    paredes.append(Data.Parede(1,1, Data.direcao["L"]))
    paredes.append(Data.Parede(1,0, Data.direcao["O"]))
    paredes.append(Data.Parede(1,2, Data.direcao["S"]))
    paredes.append(Data.Parede(2,2, Data.direcao["S"]))
    paredes.append(Data.Parede(0,0, Data.direcao["N"]))
    Sprites.DrawLines(jogador, janela, paredes)
    


    janela.update()


while(True):
    Update()


    