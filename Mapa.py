import Data
import math
import pygame
import Sprites
import copy


class MapaDungeon():
    def __init__(self, x, y):
        self.altura = x
        self.largura = y
        self.paredes = []

    def InserirParede(self, x, y, direcao):
        self.altura = x
        self.paredes.append([x,y,direcao])
    def GetParedes(self):
        return self.paredes
    
class Parede():
     def __init__(self, norte, sul, leste, oeste, textura):
        self.norte = norte
        self.sul = sul
        self.leste = leste
        self.oeste = oeste
        self.textura = textura

mapaAtual = [[0]]

texturaTeto = 0
texturaChao = 0


def GerarMapa(mapaID):
    global mapaAtual
    global texturaTeto
    global texturaChao

    n = Parede(1, 0, 0, 0, Sprites.texturas[1])
    s = Parede(0, 1, 0, 0, Sprites.texturas[1])
    l = Parede(0, 0, 1, 0, Sprites.texturas[1])
    o = Parede(0, 0, 0, 1, Sprites.texturas[1])
    O = Parede(0, 0, 0, 0, Sprites.texturas[1])

    texturaTeto = Sprites.texturas[Sprites.texturasDic["teto1"]]
    texturaChao = Sprites.texturas[Sprites.texturasDic["chao1"]]


    #game_map = [
    #[n, n, n, n, n],
    #[l, O, O, O, o],
    #[l, O, O, O, o],
    #[l, O, o, o, o],
    #[l, O, o, o, o],
    #[s, s, s, s, s]
    #]

    game_map = [
    [O, O, O, O, O, O, O, O, O, O, O, O, n, n, n, O, O, O, O, O, O, O, O, O, O],
    [O, O, O, O, O, O, O, O, O, n, n, O, o, O, l, O, O, O, O, O, O, O, O, O, O],
    [O, O, O, O, O, O, O, O, O, o, l, n, o, O, l, O, O, O, O, O, O, O, O, O, O],
    [O, O, O, O, O, O, O, O, O, o, O, O, O, O, l, O, O, O, O, O, O, O, O, O, O],
    [O, n, O, O, O, O, O, O, O, s, s, s, o, l, s, n, O, O, O, O, O, O, O, n, O],
    [l, l, l, s, o, l, s, o, l, s, o, O, o, l, l, l, O, l, s, o, l, s, o, o, o],
    [l, O, s, O, s, s, O, s, s, O, s, s, O, O, s, O, s, s, O, s, s, O, s, O, o],
    [s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s]
    ]

    mapCopy = []

    for i in range(len(game_map)):
        mapCopy.append([])
        for k in range(len(game_map[i])): 
            novaParede = Parede(0,0,0,0,0)
            novaParede.norte = game_map[i][k].norte
            novaParede.sul = game_map[i][k].sul
            novaParede.leste = game_map[i][k].leste
            novaParede.oeste = game_map[i][k].oeste
            novaParede.textura = game_map[i][k].textura

            mapCopy[i].append(novaParede)


    for i in range(len(game_map)):
        for k in range(len(game_map[i])):
            if(game_map[i][k] != 0):
                if(game_map[i][k].leste and k+1 < len(game_map[i])):
                    mapCopy[i][k+1].oeste = 1
                if(k+1 < len(game_map[i]) and game_map[i][k+1].oeste):
                    mapCopy[i][k].leste = 1

                if(game_map[i][k].norte and i+1 < len(game_map)):
                    mapCopy[i + 1][k].sul = 1
                if(i+1 < len(game_map) and game_map[i + 1][k].sul):
                    mapCopy[i][k].norte = 1

    mapaAtual = mapCopy

    return mapaAtual

def GetMapaAtual():

    return mapaAtual

