from PPlay.sprite import *
from PPlay.gameimage import *
import PPlay
import Data
import pygame


modoParede = { "frente" : 1,
               "esquerda" : 2,
               "direita" : 3

}

texturasDic = { "parede1" : 1,
                "chao1" : 2,
                "teto1" : 3, }

texturas = [None]
spriteList = []
texturasCache = {}

#classe sprite expandida para guardar imagem original e transformar se necessário
class Imagem3D(PPlay.gameimage.GameImage):
    def __init__(self,imagem, direcao, x, y):
        super().__init__(imagem)

        self.imagemOriginal = self.image
        self.rect = self.image.get_rect()
        self.coordenadas = (x,y)
        self.direcao = direcao
        self.set_position(0 - (self.width / 2), 0 - (self.height / 2))
    
    def Transformar(self, largura, altura):

        centroOriginal = self.rect.center
        imagemCopia = pygame.transform.scale(self.imagemOriginal, (largura, altura))
        self.rect = imagemCopia.get_rect()
        self.rect.center = centroOriginal
        self.image = imagemCopia
        self.set_position(self.x - (largura / 2), self.y - (altura / 2))



    def TransformarPerspectiva(self, shapeFinal, alturaInicio, alturaFim):

            larguraOG, alturaOG = self.imagemOriginal.get_size()


            surfaceFinal = pygame.Surface((shapeFinal.width, max(alturaInicio, alturaFim)), pygame.SRCALPHA)
            
            for pixel in range(shapeFinal.width):

                porcentagem = pixel / shapeFinal.width
                coluna = int(porcentagem * larguraOG)
                
                # pega o pedaço vertical da imagem original correspondente à colune do pixel que estamos
                pedaco = self.imagemOriginal.subsurface((coluna, 0, 1, alturaOG))

                #interpolação pra achar altura (não me pergunte por que funciona)
                alturaAtual = int(alturaInicio * (1 - porcentagem) + alturaFim * porcentagem)

                if alturaAtual < 1: 
                    alturaAtual = 1
                
                #escala o pedaço
                pedacoFinal = pygame.transform.scale(pedaco, (1, alturaAtual))
                
                yCentro = (surfaceFinal.get_height() / 2) - (alturaAtual / 2)
                
                # blit parece pintar um pedaço no "frame" da imagem, mas não entendo se isso causa problemas. Pelo menos funciona
                surfaceFinal.blit(pedacoFinal, (pixel, yCentro))


            self.image = surfaceFinal
            self.rect = self.image.get_rect()

            #pplay usa o topo esquerdo como origem da imagem
            self.rect.topleft = shapeFinal.topleft


    


def CarregarTexturas(janela):
    global texturasCache

    parede1 = pygame.image.load('Sprites/parede1.png').convert()
    texturas.append(parede1)
    parede1Cache = EscalarTextura(parede1, janela.height)


    chao1 = pygame.image.load('Sprites/chao1.png').convert()
    texturas.append(chao1)
    chao1Cache = EscalarTextura(chao1, janela.height)

    teto1 = pygame.image.load('Sprites/teto1.png').convert()
    texturas.append(teto1)
    teto1Cache = EscalarTextura(teto1, janela.height)

    texturasCache = { 1: parede1Cache, 2:chao1Cache, 3:teto1Cache }

def EscalarTextura(textura, janelaAltura):
    cache = []
    texturaLargura = textura.get_width()
    texturaAltura = textura.get_height()
    
    
    for coluna in range(texturaLargura):

        slice = textura.subsurface(coluna, 0, 1, texturaAltura)
        
        pedacoDaColunaEscalado = {}

        
        for altura in range(1, int(janelaAltura * 2) + 1):
            pedacoDaColunaEscalado[altura] = pygame.transform.scale(slice, (1, altura))
            
        cache.append(pedacoDaColunaEscalado)
    return cache


def CriarImagens():

    parede1 = Imagem3D("sprites/spriteteste.png", Data.direcao["S"])
    parede2 = Imagem3D("sprites/spriteteste.png", Data.direcao["L"])
    parede3 = Imagem3D("sprites/spriteteste.png", Data.direcao["O"])

    spriteList.append(parede1)
    spriteList.append(parede2)
    spriteList.append(parede3)
    parede1.draw()





