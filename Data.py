from enum import Enum
from PPlay.sprite import *
import HUD

direcao = { "N" : 0,
            "L" : 1,
            "S" : 2,
            "O" : 3
}

coordenadasDirecao = { 0 : (0.0, 1.0),
                       1 : (1.0, 0.0),
                       2 : (0.0, -1.0),
                       3 : (-1.0, 0.0),
}

tipoEntidade = { "Limite" : 0,
         #   "Derivada" : 1,
          #  "Integral" : 2,
          "Jogador" : 99,
}


class EANDAR(Enum):
    EANDAR1 = 1
    EANDAR2 = 2
    EANDAR3 = 3



class EEstado(Enum):
    MAINMENU = 1
    ANDANDO = 2
    LUTA = 3

class ELuta(Enum):
    ITEM = 1
    ATACAR = 2
    HABILIDADE = 3
    FUGIR = 4


class Entidade():
    def __init__(self, nome, tipo, vida, vidaMaxima, energia, energiaMaxima, velocidade, dano):
        self.nome = nome
        self.tipo = tipo
        self.vida = vida
        self.vidaMaxima = vidaMaxima
        self.energia = energia
        self.energiaMaxima = energiaMaxima
        self.velocidade = velocidade
        self.dano = dano

    def TomarDano(self, dano):
        self.vida = max(0, self.vida - dano)

        
class Jogador(Entidade):
    def __init__(self, coordenadaX, coordenadaY, angulo, direcao, velocidade):
        super().__init__("Jogador", tipoEntidade["Jogador"], 100, 100, 100, 100, velocidade, 80)
        self.x = coordenadaX
        self.y = coordenadaY
        self.angulo = angulo
        self.direcao = direcao
        self.dirX = 0.0
        self.dirY = 1.0  # Direction vector
        self.planeX = 0.66 # The camera plane vector
        self.planeY = 0.0

        self.level = 1
        self.xp = 0

class Inimigo(Entidade):
    def __init__(self, nome, tipo, vida, vidaMaxima, energia, energiaMaxima, sprite, velocidade, dano, xp):
        super().__init__(nome, tipo, vida, vidaMaxima, energia, energiaMaxima, velocidade, dano)
        self.xpDado = xp
        self.sprite = sprite
        self.barraHPBackground = HUD.GameImageMelhor('Sprites/HUD/BarraVidaVazia.png', 0, 0)
        self.barraHP = HUD.GameImageMelhor('Sprites/HUD/BarraVida.png', 0, 0)


class Parede():
    def __init__(self, coordenadaX, coordenadaY, direcao):
        self.x = coordenadaX
        self.y = coordenadaY
        self.direcao = direcao

class ILimite(Inimigo):
     def __init__(self, nome):
        super().__init__(nome, tipoEntidade["Limite"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/ILimite.png', 0, 0), 100, 5, 10)