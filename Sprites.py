import numpy as np
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
import PPlay
import Data
import pygame
import functools

modoParede = { "frente" : 1,
               "esquerda" : 2,
               "direita" : 3

}

texturasDic = { "parede1" : 1,
                "chao1" : 2,
                "teto1" : 3, }

texturas = [None]
spriteTexturas = [None]
geradoresCache = [None]
geradoresCacheSprites = [None]
spriteList = []
texturasCache = {}

contador_do_loading=0
tempo_inicial_pro_loading=time.time()
ja_passou_pelo_loading=False
loading=Sprite(f'Sprites/loading/Loading{contador_do_loading%8}.png')
loading.set_position(320, 180)
chao_w = 0
chao_h = 0
teto_w = 0
teto_h = 0
texturaChao_array = []
texturaTeto_array = []
y_indices_full = 0

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

class FadeSprite():
    def __init__(self, largura, altura):
        self.surface = pygame.Surface((largura, altura))
        self.surface.fill((0, 0, 0))
        self.alpha = 0
        self.fading = False
        self.tempo = 0

    def FadeIn(self, passo):
        self.surface.set_alpha(self.alpha + passo)
        self.alpha = self.surface.get_alpha()
        self.tempo = 0
        print(self.alpha)


    def FadeOut(self, passo):
        self.surface.set_alpha(self.alpha - passo)
        self.alpha = self.surface.get_alpha()
        self.tempo = 0
        print(self.alpha)

    def Cooldown(self, deltatime):
        self.tempo += deltatime

    def FadeRed(self):
        self.surface.fill((237, 68, 69))
        
    def FadeBlack(self):
        self.surface.fill((0, 0, 0))

def Tela_de_Loading(janela):
    global contador_do_loading
    global tempo_inicial_pro_loading
    global loading


    if (time.time()-tempo_inicial_pro_loading>0.5):
        tempo_inicial_pro_loading=time.time()
        contador_do_loading+=1
        loading=Sprite(f'Sprites/Loading{contador_do_loading%8}.png')
        loading.set_position(320, 180)
    
    janela.set_background_color((0, 0, 0))
    loading.draw()
    janela.update()


def CriarGeradorCache(fatias):
    cacheGenerators = []

    for fatia in fatias:
        
        # This function creates *another* function
        def create_scaler_for_slice(slice_to_scale):
            """
            A closure to capture the specific 'slice_to_scale'.
            """
            
            # --- THIS IS THE MAGIC ---
            # We attach the LRU cache to this inner function.
            # It will store up to 512 *different heights* for this *one column*.
            @functools.lru_cache(maxsize=512) 
            def get_scaled_slice(altura):
                """
                Generates and caches a scaled slice.
                """
                # This is the "slow" part, but it only runs
                # if the (altura) isn't in this column's cache.
                return pygame.transform.scale(slice_to_scale, (1, altura))
            
            return get_scaled_slice

        # Add the newly created generator (with its own private cache) to our list
        cacheGenerators.append(create_scaler_for_slice(fatia))

    return cacheGenerators

def CriarGeradorCacheSprite(textura):
    
    @functools.lru_cache(maxsize=700) 
    def get_scaled_sprite(largura, altura):
        return pygame.transform.scale(textura, (largura, altura))
    return get_scaled_sprite