def CalcularSprite(sprite, localParede, coordenadaJogador):

    if(localParede == 0):
        pass
    else:

        ratioW = 1
        ratioH = 1
        if(localParede == 1):
                distancia = abs(sprite.coordenadas[0] - coordenadaJogador[0])
                if(distancia >= 5):
                    ratioW = 0
                elif(distancia >= 4):
                    ratioW = 0.2
                elif(distancia >= 3):
                    ratioW = 0.4
                elif(distancia >= 2):
                    ratioW = 0.6
                elif(distancia >= 1):
                    ratioW = 0.8
                elif(distancia <= 0):
                    ratioW = 1

                ratioH = ratioW
                sprite.Transformar(sprite.width * ratioW, sprite.height *  ratioH)

        elif(localParede == 2):
            ratioH = 0.7
            shapeFinal = pygame.Rect(200, 250, sprite.width * 0.3 , 200) 


            sprite.TransformarPerspectiva(shapeFinal, 600, 300)

        elif(localParede == 3):
            ratioH = 0.7
            shapeFinal = pygame.Rect(200, 250, sprite.width * 0.3 , 200) 


            sprite.TransformarPerspectiva(shapeFinal, 300, 600)
                    



    




def UpdateSprites(coordenadaJogador, direcaoJogador):

    for sprite in spriteList:
        
        if(direcaoJogador == sprite.direcao):
            pass
        else:
            localParede = 0
            desenhar = False


            if(direcaoJogador == Data.direcao["N"]):
                if(sprite.direcao == Data.direcao["S"]):
                        if(coordenadaJogador[0] < sprite.coordenadas[0]):
                            sprite.set_position(400, 300)
                            localParede = 1    
                            desenhar = True               
                elif(sprite.direcao == Data.direcao["L"]):
                        if(coordenadaJogador[0] < sprite.coordenadas[0]):
                            sprite.set_position(0, 50)
                            localParede = 2 
                            desenhar = True     
                elif(sprite.direcao == Data.direcao["O"]):
                        if(coordenadaJogador[0] < sprite.coordenadas[0]):
                            sprite.set_position(700, 50)
                            localParede = 3
                            desenhar = True            



            elif(direcaoJogador == Data.direcao["S"]):
                pass    
            elif(direcaoJogador == Data.direcao["L"]):
                if(sprite.direcao == Data.direcao["S"]):
                     if(coordenadaJogador[0] < sprite.coordenadas[0]):
                            localParede = 2    
                            desenhar = True       

            elif(direcaoJogador == Data.direcao["O"]):
                pass
             


        if(desenhar):
            CalcularSprite(sprite, localParede, coordenadaJogador)
            sprite.draw()



def DrawLines(Jogador, janela, paredes):
    #arbitrário
    FOV = janela.width / 4

    pygame.draw.rect(janela.get_screen(), (50, 50, 50), (0, 0, 800, 600 / 2)) # Dark gray ceiling
    # distanciaY = 1 - (Jogador.y + 0.5)
    # distanciaX = 1 - (Jogador.x + 0.5)

    # alturaParede = (1 / distanciaY) * (FOV/ 2)
    # paredeY1 = (janela.height / 2) - (alturaParede / 2)
    # paredeY2 =  (janela.height / 2) + (alturaParede / 2)
    # paredeX = (janela.width / 2) + (distanciaX / distanciaY) * FOV
    # pygame.draw.line(janela.get_screen(), (255, 255, 255), (paredeX, paredeY1), (paredeX, paredeY2) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (paredeX, paredeY2), (400, 300) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (paredeX, paredeY1), (400, 300) )


    # distanciaY = 1 - (Jogador.y + 0.5)
    # distanciaX = 2 - (Jogador.x + 0.5)

    # alturaParede = (1 / distanciaY) * (FOV/ 2)
    # paredeY1 = (janela.height / 2) - (alturaParede / 2)
    # paredeY2 =  (janela.height / 2) + (alturaParede / 2)
    # paredeX = (janela.width / 2) + (distanciaX / distanciaY) * FOV
    # pygame.draw.line(janela.get_screen(), (255, 255, 255), (paredeX, paredeY1), (paredeX, paredeY2) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (paredeX, paredeY2), (400, 300) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (paredeX, paredeY1), (400, 300) )

    for parede in paredes:
        if(Jogador.direcao != parede.direcao):
            CalcularParede(Jogador.x, Jogador.y, janela, CalcularVertices(parede, Jogador.direcao), Jogador.direcao, FOV)


