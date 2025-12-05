from PPlay.window import *
from PPlay.sprite import *

from Janela import CriarJanela

janela = CriarJanela()


import Sprites
import Data
import Input
import Mapa
import math
import HUD
import luta


Sprites.CarregarTexturas(janela)
jogadorHUD = HUD.CriarHUD(janela)
lutaHUD = luta.CriarLutaHUD(janela)


estadoJogo = Data.EEstado.ANDANDO

inimigosNaLuta = []
posicoesBotoesLuta = [ (janela.width * 0.075, janela.height - (7 * janela.height / 30)), (janela.width * 0.03, janela.height - (3 * janela.height / 10)),  (janela.width * 0.01, janela.height - (janela.height / 10)), (janela.width * 0.03, janela.height - (janela.height / 6)),]
botaoSelecionadoLuta = Data.ELuta.ATACAR
ultimoMovimentoBotao = time.time()
botaoSolto = True

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
mapaAtual = Mapa.GerarMapa(0, 0)



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
    global estadoJogo
    global botaoSelecionadoLuta
    global ultimoMovimentoBotao
    global botaoSolto


    deltaTime = time.time() - tempoUltimoFrame
    tempoUltimoFrame = time.time()

    segundo += deltaTime

    ultimoDraw += deltaTime


  

    ultimoInput = Input.LerInput(teclado, janela)
    if(ultimoInput == 0):
        botaoSolto = True


    if(estadoJogo == Data.EEstado.ANDANDO):
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

        





        if(ultimoInput == 9):
            
            PrepararLuta()
            estadoJogo = Data.EEstado.LUTA
            luta.self.estadoLuta = luta.EEstadoLuta.ANIMACAO


        RenderizarMapa()


    elif(estadoJogo == Data.EEstado.LUTA):

        if(luta.self.estadoLuta == luta.EEstadoLuta.ANIMACAO):
            if(luta.self.estadoAnimacao <= 1):
                if(luta.EntrarLuta(janela, deltaTime) == 1):
                    botaoSelecionadoLuta = Data.ELuta.ATACAR
                    CalcularBotoesLuta()
                    
                    DesenharLutaHUD()
                    DesenharInimigos()
                    DesenharLutaBotoes()
                    luta.EntrarLuta(janela, 0.001)
                
            elif(luta.self.estadoAnimacao == 2):
                luta.AnimarTrocaBotoesLoop(janela, deltaTime, lutaHUD, botaoSelecionadoLuta, posicoesBotoesLuta)

        elif(luta.self.estadoLuta == luta.EEstadoLuta.LUTANDO):
            

            if(time.time() - ultimoMovimentoBotao > 0.1 and botaoSolto):
                if(ultimoInput == 2):
                    if(botaoSelecionadoLuta == Data.ELuta.ATACAR):
                        botaoSelecionadoLuta = Data.ELuta.HABILIDADE


                    elif(botaoSelecionadoLuta == Data.ELuta.HABILIDADE):
                        botaoSelecionadoLuta = Data.ELuta.ITEM


                    elif(botaoSelecionadoLuta == Data.ELuta.ITEM):
                        botaoSelecionadoLuta = Data.ELuta.FUGIR


                    elif(botaoSelecionadoLuta == Data.ELuta.FUGIR):
                        botaoSelecionadoLuta = Data.ELuta.ATACAR

                    luta.AnimarTrocaBotoes(lutaHUD)

                    ultimoMovimentoBotao = time.time()
                    botaoSolto = False

                elif(ultimoInput == 1):
                    if(botaoSelecionadoLuta == Data.ELuta.ATACAR):
                        botaoSelecionadoLuta = Data.ELuta.FUGIR


                    elif(botaoSelecionadoLuta == Data.ELuta.FUGIR):
                        botaoSelecionadoLuta = Data.ELuta.ITEM


                    elif(botaoSelecionadoLuta == Data.ELuta.ITEM):
                        botaoSelecionadoLuta = Data.ELuta.HABILIDADE


                    elif(botaoSelecionadoLuta == Data.ELuta.HABILIDADE):
                        botaoSelecionadoLuta = Data.ELuta.ATACAR

                    luta.AnimarTrocaBotoes(lutaHUD)

                    ultimoMovimentoBotao = time.time()
                    botaoSolto = False

            RenderizarLuta()

        

   

 


    numeroFrames += 1
    janela.update()

    if(segundo > 1):
        print(numeroFrames)
        numeroFrames = 0
        segundo -= 1



def RenderizarLuta():

    
    DesenharLutaHUD()
    DesenharInimigos()
    DesenharLutaBotoes()
    janela.update()


def RenderizarMapa():
    global ultimoDraw
    global janela
    global janelaMenor
    global GAME_HEIGHT
    global GAME_WIDTH
    global jogador


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



def ChecarColisao(novaPosicaoX, novaPosicaoY):

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
    jogadorHUD.barraHP.Transformar((janela.width * 0.2) * max(1, (jogador.vida / jogador.vidaMaxima)), janela.height* 0.03)
    jogadorHUD.barraHP.draw()

    jogadorHUD.barraEnergiaBackground.draw()
    jogadorHUD.barraHP.Transformar((janela.width * 0.2) * max(1, (jogador.energia / jogador.energiaMaxima)), janela.height* 0.03)
    jogadorHUD.barraEnergia.draw()


    janela.draw_text("Vida:    " + str(jogador.vida) + " / " + str(jogador.vidaMaxima), janela.width * 0.18, janela.height * 0.89, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )
    janela.draw_text("Energia: " + str(jogador.energia)+ " / " + str(jogador.energiaMaxima), janela.width * 0.42, janela.height * 0.89, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )

    janela.draw_text("Level: " + str(jogador.level), janela.width * 0.72, janela.height * 0.9, "Sprites/HUD/PressStart2P-Regular.ttf", 14 * int((1280/janela.width)), (63,78,182), )
    janela.draw_text("XP: " + str(jogador.xp)+ " / " + str(jogador.energiaMaxima), janela.width * 0.72, janela.height * 0.95, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )



def DesenharLutaHUD():
    lutaHUD.background.draw()
   
               
def DesenharLutaBotoes():
    
    lutaHUD.bAtacar.draw()
    lutaHUD.bHabilidade.draw()
    lutaHUD.bItem.draw()
    lutaHUD.bFugir.draw()

def CalcularBotoesLuta():

    lutaHUD.bItem.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][1])
    lutaHUD.bFugir.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][1] )
    lutaHUD.bHabilidade.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][0],posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][1] )
    lutaHUD.bAtacar.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][1])




def DesenharInimigos():
    global inimigosNaLuta
   
    i = 0

    ordemDesenhar = []
    for inimigo in inimigosNaLuta:
       if(inimigo.tipo == Data.tipoInimigo["Limite"]):
            inimigo.sprite.Transformar(int(317 * (janela.width/1920)), int(497 * (janela.height/1080)))
            largura = (inimigo.sprite.largura / 2)
            altura = (inimigo.sprite.altura / 2)

            if(i == 0):
                inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.65 * janela.height - altura )    )
            
            elif(i == 1):
                inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.65 * janela.height  - altura)    )

            elif(i == 2):
                inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.55 * janela.height - altura )    )
            
            elif(i == 3):
                inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.55 * janela.height - altura )    )


            ordemDesenhar.insert(0, inimigo)
            i += 1

    for inimigo in ordemDesenhar:
        inimigo.sprite.draw()


def PrepararLuta():
    global inimigosNaLuta

    inimigosNaLuta.clear()
    inimigosNaLuta = luta.CalcularInimigos(Data.EANDAR.EANDAR1)




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


    