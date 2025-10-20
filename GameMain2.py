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
import Luta
import GameInstance

Sprites.CarregarTexturas(janela)
jogo = GameInstance.Jogo(janela)
luta = jogo.luta


def Update():
    

    jogo.deltaTime = time.time() - jogo.tempoUltimoFrame
    jogo.tempoUltimoFrame = time.time()

    jogo.segundo += jogo.deltaTime

    jogo.ultimoDraw += jogo.deltaTime


  

    jogo.ultimoInput = Input.LerInput(jogo.teclado, janela)
    if(jogo.ultimoInput == 0):
        jogo.botaoSolto = True


    if(jogo.estadoJogo == Data.EEstado.ANDANDO):
        if(time.time() - jogo.ultimaRotacao > 0.005):
            if(jogo.isRodando):
                
                VirarJogadorLoop(jogo.ultimaDirecaoX, jogo.ultimaDirecaoY)

            else:


                if(jogo.ultimoInput == 3):
                    AtualizarDirecaoJogador(jogo.ultimoInput)
                    jogo.rodandoDirecao = 1
                    jogo.isRodando = True
                    jogo.ultimaDirecaoX = jogo.jogador.dirX
                    jogo.ultimaDirecaoY = jogo.jogador.dirY


                elif(jogo.ultimoInput == 4):
                    AtualizarDirecaoJogador(jogo.ultimoInput)
                    jogo.rodandoDirecao = 2
                    jogo.isRodando = True
                    jogo.ultimaDirecaoX = jogo.jogador.dirX
                    jogo.ultimaDirecaoY = jogo.jogador.dirY




        if(time.time() - jogo.ultimoMovimento > 0.1):

            if(jogo.isAndando):
                AndarJogadorLoop(jogo.jogador, jogo.andandoDestino, jogo.inicioJogador, jogo.andarVelocidade)

                if(abs(jogo.andandoDestino[0] - jogo.jogador.x) < 0.05 and abs(jogo.andandoDestino[1] - jogo.jogador.y) < 0.05):
                    jogo.jogador.x = jogo.andandoDestino[0]
                    jogo.jogador.y = jogo.andandoDestino[1]

                    jogo.isAndando = False
                    jogo.ultimoMovimento = time.time()

            elif(AndarJogador(jogo.ultimoInput)):
                

                jogo.isAndando = True

        





        if(jogo.ultimoInput == 9):
            
            PrepararLuta()
            jogo.estadoJogo = Data.EEstado.LUTA
            luta.estadoLuta = luta.EEstadoLuta.ANIMACAO


        RenderizarMapa()


    elif(jogo.estadoJogo == Data.EEstado.LUTA):

        if(luta.estadoLuta == luta.EEstadoLuta.ANIMACAO):
            if(luta.estadoAnimacao <= 1):
                if(luta.EntrarLuta(janela, jogo.deltaTime) == 1):
                    jogo.botaoSelecionadoLuta = Data.ELuta.ATACAR
                    luta.ResetarBotoes(jogo.lutaHUD, jogo.botaoSelecionadoLuta, jogo.posicoesBotoesLuta)
                    CalcularBotoesLuta()
                    
                    DesenharLutaHUD()
                    DesenharInimigos()
                    DesenharLutaBotoes()
                    luta.EntrarLuta(janela, 0.001)
                
            elif(luta.estadoAnimacao == 2):
                luta.AnimarTrocaBotoesLoop(janela, jogo.deltaTime, jogo.lutaHUD, jogo.botaoSelecionadoLuta, jogo.posicoesBotoesLuta)
                RenderizarLuta()

        elif(luta.estadoLuta == luta.EEstadoLuta.LUTANDO):
            

            if(time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto):
                if(jogo.ultimoInput == 2):
                    jogo.botaoAntigo = jogo.botaoSelecionadoLuta

                    if(jogo.botaoSelecionadoLuta == Data.ELuta.ATACAR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.HABILIDADE


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.HABILIDADE):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ITEM


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.ITEM):
                        jogo.botaoSelecionadoLuta = Data.ELuta.FUGIR


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.FUGIR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ATACAR

                    luta.AnimarTrocaBotoes(jogo.lutaHUD, jogo.botaoAntigo, jogo.botaoSelecionadoLuta)

                    jogo.ultimoMovimentoBotao = time.time()
                    jogo.botaoSolto = False

                elif(jogo.ultimoInput == 1):
                    jogo.botaoAntigo = jogo.botaoSelecionadoLuta

                    if(jogo.botaoSelecionadoLuta == Data.ELuta.ATACAR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.FUGIR


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.FUGIR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ITEM


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.ITEM):
                        jogo.botaoSelecionadoLuta = Data.ELuta.HABILIDADE


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.HABILIDADE):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ATACAR

                    luta.AnimarTrocaBotoes(jogo.lutaHUD, jogo.botaoAntigo, jogo.botaoSelecionadoLuta)

                    jogo.ultimoMovimentoBotao = time.time()
                    jogo.botaoSolto = False

            RenderizarLuta()

        

   

 


    jogo.numeroFrames += 1
    janela.update()

    if(jogo.segundo > 1):
        print(jogo.numeroFrames)
        jogo.numeroFrames = 0
        jogo.segundo -= 1



