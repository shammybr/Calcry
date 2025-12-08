import PPlay
import Data
import HUD
from PPlay.window import *
from PPlay.sprite import *

class MainMenu():
    def __init__(self):
        self.background = HUD.GameImageMelhor('Sprites/MainMenu.png', 0, 0)
        self.background.Transformar(1280, 720)

    def DesenharMainMenu(self, janela, lista):
        self.background.draw()
        for i in range(4):
            lista[i].draw()
        janela.update()

    def Desenharopcoes(self, janela, lista1, lista2, volume):
        self.background.draw()
        for i1 in range(4, 7):
            lista1[i1].draw()
        lista2[volume//10].draw()
        lista2[11].draw()
        janela.update()

class SubMenu():
    def __init__(self):
        self.background = HUD.GameImageMelhor('Sprites/MainMenu.png', 0, 0)
        self.background.Transformar(1280, 720)
        
    def DesenharSubMenu(self, janela, lista):
        self.background.draw()
        for i in range(4):
            lista[i].draw()
        janela.update()

    def Desenharopcoes(self, janela, lista1, lista2, volume):
        self.background.draw()
        for i1 in range(4, 7):
            lista1[i1].draw()
        lista2[volume//10].draw()
        lista2[11].draw()
        janela.update()
    
    def DesenharControles(self, janela, lista):
        self.background.draw()
        lista[6].draw()
        lista[7].draw()
        janela.update()

