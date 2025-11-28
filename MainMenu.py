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

    def Desenharopcoes(self, janela, lista):
        janela.set_background_color([0, 0, 0])
        for i1 in range(4, 7):
            lista[i1].draw()
        janela.update()