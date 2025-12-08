import Data
import math
import pygame
import Sprites
import copy
import numpy as np

class MapaDungeon():
    def __init__(self, x, y):
        self.altura = x
        self.largura = y
        self.paredes = []

    def InserirParede(self, x, y, direcao):
        self.altura = x
        self.paredes.append([x,y,direcao])
    def GetParedes(self):
        return self.paredes
    
class Parede():
    def __init__(self, norte, sul, leste, oeste, textura, offsetX = 0, offsetY = 0, wAltura=1.0, wLargura=1.0):
        self.norte = norte
        self.sul = sul
        self.leste = leste
        self.oeste = oeste
        self.textura = textura
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.wAltura = wAltura
        self.wLargura = wLargura 

    def __eq__(self, other):
        if not isinstance(other, Parede):
            return False
            
        return (self.norte == other.norte and
                self.sul == other.sul and
                self.leste == other.leste and
                self.oeste == other.oeste)

mapaAtual = [[0]]
mapaObjetosAtual = [[0]]
mapaTexturasAtual = [[0]]
mapaEventosAtual = [[0]]
mapaInteracoesAtual = [[0]]
game_mapInvertido = [[0]]

texturaTeto = 0
texturaChao = 0


def GerarMapa(mapaID, jogo):
    global mapaAtual
    global texturaTeto
    global texturaChao
    global mapaObjetosAtual
    global mapaTexturasAtual
    global game_mapInvertido
    global mapaEventosAtual
    global mapaInteracoesAtual
    
    T = Parede(1, 0, 0, 0, 1)
    _ = Parede(0, 1, 0, 0, 1)
    d = Parede(0, 0, 1, 0, 1)
    b = Parede(0, 0, 0, 1, 1)
    ר = Parede(1, 0, 1, 0, 1)
    J = Parede(0, 1, 1, 0, 1)
    Г = Parede(1, 0, 0, 1, 1)
    L = Parede(0, 1, 0, 1, 1)
    O = Parede(0, 0, 0, 0, 1)

    T2 = Parede(1, 0, 0, 0, 2)
    
    texturaTeto = Sprites.texturas[Sprites.texturasDic["teto1"]]
    texturaChao = Sprites.texturas[Sprites.texturasDic["chao1"]]


    #game_map = [
    #[n, n, n, n, n],
    #[l, O, O, O, o],
    #[l, O, O, O, o],
    #[l, O, o, o, o],
    #[l, O, o, o, o],
    #[s, s, s, s, s]
    #]

    pd = Parede(0, 0, 1, 0, 3)
    pT = Parede(1, 0, 0, 0, 3)
    pT2 = Parede(1, 0, 0, 0, 4)
    pT3 = Parede(1, 0, 0, 0, 5)
    pT4 = Parede(0, 0, 1, 0, 11)

    c = Parede(0, 0, 0, 1, 100, 0, 0, 0.6, 1)
    c2 = Parede(0, 0, 1, 0, 100, 0, 0, 0.6, 1)
    bb = Parede(0, 1, 0, 0, 101, 0, -0.4, 0.5, 1)
    pb = Parede(0, 0, 0, 1, 102, 0.4, 0, 1, 1)
    l = Parede(0, 1, 0, 0, 103, 0, -0.4, 0.5, 1)
    l2 = Parede(0, 1, 0, 0, 103, 0 , 0.4, 0.5, 1)
    cm = Parede(0, 0, 0, 1, 104, 0, 0.3, 0.6, 1)
    i =  Parede(1, 0, 0, 0, 105, -0.5, -0.5, 1, 1)
    i2 =  Parede(1, 0, 0, 0, 105, 0.5, 0.5, 1, 1)
    p =  Parede(1, 0, 0, 0, 106, 0, 0, 0.7, 0.7)
    pf =  Parede(1, 0, 0, 0, 106, 0, 0, 0.7, 0.7)
    ac = Parede(1, 0, 0, 0, 107, 0, 0, 0.7, 0.7)

    E = Data.Interacao(0, 0, 0, 0, 0, 0)
    el = Data.Interacao(0, 0, 1, 0, 10, 0)
    bi = Data.Interacao(0, 1, 0, 0, 1, 1)
    h1 = Data.Interacao(1, 1, 1, 1, 3, 3)
    pp = Data.Interacao(0, 1, 0, 0, 2, 2)
    b1 = Data.Interacao(0, 1, 0, 0, 4, 4)
    b2 = Data.Interacao(1, 0, 0, 0, 4, 4)
    b3 = Data.Interacao(0, 0, 0, 1, 4, 4)
    e1 = Data.Interacao(1, 0, 0, 0, 5, 5)
    pc1 = Data.Interacao(0, 0, 0, 1, 6, 6)
    pc2 = Data.Interacao(0, 1, 0, 1, 6, 6)
    al = Data.Interacao(1, 0, 0, 1, 9, 9)
    pl1 = Data.Interacao(0, 1, 0, 1, 12, 12)
    pl2 = Data.Interacao(1, 0, 0, 1, 12, 12)
    pl3 = Data.Interacao(0, 0, 0, 1, 12, 12)
    bq = Data.Interacao(0, 1, 0, 0, 13, 13)
    ch = Data.Interacao(0, 1, 0, 0, 15, 15)

    pf1 =  Data.Interacao(0, 1, 0, 1, 98, 98)
    pf2 =  Data.Interacao(1, 0, 0, 1, 98, 98)
    pf3 =  Data.Interacao(0, 0, 0, 1, 98, 98)

    z1 = Data.Interacao(0, 0, 0, 1, 20, 0)
    z2 = Data.Interacao(0, 0, 0, 1, 20, 1)
    z3 = Data.Interacao(0, 0, 0, 1, 20, 2)
    z4 = Data.Interacao(0, 0, 1, 0, 20, 3)

    z5 = Data.Interacao(0, 0, 0, 1, 21, 0)
    z6 = Data.Interacao(0, 0, 0, 1, 21, 1)
    z7 = Data.Interacao(0, 0, 0, 1, 21, 2)
    z8 = Data.Interacao(0, 0, 0, 1, 21, 3)
    z9 = Data.Interacao(0, 0, 1, 0, 21, 4)


    z10 = Data.Interacao(0, 0, 0, 1, 22, 0)
    z11 = Data.Interacao(0, 0, 0, 1, 22, 1)
    z12 = Data.Interacao(0, 0, 0, 1, 22, 2)
    z13 = Data.Interacao(0, 0, 0, 1, 22, 3)
    z14 = Data.Interacao(0, 0, 1, 0, 22, 4)

    lx1 = Data.Interacao(0, 1, 0, 0, 30, 0)
    lx2 = Data.Interacao(0, 1, 0, 0, 30, 1)
    lx3 = Data.Interacao(0, 1, 0, 0, 30, 2)
    lx4 = Data.Interacao(0, 1, 0, 0, 30, 3)

    if(mapaID == 1):
        mapaObjetosInvertido = [
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O,  O,  O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O,pd, O, O, O, O, O, O, O, O, O, i2, i,  O,  O , O,cm, l,cm, O,cm,bb,  O,cm, O,i2, i, O, O, O, O, O, O, O,pd, O, O, O, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O,pT2,  O,pT3, O, O, O, O, O, O,pT3, O,pT2,O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, p, c, c, O, O,pT, c, c, c,pT, c, c, c, O,  O,  O,  O, ac, O, O, O, O, O, O, ac, O, O, O, O,pT, c, c, c,pT, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O,  O,  O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O,  O,  O,  O, O, O, O, O, O, O,  O, O, O, O, O, p, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O,  O,  O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O,pT3,pT3, l2,pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,pT4,  O,pT4,  O,pb, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,pT4,  O,pT4,  O,pb, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,pT4,  O,pT4,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,pT4,  O,  O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O,  O,  O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]
        ]


        game_map = []

        game_mapInvertido = [
        [d, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, Г, ר, O, Г, T, ר, O, Г, T, ר, T, T, b, Г, b, Г, ר, O, O, O, Г, b, Г, b, Г, ר, O, Г, T, ר, O, Г, T,ר,ר, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, b, b, b, b, d, O, O, O, b, b, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, T, T, T, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, T, b, O, b, O, O, d, b, O, O, d, b, T, T, T, b, O, O, O, O, b],
        [d, T, T, T, b, d, _, _, _, _, b, _, _, _, b, J, T, T, T, T, T, O, O, O, b, b, O, d, d, O, L, _, _, d, b, _, _, d, b, T, T, T, b, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, T, O, O, d, _, J, O, b, T, ר, ר, O, O, O, b, b, O, O, O, O, O, O, O, T, T, O, O, T, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, b, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, T, T, T, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, b]
        ]

        game_mapTexturasInvertido = [
        [ 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7,13, 1, 1, 6, 6, 1, 1, 6, 6, 6, 1, 1, 6, 6, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 2, 2, 0, 0, 0],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [10, 0, 0, 0, 2, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 0, 0, 9,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 2, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 7, 8, 7, 7, 7, 8, 2, 7, 7, 7, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1, 8, 7, 7, 7, 8, 2, 7, 7, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        game_mapEventosInvertido = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,15, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        game_mapInteracoesInvertido = [
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E,al, E, E, E, E, E, lx1, E, E, E,bi, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z4, E, E, E, E, E, E],
        [E,b1, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,ch, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z4, E, E, E, E, E, E],
        [E, E,b3, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z4, E, E, E, E, E, E],
        [E,b2, E, E, E, E,z1, E, E, E,z2, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E,pp, E, E, E,z3, E, E, E, E, E, E,z4, E, E, E, E, E, E],
        [E, E, E, E, E, E,z1, E, E, E,z2, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z3, E,h1, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,e1, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E]
        ]
    
    elif(mapaID == 2):

        if(jogo and jogo.jogador.quests[1] == 99):
            mapaObjetosInvertido = [
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, p, O, O,pd, O, O, O, O, O, O, O, O, O, i2,  i, O, O, O,cm, l,cm, O,cm,bb,  O,cm, O,i2, i, O, O, O, O, O, O, O,pd, O, O, O, O, O, O, O, O, O, O],
            [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O,pT2,O,pT3, O, O, O, O, O, O,pT3, O,pT2,O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, c, c, O, O,pT, c, c, c,pT, c, c, c, O,  O, O, O, ac, O, O, O, O, O, O, ac, O, O, O, O,pT, c, c, c,pT, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O,pT3,pT3,l2,pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  c, c, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, c,  c, c, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  c, c, pT4,O, c, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, c,  c, c, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]
            ]
            
        else:
            mapaObjetosInvertido = [
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, p, O, O,pd, O, O, O, O, O, O, O, O, O, i2,  i, O, O, O,cm, l,cm, O,cm,bb,  O,cm, O,i2, i, O, O, O, O, O, O, O,pd, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, c, c, c, O, c, c, c, O,  O,pT2,O,pT3, O, O, O, O, O, O,pT3, O,pT2,O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, O, O, O, O,pT, c, c, c,pT, c, c, c, O,  O, O, O, ac, O, O, O, O, O, O, ac, O, O, O, O,pT, c, c, c,pT, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O,pT3,pT3,l2,pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  c, c, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, c,  c, c, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  c, c, pT4,O, c, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, c,  c, c, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
            [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]
            ]


        game_map = []

        game_mapInvertido = [
        [d, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, Г, ר, O, Г, T, ר, O, Г, T, ר, T, T, b, Г, b, Г, ר, O, O, O, Г, b, Г, b, Г, ר, O, Г, T, ר, O, Г, T,ר,ר, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, b, b, b, b, d, O, O, O, b, b, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, T, T, T, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, T, b, O, b, O, O, d, b, O, O, d, b, T, T, T, b, O, O, O, O, b],
        [d, T, T, T, b, d, _, _, _, _, b, _, _, _, b, J, T, T, T, T, T, O, O, O, b, b, O, d, d, O, L, _, _, d, b, _, _, d, b, T, T, T, b, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, T, O, O, d, _, J, O, b, T, ר, ר, O, O, O, b, b, O, O, O, O, O, O, O, T, T, O, O, T, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, b, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, T, T, T, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, b]
        ]

        game_mapTexturasInvertido = [
        [ 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7,13, 1, 1, 6, 6, 1, 1, 6, 6, 6, 1, 1, 6, 6, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 2, 2, 0, 0, 0],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [10, 0, 0, 0, 2, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 0, 0, 9,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 2, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 7, 8, 7, 7, 7, 8, 2, 7, 7, 7, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1, 8, 7, 7, 7, 8, 2, 7, 7, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        
        game_mapEventosInvertido = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        game_mapInteracoesInvertido = [
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,pc1, E, E, E, E, E, E, E, E, E, E, E,al, E, E, E, E, E, lx2, E, E, E,bi, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z9, E, E, E, E, E, E],
        [E,pc2, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z9, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z9, E, E, E, E, E, E],
        [E, E,  E, E, E, E,z5, E, E, E,z6, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E,z7, E, E, E,z8, E, E, E, E, E, E,z9, E, E, E, E, E, E],
        [E, E,  E, E, E, E,z5, E, E, E,z6, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z7, E, E, E,z8, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E]
        ]

    elif(mapaID == 3):


        mapaObjetosInvertido = [
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O,pd, O, O, O, O, O, O, O, O, O, i2,  i, O, O, O,cm, l,cm, O,cm,bb,  O,cm, O,i2, i, O, O, O, O, O, O, O,pd, O, O, O, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O,pT2,O,pT3, O, O, O, O, O, O,pT3, O,pT2,O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O,pT, c, c, c,pT, c, c, c, O,  O, O, O, ac, O, O, O, O, O, O, ac, O, O, O, O,pT, c, c, c,pT, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, p, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O,pT3,pT3,l2,pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  O, O, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  O, O, pT4,O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]
        ]



        game_map = []

        game_mapInvertido = [
        [d, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, Г, ר, O, Г, T, ר, O, Г, T, ר, T, T, b, Г, b, Г, ר, O, O, O, Г, b, Г, b, Г, ר, O, Г, T, ר, O, Г, T,ר,ר, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, b, b, b, b, d, O, O, O, b, b, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, T, T, T, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, T, b, O, b, O, O, d, b, O, O, d, b, T, T, T, b, O, O, O, O, b],
        [d, T, T, T, b, d, _, _, _, _, b, _, _, _, b, J, T, T, T, T, T, O, O, O, b, b, O, d, d, O, L, _, _, d, b, _, _, d, b, T, T, T, b, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, T, O, O, d, _, J, O, b, T, ר, ר, O, O, O, b, b, O, O, O, O, O, O, O, T, T, O, O, T, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, b, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, T, T, T, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, b]
        ]

        game_mapTexturasInvertido = [
        [ 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7,13, 1, 1, 6, 6, 1, 1, 6, 6, 6, 1, 1, 6, 6, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 2, 2, 0, 0, 0],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [10, 0, 0, 0, 2, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 0, 0, 9,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 2, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 7, 8, 7, 7, 7, 8, 2, 7, 7, 7, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1, 8, 7, 7, 7, 8, 2, 7, 7, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        
        game_mapEventosInvertido = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,16, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]


        game_mapInteracoesInvertido = [
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, lx3, E, E, E,bq, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,z14, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,z14, E, E, E, E, E, E],
        [E,pl1, E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,z14, E, E, E, E, E, E],
        [E, E,pl3, E, E, E,z10, E, E, E,z11, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E,z12, E, E, E,z13,  E, E, E, E, E, E,z14, E, E, E, E, E, E],
        [E, E,  E, E, E, E,z10, E, E, E,z11, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,z12, E, E, E,z13,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E,e1, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E],
        [E, E,  E, E, E, E,  E, E, E, E,  E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,  E, E, E, E,  E,  E, E, E, E, E, E,  E, E, E, E, E, E, E]
        ]

    elif(mapaID == 4):


        mapaObjetosInvertido = [
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O,pd, O, O, O, O, O, O, O, O, O, i2,  i, O, O, O,cm, l,cm, O,cm,bb,  O,cm, O,i2, i, O, O, O, O, O, O, O,pd, O, O, O, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O,pT2,O,pT3, O, O, O, O, O, O,pT3, O,pT2,O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O,pf, c, c, O, O,pT, c, c, c,pT, c, c, c, O,  O, O, O, ac, O, O, O, O, O, O, ac, O, O, O, O,pT, c, c, c,pT, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, c, c, O, O, O, c, c, c, O, c, c, c, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, c, c, c, O, c, c, c, O,c2,c2, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O,pT3,pT3,l2,pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  O, O, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, pT4,O, pb,O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, pT4,  O, O, pT4,O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,  O, O, O,  O, O, O, O, O, O, O,  O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]
        ]



        game_map = []

        game_mapInvertido = [
        [d, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, Г, ר, O, Г, T, ר, O, Г, T, ר, T, T, b, Г, b, Г, ר, O, O, O, Г, b, Г, b, Г, ר, O, Г, T, ר, O, Г, T,ר,ר, O, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, b, b, b, b, d, O, O, O, b, b, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, O, O, O, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, b, b, O, b, O, O, d, b, O, O, d, b, b, O, O, b, O, O, O, O, b],
        [d, T, T, T, b, d, O, O, O, d, b, O, O, d, b, O, T, T, T, b, d, O, O, O, b, T, b, T, b, O, b, O, O, d, b, O, O, d, b, T, T, T, b, O, O, O, O, b],
        [d, T, T, T, b, d, _, _, _, _, b, _, _, _, b, J, T, T, T, T, T, O, O, O, b, b, O, d, d, O, L, _, _, d, b, _, _, d, b, T, T, T, b, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, T, O, O, d, _, J, O, b, T, ר, ר, O, O, O, b, b, O, O, O, O, O, O, O, T, T, O, O, T, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, d, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, O, d, b, T, T, T, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, O, O, O, O, O, O, O, O, O, O, O, O, d, T, O, O, Г, T, T, T, O, O, O, b, b, O, O, O, O, O, O, O, O, O, O, O, b, O, O, O, O, O, O, O, O, O, b],
        [d, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, b]
        ]

        game_mapTexturasInvertido = [
        [ 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7,13, 1, 1, 6, 6, 1, 1, 6, 6, 6, 1, 1, 6, 6, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 2, 2, 0, 0, 0],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [10, 0, 0, 0, 2, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 8, 2, 2, 2, 8, 2, 2, 2, 2, 2, 0, 0, 9,10, 0, 0, 0, 0, 0],
        [ 9, 0, 0, 0, 2,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1,10, 0, 0, 0,10, 2, 0, 0, 2, 2, 0, 0,10,9, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 2, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 9, 0, 0, 0, 9, 2, 0, 0, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 8, 7, 7, 7, 7, 8, 7, 7, 7, 8, 2, 7, 7, 7, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 1, 1, 1, 1, 8, 7, 7, 7, 8, 2, 7, 7, 2, 2, 7, 7, 7,8, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [ 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        
        game_mapEventosInvertido = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,99, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0,98, 0, 0, 0, 0,99, 0, 0, 0,99, 0, 0, 0, 0,99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,99, 0, 0, 0,99, 0, 0, 0,99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]


        game_mapInteracoesInvertido = [
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,al, E, E, E, lx4, E, E,bi, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E,pf1, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E,pf3, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E,pf2, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E,pp, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,h1, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E,el, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E]
        ]


    game_map = game_mapInvertido[::-1]
    mapaObjetos = mapaObjetosInvertido[::-1]
    mapaTexturas = game_mapTexturasInvertido[::-1]
    mapaEventos = game_mapEventosInvertido[::-1]
    mapaInteracoes = game_mapInteracoesInvertido[::-1]


    mapCopy = []

    for i in range(len(game_map)):
        mapCopy.append([])
        for k in range(len(game_map[i])): 
            novaParede = Parede(0,0,0,0,0)
            novaParede.norte = game_map[i][k].norte
            novaParede.sul = game_map[i][k].sul
            novaParede.leste = game_map[i][k].leste
            novaParede.oeste = game_map[i][k].oeste
            novaParede.textura = mapaTexturas[i][k]

            mapCopy[i].append(novaParede)


    for i in range(len(game_map)):
        for k in range(len(game_map[i])):
            if(game_map[i][k] != 0):
                if(game_map[i][k].leste and k+1 < len(game_map[i])):
                    mapCopy[i][k+1].oeste = 1
                    if mapCopy[i][k + 1].textura == 0:
                        mapCopy[i][k+1].textura = mapCopy[i][k].textura
                if(k+1 < len(game_map[i]) and game_map[i][k+1].oeste):
                    mapCopy[i][k].leste = 1
                    if mapCopy[i][k].textura == 0:
                        mapCopy[i][k].textura = mapCopy[i][k+1].textura
                if(game_map[i][k].norte and i+1 < len(game_map)):
                    mapCopy[i + 1][k].sul = 1
                    if mapCopy[i + 1][k].textura == 0:
                        mapCopy[i + 1][k].textura = mapCopy[i][k].textura
                if(i+1 < len(game_map) and game_map[i + 1][k].sul):
                    mapCopy[i][k].norte = 1
                    if mapCopy[i ][k].textura == 0:
                        mapCopy[i][k].textura = mapCopy[i + 1][k].textura

    mapaAtual = mapCopy

    mapaObjetosCopy = []
    
    for i in range(len(mapaObjetos)):
        mapaObjetosCopy.append([])
        for k in range(len(mapaObjetos[i])): 
            novaParede = Parede(0,0,0,0,0)
            novaParede.norte = mapaObjetos[i][k].norte
            novaParede.sul = mapaObjetos[i][k].sul
            novaParede.leste = mapaObjetos[i][k].leste
            novaParede.oeste = mapaObjetos[i][k].oeste
            novaParede.textura = mapaObjetos[i][k].textura
            novaParede.offsetX = mapaObjetos[i][k].offsetX
            novaParede.offsetY = mapaObjetos[i][k].offsetY
            novaParede.wLargura = mapaObjetos[i][k].wLargura
            novaParede.wAltura = mapaObjetos[i][k].wAltura

            mapaObjetosCopy[i].append(novaParede)

    for i in range(len(mapaObjetos)):
        for k in range(len(mapaObjetos[i])):
            if(mapaObjetos[i][k] != 0):
                if(mapaObjetos[i][k].textura < 100):
                    if(mapaObjetos[i][k].leste and k+1 < len(mapaObjetos[i])):
                        mapaObjetosCopy[i][k+1].oeste = 1
                        mapaObjetosCopy[i][k+1].textura = mapaObjetos[i][k].textura
                    if(k+1 < len(mapaObjetos[i]) and  mapaObjetos[i][k+1].textura < 100 and  mapaObjetos[i][k+1].oeste ):
                        mapaObjetosCopy[i][k].leste = 1
                        mapaObjetosCopy[i][k].textura = mapaObjetos[i][k+1].textura
                    if(mapaObjetos[i][k].norte and i+1 < len(mapaObjetos)):
                        mapaObjetosCopy[i + 1][k].sul = 1
                        mapaObjetosCopy[i + 1][k].textura = mapaObjetos[i][k].textura
                    if(i+1 < len(mapaObjetos) and  mapaObjetos[i + 1][k].textura < 100 and mapaObjetos[i + 1][k].sul):
                        mapaObjetosCopy[i][k].norte = 1
                        mapaObjetosCopy[i][k].textura = mapaObjetos[i + 1][k].textura
                    


    mapaObjetosAtual = mapaObjetosCopy

    
    mapaEventosAtual = mapaEventos
    mapaInteracoesAtual = mapaInteracoes

    return mapaAtual

def GetMinimapaComp(jogador):
    
    mapa=GetMapaAtual()

    minimapa=[]
    for i1 in range (len(mapa)):
        minimapa.append([0]*len(mapa[0]))
    
    pilha=[[int(jogador.x), int(jogador.y)]]
    while pilha != []:
        quad=pilha[0]
        if minimapa[quad[1]][quad[0]]==0:
            minimapa[quad[1]][quad[0]]=1
            if mapa[quad[1]][quad[0]].norte==0:
                pilha.append([quad[0], quad[1]+1])
            if mapa[quad[1]][quad[0]].sul==0:
                pilha.append([quad[0], quad[1]-1])
            if mapa[quad[1]][quad[0]].leste==0:
                pilha.append([quad[0]+1, quad[1]])
            if mapa[quad[1]][quad[0]].oeste==0:
                pilha.append([quad[0]-1, quad[1]])
        del pilha[0]
    
    return minimapa

def GetMapaAtual():

    return mapaAtual

def GetMapaObjetos():

    return mapaObjetosAtual

def GetMapaAtual():

    return mapaAtual

def GetMapaObjetos():

    return mapaObjetosAtual

def GetMapaEventos():

    return mapaEventosAtual

def GetMapaInteracoes():

    return mapaInteracoesAtual

def RenderizarSprites(janela, jogador, zBuffer, mapaObjetos):


    sprites_a_renderizar = []
    

    for tile in tilesVisiveis:
        objeto = mapaObjetos[tile[0]][tile[1]]
        tex_index = objeto.textura
        if tex_index > 99:
            spriteX = tile[1] + 0.5 + objeto.offsetX
            spriteY = tile[0] + 0.5 + objeto.offsetY
            largura = objeto.wLargura
            altura = objeto.wAltura

            #frente = 0, trás = 1, lado = 2
            posicao = 0

            distX = jogador.x - spriteX
            distY = jogador.y - spriteY



            if abs(distX) >= abs(distY):
                if distX > 0:
                    #return "LESTE"    
                    if(objeto.norte):
                        posicao = 3

                    elif(objeto.sul):
                        posicao = 2
                        
                    elif(objeto.leste):
                        posicao = 0
                        
                    elif(objeto.oeste):
                        posicao = 1
                else:
                   # return "OESTE"
                    if(objeto.norte):
                        posicao = 2

                    elif(objeto.sul):
                        posicao = 3
                        
                    elif(objeto.leste):
                        posicao = 1
                        
                    elif(objeto.oeste):
                        posicao = 0
                    
           
            else: # abs(rel_y) >= abs(rel_x)
                if distY > 0:
                    #return "SUL"
                    
                    if(objeto.norte):
                        posicao = 1

                    elif(objeto.sul):
                        posicao = 0
                        
                    elif(objeto.leste):
                        posicao = 3
                        
                    elif(objeto.oeste):
                        posicao = 2

                else:
                   # return "NORTE"
                    if(objeto.norte):
                        posicao = 0

                    elif(objeto.sul):
                        posicao = 1
                        
                    elif(objeto.leste):
                        posicao = 2
                        
                    elif(objeto.oeste):
                        posicao = 3


            distancia_sq = ((jogador.x - spriteX)**2 + (jogador.y - spriteY)**2)
            if(distancia_sq > 0.1):
                sprites_a_renderizar.append((distancia_sq, spriteX, spriteY, tex_index - 99, posicao, largura, altura))

   
    sprites_a_renderizar.sort(key=lambda item: item[0], reverse=True) 


    EPSILON = 0.1 

    for distancia_sq, spriteX, spriteY, tex_index, posicao, largura, altura in sprites_a_renderizar:
        

        relativeX = spriteX - jogador.x
        relativeY = spriteY - jogador.y
        
      
        invDet = 1.0 / (jogador.planeX * jogador.dirY - jogador.dirX * jogador.planeY)


        transformX = invDet * (jogador.dirY * relativeX - jogador.dirX * relativeY)
        transformY = invDet * (-jogador.planeY * relativeX + jogador.planeX * relativeY)
        

        if transformY <= EPSILON:
            continue
            

        spriteScreenX = int((janela.width / 2) * (1 + transformX / transformY))
        


 


        original_texture = Sprites.spriteTexturas[tex_index][posicao]
        TexW, TexH = original_texture.get_size()

        spriteHeight = abs(int((janela.height / transformY) * altura))    
        spriteWidth = int(spriteHeight * (TexW / TexH))
        

        unit_projected_height = abs(int(janela.height / transformY))

        spriteHeight = abs(int(unit_projected_height * altura))


        ground_level_y = janela.height // 2 + (unit_projected_height // 2)


        drawStartY = ground_level_y - spriteHeight

        drawStartX = spriteScreenX - spriteWidth // 2
        drawEndX = drawStartX + spriteWidth



        get_scaled_sprite = Sprites.geradoresCacheSprites[tex_index][posicao]
        scaled_sprite = get_scaled_sprite(spriteWidth, spriteHeight)


        start_loop_x = max(0, drawStartX)
        end_loop_x = min(janela.width, drawEndX)

        final_clip_start = start_loop_x - drawStartX 
        final_clip_end = end_loop_x - drawStartX 


        for stripe_x in range(start_loop_x, end_loop_x):
           
            if transformY < zBuffer[stripe_x]:
                break
            else:
              
                final_clip_start += 1 

        
        if final_clip_start >= final_clip_end:
             continue


        for stripe_x in range(end_loop_x - 1, start_loop_x + final_clip_start - 1, -1):
            
            if transformY < zBuffer[stripe_x]:

                final_clip_end = stripe_x - drawStartX + 1 
                break 
            else:
               
                final_clip_end -= 1


        
        if final_clip_end > final_clip_start:
           
            visible_width = final_clip_end - final_clip_start
            visible_rect = pygame.Rect(final_clip_start, 0, visible_width, spriteHeight)
            
          
            visible_sprite_part = scaled_sprite.subsurface(visible_rect)
            
         
            final_draw_x = drawStartX + final_clip_start 

            janela.get_screen().blit(visible_sprite_part, (final_draw_x, drawStartY))



def RenderizarMapa3D(janela, jogador):
    global tilesVisiveis
    tilesVisiveis = []
    tilesVisiveis.append([int(jogador.y), int(jogador.x)]) 
    game_map = GetMapaAtual()
    mapaObjetos = GetMapaObjetos()
    zBuffer = [float('inf')] * janela.width

    for coluna in range(janela.width):
        #de 0 a 1, onde a coluna está
        porcentagemDaTela = coluna / float(janela.width)

        #transforma o 0 a 1 em -1 a 1
        cameraX = 2 * (porcentagemDaTela) - 1
        

        tamanhoMapaX = len(game_map[0])
        tamanhoMapaY = len(game_map)


        direcaoRaioX = jogador.dirX + jogador.planeX * cameraX
        direcaoRaioY = jogador.dirY + jogador.planeY * cameraX


        #DDA

        if(direcaoRaioX != 0):
            deltaDistanciaX = abs(1 / direcaoRaioX)
        else:
            #se o X for 0, o raio nunca crusa uma linha horizontal
            deltaDistanciaX = float('inf')


        if(direcaoRaioY != 0):
            deltaDistanciaY = abs(1 / direcaoRaioY)
        else:
            #se o Y for 0, o raio nunca crusa uma linha vertical
            deltaDistanciaY = float('inf')

        #direção do passo no eixo X
        passoX = 0

        #distância para a próxima linha do grid (distancias posteriores são normalizadas)
        #apesar do player, nesse projeto, estar sempre em 0.5 em relação ao grid, eu quero
        #implementar uma "animação" de andar até o próximo grid, então essa parte ainda é necessária
        distanciaX = 0
        distanciaY = 0

        jogadorXArredondado = int(jogador.x)
        jogadorYArredondado = int(jogador.y)
        if(direcaoRaioX < 0):
            #esquerda do grid
            passoX = -1
                        #jogador X inteiro - o grid anterior (parte inteira do X ex: 1.5 é 1) = 1.5 - 1 = 0.5
            distanciaX = (jogador.x - jogadorXArredondado) * deltaDistanciaX 
        else:
            #direita do grid
            passoX = 1
                        #parte inteira do X (ex: 1.5 é ) + 1 = próximo grid (2), - a fração (ex 1.5 é 0.5) = 0.5 de distância
            distanciaX = (jogadorXArredondado + 1.0 - jogador.x) * deltaDistanciaX

        if(direcaoRaioY < 0):
            #sul do grid
            passoY = -1
            distanciaY = (jogador.y - jogadorYArredondado) * deltaDistanciaY
        else:
            #norte do grid
            passoY = 1
            distanciaY = (jogadorYArredondado + 1.0 - jogador.y) * deltaDistanciaY

        mapaX = jogadorXArredondado
        mapaY = jogadorYArredondado
        hit = 0

        horizontal = 0

        while(not hit):

            #próximo square mais próximo
            if(distanciaX < distanciaY):
                distanciaX += deltaDistanciaX
                mapaX += passoX
                #parede vertical
                horizontal = 0
                
                if([mapaY, mapaX] not in tilesVisiveis):
                    tilesVisiveis.append([mapaY, mapaX]) 

                if(mapaX < tamanhoMapaX and mapaX >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):
                        if (passoX > 0 and tile.oeste) or (passoX < 0 and tile.leste):
                            hit = tile.textura
                        else:
                            tile = mapaObjetos[mapaY][mapaX]
                            if(tile != 0):
                                if(tile.textura < 99):
                                    if (passoX > 0 and tile.oeste) or (passoX < 0 and tile.leste):
                                        hit = tile.textura
                else:
                    break

            else:
                distanciaY += deltaDistanciaY
                mapaY += passoY
                #parede horizontal
                horizontal = 1

                if([mapaY, mapaX] not in tilesVisiveis):
                    tilesVisiveis.append([mapaY, mapaX]) 

                if(mapaY < tamanhoMapaY and mapaY >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoY > 0 and tile.sul) or (passoY < 0 and tile.norte):
                            hit = tile.textura

                        else:
                            tile = mapaObjetos[mapaY][mapaX]
                            if(tile != 0):
                                if(tile.textura < 99):
                                    if (passoY > 0 and tile.sul) or (passoY < 0 and tile.norte):
                                        hit = tile.textura

                else:
                    break
                #se tem parede, acerta (o mapa sempre tem que ser cercado de paredes)
            #if(game_map[mapaY][mapaX] > 0):
            #    hit = 1



        distanciaPerpendicular = 0

        if(horizontal):
            distanciaPerpendicular = (mapaY - jogador.y + ((1 -passoY) / 2 )) / direcaoRaioY
        else:                                                
                                                        #mágica que, infelizmente, não é de minha autoria
                                                        #se o passo for 1 calcula a distancia correta pra direita
                                                        #se for -1, ajusta para o grid correto no mapa
            distanciaPerpendicular = (mapaX - jogador.x +         ((1 - passoX) / 2) )                          / direcaoRaioX
        
        if(distanciaPerpendicular > 0):
            alturaDaLinha = int(janela.height / distanciaPerpendicular)
        else:
            #se a distância ate a parede for 0, o jogador está dentro da parede
            #então desenha a tela inteira (nunca vai acontecer, mas é bom ilustrar)
            alturaDaLinha = janela.height

        zBuffer[coluna] = distanciaPerpendicular

         # Calcula onde a parede foi acertada
        if horizontal == 0: # vertical 
            wallX = jogador.y + distanciaPerpendicular * direcaoRaioY
        else: #  horizontal 
            wallX = jogador.x + distanciaPerpendicular * direcaoRaioX
        
        # Parte fracional da parede X
        wallX -= math.floor(wallX)
        



        #a visão do player sempre vai estar no meio da tela, então calculamos todas as paredes como sendo metade
        #acima e metade abaixo
        comecoDaLinha = -alturaDaLinha / 2 + janela.height / 2


        finalDaLinha = alturaDaLinha / 2 + janela.height / 2

        if finalDaLinha >= janela.height:
            finalDaLinha = janela.height



        #if(hit):
           # pygame.draw.line(janela.get_screen(), color, (coluna, comecoDaLinha), (coluna, finalDaLinha))

        QUANTIZE_STEP = 2
        snapped_key = (int(alturaDaLinha) // QUANTIZE_STEP) * QUANTIZE_STEP


                # acha a coluna da textura para desenhar (porcentagem de onde está na parede * largura da imagem)
        textura = Sprites.texturas[hit]

        texX = int(wallX * float(textura.get_width()))
        
        try:


            get_slice_from_cache = Sprites.geradoresCache[hit][texX]


            pedacoEscalado = get_slice_from_cache(snapped_key)


            janela.get_screen().blit(pedacoEscalado, (coluna, comecoDaLinha))

        except IndexError:
            print("error1")

            pass
        except ValueError:
            print("error2")

            pass

    RenderizarSprites(janela, jogador, zBuffer, mapaObjetos)


def RenderizarMapa3DLowPoly(janela, janelaAltura, janelaLargura, jogador):

    game_map = GetMapaAtual()



    for coluna in range(janelaLargura):
        #de 0 a 1, onde a coluna está
        porcentagemDaTela = coluna / float(janelaLargura)

        #transforma o 0 a 1 em -1 a 1
        cameraX = 2 * (porcentagemDaTela) - 1
        

        tamanhoMapaX = len(game_map[0])
        tamanhoMapaY = len(game_map)


        direcaoRaioX = jogador.dirX + jogador.planeX * cameraX
        direcaoRaioY = jogador.dirY + jogador.planeY * cameraX


        #DDA

        if(direcaoRaioX != 0):
            deltaDistanciaX = abs(1 / direcaoRaioX)
        else:
            #se o X for 0, o raio nunca crusa uma linha horizontal
            deltaDistanciaX = float('inf')


        if(direcaoRaioY != 0):
            deltaDistanciaY = abs(1 / direcaoRaioY)
        else:
            #se o Y for 0, o raio nunca crusa uma linha vertical
            deltaDistanciaY = float('inf')

        #direção do passo no eixo X
        passoX = 0

        #distância para a próxima linha do grid (distancias posteriores são normalizadas)
        #apesar do player, nesse projeto, estar sempre em 0.5 em relação ao grid, eu quero
        #implementar uma "animação" de andar até o próximo grid, então essa parte ainda é necessária
        distanciaX = 0
        distanciaY = 0

        jogadorXArredondado = int(jogador.x)
        jogadorYArredondado = int(jogador.y)
        if(direcaoRaioX < 0):
            #esquerda do grid
            passoX = -1
                        #jogador X inteiro - o grid anterior (parte inteira do X ex: 1.5 é 1) = 1.5 - 1 = 0.5
            distanciaX = (jogador.x - jogadorXArredondado) * deltaDistanciaX 
        else:
            #direita do grid
            passoX = 1
                        #parte inteira do X (ex: 1.5 é ) + 1 = próximo grid (2), - a fração (ex 1.5 é 0.5) = 0.5 de distância
            distanciaX = (jogadorXArredondado + 1.0 - jogador.x) * deltaDistanciaX

        if(direcaoRaioY < 0):
            #sul do grid
            passoY = -1
            distanciaY = (jogador.y - jogadorYArredondado) * deltaDistanciaY
        else:
            #norte do grid
            passoY = 1
            distanciaY = (jogadorYArredondado + 1.0 - jogador.y) * deltaDistanciaY

        mapaX = jogadorXArredondado
        mapaY = jogadorYArredondado
        hit = 0

        horizontal = 0

        while(not hit):

            #próximo square mais próximo
            if(distanciaX < distanciaY):
                distanciaX += deltaDistanciaX
                mapaX += passoX
                #parede vertical
                horizontal = 0
                

                if(mapaX < tamanhoMapaX and mapaX >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoX > 0 and tile.oeste) or (passoX < 0 and tile.leste):
                            hit = 1
                else:
                    break

            else:
                distanciaY += deltaDistanciaY
                mapaY += passoY
                #parede horizontal
                horizontal = 1


                if(mapaY < tamanhoMapaY and mapaY >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoY > 0 and tile.sul) or (passoY < 0 and tile.norte):
                            hit = 1
                else:
                    break
                #se tem parede, acerta (o mapa sempre tem que ser cercado de paredes)
            #if(game_map[mapaY][mapaX] > 0):
            #    hit = 1



        distanciaPerpendicular = 0

        if(horizontal):
            distanciaPerpendicular = (mapaY - jogador.y + ((1 -passoY) / 2 )) / direcaoRaioY
        else:                                                
                                                        #mágica que, infelizmente, não é de minha autoria
                                                        #se o passo for 1 calcula a distancia correta pra direita
                                                        #se for -1, ajusta para o grid correto no mapa
            distanciaPerpendicular = (mapaX - jogador.x +         ((1 - passoX) / 2) )                          / direcaoRaioX
        
        if(distanciaPerpendicular > 0):
            alturaDaLinha = int(janelaAltura / distanciaPerpendicular)
        else:
            #se a distância ate a parede for 0, o jogador está dentro da parede
            #então desenha a tela inteira (nunca vai acontecer, mas é bom ilustrar)
            alturaDaLinha = janelaAltura



         # Calculate where exactly the wall was hit
        if horizontal == 0: # A vertical wall
            wallX = jogador.y + distanciaPerpendicular * direcaoRaioY
        else: # A horizontal wall
            wallX = jogador.x + distanciaPerpendicular * direcaoRaioX
        
        # Get the fractional part of wallX
        wallX -= math.floor(wallX)
        




        finalDaLinha = alturaDaLinha / 2 + janelaAltura / 2 - 2

        if finalDaLinha >= janelaAltura:
            finalDaLinha = janelaAltura - 1





        texturaTeto = Sprites.texturas[Sprites.texturasDic["teto1"]]
        texturaChao = Sprites.texturas[Sprites.texturasDic["chao1"]]




        if horizontal == 0 and direcaoRaioX > 0:
            # WEST
            floorXWall = mapaX
            floorYWall = mapaY + wallX
        elif horizontal == 0 and direcaoRaioX < 0:
            # EAST
            floorXWall = mapaX + 1.0
            floorYWall = mapaY + wallX
        elif horizontal == 1 and direcaoRaioY > 0:
            # nORTH
            floorXWall = mapaX + wallX
            floorYWall = mapaY
        else: # horizontal == 1 and direcaoRaioY < 0
            # SOUTH
            floorXWall = mapaX + wallX
            floorYWall = mapaY + 1.0


        for y in range(int(finalDaLinha) , janelaAltura + 2):
            
            current_dist = janelaAltura / (2.0 * y - janelaAltura)
            
           
            weight = current_dist / distanciaPerpendicular
            current_floor_x = weight * floorXWall + (1.0 - weight) * jogador.x
            current_floor_y = weight * floorYWall + (1.0 - weight) * jogador.y
            

            floor_tex_x = int(current_floor_x * texturaChao.get_width()) % texturaChao.get_width()
            floor_tex_y = int(current_floor_y * texturaChao.get_height()) % texturaChao.get_height()
            

            floor_color = texturaChao.get_at((floor_tex_x, floor_tex_y))
            janela.set_at((coluna, y - 1), floor_color)


            ceiling_color = texturaTeto.get_at((floor_tex_x, floor_tex_y))
            janela.set_at((coluna, janelaAltura - y), ceiling_color)


def RenderizarMapa3DLowPoly2(janela, janelaAltura, janelaLargura, jogador):
    

    pixels_janela = pygame.surfarray.array3d(janela)

    game_map = GetMapaAtual()


    tamanhoMapaX = len(game_map[0])
    tamanhoMapaY = len(game_map)
    jogadorXArredondado = int(jogador.x)
    jogadorYArredondado = int(jogador.y)


    texturaChao_arr = Sprites.texturaChao_array
    texturaTeto_arr = Sprites.texturaTeto_array
    tex_width = texturaChao_arr.shape[1]
    tex_height = texturaChao_arr.shape[0]


    for coluna in range(janelaLargura):
        porcentagemDaTela = coluna / float(janelaLargura)

        #transforma o 0 a 1 em -1 a 1
        cameraX = 2 * (porcentagemDaTela) - 1
        

        tamanhoMapaX = len(game_map[0])
        tamanhoMapaY = len(game_map)


        direcaoRaioX = jogador.dirX + jogador.planeX * cameraX
        direcaoRaioY = jogador.dirY + jogador.planeY * cameraX


        #DDA

        if(direcaoRaioX != 0):
            deltaDistanciaX = abs(1 / direcaoRaioX)
        else:
            #se o X for 0, o raio nunca crusa uma linha horizontal
            deltaDistanciaX = float('inf')


        if(direcaoRaioY != 0):
            deltaDistanciaY = abs(1 / direcaoRaioY)
        else:
            #se o Y for 0, o raio nunca crusa uma linha vertical
            deltaDistanciaY = float('inf')

        #direção do passo no eixo X
        passoX = 0


        distanciaX = 0
        distanciaY = 0

        jogadorXArredondado = int(jogador.x)
        jogadorYArredondado = int(jogador.y)
        if(direcaoRaioX < 0):
            #esquerda do grid
            passoX = -1
                        #jogador X inteiro - o grid anterior (parte inteira do X ex: 1.5 é 1) = 1.5 - 1 = 0.5
            distanciaX = (jogador.x - jogadorXArredondado) * deltaDistanciaX 
        else:
            #direita do grid
            passoX = 1
                        #parte inteira do X (ex: 1.5 é ) + 1 = próximo grid (2), - a fração (ex 1.5 é 0.5) = 0.5 de distância
            distanciaX = (jogadorXArredondado + 1.0 - jogador.x) * deltaDistanciaX

        if(direcaoRaioY < 0):
            #sul do grid
            passoY = -1
            distanciaY = (jogador.y - jogadorYArredondado) * deltaDistanciaY
        else:
            #norte do grid
            passoY = 1
            distanciaY = (jogadorYArredondado + 1.0 - jogador.y) * deltaDistanciaY

        mapaX = jogadorXArredondado
        mapaY = jogadorYArredondado
        hit = 0

        horizontal = 0

        while(not hit):

            #próximo square mais próximo
            if(distanciaX < distanciaY):
                distanciaX += deltaDistanciaX
                mapaX += passoX
                #parede vertical
                horizontal = 0
                

                if(mapaX < tamanhoMapaX and mapaX >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoX > 0 and tile.oeste) or (passoX < 0 and tile.leste):
                            hit = 1
                else:
                    break

            else:
                distanciaY += deltaDistanciaY
                mapaY += passoY
                #parede horizontal
                horizontal = 1


                if(mapaY < tamanhoMapaY and mapaY >= 0):
                    tile = game_map[mapaY][mapaX]
                    if(tile != 0):

                        if (passoY > 0 and tile.sul) or (passoY < 0 and tile.norte):
                            hit = 1
                else:
                    break
                #se tem parede, acerta (o mapa sempre tem que ser cercado de paredes)
            #if(game_map[mapaY][mapaX] > 0):
            #    hit = 1



        distanciaPerpendicular = 0

        if(horizontal):
            distanciaPerpendicular = (mapaY - jogador.y + ((1 -passoY) / 2 )) / direcaoRaioY
        else:                                                
                                                        #mágica que, infelizmente, não é de minha autoria
                                                        #se o passo for 1 calcula a distancia correta pra direita
                                                        #se for -1, ajusta para o grid correto no mapa
            distanciaPerpendicular = (mapaX - jogador.x +         ((1 - passoX) / 2) )                          / direcaoRaioX
        
        if(distanciaPerpendicular > 0):
            alturaDaLinha = int(janelaAltura / distanciaPerpendicular)
        else:
            #se a distância ate a parede for 0, o jogador está dentro da parede
            #então desenha a tela inteira (nunca vai acontecer, mas é bom ilustrar)
            alturaDaLinha = janelaAltura




        if horizontal == 0: # vertical
            wallX = jogador.y + distanciaPerpendicular * direcaoRaioY
        else: # horizontal
            wallX = jogador.x + distanciaPerpendicular * direcaoRaioX
        

        wallX -= math.floor(wallX)
        





        if horizontal == 0 and direcaoRaioX > 0:

            floorXWall = mapaX
            floorYWall = mapaY + wallX
        elif horizontal == 0 and direcaoRaioX < 0:

            floorXWall = mapaX + 1.0
            floorYWall = mapaY + wallX
        elif horizontal == 1 and direcaoRaioY > 0:

            floorXWall = mapaX + wallX
            floorYWall = mapaY
        else:

            floorXWall = mapaX + wallX
            floorYWall = mapaY + 1.0

        # 'finalDaLinha' é o último pixel da parede
        finalDaLinha = alturaDaLinha / 2 + janelaAltura / 2 - 2
        if finalDaLinha >= janelaAltura:
            finalDaLinha = janelaAltura - 1

        # Ponto de início do chão (o pixel *depois* da parede)
        chao_start_y = int(finalDaLinha) + 1



        y_range = np.arange(chao_start_y, janelaAltura)

        # Se o array estiver vazio (parede ocupa tudo), pule
        if y_range.size == 0:
            continue


        current_dist = janelaAltura / (2.0 * y_range - janelaAltura)
        weight = current_dist / distanciaPerpendicular


        current_floor_x = weight * floorXWall + (1.0 - weight) * jogador.x
        current_floor_y = weight * floorYWall + (1.0 - weight) * jogador.y


        floor_tex_x = (current_floor_x * tex_width).astype(int) % tex_width
        floor_tex_y = (current_floor_y * tex_height).astype(int) % tex_height

        ceil_tex_x = (current_floor_x * tex_width).astype(int) % texturaTeto_arr.shape[1]
        ceil_tex_y = (current_floor_y * tex_height).astype(int) % texturaTeto_arr.shape[0]


        floor_colors = texturaChao_arr[floor_tex_y, floor_tex_x]
        ceiling_colors = texturaTeto_arr[ceil_tex_y, ceil_tex_x]


        pixels_janela[coluna, y_range] = floor_colors

        y_ceiling_range = janelaAltura - 1 - y_range
        pixels_janela[coluna, y_ceiling_range] = ceiling_colors

    pygame.surfarray.blit_array(janela, pixels_janela)