def RenderizarMapa3D(janela, jogador):
    global tilesVisiveis
    tilesVisiveis = []

    game_map = GetMapaAtual()



    for coluna in range(janela.width):
        #de 0 a 1, onde a coluna está
        porcentagemDaTela = coluna / float(janela.width)

        #transforma o 0 a 1 em -1 a 1
        cameraX = 2 * (porcentagemDaTela) - 1
        

        tamanhoMapaX = len(game_map[0])
        tamanhoMapaY = len(game_map)


        direcaoRaioX = jogador.dirX + jogador.planeX * cameraX
        direcaoRaioY = jogador.dirY + jogador.planeY * cameraX


        #DDA

        if(direcaoRaioX != 0):
            deltaDistanciaX = abs(1 / direcaoRaioX)
        else:
            #se o X for 0, o raio nunca crusa uma linha horizontal
            deltaDistanciaX = float('inf')


        if(direcaoRaioY != 0):
            deltaDistanciaY = abs(1 / direcaoRaioY)
        else:
            #se o Y for 0, o raio nunca crusa uma linha vertical
            deltaDistanciaY = float('inf')

        #direção do passo no eixo X
        passoX = 0

        #distância para a próxima linha do grid (distancias posteriores são normalizadas)
        #apesar do player, nesse projeto, estar sempre em 0.5 em relação ao grid, eu quero
        #implementar uma "animação" de andar até o próximo grid, então essa parte ainda é necessária
        distanciaX = 0
        distanciaY = 0

        jogadorXArredondado = int(jogador.x)
        jogadorYArredondado = int(jogador.y)
        if(direcaoRaioX < 0):
            #esquerda do grid
            passoX = -1
                        #jogador X inteiro - o grid anterior (parte inteira do X ex: 1.5 é 1) = 1.5 - 1 = 0.5
            distanciaX = (jogador.x - jogadorXArredondado) * deltaDistanciaX 
        else:
            #direita do grid
            passoX = 1
                        #parte inteira do X (ex: 1.5 é ) + 1 = próximo grid (2), - a fração (ex 1.5 é 0.5) = 0.5 de distância
            distanciaX = (jogadorXArredondado + 1.0 - jogador.x) * deltaDistanciaX

        if(direcaoRaioY < 0):
            #sul do grid
            passoY = -1
            distanciaY = (jogador.y - jogadorYArredondado) * deltaDistanciaY
        else:
            #norte do grid
            passoY = 1
            distanciaY = (jogadorYArredondado + 1.0 - jogador.y) * deltaDistanciaY

        mapaX = jogadorXArredondado
        mapaY = jogadorYArredondado
        hit = 0

        horizontal = 0

        while(not hit):

            #próximo square mais próximo
            if(distanciaX < distanciaY):
                distanciaX += deltaDistanciaX
                mapaX += passoX
                #parede vertical
                horizontal = 0
                
                if([mapaY, mapaX] not in tilesVisiveis):
                    tilesVisiveis.append([mapaY, mapaX]) 

                if(mapaX < tamanhoMapaX and mapaX >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoX > 0 and tile.oeste) or (passoX < 0 and tile.leste):
                            hit = 1
                else:
                    break

            else:
                distanciaY += deltaDistanciaY
                mapaY += passoY
                #parede horizontal
                horizontal = 1

                if([mapaY, mapaX] not in tilesVisiveis):
                    tilesVisiveis.append([mapaY, mapaX]) 

                if(mapaY < tamanhoMapaY and mapaY >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoY > 0 and tile.sul) or (passoY < 0 and tile.norte):
                            hit = 1
                else:
                    break
                #se tem parede, acerta (o mapa sempre tem que ser cercado de paredes)
            #if(game_map[mapaY][mapaX] > 0):
            #    hit = 1



        distanciaPerpendicular = 0

        if(horizontal):
            distanciaPerpendicular = (mapaY - jogador.y + ((1 -passoY) / 2 )) / direcaoRaioY
        else:                                                
                                                        #mágica que, infelizmente, não é de minha autoria
                                                        #se o passo for 1 calcula a distancia correta pra direita
                                                        #se for -1, ajusta para o grid correto no mapa
            distanciaPerpendicular = (mapaX - jogador.x +         ((1 - passoX) / 2) )                          / direcaoRaioX
        
        if(distanciaPerpendicular > 0):
            alturaDaLinha = int(janela.height / distanciaPerpendicular)
        else:
            #se a distância ate a parede for 0, o jogador está dentro da parede
            #então desenha a tela inteira (nunca vai acontecer, mas é bom ilustrar)
            alturaDaLinha = janela.height



         # Calcula onde a parede foi acertada
        if horizontal == 0: # vertical 
            wallX = jogador.y + distanciaPerpendicular * direcaoRaioY
        else: #  horizontal 
            wallX = jogador.x + distanciaPerpendicular * direcaoRaioX
        
        # Parte fracional da parede X
        wallX -= math.floor(wallX)
        



        #a visão do player sempre vai estar no meio da tela, então calculamos todas as paredes como sendo metade
        #acima e metade abaixo
        comecoDaLinha = -alturaDaLinha / 2 + janela.height / 2


        finalDaLinha = alturaDaLinha / 2 + janela.height / 2

        if finalDaLinha >= janela.height:
            finalDaLinha = janela.height

        # #cor da parede
        
        # if(horizontal):
        #     color = (150, 150, 150)
        # else:
        #     color = (250, 250, 250)

        #if(hit):
           # pygame.draw.line(janela.get_screen(), color, (coluna, comecoDaLinha), (coluna, finalDaLinha))




        # #--------TEXTURAAAAAAAAAAAAAA-----------------------------
        #tipo da textura é baseado no número da parede
        textura = Sprites.texturas[1]
        # acha a coluna da textura para desenhar (porcentagem de onde está na parede * largura da imagem)
        texX = int(wallX * float(textura.get_width()))


        # flipa imagem se for na parede da esquerda
        if horizontal == 0 and direcaoRaioX > 0:
            texX = textura.get_width() - texX - 1
        #flipa se for na parede do sul, olhando pro norte, e o player... 
        #só funciona
        if horizontal == 1 and direcaoRaioY < 0:
            texX = textura.get_width() - texX - 1 
        
        #pega uma coluna da textura baseado na posição X da imagem e escala pra parede
        pedacoDaTextura = textura.subsurface(texX, 0, 1, textura.get_height())
        
            # Clamp the height to be within the cache's bounds
        if(alturaDaLinha > janela.height * 3):
            print(alturaDaLinha)
            pedacoEscalado = pygame.transform.scale(pedacoDaTextura, (1, alturaDaLinha)) 
        else:
        
            # 1. Get the correct cache for the type of wall we hit
            wall_cache = Sprites.texturasCache[1]
            
            # 2. Look up the pre-scaled slice from the cache
            #    wall_cache[texture_column][desired_height]
            pedacoEscalado = wall_cache[texX][alturaDaLinha]
        

        #waow
        janela.get_screen().blit(pedacoEscalado, (coluna, comecoDaLinha))