def CarregarTexturas(janela):
    global texturasCache
    global teto_w
    global teto_h
    global chao_w
    global chao_h 
    global floor_buffer
    global texturaChao_array
    global texturaTeto_array
    global y_indices_full

    Tempo_inicial_para_entender_codigo=time.time()
    agora1 = time.time()

    parede1 = pygame.image.load('Sprites/parede1.png').convert()
    texturas.append(parede1)
    #parede1Cache = EscalarTextura(parede1, janela.height, janela)

    parede2 = pygame.image.load('Sprites/parede2.png').convert()
    texturas.append(parede2)


    porta1 = pygame.image.load('Sprites/porta1.png').convert()
    texturas.append(porta1)

    porta2 = pygame.image.load('Sprites/parede1porta.png').convert()
    texturas.append(porta2)

    porta3 = pygame.image.load('Sprites/parede1porta2.png').convert()
    texturas.append(porta3)

    parede3 = pygame.image.load('Sprites/parede1janela.png').convert()
    texturas.append(parede3)

    parede4 = pygame.image.load('Sprites/parede3janela.png').convert()
    texturas.append(parede4)

    parede5 = pygame.image.load('Sprites/parede3.png').convert()
    texturas.append(parede5)

    
    parede6 = pygame.image.load('Sprites/parede3quadro1.png').convert()
    texturas.append(parede6)



    parede7 = pygame.image.load('Sprites/parede3quadro2.png').convert()
    texturas.append(parede7)



    portabanheiro = pygame.image.load('Sprites/portabanheiro.png').convert()
    texturas.append(portabanheiro)

    parede1Elevador = pygame.image.load('Sprites/parede1Elevador.png').convert()
    texturas.append(portabanheiro)

    paredeAlarme = pygame.image.load('Sprites/alarme.png').convert()
    texturas.append(paredeAlarme)

    chao1 = pygame.image.load('Sprites/chao1.png').convert()

    #chao1Cache = EscalarTextura(chao1, janela.height, janela)




    teto1 = pygame.image.load('Sprites/teto1.png').convert()

    #teto1Cache = EscalarTextura(teto1, janela.height, janela)


    chao_w, chao_h = chao1.get_size()
    teto_w, teto_h = teto1.get_size()

    floor_buffer = pygame.Surface(janela.get_screen().get_size())
    

    parede1_fatias = PrepararFatias(parede1)
    geradoresCache.append(CriarGeradorCache(parede1_fatias))

    parede2_fatias = PrepararFatias(parede2)



    geradoresCache.append(CriarGeradorCache(parede2_fatias))

    porta1_fatias = PrepararFatias(porta1)
    geradoresCache.append(CriarGeradorCache(porta1_fatias))



    porta2_fatias = PrepararFatias(porta2)
    geradoresCache.append(CriarGeradorCache(porta2_fatias))



    
    porta3_fatias = PrepararFatias(porta3)
    geradoresCache.append(CriarGeradorCache(porta3_fatias))



    parede3_fatias = PrepararFatias(parede3)
    geradoresCache.append(CriarGeradorCache(parede3_fatias))

    parede4_fatias = PrepararFatias(parede4)
    geradoresCache.append(CriarGeradorCache(parede4_fatias))

    parede5_fatias = PrepararFatias(parede5)
    geradoresCache.append(CriarGeradorCache(parede5_fatias))

    parede6_fatias = PrepararFatias(parede6)
    geradoresCache.append(CriarGeradorCache(parede6_fatias))

    parede7_fatias = PrepararFatias(parede7)
    geradoresCache.append(CriarGeradorCache(parede7_fatias))

    portabanheiro_fatias = PrepararFatias(portabanheiro)
    geradoresCache.append(CriarGeradorCache(portabanheiro_fatias))

    parede1Elevador_fatias = PrepararFatias(parede1Elevador)
    geradoresCache.append(CriarGeradorCache(parede1Elevador_fatias))

    alarme_fatias = PrepararFatias(paredeAlarme)
    geradoresCache.append(CriarGeradorCache(alarme_fatias))

    texturaChao = pygame.image.load('Sprites/chao1.png').convert()
    texturaTeto = pygame.image.load('Sprites/teto1.png').convert()


    texturaChao_array = pygame.surfarray.array3d(texturaChao)
    texturaTeto_array = pygame.surfarray.array3d(texturaTeto)

    chao_w, chao_h = texturaChao.get_size()
    teto_w, teto_h = texturaTeto.get_size()



    cadeira1F = pygame.image.load('Sprites/cadeira1F.png').convert_alpha()
    cadeira1T = pygame.image.load('Sprites/cadeira1T.png').convert_alpha()
    cadeira1L = pygame.image.load('Sprites/cadeira1L.png').convert_alpha()
    cadeira1O = pygame.image.load('Sprites/cadeira1O.png').convert_alpha()

    spriteTexturas.append([cadeira1F, cadeira1T, cadeira1L, cadeira1O])
    geradoresCacheSprites.append([CriarGeradorCacheSprite(cadeira1F), CriarGeradorCacheSprite(cadeira1T),CriarGeradorCacheSprite(cadeira1L), CriarGeradorCacheSprite(cadeira1O)])

    bebedouroF = pygame.image.load('Sprites/bebedouroF.png').convert_alpha()
    bebedouroT = pygame.image.load('Sprites/bebedouroT.png').convert_alpha()
    bebedouroL = pygame.image.load('Sprites/bebedouroL.png').convert_alpha()
    bebedouroO = pygame.image.load('Sprites/bebedouroO.png').convert_alpha()

    spriteTexturas.append([bebedouroF, bebedouroT, bebedouroL, bebedouroO])
    geradoresCacheSprites.append([CriarGeradorCacheSprite(bebedouroF), CriarGeradorCacheSprite(bebedouroT),CriarGeradorCacheSprite(bebedouroL), CriarGeradorCacheSprite(bebedouroO)])

    piabanheiroF = pygame.image.load('Sprites/banheiropiaF.png').convert_alpha()
    piabanheiroL = pygame.image.load('Sprites/banheiropiaL.png').convert_alpha()
    piabanheiroO = pygame.image.load('Sprites/banheiropiaO.png').convert_alpha()

    spriteTexturas.append([piabanheiroF, piabanheiroF, piabanheiroL, piabanheiroO])
    geradorSame = CriarGeradorCacheSprite(piabanheiroF)
    geradoresCacheSprites.append([geradorSame, geradorSame,CriarGeradorCacheSprite(piabanheiroL), CriarGeradorCacheSprite(piabanheiroO)])

    lataLixo = pygame.image.load('Sprites/lataLixo.png').convert_alpha()

    spriteTexturas.append([lataLixo, lataLixo, lataLixo, lataLixo])
    geradorSame = CriarGeradorCacheSprite(lataLixo)
    geradoresCacheSprites.append([geradorSame, geradorSame,geradorSame, geradorSame])


    cadeirasMesaF = pygame.image.load('Sprites/cadeirasmesaF.png').convert_alpha()
    cadeirasMesaT = pygame.image.load('Sprites/cadeirasmesaT.png').convert_alpha()
    cadeirasMesaL = pygame.image.load('Sprites/cadeirasmesaL.png').convert_alpha()

    spriteTexturas.append([cadeirasMesaF, cadeirasMesaF, cadeirasMesaL, cadeirasMesaL])
    geradorSameL = CriarGeradorCacheSprite(cadeirasMesaL)

    geradoresCacheSprites.append([CriarGeradorCacheSprite(cadeirasMesaF), CriarGeradorCacheSprite(cadeirasMesaT), geradorSameL, geradorSameL])


    intersec = pygame.image.load('Sprites/intersec.png').convert_alpha()


    spriteTexturas.append([intersec, intersec, intersec, intersec])
    geradorSame = CriarGeradorCacheSprite(intersec)
    geradoresCacheSprites.append([geradorSame, geradorSame, geradorSame, geradorSame])

    professor = pygame.image.load('Sprites/NPCs/professor.png').convert_alpha()


    spriteTexturas.append([professor, professor, professor, professor])
    geradorSame = CriarGeradorCacheSprite(professor)

    geradoresCacheSprites.append([geradorSame, geradorSame, geradorSame, geradorSame])

    almo = pygame.image.load('Sprites/almoxarifado.png').convert_alpha()
    spriteTexturas.append([almo, almo, almo, almo])
    geradorSame = CriarGeradorCacheSprite(almo)

    geradoresCacheSprites.append([geradorSame, geradorSame, geradorSame, geradorSame])




    agora2 = time.time() - agora1 
    print("Demorou " + str(agora2))

    


    #texturasCache = { 1: parede1Cache, 2:chao1Cache, 3:teto1Cache }

