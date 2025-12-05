import PPlay
import Data
import HUD
from PPlay.window import *
from PPlay.sprite import *

class MainMenu():
    def __init__(self):
        self.background = HUD.GameImageMelhor('Sprites/HUD/HUDBot.png', 0, 0)

    def DesenharMainMenu(self, janela, lista):
        janela.set_background_color([0, 0, 0])
        for i in range(4):
            lista[i].draw()
        janela.update()

#Alterações 5/12 - Inicio

    def Desenharopcoes(self, janela, lista1, lista2, volume):
        janela.set_background_color([0, 0, 0])
        for i1 in range(4, 7):
            lista1[i1].draw()
        lista2[volume//10].draw()
        lista2[11].draw()
        janela.update()

class SubMenu():
    def __init__(self):
        self.background = HUD.GameImageMelhor('Sprites/HUD/HUDBot.png', 0, 0)
    
    def DesenharSubMenu(self, janela, lista):
        janela.set_background_color([0, 0, 0])
        for i in range(4):
            lista[i].draw()
        janela.update()

    def Desenharopcoes(self, janela, lista1, lista2, volume):
        janela.set_background_color([0, 0, 0])
        for i1 in range(4, 7):
            lista1[i1].draw()
        lista2[volume//10].draw()
        lista2[11].draw()
        janela.update()
    
    def DesenharControles(self, janela, lista):
        janela.set_background_color([0, 0, 0])
        lista[6].draw()
        janela.update()

#Alterações 5/12 - Fim
