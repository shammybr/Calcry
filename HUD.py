from PPlay.sprite import *
from PPlay.gameimage import *
import PPlay
import Data
import pygame


class GameImageMelhor(PPlay.gameimage.GameImage):
    def __init__(self,imagem, x, y):
        super().__init__(imagem)

        self.imagemOriginal = self.image
        self.rect = self.image.get_rect()
        self.coordenadas = (x,y)
        self.set_position(x, y)
        self.largura = self.rect.width
        self.altura = self.rect.height

    def Transformar(self, largura, altura):

        centroOriginal = self.rect.center
        imagemCopia = pygame.transform.scale(self.imagemOriginal, (largura, altura))
        self.rect = imagemCopia.get_rect()
        self.rect.center = centroOriginal
        self.image = imagemCopia
        self.largura = self.rect.width
        self.altura = self.rect.height
    
    def MudarImagem(self, novaImagem):

        imagemOG = pygame.image.load(novaImagem).convert_alpha()
        self.image = pygame.transform.scale(imagemOG, (self.largura, self.altura))
        self.rect = self.image.get_rect()
        self.imagemOriginal = self.image

        




class ImagensHUD():
    def __init__(self):
        self.background = GameImageMelhor('Sprites/HUD/HUDBot.png', 0, 0)
        self.barraHPBackground = GameImageMelhor('Sprites/HUD/BarraVidaVazia.png', 0, 0)
        self.barraHP = GameImageMelhor('Sprites/HUD/BarraVida.png', 0, 0)
        self.barraEnergiaBackground = GameImageMelhor('Sprites/HUD/BarraVidaVazia.png', 0, 0)
        self.barraEnergia = GameImageMelhor('Sprites/HUD/BarraEnergia.png', 0, 0)

def CriarHUD(janela):
    jogadorHUD = ImagensHUD()
    
    jogadorHUD.background.Transformar(janela.width, janela.height* 0.3)
    jogadorHUD.background.set_position(0, janela.height - (janela.height* 0.3))

    jogadorHUD.barraHPBackground.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogadorHUD.barraHPBackground.set_position(janela.width * 0.18, janela.height * 0.925)

    jogadorHUD.barraHP.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogadorHUD.barraHP.set_position(janela.width * 0.18, janela.height * 0.925)


    jogadorHUD.barraEnergiaBackground.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogadorHUD.barraEnergiaBackground.set_position(janela.width * 0.42, janela.height * 0.925)

    jogadorHUD.barraEnergia.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogadorHUD.barraEnergia.set_position(janela.width * 0.42, janela.height * 0.925)


    return jogadorHUD