def RenderizarMapa3DLowPoly(janela, janelaAltura, janelaLargura, jogador):

    game_map = GetMapaAtual()



    for coluna in range(janelaLargura):
        #de 0 a 1, onde a coluna está
        porcentagemDaTela = coluna / float(janelaLargura)

        #transforma o 0 a 1 em -1 a 1
        cameraX = 2 * (porcentagemDaTela) - 1
        

        tamanhoMapaX = len(game_map[0])
        tamanhoMapaY = len(game_map)


        direcaoRaioX = jogador.dirX + jogador.planeX * cameraX
        direcaoRaioY = jogador.dirY + jogador.planeY * cameraX


        #DDA

        if(direcaoRaioX != 0):
            deltaDistanciaX = abs(1 / direcaoRaioX)
        else:
            #se o X for 0, o raio nunca crusa uma linha horizontal
            deltaDistanciaX = float('inf')


        if(direcaoRaioY != 0):
            deltaDistanciaY = abs(1 / direcaoRaioY)
        else:
            #se o Y for 0, o raio nunca crusa uma linha vertical
            deltaDistanciaY = float('inf')

        #direção do passo no eixo X
        passoX = 0

        #distância para a próxima linha do grid (distancias posteriores são normalizadas)
        #apesar do player, nesse projeto, estar sempre em 0.5 em relação ao grid, eu quero
        #implementar uma "animação" de andar até o próximo grid, então essa parte ainda é necessária
        distanciaX = 0
        distanciaY = 0

        jogadorXArredondado = int(jogador.x)
        jogadorYArredondado = int(jogador.y)
        if(direcaoRaioX < 0):
            #esquerda do grid
            passoX = -1
                        #jogador X inteiro - o grid anterior (parte inteira do X ex: 1.5 é 1) = 1.5 - 1 = 0.5
            distanciaX = (jogador.x - jogadorXArredondado) * deltaDistanciaX 
        else:
            #direita do grid
            passoX = 1
                        #parte inteira do X (ex: 1.5 é ) + 1 = próximo grid (2), - a fração (ex 1.5 é 0.5) = 0.5 de distância
            distanciaX = (jogadorXArredondado + 1.0 - jogador.x) * deltaDistanciaX

        if(direcaoRaioY < 0):
            #sul do grid
            passoY = -1
            distanciaY = (jogador.y - jogadorYArredondado) * deltaDistanciaY
        else:
            #norte do grid
            passoY = 1
            distanciaY = (jogadorYArredondado + 1.0 - jogador.y) * deltaDistanciaY

        mapaX = jogadorXArredondado
        mapaY = jogadorYArredondado
        hit = 0

        horizontal = 0

        while(not hit):

            #próximo square mais próximo
            if(distanciaX < distanciaY):
                distanciaX += deltaDistanciaX
                mapaX += passoX
                #parede vertical
                horizontal = 0
                

                if(mapaX < tamanhoMapaX and mapaX >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoX > 0 and tile.oeste) or (passoX < 0 and tile.leste):
                            hit = 1
                else:
                    break

            else:
                distanciaY += deltaDistanciaY
                mapaY += passoY
                #parede horizontal
                horizontal = 1


                if(mapaY < tamanhoMapaY and mapaY >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoY > 0 and tile.sul) or (passoY < 0 and tile.norte):
                            hit = 1
                else:
                    break
                #se tem parede, acerta (o mapa sempre tem que ser cercado de paredes)
            #if(game_map[mapaY][mapaX] > 0):
            #    hit = 1



        distanciaPerpendicular = 0

        if(horizontal):
            distanciaPerpendicular = (mapaY - jogador.y + ((1 -passoY) / 2 )) / direcaoRaioY
        else:                                                
                                                        #mágica que, infelizmente, não é de minha autoria
                                                        #se o passo for 1 calcula a distancia correta pra direita
                                                        #se for -1, ajusta para o grid correto no mapa
            distanciaPerpendicular = (mapaX - jogador.x +         ((1 - passoX) / 2) )                          / direcaoRaioX
        
        if(distanciaPerpendicular > 0):
            alturaDaLinha = int(janelaAltura / distanciaPerpendicular)
        else:
            #se a distância ate a parede for 0, o jogador está dentro da parede
            #então desenha a tela inteira (nunca vai acontecer, mas é bom ilustrar)
            alturaDaLinha = janelaAltura



         # Calculate where exactly the wall was hit
        if horizontal == 0: # A vertical wall
            wallX = jogador.y + distanciaPerpendicular * direcaoRaioY
        else: # A horizontal wall
            wallX = jogador.x + distanciaPerpendicular * direcaoRaioX
        
        # Get the fractional part of wallX
        wallX -= math.floor(wallX)
        




        finalDaLinha = alturaDaLinha / 2 + janelaAltura / 2

        if finalDaLinha >= janelaAltura:
            finalDaLinha = janelaAltura - 1





        texturaTeto = Sprites.texturas[Sprites.texturasDic["teto1"]]
        texturaChao = Sprites.texturas[Sprites.texturasDic["chao1"]]



            # Find the exact world coordinate of the wall where it meets the floor.
        if horizontal == 0 and direcaoRaioX > 0:
            # Ray hit a WEST-facing wall.
            floorXWall = mapaX
            floorYWall = mapaY + wallX
        elif horizontal == 0 and direcaoRaioX < 0:
            # Ray hit an EAST-facing wall.
            floorXWall = mapaX + 1.0
            floorYWall = mapaY + wallX
        elif horizontal == 1 and direcaoRaioY > 0:
            # Ray hit a NORTH-facing wall.
            floorXWall = mapaX + wallX
            floorYWall = mapaY
        else: # horizontal == 1 and direcaoRaioY < 0
            # Ray hit a SOUTH-facing wall.
            floorXWall = mapaX + wallX
            floorYWall = mapaY + 1.0

        # Loop from the bottom of the wall to the bottom of the screen
        for y in range(int(finalDaLinha) , janelaAltura):
            # 1. Calculate the perspective-correct distance from the camera to this floor pixel.
            current_dist = janelaAltura / (2.0 * y - janelaAltura)
            
            # 2. Find the real-world (x,y) coordinates by interpolating between the player
            #    and the wall reference point. This creates the perspective effect.
            weight = current_dist / distanciaPerpendicular
            current_floor_x = weight * floorXWall + (1.0 - weight) * jogador.x
            current_floor_y = weight * floorYWall + (1.0 - weight) * jogador.y
            
            # 3. Get the corresponding coordinates for the floor texture.
            #    The '%' operator makes the texture tile seamlessly.
            floor_tex_x = int(current_floor_x * texturaChao.get_width()) % texturaChao.get_width()
            floor_tex_y = int(current_floor_y * texturaChao.get_height()) % texturaChao.get_height()
            
            # 4. Get the color from the texture and draw the floor pixel.
            #    (Assuming you've loaded 'floor_texture' and 'ceiling_texture')
            floor_color = texturaChao.get_at((floor_tex_x, floor_tex_y))
            janela.set_at((coluna, y - 1), floor_color)

            # 5. Symmetrically draw the ceiling pixel.
            ceiling_color = texturaTeto.get_at((floor_tex_x, floor_tex_y))
            janela.set_at((coluna, janelaAltura - y), ceiling_color)




