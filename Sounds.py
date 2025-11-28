from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
import Sprites
import Data
import Input
import Mapa
import math
import HUD
import Luta
import MainMenu

class musica():
    def __init__(self, lista_musicas):
        self.musica_atual = lista_musicas[0]
        self.lista_musicas = lista_musicas
    def atualizar_musica(self, estado):
        if (estado==Data.EEstado.MAINMENU):
            self.musica_atual=self.lista_musicas[0]
        elif (estado==Data.EEstado.ANDANDO) or (estado==Data.EEstado.DIALOGO):
            self.musica_atual=self.lista_musicas[1]
        else:
            self.musica_atual=self.lista_musicas[2]

def criar_lista_musicas():
    lista=[]

    lista.append(Sound("musicas/menu.ogg"))
    lista.append(Sound("musicas/andando.ogg"))
    lista.append(Sound("musicas/luta.ogg"))

    return lista