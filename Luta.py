import pygame
import HUD
import Data
from PPlay.window import *
from PPlay.gameimage import *
from enum import Enum
import random



class EEstadoLuta(Enum):
    ANIMACAO = 1
    LUTANDO = 2



estadoLuta = 0
estadoAnimacao = 0
velocidadeAnimacao = 700
tempoAnimacao = 1
tempoPassado = 0
posicaoBotoesInicial = []

class LutaHUD():
    def __init__(self):
        self.background = HUD.GameImageMelhor('Sprites/Luta/LutaBG.png', 0, 0)
        self.bAtacar = HUD.GameImageMelhor('Sprites/Luta/BAtacar.png', 0, 0)
        self.bHabilidade = HUD.GameImageMelhor('Sprites/Luta/BHabilidade.png', 0, 0)
        self.bItem = HUD.GameImageMelhor('Sprites/Luta/BItem.png', 0, 0)
        self.bFugir = HUD.GameImageMelhor('Sprites/Luta/BFugir.png', 0, 0)
        self.bAtacarSelecionado = HUD.GameImageMelhor('Sprites/Luta/BAtacarHL.png', 0, 0)
        self.bItemSelecionado = HUD.GameImageMelhor('Sprites/Luta/BItemHL.png', 0, 0)
        self.bFugirSelecionado = HUD.GameImageMelhor('Sprites/Luta/BFugirHL.png', 0, 0)        
        self.bHabilidadeSelecionado = HUD.GameImageMelhor('Sprites/Luta/BHabilidadeHL.png', 0, 0)



def EntrarLuta(janela, deltaTime):
    global velocidadeAnimacao
    global tempoAnimacao
    global tempoPassado
    global estadoAnimacao
    global janelaSurface
    global estadoLuta
    
    if(estadoAnimacao == 0):
        centro = [int(janela.width / 2), int(janela.height / 2)]
        tempoPassado += min(0.1, deltaTime)
        progresso = min(1.0, tempoPassado / tempoAnimacao)



        posX = int(progresso * janela.width)
        posY = int(progresso * janela.height)


        novaJanela = pygame.Surface((janela.width, janela.height), pygame.SRCALPHA)
        corPixel = (0, 0, 0) 


        pontosTTL = [ (0, 0), (0, posY), (centro[0], centro[1]) ]


        pontosTTR = [ (janela.width, 0), (janela.width - posX, 0), (centro[0], centro[1]) ]


        pontosTBL = [ (0, janela.height), (posX, janela.height), (centro[0], centro[1]) ]


        pontosTBR = [ (janela.width, janela.height), (janela.width, janela.height - posY), (centro[0], centro[1]) ]


        pygame.draw.polygon(novaJanela, corPixel, pontosTTL)
        pygame.draw.polygon(novaJanela, corPixel, pontosTTR)
        pygame.draw.polygon(novaJanela, corPixel, pontosTBL)
        pygame.draw.polygon(novaJanela, corPixel, pontosTBR)
        

        janela.get_screen().blit(novaJanela, (0, 0))

        if(progresso == 1):
            estadoAnimacao = 1
            tempoPassado = 0
            return 1


    elif(estadoAnimacao == 1):
        if(tempoPassado == 0):
            janelaSurface = janela.get_screen().copy()
            janela.get_screen().fill((0, 0, 0)) # cinza

        tempoPassado += min(0.1, deltaTime)
        progresso = min(1.0, tempoPassado / tempoAnimacao)

        metadeEsquerda = pygame.Rect(0, 0, int(janela.width / 2), janela.height)
        metadeDireita =  pygame.Rect(int(janela.width / 2), 0, int(janela.width / 2), janela.height)

        janela.get_screen().blit(janelaSurface, (int(progresso * int(janela.width / 2)) - int(janela.width / 2) , 0), metadeEsquerda)
        janela.get_screen().blit(janelaSurface, (int(janela.width) - int(progresso * int(janela.width / 2)) , 0), metadeDireita)

        if(progresso == 1):
            estadoAnimacao = -1
            estadoLuta = EEstadoLuta.LUTANDO



def CriarLutaHUD(janela):
    lutaHUD = LutaHUD()
    lutaHUD.background.Transformar(janela.width, janela.height)
    lutaHUD.background.set_position(0, 0)

    lutaHUD.bAtacar.Transformar(388 * (janela.width/1920) , 103 * (janela.height/1080) )
    lutaHUD.bAtacar.set_position(janela.width * 0.075, janela.height - (7 * janela.height / 30))

    lutaHUD.bHabilidade.Transformar(388 * (janela.width/1920) , 103 * (janela.height/1080) )
    lutaHUD.bHabilidade.set_position(janela.width * 0.03, janela.height - (3 * janela.height / 10))

    lutaHUD.bItem.Transformar(388 * (janela.width/1920) , 103 * (janela.height/1080) )
    lutaHUD.bItem.set_position(janela.width * 0.03, janela.height - (janela.height / 6))

    lutaHUD.bFugir.Transformar(388 * (janela.width/1920) , 103 * (janela.height/1080) )
    lutaHUD.bFugir.set_position(janela.width * 0.01, janela.height - (janela.height / 10))

    return lutaHUD


