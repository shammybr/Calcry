import math
import pygame
import HUD
import Data
from PPlay.window import *
from PPlay.gameimage import *
from enum import Enum
import random

class Luta():
    def __init__(self):
        self.estadoLuta = 0
        self.estadoAnimacao = 0
        self.velocidadeAnimacao = 700
        self.tempoAnimacao = 1
        self.tempoAnimacaoBotoes = 0.3
        self.habilidadeSelecionada = 0
        self.tempoPassado = 0
        self.botaoAntigo = 0

        self.tempoAnimacaoDano = 0.4
        self.posicaoOriginalDano = (0, 0)

        self.ordemTurno = []
        self.iTurno = 0
        self.ultimoTurno = 0

        self.mensagem = []
        self.esperandoInput = False

    class EEstadoLuta(Enum):
        ANIMACAO = 1
        LUTANDO = 2
        ESCOLHENDOALVO = 3
        PROCESSANDOTURNO = 4
        FIM = 5
        RESULTADO = 6
        ESCOLHENDOHABILIDADE = 7


    class LutaHUD():
        def __init__(self):
            self.background = HUD.GameImageMelhor('Sprites/Luta/LutaBG.png', 0, 0)
            self.bAtacar = HUD.GameImageMelhor('Sprites/Luta/BAtacarHL.png', 0, 0)
            self.bHabilidade = HUD.GameImageMelhor('Sprites/Luta/BHabilidade.png', 0, 0)
            self.bItem = HUD.GameImageMelhor('Sprites/Luta/BItem.png', 0, 0)
            self.bFugir = HUD.GameImageMelhor('Sprites/Luta/BFugir.png', 0, 0)

            self.bAtacarN = 'Sprites/Luta/BAtacar.png'
            self.bItemN = 'Sprites/Luta/BItem.png'
            self.bFugirN = 'Sprites/Luta/BFugir.png'    
            self.bHabilidadeN = 'Sprites/Luta/BHabilidade.png'

            self.bAtacarSelecionado = 'Sprites/Luta/BAtacarHL.png'
            self.bItemSelecionado = 'Sprites/Luta/BItemHL.png'
            self.bFugirSelecionado = 'Sprites/Luta/BFugirHL.png'    
            self.bHabilidadeSelecionado = 'Sprites/Luta/BHabilidadeHL.png'


            self.itemMenuBackground = HUD.GameImageMelhor('Sprites/Luta/itemMenu.png', 0, 0)
            self.habilidadeMenuBackground = HUD.GameImageMelhor('Sprites/Luta/itemMenu.png', 0, 0)
            self.itemSelecionado = HUD.GameImageMelhor('Sprites/Luta/itemMenuSelect.png', 0, 0)
            self.itemSelecionadoAparecendo = True
            
            self.logBG = HUD.GameImageMelhor('Sprites/Luta/logBG.png', 0, 0)

            self.setaSelecionarAlvo = HUD.GameImageMelhor('Sprites/Luta/selecionarAlvo.png', 0, 0)





    def EntrarLuta(self, janela, deltaTime):
        
        if(self.estadoAnimacao == 0):
            centro = [int(janela.width / 2), int(janela.height / 2)]
            self.tempoPassado += min(0.1, deltaTime)
            progresso = min(1.0, self.tempoPassado / self.tempoAnimacao)



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
                self.estadoAnimacao = 1
                self.tempoPassado = 0
                return 1


        elif(self.estadoAnimacao == 1):
            if(self.tempoPassado == 0):
                self.janelaSurface = janela.get_screen().copy()
                janela.get_screen().fill((0, 0, 0)) # cinza

            self.tempoPassado += min(0.1, deltaTime)
            progresso = min(1.0, self.tempoPassado / self.tempoAnimacao)

            metadeEsquerda = pygame.Rect(0, 0, int(janela.width / 2), janela.height)
            metadeDireita =  pygame.Rect(int(janela.width / 2), 0, int(janela.width / 2), janela.height)

            janela.get_screen().blit(self.janelaSurface, (int(progresso * int(janela.width / 2)) - int(janela.width / 2) , 0), metadeEsquerda)
            janela.get_screen().blit(self.janelaSurface, (int(janela.width) - int(progresso * int(janela.width / 2)) , 0), metadeDireita)

            if(progresso == 1):
                self.estadoAnimacao = -1
                self.estadoLuta = self.EEstadoLuta.PROCESSANDOTURNO

    def GetVelocidade(self, entidade):
        return entidade.velocidade
    
    def CriarTurno(self, inimigos, jogador):
        self.ordemTurno.clear()
        for inimigo in inimigos:
            self.ordemTurno.append(inimigo)

        self.ordemTurno.append(jogador)

        self.ordemTurno.sort(key=self.GetVelocidade, reverse=True)
        self.iTurno = 0


    def PassoTurno(self):
        
        if((self.iTurno) > (len(self.ordemTurno) - 1)):
            self.iTurno = 0
        

        for i , entidade in enumerate(self.ordemTurno[self.iTurno:], start = self.iTurno):
            if(entidade.vida > 0):
                print("Turno de: " + str(entidade.tipo))
                self.iTurno = i
                break


            if(i == (len(self.ordemTurno) - 1)):
                self.iTurno = 0
                break
    
    def ProcessarTurno(self, jogador):
        self.mensagem.clear()

        if(self.ordemTurno[self.iTurno].tipo == Data.tipoEntidade["Jogador"]):
            for buff in jogador.buffs:
                buff.Iturnos += 1

                if(buff.Iturnos >= buff.turnosTotais):
                    self.mensagem.append(buff.nome + " acabou.")
                    jogador.buffs.remove(buff)
                    self.esperandoInput = True             

            if(not self.esperandoInput):
                self.estadoLuta = self.EEstadoLuta.LUTANDO
            else:
                self.iTurno -= 1

        else:
            if(self.ordemTurno[self.iTurno].tipo == Data.tipoEntidade["Limite"]):
                print("Atacando player...")
                self.mensagem.append(self.ordemTurno[self.iTurno].nome + " ataca!")
                danoCausado = self.Atacar(jogador, self.ordemTurno[self.iTurno].dano)
                self.mensagem.append("Causou " + str(danoCausado) + " de dano!")
                self.esperandoInput = True

            elif(self.ordemTurno[self.iTurno].tipo == Data.tipoEntidade["Derivada"]):
                print("Atacando player...")
                self.mensagem.append(self.ordemTurno[self.iTurno].nome + " ataca!")
                danoCausado = self.Atacar(jogador, self.ordemTurno[self.iTurno].dano)
                self.mensagem.append("Causou " + str(danoCausado) + " de dano!")
                self.esperandoInput = True

            elif(self.ordemTurno[self.iTurno].tipo == Data.tipoEntidade["Integral"]):
                print("Atacando player...")
                self.mensagem.append(self.ordemTurno[self.iTurno].nome + " ataca!")
                danoCausado = self.Atacar(jogador, self.ordemTurno[self.iTurno].dano)
                self.mensagem.append("Causou " + str(danoCausado) + " de dano!")
                self.esperandoInput = True
        
        self.iTurno += 1


    def CriarLutaHUD(self,janela):
        lutaHUD = self.LutaHUD()
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

        lutaHUD.logBG.Transformar(835 * (janela.width/1920) , 136 * (janela.height/1080) )
        lutaHUD.logBG.set_position(janela.width * 0.5 - (lutaHUD.logBG.largura / 2), janela.height * 0.05)

        lutaHUD.itemMenuBackground.Transformar(385 * (janela.width/1920) , 502 * (janela.height/1080) )
        lutaHUD.itemMenuBackground.set_position(janela.width * 0.8, janela.height * 0.52)

        lutaHUD.habilidadeMenuBackground.Transformar(385 * (janela.width/1920) , 502 * (janela.height/1080) )
        lutaHUD.habilidadeMenuBackground.set_position(janela.width * 0.8, janela.height * 0.52)

        lutaHUD.itemSelecionado.Transformar(349 * (janela.width/1920) , 42 * (janela.height/1080) )
        lutaHUD.itemSelecionado.set_position(janela.width * 0.85, janela.height * 0.55)
        lutaHUD.itemSelecionado.image.set_alpha(0)
        

        return lutaHUD


    def CalcularInimigos(self, lugar):
        if(lugar == Data.EANDAR.EANDAR1):
            nInimigos = random.randint(1, 100)
            inimigosLuta = []
            
            if(nInimigos < 50):
                nInimigos = 1
            elif(nInimigos < 80):
                nInimigos = 2
            elif(nInimigos < 90):
                nInimigos = 3
            else:
                nInimigos = 4

            nInimigos = 4

            for i in range(0, nInimigos):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                lInimigos = [value for value in Data.tipoEntidade.values() if value != 99]

                tipoInimigo = random.choice(list(lInimigos))


                if(tipoInimigo == Data.tipoEntidade["Limite"]):
                    nlimite = 0
                    for i in range(0, len(inimigosLuta)):
                        if(inimigosLuta[i].tipo == Data.tipoEntidade["Limite"]):
                            nlimite += 1

                    inimigo = Data.ILimite("Limite " + chr(65 + nlimite))
                    print("Foi")

                elif(tipoInimigo == Data.tipoEntidade["Derivada"]):
                    nderivada = 0
                    for i in range(0, len(inimigosLuta)):
                        if(inimigosLuta[i].tipo == Data.tipoEntidade["Derivada"]):
                            nderivada += 1

                    inimigo = Data.IDerivada("Derivada " + chr(65 + nderivada))
                    print("Foi")


                elif(tipoInimigo == Data.tipoEntidade["Integral"]):
                    nintegral = 0
                    for i in range(0, len(inimigosLuta)):
                        if(inimigosLuta[i].tipo == Data.tipoEntidade["Integral"]):
                            nintegral += 1

                    inimigo = Data.IIntegral("Integral " + chr(65 + nintegral))
                    print("Foi")


                inimigosLuta.append(inimigo)

            return inimigosLuta
        
    def ResetarBotoes(self, lutaHUD, botaoSelecionadoLuta, posicoesBotoesLuta):

        lutaHUD.bItem.set_position(posicoesBotoesLuta[(1) % 4][0], posicoesBotoesLuta[(1) % 4][1])
        lutaHUD.bFugir.set_position(posicoesBotoesLuta[(1 + 1) % 4][0], posicoesBotoesLuta[(1 + 1) % 4][1] )
        lutaHUD.bHabilidade.set_position(posicoesBotoesLuta[(1 + 2) % 4][0],posicoesBotoesLuta[(1 + 2) % 4][1] )
        lutaHUD.bAtacar.set_position(posicoesBotoesLuta[(1 + 3) % 4][0], posicoesBotoesLuta[(1 + 3) % 4][1])
        


        lutaHUD.bAtacar.MudarImagem(lutaHUD.bAtacarSelecionado)
        lutaHUD.bHabilidade.MudarImagem(lutaHUD.bHabilidadeN)
        lutaHUD.bItem.MudarImagem(lutaHUD.bItemN)
        lutaHUD.bFugir.MudarImagem(lutaHUD.bFugirN)

        lutaHUD.bItem.image.set_alpha(max(0, 255 - abs(lutaHUD.bItem.y - posicoesBotoesLuta[0][1])))
        lutaHUD.bAtacar.image.set_alpha(max(0, 255 - abs(lutaHUD.bAtacar.y - posicoesBotoesLuta[0][1])))
        lutaHUD.bHabilidade.image.set_alpha(max(0, 255 - abs(lutaHUD.bHabilidade.y - posicoesBotoesLuta[0][1])))
        lutaHUD.bFugir.image.set_alpha(max(0, 255 - abs(lutaHUD.bFugir.y - posicoesBotoesLuta[0][1])))


            



    def AnimarTrocaBotoes(self, lutaHUD, botaoAntigo, botaoSelecionadoLuta):

        lutaHUD.bAtacar.MudarImagem(lutaHUD.bAtacarN)
        lutaHUD.bHabilidade.MudarImagem(lutaHUD.bHabilidadeN)
        lutaHUD.bItem.MudarImagem(lutaHUD.bItemN)
        lutaHUD.bFugir.MudarImagem(lutaHUD.bFugirN)

        if(botaoSelecionadoLuta.value == 1):
            lutaHUD.bItem.MudarImagem(lutaHUD.bItemSelecionado)
        elif(botaoSelecionadoLuta.value == 2):
            lutaHUD.bAtacar.MudarImagem(lutaHUD.bAtacarSelecionado)   
        elif(botaoSelecionadoLuta.value == 3):
            lutaHUD.bHabilidade.MudarImagem(lutaHUD.bHabilidadeSelecionado)   
        elif(botaoSelecionadoLuta.value == 4):
            lutaHUD.bFugir.MudarImagem(lutaHUD.bFugirSelecionado)
            

        self.botaoAntigo = botaoAntigo
        self.tempoPassado = 0
        self.estadoAnimacao = 2
        self.estadoLuta = self.EEstadoLuta.ANIMACAO

    def AnimarTrocaBotoesLoop(self, janela, deltaTime, lutaHUD, botaoSelecionadoLuta, posicoesBotoesLuta):


        progresso = min(1.0, self.tempoPassado / self.tempoAnimacaoBotoes)

        bItemAntigoX = posicoesBotoesLuta[(self.botaoAntigo.value + 3) % 4][0]
        bAtacarAntigoX = posicoesBotoesLuta[(self.botaoAntigo.value + 2) % 4][0]
        bHabilidadeAntigoX = posicoesBotoesLuta[(self.botaoAntigo.value + 1) % 4][0]
        bFugirAntigoX = posicoesBotoesLuta[(self.botaoAntigo.value) % 4][0]

        

        bItemNovoX = posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][0]
        bAtacarNovoX = posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][0]
        bHabilidadeNovoX = posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][0]
        bFugirNovoX = posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][0]
       
     

        bItemAntigoY = posicoesBotoesLuta[(self.botaoAntigo.value + 3) % 4][1]
        bAtacarAntigoY = posicoesBotoesLuta[(self.botaoAntigo.value + 2) % 4][1]
        bHabilidadeAntigoY = posicoesBotoesLuta[(self.botaoAntigo.value + 1) % 4][1]
        bFugirAntigoY = posicoesBotoesLuta[(self.botaoAntigo.value) % 4][1]
        
        

        bItemNovoY = posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][1]
        bAtacarNovoY = posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][1]
        bHabilidadeNovoY = posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][1]
        bFugirNovoY = posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][1]
        
        

        if(progresso < 1):
            lutaHUD.bItem.set_position(bItemAntigoX + ((bItemNovoX - bItemAntigoX) * progresso), bItemAntigoY + ((bItemNovoY - bItemAntigoY) * progresso))
            lutaHUD.bAtacar.set_position(bAtacarAntigoX + ((bAtacarNovoX - bAtacarAntigoX) * progresso), bAtacarAntigoY + ((bAtacarNovoY - bAtacarAntigoY) * progresso))
            lutaHUD.bHabilidade.set_position(bHabilidadeAntigoX + ((bHabilidadeNovoX - bHabilidadeAntigoX) * progresso),bHabilidadeAntigoY + ((bHabilidadeNovoY - bHabilidadeAntigoY) * progresso) )
            lutaHUD.bFugir.set_position(bFugirAntigoX + ((bFugirNovoX - bFugirAntigoX) * progresso), bFugirAntigoY + ((bFugirNovoY - bFugirAntigoY) * progresso) )
           



            
            self.tempoPassado += deltaTime
        
        
        else:
            lutaHUD.bItem.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 3) % 4][1])
            lutaHUD.bAtacar.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value + 2) % 4][1])
            lutaHUD.bHabilidade.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][0],posicoesBotoesLuta[(botaoSelecionadoLuta.value + 1) % 4][1] )
            lutaHUD.bFugir.set_position(posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][0], posicoesBotoesLuta[(botaoSelecionadoLuta.value) % 4][1] )


            self.estadoLuta = self.EEstadoLuta.LUTANDO

        lutaHUD.bItem.image.set_alpha(max(0, 255 - abs(lutaHUD.bItem.y - posicoesBotoesLuta[0][1])))
        lutaHUD.bAtacar.image.set_alpha(max(0, 255 - abs(lutaHUD.bAtacar.y - posicoesBotoesLuta[0][1])))
        lutaHUD.bHabilidade.image.set_alpha(max(0, 255 - abs(lutaHUD.bHabilidade.y - posicoesBotoesLuta[0][1])))
        lutaHUD.bFugir.image.set_alpha(max(0, 255 - abs(lutaHUD.bFugir.y - posicoesBotoesLuta[0][1])))



    def Atacar(self, alvoLuta, dano):
        return alvoLuta.TomarDano(dano)


    def AnimarDano(self, posicaoOriginalDanoX, posicaoOriginalDanoY):
        self.posicaoOriginalDano = (posicaoOriginalDanoX, posicaoOriginalDanoY)
        self.estadoLuta = self.EEstadoLuta.ANIMACAO
        self.estadoAnimacao = 3
        self.tempoPassado = 0

    def AnimarDanoLoop(self, janela, alvoluta, deltaTime):

        progresso = min(1.0, self.tempoPassado / self.tempoAnimacaoDano)

        if(progresso < 1):
            alvoluta.sprite.set_position(self.posicaoOriginalDano[0] + ((janela.width * 0.02) * math.sin(progresso * 6 * math.pi)), alvoluta.sprite.y)
            alvoluta.sprite.draw()
            self.tempoPassado += deltaTime

        else:
            alvoluta.sprite.set_position(self.posicaoOriginalDano[0], self.posicaoOriginalDano[1])
            self.esperandoInput = True

    def AcabarLuta(self):
        self.estadoLuta = self.EEstadoLuta.ANIMACAO
        self.estadoAnimacao = 99
        self.tempoPassado = 0
    
    def SairLutaLoop(self, janela, deltaTime):

        if(self.estadoAnimacao == 99):
            centro = [int(janela.width / 2), int(janela.height / 2)]
            self.tempoPassado += min(0.1, deltaTime)
            progresso = min(1.0, self.tempoPassado / self.tempoAnimacao)



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
                self.estadoAnimacao = 100
                self.tempoPassado = 0
                return 1


        elif(self.estadoAnimacao == 100):
            if(self.tempoPassado == 0):
                self.janelaSurface = janela.get_screen().copy()
                janela.get_screen().fill((0, 0, 0)) # cinza

            self.tempoPassado += min(0.1, deltaTime)
            progresso = min(1.0, self.tempoPassado / self.tempoAnimacao)

            metadeEsquerda = pygame.Rect(0, 0, int(janela.width / 2), janela.height)
            metadeDireita =  pygame.Rect(int(janela.width / 2), 0, int(janela.width / 2), janela.height)

            janela.get_screen().blit(self.janelaSurface, (int(progresso * int(janela.width / 2)) - int(janela.width / 2) , 0), metadeEsquerda)
            janela.get_screen().blit(self.janelaSurface, (int(janela.width) - int(progresso * int(janela.width / 2)) , 0), metadeDireita)

            if(progresso == 1):
                self.tempoPassado = 0
                self.estadoAnimacao = -1
                self.estadoLuta = self.EEstadoLuta.FIM

    def TentarFugir(self, inimigos):
        nInimigos = len(inimigos)
        if(random.randint(0, 100) > nInimigos * 10):
            return True
        
        return False


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


