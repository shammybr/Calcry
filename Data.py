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
                 "Derivada" : 1,
                 "Integral" : 2,
                 "Jogador" : 99,
}

Datributo = { "Vida" : 0,
                 "Energia" : 1,
                 "Ataque" : 2,
                 "Defesa" : 3,
}



xpProximoLevel = { 1 : 100,
                       2 : 120,
                       3 : 150,
                       4 : 200,
}

statusPorLevel = { 1: [10, 30, 10],
                   2: [10, 30, 10],
                   3: [10, 30, 10],
                   4: [10, 30, 10],


}

class EANDAR(Enum):
    EANDAR1 = 1
    EANDAR2 = 2
    EANDAR3 = 3



class EEstado(Enum):
    MAINMENU = 1
    ANDANDO = 2
    LUTA = 3
    ESCOLHA = 4
    ANIMACAOOVERWORLD = 5
    DIALOGO = 6

class ELuta(Enum):
    ITEM = 1
    ATACAR = 2
    HABILIDADE = 3
    FUGIR = 4

class EANIMACAOOVERWORLD(Enum):
    NADA = 0
    MUDARANDAR = 1


class Entidade():
    def __init__(self, nome, tipo, vida, vidaMaxima, energia, energiaMaxima, velocidade, dano, defesa):
        self.nome = nome
        self.tipo = tipo
        self.vida = vida
        self.vidaMaxima = vidaMaxima
        self.energia = energia
        self.energiaMaxima = energiaMaxima
        self.velocidade = velocidade
        self.dano = dano
        self.defesa = defesa
        self.buffs = []


    def TomarDano(self, dano):
        modDefesa = 0

        for buff in self.buffs:
            for i in range(0, len(buff.atributos)):
                if(buff.atributos[i] == Datributo["Defesa"]):
                    modDefesa += buff.valores[i]

        self.vida = max(0, self.vida - int(dano * (1 - ( (self.defesa + modDefesa) / 100 ) )   ))
        return int(dano * (1 - ( (self.defesa + modDefesa) / 100 ) )   )

    def Curar(self, hp, energia):
        self.vida = min(self.vidaMaxima, self.vida + hp)
        self.energia = min(self.energiaMaxima, self.energia + energia)

class Jogador(Entidade):
    def __init__(self, coordenadaX, coordenadaY, angulo, direcao, velocidade):
        super().__init__("Jogador", tipoEntidade["Jogador"], 100, 100, 100, 100, velocidade, 100, 0)
        self.x = coordenadaX
        self.y = coordenadaY
        self.angulo = angulo
        self.direcao = direcao
        self.dirX = 1.0
        self.dirY = 0.0  # Direction vector
        self.planeX = 0.0 # The camera plane vector
        self.planeY = -0.66
        self.habilidades = []
        self.items = []
        self.level = 1
        self.xp = 99
        self.danoGuardado = 0
        self.andar = 1
        self.engrenagems = [False, False, False]

    def GanharXP(self, xp):
        self.xp = self.xp + xp
        if(self.xp >= xpProximoLevel[self.level]):
            self.UparDeLevel()
            return True
        return False
    

    def UparDeLevel(self):
        self.xp = self.xp - xpProximoLevel[self.level]
        self.level += 1
        self.dano += statusPorLevel[self.level][0]
        self.vidaMaxima += statusPorLevel[self.level][1]
        self.energiaMaxima += statusPorLevel[self.level][2]
        self.Curar(self.vidaMaxima, self.energiaMaxima)

    def AprenderHabilidade(self, habilidade):
        self.habilidades.append(habilidade)

    def ObterItem(self, item):
        for itemNaBag in self.items:
            if(itemNaBag.ID == item.ID):
                itemNaBag.quantidade += 1
                return 1

        self.items.append(item)


    def TomarDano(self, dano):
        danoAtual = dano

        for buff in self.buffs:
            if(buff.ID == 3):
                danoAtual = danoAtual * 0.5
                self.danoGuardado += (dano * 3)

        danoTomado = super().TomarDano(danoAtual)

        return danoTomado


