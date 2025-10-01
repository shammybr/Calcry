direcao = { "N" : 0,
            "L" : 1,
            "S" : 2,
            "O" : 3
}

class Jogador():
    def __init__(self, coordenadaX, coordenadaY, angulo, direcao):
        self.x = coordenadaX
        self.y = coordenadaY
        self.angulo = angulo
        self.direcao = direcao
        self.dirX = 0.0
        self.dirY = 1.0  # Direction vector
        self.planeX = 0.66 # The camera plane vector
        self.planeY = 0.0

        self.vida = 100
        self.vidaMaxima = 100
        self.energia = 100
        self.energiaMaxima = 100
        
class Parede():
    def __init__(self, coordenadaX, coordenadaY, direcao):
        self.x = coordenadaX
        self.y = coordenadaY
        self.direcao = direcao