import PPlay
import Data
import HUD
from PPlay.window import *
from PPlay.sprite import *

class MainMenu():
    def __init__(self):
        self.background = HUD.GameImageMelhor('Sprites/HUD/HUDBot.png', 0, 0)

    def DesenharMainMenu(self, janela):
        
        janela.update()