def CalcularVertices(parede, direcaoJogador):
    paredeX1 = paredeX2 = paredeY1 = paredeY2 = 0

    direcaoDireitas = direcaoJogador - parede.direcao

    if(direcaoDireitas != 0):
        if(direcaoDireitas > 0):
            direcaoDireitas -= 4
            
        if(direcaoDireitas == -3):
            paredeX1 = parede.x + 0.5
            paredeY1 = parede.y - 0.5

            paredeX2 = paredeX1
            paredeY2 = parede.y + 0.5
        elif(direcaoDireitas == -2):
            paredeX1 = parede.x - 0.5
            paredeY1 = parede.y + 0.5

            paredeX2 = parede.x + 0.5
            paredeY2 = paredeY1
        elif(direcaoDireitas == -1):
            paredeX1 = parede.x - 0.5
            paredeY1 = parede.y - 0.5

            paredeX2 = paredeX1
            paredeY2 = parede.y + 0.5


    return (paredeX1, paredeX2, paredeY1, paredeY2)
       



def CalcularParede(jogadorX, jogadorY, janela, vertices, jogadorDirecao, FOV):
    #calcular usando o plano 0 causa divisão por 0 em paredes na mesma liha que o player, então isso aqui vai ter que dar
    NEAR_PLANE_DISTANCE = 0.0001
    paredeX1, paredeX2, paredeY1, paredeY2 = vertices
    

    Ponto1distanciaY = paredeY1 - (jogadorY)
    Ponto1distanciaX = paredeX1 - (jogadorX)



    Ponto1alturaParede = (1 / Ponto1distanciaY) * (FOV/ 2)
    Ponto1paredeY1 = (janela.height / 2) - (Ponto1alturaParede / 2)
    Ponto1paredeY2 =  (janela.height / 2) + (Ponto1alturaParede / 2)
    Ponto1paredeX = (janela.width / 2) + (Ponto1distanciaX / Ponto1distanciaY) * FOV
   

    Ponto2distanciaY = paredeY2 - (jogadorY)
    Ponto2distanciaX = paredeX2 - (jogadorX)


    Ponto2alturaParede = (1 / Ponto2distanciaY) * (FOV/ 2)
    Ponto2paredeY1 = (janela.height / 2) - (Ponto2alturaParede / 2)
    Ponto2paredeY2 =  (janela.height / 2) + (Ponto2alturaParede / 2)
    Ponto2paredeX = (janela.width / 2) + (Ponto2distanciaX / Ponto2distanciaY) * FOV
    
    intersection_x = 0
    intersection_y = 0

    isP1Visivel = Ponto1distanciaY >= NEAR_PLANE_DISTANCE
    isP2Visivel = Ponto2distanciaY >= NEAR_PLANE_DISTANCE


    if not isP1Visivel and not isP2Visivel:
        return


    #se o ponto estiver atrás, desenhar parcialmente
    if(not isP1Visivel or not isP2Visivel):

        t = (Ponto1distanciaY - NEAR_PLANE_DISTANCE) / (Ponto1distanciaY - Ponto2distanciaY)        

        intersection_x = paredeX1 + t * (paredeX2 - paredeX1)
        intersection_y = paredeY1 + t * (paredeY2 - paredeY1) 

        Ponto1distanciaY = intersection_y - (jogadorY)
        Ponto1distanciaX = intersection_x - (jogadorX)


        
        Ponto1alturaParede = (1 / Ponto1distanciaY) * (FOV/ 2)
        Ponto1paredeY1 = (janela.height / 2) - (Ponto1alturaParede / 2)
        Ponto1paredeY2 =  (janela.height / 2) + (Ponto1alturaParede / 2)
        Ponto1paredeX = (janela.width / 2) + (Ponto1distanciaX / Ponto1distanciaY) * FOV
        
    
    # pygame.draw.line(janela.get_screen(), (255, 255, 255), (Ponto1paredeX, Ponto1paredeY1), (Ponto1paredeX, Ponto1paredeY2) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (Ponto1paredeX, Ponto1paredeY2), (400, 300) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (Ponto1paredeX, Ponto1paredeY1), (400, 300) )


    # pygame.draw.line(janela.get_screen(), (255, 255, 255), (Ponto2paredeX, Ponto2paredeY1), (Ponto2paredeX, Ponto2paredeY2) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (Ponto2paredeX, Ponto2paredeY2), (400, 300) )
    # pygame.draw.line(janela.get_screen(), (255, 0, 0), (Ponto2paredeX, Ponto2paredeY1), (400, 300) )



    if(abs(Ponto1distanciaX) > Ponto1distanciaY and abs(Ponto2distanciaX) > Ponto2distanciaY):
         return

    coordenadasPoligono = [
        (Ponto1paredeX, Ponto1paredeY2),
        (Ponto2paredeX, Ponto2paredeY2),
        (Ponto2paredeX, Ponto2paredeY1),
        (Ponto1paredeX, Ponto1paredeY1)
    ]


    pygame.draw.polygon(janela.get_screen(), (200, 200, 200), coordenadasPoligono)