def RenderizarLuta():

    
    DesenharLutaHUD()
    DesenharInimigos()
    DesenharLutaBotoes()
    janela.update()


def RenderizarMapa():

        #dar update em 60 frames
    if(jogo.ultimoDraw > 0.016):

        janela.get_screen().fill((100, 100, 100)) # cinza
        jogo.janelaMenor.fill((100, 100, 100))


        Mapa.RenderizarMapa3DLowPoly(jogo.janelaMenor,jogo.GAME_HEIGHT, jogo.GAME_WIDTH, jogo.jogador)
        scaled_surface = pygame.transform.scale(jogo.janelaMenor, (janela.width, janela.height))
    

        janela.get_screen().blit(scaled_surface, (0, 0))
        Mapa.RenderizarMapa3D(janela, jogo.jogador)


        DesenharHUD()


        janela.update()




        jogo.ultimoDraw = 0



def ChecarColisao(novaPosicaoX, novaPosicaoY):

    if(novaPosicaoX - jogo.jogador.x > 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].oeste):
            return True
        
    elif(novaPosicaoX - jogo.jogador.x < 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].leste):
            return True
        
    elif(novaPosicaoY - jogo.jogador.y < 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].norte):
            return True
        
    elif(novaPosicaoY - jogo.jogador.y > 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].sul):
            return True


    return False

def AndarJogadorLoop(jogador, andandoDestino, inicioJogador, velocidade):
    
    if(andandoDestino[1] == jogador.y):
        jogador.x += (andandoDestino[0] - inicioJogador.x) * velocidade * jogo.deltaTime
    elif(andandoDestino[0] == jogador.x):
        jogador.y += (andandoDestino[1] - inicioJogador.y) * velocidade * jogo.deltaTime

def AndarJogador(ultimoInput):

    passo = 0

    if(ultimoInput == 1):
        passo = 1

        
    elif(ultimoInput == 2):
        passo = -1


    if(passo != 0):
        #norte
        if(jogo.jogador.dirX == 0 and jogo.jogador.dirY == 1):
            if(not ChecarColisao(jogo.jogador.x, (jogo.jogador.y + passo))):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x
                jogo.andandoDestino[1] = jogo.jogador.y + passo
                return True
        #sul
        elif(jogo.jogador.dirX == 0 and jogo.jogador.dirY == -1 ):
            if(not ChecarColisao(jogo.jogador.x, (jogo.jogador.y - passo))):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x
                jogo.andandoDestino[1] = jogo.jogador.y - passo
                return True
        #leste
        if(jogo.jogador.dirX == 1 and jogo.jogador.dirY == 0):
            if(not ChecarColisao(jogo.jogador.x + passo, jogo.jogador.y)):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x + passo
                jogo.andandoDestino[1] = jogo.jogador.y
                return True
        #oeste
        elif(jogo.jogador.dirX == -1 and jogo.jogador.dirY == 0 ):
            if(not ChecarColisao(jogo.jogador.x - passo, jogo.jogador.y)):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x - passo
                jogo.andandoDestino[1] = jogo.jogador.y
                return True


def AtualizarDirecaoJogador(input):

    if(input == 3):
        if(jogo.jogador.direcao == Data.direcao["O"]):
            jogo.jogador.direcao = Data.direcao["N"]
        else:
            jogo.jogador.direcao += 1
    elif(input == 4):
        if(jogo.jogador.direcao == Data.direcao["N"]):
            jogo.jogador.direcao = Data.direcao["O"]
        else:
            jogo.jogador.direcao -= 1

#virar aos poucos pra ficar bonitinho
def VirarJogadorLoop(ultimaDirecaoX, ultimaDirecaoY):

    # print("Ultima direção X:  " + str(ultimaDirecaoX))
    # print("jogador.dirX:  " + str(jogador.dirX))

    VirarJogador(jogo.rodandoDirecao, ultimaDirecaoX, ultimaDirecaoY)

    jogo.ultimaRotacao = time.time()
    




    