class Inimigo(Entidade):
    def __init__(self, nome, tipo, vida, vidaMaxima, energia, energiaMaxima, sprite, velocidade, dano, defesa, xp):
        super().__init__(nome, tipo, vida, vidaMaxima, energia, energiaMaxima, velocidade, dano, defesa)
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
        super().__init__(nome, tipoEntidade["Limite"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/ILimite.png', 0, 0), 100, 5, 9, 10)

class IDerivada(Inimigo):
     def __init__(self, nome):
        super().__init__(nome, tipoEntidade["Derivada"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/IDerivada.png', 0, 0), 100, 5, 15, 10)

class IIntegral(Inimigo):
     def __init__(self, nome):
        super().__init__(nome, tipoEntidade["Integral"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/IIntegral.png', 0, 0), 100, 5, 20, 10)

class Habilidade():
    def __init__(self, nome, ID, valores, desc, temAlvo, funcs):
        self.nome = nome
        self.ID = ID
        self.valores = valores
        self.desc = desc
        self.temAlvo = temAlvo
        self.funcs = funcs

class Buff():
    def __init__(self, nome, ID, atributos, valores, turnosTotais):
        self.nome = nome
        self.ID = ID
        self.atributos = atributos
        self.valores = valores
        self.turnosTotais = turnosTotais
        self.Iturnos = 0

class Item():
    def __init__(self, nome, ID, valores, desc, temAlvo, funcs, quantidade):
        self.nome = nome
        self.ID = ID
        self.valores = valores
        self.desc = desc
        self.temAlvo = temAlvo
        self.funcs = funcs
        self.quantidade = quantidade

class Escolha():
    def __init__(self, desc, spriteNormal, spriteSelecionada, funcoes):
        self.desc = desc
        self.spriteNormal = spriteNormal
        self.spriteSelecionada = spriteSelecionada
        self.funcoes = funcoes
        self.selecionado = False
        self.imagem = HUD.GameImageMelhor(spriteNormal, 0, 0)

    
    def Selecionar(self, on):
        if(self.selecionado):
            if(not on):
                self.imagem.MudarImagem(self.spriteNormal)
                self.selecionado = False
        else:
            if(on):
                self.imagem.MudarImagem(self.spriteSelecionada)
                self.selecionado = True

    def AdicionarFunc(self, func):
        self.funcoes.append(func)
                
class Interacao():
    def __init__(self, norte, sul, leste, oeste, interacao, id):
        self.norte = norte
        self.sul = sul
        self.leste = leste
        self.oeste = oeste
        self.interacao = interacao
        self.id = id


def BuffarAtaque(entidades, valores):
    mensagens = []
    for entidade in entidades:
        for buff in entidade.buffs:
            if(buff.ID == 1):
                entidade.buffs.remove(buff)

        entidade.buffs.append(Buff("Buff de Ataque", 1, [Datributo["Ataque"]], [10], 3))
        mensagens.append("Ataque de " + entidade.nome + " aumentado em 10!")

    return mensagens


def BuffarDefesa(entidades, valores):
    mensagens = []

    for entidade in entidades:
        for buff in entidade.buffs:
            if(buff.ID == 2):
                entidade.buffs.remove(buff)

        entidade.buffs.append(Buff("Buff de Defesa", 2, [Datributo["Defesa"]], [10], 3))
        mensagens.append("Defesa de " + entidade.nome + " aumentado em 10!")
        
    return mensagens

def CurarEnergia(entidades, valores):
    mensagens = []

    for entidade in entidades:
        entidade.Curar(0, valores)
        mensagens.append("Energia de " + entidade.nome +  " restaurada em " + str(valores) +" !")

    return mensagens

def AbsorverAtaque(entidades, valores):
    mensagens = []

    for entidade in entidades:
        entidade.buffs.append(Buff("Postura defensiva", 3, [], [0], 1))
        entidade.danoGuardado = 0
        mensagens.append(entidade.nome +  " toma uma postura defensiva... ")

    return mensagens


def CurarVida(entidades, valores):
    mensagens = []

    for entidade in entidades:
        entidade.Curar(valores,0)
        mensagens.append("Vida de " + entidade.nome +  " restaurada em " + str(valores) +" !")

    return mensagens

def SubirDeAndar(jogador):
    jogador.andar += 1

    print("Subiu")

    return True


def DescerDeAndar(jogador):
    jogador.andar -= 1

    print("Subiu")

    return True


def Voltar(jogador):

    print("Voltou")

    return True



habilidadeBD = [ Habilidade("Concentração", 1, [40, 10, 10], ["Concentre-se na tarefa!", "Aumenta o ataque e a defesa - 3 turnos"], False, [BuffarAtaque, BuffarDefesa]),
                 Habilidade("Meditação", 2, [0, 30], ["Controle sua mente!", "Recupera sua energia em 30"], False, [CurarEnergia]),
                 Habilidade("Preparação", 2, [80, 30], ["Transforme dor em força!", "Aumenta o seu dano de acordo com o dano recebido."], False, [AbsorverAtaque]),

]

itemBD = [  Item("Energético", 1, [0, 9999], ["Energético com gosto de manga.", "Recupera toda a energia."], False, [CurarEnergia], 1),
            Item("Analgésico", 2, [0, 50], ["Analgésico genérico.", "Recupera sua vida em 50."], False, [CurarVida], 1),
          
]

escolhaBD = [   Escolha('Subir de andar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Voltar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Descer de andar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Aceitar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Recusar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', [])



]