def CalcularInimigos(lugar):
    if(lugar == Data.EANDAR.EANDAR1):
        nInimigos = random.randint(1, 4)
        inimigosLuta = []
        nInimigos = 4
        for i in range(0, nInimigos):
            inimigo = Data.Inimigo(0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0))

            tipoInimigo = random.choice(list(Data.tipoInimigo.values()))
            if(tipoInimigo == Data.tipoInimigo["Limite"]):
                inimigo = Data.ILimite()
                print("Foi")

            inimigosLuta.append(inimigo)

        return inimigosLuta
    

def AnimarTrocaBotoes(lutaHUD):
    global estadoAnimacao
    global estadoLuta
    global tempoPassado

   # posicaoBotoesInicial.append(lutaHUD.bItem.)

    tempoPassado = 0
    estadoAnimacao = 2
    estadoLuta = EEstadoLuta.ANIMACAO

def AnimarTrocaBotoesLoop(janela, deltaTime, lutaHUD, botaoSelecionadoLuta, posicoesBotoesLuta):
    global estadoLuta
    global tempoAnimacao
    global tempoPassado

    progresso = min(1.0, tempoPassado / tempoAnimacao)


    if(progresso < 0):
        lutaHUD.bItem.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][1])
        lutaHUD.bFugir.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][1] )
        lutaHUD.bHabilidade.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][0],posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][1] )
        lutaHUD.bAtacar.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][1])
    
    
    
    else:
        lutaHUD.bItem.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][1])
        lutaHUD.bFugir.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][1] )
        lutaHUD.bHabilidade.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][0],posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][1] )
        lutaHUD.bAtacar.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][1])

        estadoLuta = EEstadoLuta.LUTANDO


    

    # def get_line_pixels_bresenham(x0, y0, x1, y1):
    # """
    # Gets all integer pixel coordinates for a line using Bresenham's algorithm.
    # """
    # pixels = []
    # dx = abs(x1 - x0)
    # dy = -abs(y1 - y0)
    
    # Determine the direction of the line
    # sx = 1 if x0 < x1 else -1
    # sy = 1 if y0 < y1 else -1
    
    # err = dx + dy  # Error value
    
    # while True:
    #     pixels.append((x0, y0))
    #     if x0 == x1 and y0 == y1:
    #         break
            
    #     e2 = 2 * err
    #     if e2 >= dy:
    #         err += dy
    #         x0 += sx
    #     if e2 <= dx:
    #         err += dx
    #         y0 += sy
            
    # return pixels

# def EntrarLuta(janela, deltaTime):
#     global animacaoILados
#     global animacaoICimaBaixo
#     global texturaAntiga
#     global ultimaAnimacaoI
#     global velocidadeAnimacao
#     global ultimaAnimacaoICimaBaixo
#     global tempoAnimacao
#     global tempoPassado


#     centro = [int(janela.width / 2), int(janela.height / 2)]

#     novaJanela = pygame.Surface((janela.width, janela.height), pygame.SRCALPHA)
#     corPixel = (0, 0, 0)



#     tempoPassado += min(0.1, deltaTime)


#     progresso = min(1.0, tempoPassado / tempoAnimacao)


#     posX = int(progresso * janela.width)
#     posY = int(progresso * janela.height)


        
#     if(animacaoILados == 0):
#         novaJanela.set_at((centro[0], centro[1]), corPixel)


#     if(posY <= janela.height):
#         for pontos in get_line_pixels_bresenham(centro[0], centro[1], 0, ultimaAnimacaoI):
#             novaJanela.blit((min(pontos[0], posY), min(pontos[1] + 1, posY)), corPixel)

#         for passoAnimacao in range(ultimaAnimacaoI, posY):
#             if(passoAnimacao < janela.height):
            
#                 for pontos in get_line_pixels_bresenham(centro[0], centro[1], 0, passoAnimacao):
#                    # corPixel = janela.get_screen().get_at((min(pontos[0], janela.width - 1), min(pontos[1], janela.height - 1)))
#                     novaJanela.set_at((min(pontos[0], janela.width - 1), min(pontos[1] + 1, janela.height - 1)), corPixel)
                
#                 for pontos in get_line_pixels_bresenham(centro[0], centro[1], janela.width , janela.height - passoAnimacao):
#                   #  corPixel = janela.get_screen().get_at((min(pontos[0], janela.width - 1), min(pontos[1], janela.height - 1)))
#                     novaJanela.set_at((min(pontos[0], janela.width - 1), min(pontos[1] - 1, janela.height - 1)), corPixel)
    



#         ultimaAnimacaoI = posY


#     if(posX <= janela.width):
#         for passoAnimacao in range(ultimaAnimacaoICimaBaixo, posX):
#             if(passoAnimacao < janela.width):
            
#                 for pontos in get_line_pixels_bresenham(centro[0], centro[1], janela.width - passoAnimacao, 0):
#                   #  corPixel = janela.get_screen().get_at((min(pontos[0], janela.width - 1), min(pontos[1], janela.height - 1)))
#                     novaJanela.set_at((min(pontos[0] - 1, janela.width - 1), min(pontos[1], janela.height - 1)), corPixel)
                
#                 for pontos in get_line_pixels_bresenham(centro[0], centro[1], passoAnimacao , janela.height):
#                    # corPixel = janela.get_screen().get_at((min(pontos[0], janela.width - 1), min(pontos[1], janela.height - 1)))
#                     novaJanela.set_at((min(pontos[0] + 1, janela.width - 1), min(pontos[1], janela.height - 1)), corPixel)
    

#         ultimaAnimacaoICimaBaixo = posX


#     janela.get_screen().blit(novaJanela, (0, 0))