def PrepararFatias(textura):

    fatias = []
    textura_largura = textura.get_width()
    textura_altura = textura.get_height()

    for coluna in range(textura_largura):
        
        fatia = textura.subsurface(coluna, 0, 1, textura_altura).copy()
        fatias.append(fatia)
        
    return fatias


def EscalarTextura(textura, janelaAltura, janela):
    cache = []
    texturaLargura = textura.get_width()
    texturaAltura = textura.get_height()
    
    
    for coluna in range(texturaLargura):
        

        slice = textura.subsurface(coluna, 0, 1, texturaAltura)
        
        pedacoDaColunaEscalado = {}
        
        if(coluna % 3 == 0):
            Tela_de_Loading(janela)
    
        for altura in range(1, int(janelaAltura) + 1):

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

def get_lista_botoes_menu():
    
    Lista=[]
    
    Lista.append(Sprite('Sprites/botoes/novo_jogo.png'))
    Lista.append(Sprite('Sprites/botoes/continuar.png'))
    Lista.append(Sprite('Sprites/botoes/opcoes.png'))
    Lista.append(Sprite('Sprites/botoes/sair.png'))

    for i in range(4):
        Lista[i].set_position(480, 90+i*135)

    Lista.append(Sprite('Sprites/botoes/menos.png'))
    Lista.append(Sprite(f'Sprites/botoes/mais.png'))
    Lista.append(Sprite('Sprites/botoes/voltar.png'))

    Lista[4].set_position(400, 210)
    Lista[5].set_position(720, 210)
    Lista[6].set_position(480, 345)

    return Lista



def get_lista_botoes_submenu():

    Lista=[]

    Lista.append(Sprite('Sprites/botoes/continuar.png'))
    Lista.append(Sprite('Sprites/botoes/opcoes.png'))
    Lista.append(Sprite('Sprites/botoes/controles.png'))
    Lista.append(Sprite('Sprites/botoes/voltar_menu.png'))

    for i in range(4):
        Lista[i].set_position(480, 90+i*135)

    Lista.append(Sprite('Sprites/botoes/menos.png'))
    Lista.append(Sprite('Sprites/botoes/mais.png'))
    Lista.append(Sprite('Sprites/botoes/voltar.png'))

    Lista[4].set_position(400, 210)
    Lista[5].set_position(720, 210)
    Lista[6].set_position(480, 345)

    return Lista

def get_diplay_volume():

    Lista=[]

    Lista.append(Sprite('Sprites/botoes/Display/n0.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n1.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n2.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n3.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n4.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n5.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n6.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n7.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n8.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n9.png'))
    Lista.append(Sprite('Sprites/botoes/Display/n10.png'))

    for i in range(11):
        Lista[i].set_position(560, 250)
    
    Lista.append(Sprite('Sprites/botoes/Display/volume.png'))
    Lista[11].set_position(560, 210)

    return Lista