def VirarJogador(direcao, ultimaDirecaoX, ultimaDirecaoY):
    #direita

    
    if(direcao == 1):
       
        oldDirX = jogo.jogador.dirX


        jogo.jogador.dirX = jogo.jogador.dirX * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.dirY * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.dirY = oldDirX * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.dirY * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime))

        oldPlaneX = jogo.jogador.planeX
        jogo.jogador.planeX = jogo.jogador.planeX * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.planeY * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.planeY = oldPlaneX * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.planeY * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime))







    elif(direcao == 2):


        oldDirX = jogo.jogador.dirX
        jogo.jogador.dirX = jogo.jogador.dirX * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.dirY * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.dirY = oldDirX * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.dirY * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime))

        oldPlaneX = jogo.jogador.planeX
        jogo.jogador.planeX = jogo.jogador.planeX * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.planeY * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.planeY = oldPlaneX * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.planeY * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime))

    
    if(abs(ultimaDirecaoX - jogo.jogador.dirX) >= 1):
        jogo.jogador.dirX = 0
        
        #norte
        if(jogo.jogador.dirY > 0):
            jogo.jogador.dirY = 1
            jogo.jogador.planeX = 0.66
            jogo.jogador.planeY = 0.0

        #sul
        else:
            jogo.jogador.dirY = -1
            jogo.jogador.planeX = -0.66
            jogo.jogador.planeY = 0.0

        jogo.isRodando = False
        jogo.ultimaRotacao = time.time() + jogo.cooldownRodar

    elif(abs(ultimaDirecaoY - jogo.jogador.dirY) >= 1):
        jogo.jogador.dirY = 0
        
        #leste
        if(jogo.jogador.dirX > 0):
            jogo.jogador.dirX = 1
            jogo.jogador.planeX = 0
            jogo.jogador.planeY = -0.66

        #oeste
        else:
            jogo.jogador.dirX = -1
            jogo.jogador.planeX = 0.0
            jogo.jogador.planeY = 0.66

        jogo.isRodando = False
        jogo.ultimaRotacao = time.time() + jogo.cooldownRodar



def DesenharHUD():
    jogo.jogadorHUD.background.draw()
    jogo.jogadorHUD.barraHPBackground.draw()
    jogo.jogadorHUD.barraHP.Transformar((janela.width * 0.2) * max(1, (jogo.jogador.vida / jogo.jogador.vidaMaxima)), janela.height* 0.03)
    jogo.jogadorHUD.barraHP.draw()

    jogo.jogadorHUD.barraEnergiaBackground.draw()
    jogo.jogadorHUD.barraHP.Transformar((janela.width * 0.2) * max(1, (jogo.jogador.energia / jogo.jogador.energiaMaxima)), janela.height* 0.03)
    jogo.jogadorHUD.barraEnergia.draw()


    janela.draw_text("Vida:    " + str(jogo.jogador.vida) + " / " + str(jogo.jogador.vidaMaxima), janela.width * 0.18, janela.height * 0.89, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )
    janela.draw_text("Energia: " + str(jogo.jogador.energia)+ " / " + str(jogo.jogador.energiaMaxima), janela.width * 0.42, janela.height * 0.89, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )

    janela.draw_text("Level: " + str(jogo.jogador.level), janela.width * 0.72, janela.height * 0.9, "Sprites/HUD/PressStart2P-Regular.ttf", 14 * int((1280/janela.width)), (63,78,182), )
    janela.draw_text("XP: " + str(jogo.jogador.xp)+ " / " + str(jogo.jogador.energiaMaxima), janela.width * 0.72, janela.height * 0.95, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )



def DesenharLutaHUD():
    jogo.lutaHUD.background.draw()
   
               
def DesenharLutaBotoes():


    #não olhe...
    ultimoDraw = 0
    if jogo.botaoSelecionadoLuta.value == 3 and jogo.botaoAntigo.value == 4:
        ultimoDraw = 2
    elif jogo.botaoSelecionadoLuta.value == 1 and jogo.botaoAntigo.value == 2:
        ultimoDraw = 0
    elif jogo.botaoSelecionadoLuta.value == 4 and jogo.botaoAntigo.value == 1:
        ultimoDraw = 3
    elif jogo.botaoSelecionadoLuta.value == 3 and jogo.botaoAntigo.value == 2:
        ultimoDraw = 1
    elif jogo.botaoSelecionadoLuta.value == 4 and jogo.botaoAntigo.value == 3:
        ultimoDraw = 2
    else:
        ultimoDraw = max(0, jogo.botaoAntigo.value - jogo.botaoSelecionadoLuta.value)

    jogo.botoesLuta[ultimoDraw].draw()


    for i, button in enumerate(jogo.botoesLuta):
        if i != ultimoDraw:
            button.draw()


    


def CalcularBotoesLuta():

    jogo.lutaHUD.bItem.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value) % 4][0], jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value) % 4][1])
    jogo.lutaHUD.bFugir.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 1) % 4][0], jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 1) % 4][1] )
    jogo.lutaHUD.bHabilidade.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 2) % 4][0],jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 2) % 4][1] )
    jogo.lutaHUD.bAtacar.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 3) % 4][0], jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 3) % 4][1])




def DesenharInimigos():
   
    i = 0

    ordemDesenhar = []
    for inimigo in jogo.inimigosNaLuta:
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


    jogo.inimigosNaLuta.clear()
    jogo.inimigosNaLuta = luta.CalcularInimigos(Data.EANDAR.EANDAR1)




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
    Sprites.DrawLines(jogo.jogador, janela, paredes)
    


    janela.update()


while(True):
    Update()


    