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
        self.musica_atual.stop()
        if (estado==Data.EEstado.MAINMENU):
            self.musica_atual=self.lista_musicas[0]
        elif (estado==Data.EEstado.ANDANDO) or (estado==Data.EEstado.DIALOGO):
            self.musica_atual=self.lista_musicas[1]
        else:
            self.musica_atual=self.lista_musicas[2]
        self.musica_atual.play()
    
    def atualizar_musica_mais_facil(self, estado):
        if (estado==Data.EEstado.MAINMENU):
            if (self.musica_atual!=self.lista_musicas[0]):
                volume=self.musica_atual.volume
                self.musica_atual.stop()
                self.musica_atual=self.lista_musicas[0]
                self.musica_atual.set_volume(volume)
                self.musica_atual.play()
        elif (estado==Data.EEstado.LUTA):
            if (self.musica_atual!=self.lista_musicas[2]):
                volume=self.musica_atual.volume
                self.musica_atual.stop()
                self.musica_atual=self.lista_musicas[2]
                self.musica_atual.set_volume(volume)
                self.musica_atual.play()
        else:
            if (self.musica_atual!=self.lista_musicas[1]):
                volume=self.musica_atual.volume
                self.musica_atual.stop()
                self.musica_atual=self.lista_musicas[1]
                self.musica_atual.set_volume(volume)
                self.musica_atual.play()

    
def criar_lista_musicas():
    lista=[]

    lista.append(Sound("Soms/Musicas/menu.ogg"))
    lista.append(Sound("Soms/Musicas/andando.ogg"))
    lista.append(Sound("Soms/Musicas/luta.ogg"))
    for i in range(3):
        lista[i].set_repeat(True)
    return lista