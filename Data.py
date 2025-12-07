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
                 "Bixo de 7 Cabeças" : 3,
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
                       5 : 250,
                       6 : 300,
                       7 : 350,
                       8 : 400,
                       9 : 450,
                       10 : 500,
                       
}

statusPorLevel = { 1: [10, 50, 10],
                   2: [10, 50, 10],
                   3: [10, 50, 10],
                   4: [10, 50, 10],
                   5: [10, 50, 10],
                   6: [10, 50, 10],
                   7: [10, 50, 10],
                   8: [10, 50, 10],
                   9: [10, 50, 10],
                   10: [10, 50, 10],


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
    FIM = 7
    GAMEOVER = 8
    FINALJOGO = 9

class ELuta(Enum):
    ITEM = 1
    ATACAR = 2
    HABILIDADE = 3
    FUGIR = 4

class EANIMACAOOVERWORLD(Enum):
    NADA = 0
    MUDARANDAR = 1
    CADEIRAS = 2


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
        super().__init__("Jogador", tipoEntidade["Jogador"], 300, 300, 100, 100, velocidade, 30, 0)
        self.x = coordenadaX
        self.y = coordenadaY
        self.angulo = angulo
        self.direcao = direcao
        self.dirX = -1.0
        self.dirY = 0.0  # Direction vector
        self.planeX = 0.0 # The camera plane vector
        self.planeY = 0.66
        self.habilidades = []
        self.items = []
        self.level = 1
        self.xp = 0
        self.danoGuardado = 0
        self.andar = 1
        self.engrenagems = [False, False, False]
        self.quests = [0, 0, 0]
        self.provas = [False, False, False]
        self.aulas = [[False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]]
        self.itemPego = [False, False, False, False, False]

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
        if(self.habilidades.count(habilidade) == 0):
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
        super().__init__(nome, tipoEntidade["Limite"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/ILimite.png', 0, 0), 100, 5, 9, 40)
        self.danoAcumulado = 0
        self.defesaAcumulada = 0

    def TomarDano(self, dano):

        modDefesa = self.defesaAcumulada

        for buff in self.buffs:
            for i in range(0, len(buff.atributos)):
                if(buff.atributos[i] == Datributo["Defesa"]):
                    modDefesa += buff.valores[i]

        self.vida = max(0, self.vida - int(dano * (1 - ( (self.defesa + modDefesa) / 100 ) )   ))
        return int(dano * (1 - ( (self.defesa + modDefesa) / 100 ) )   )
    

class IDerivada(Inimigo):
     def __init__(self, nome):
        super().__init__(nome, tipoEntidade["Derivada"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/IDerivada.png', 0, 0), 100, 10, 15, 60)

class IIntegral(Inimigo):
     def __init__(self, nome):
        super().__init__(nome, tipoEntidade["Integral"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/IIntegral.png', 0, 0), 100, 20, 20, 80)
        self.dobrado = False

class IBOSS(Inimigo):
     def __init__(self, nome):
        super().__init__(nome, tipoEntidade["Bixo de 7 Cabeças"], 100, 100, 100, 100, HUD.GameImageMelhor('Sprites/Inimigos/IIntegral.png', 0, 0), 100, 5, 20, 10)


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

        entidade.buffs.append(Buff("Buff de Ataque", 1, [Datributo["Ataque"]], [25], 4))
        mensagens.append("Ataque de " + entidade.nome + " aumentado em 10!")

    return mensagens


def BuffarDefesa(entidades, valores):
    mensagens = []

    for entidade in entidades:
        for buff in entidade.buffs:
            if(buff.ID == 2):
                entidade.buffs.remove(buff)

        entidade.buffs.append(Buff("Buff de Defesa", 2, [Datributo["Defesa"]], [10], 4))
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

def Taylor(entidades, valores):

    mensagens = []

    for entidade in entidades:
        entidade.buffs.append(Buff("Taylor", 4, [Datributo["Ataque"]], [valores * 15], 5))
        mensagens.append("Série expandida por " + str(valores) + "!")
        mensagens.append("Ataque aumentado em " + str(valores * 15) + "!")
        
    return mensagens

def Sanduiche(entidades, valores):
    mensagens = []

    for entidade in entidades:
        if(entidade.danoAcumulado > 0):
            entidade.danoAcumulado *= -1
            mensagens.append("Ataque extra de " + entidade.nome + " foi para " + str(entidade.danoAcumulado))

        if(entidade.defesaAcumulada > 0):
            entidade.defesaAcumulada *= -1
            mensagens.append("Defesa extra de " + entidade.nome + " foi para " + str(entidade.defesaAcumulada))
        
    if(len(mensagens) == 0):
        mensagens.append("Nenhum limite afetado.")

    return mensagens

def Rolle(entidades, valores):
    mensagens = []

    i = 0
    for entidade in entidades:
        danoTomado = entidade.TomarDano(int(valores[i]))
        mensagens.append(entidade.nome + " tomou " + str(danoTomado) + " de dano")
        i += 1

    if(len(mensagens) == 0):
        mensagens.append("Nenhuma derivada com mesmo HP encontrada.")

    return mensagens

def TFC(entidades, valores):
    mensagens = []

    for entidade in entidades:
        entidade.buffs.append(Buff("TFC", 5, [], [valores], 5))
        mensagens.append("Cada problema resolvido te revigora!")

    return mensagens

def Cola(entidades, valores):
    mensagens = []

    for entidade in entidades:
        entidade.tomarDano(valores)
        mensagens.append(entidade.nome +  " recebeu " + str(valores) +" de dano!")

    return mensagens


habilidadeBD = [ Habilidade("Concentração", 1, [40, 25, 10], ["Concentre-se na tarefa!", "Aumenta o ataque e a defesa - 3 turnos"], False, [BuffarAtaque, BuffarDefesa]),
                 Habilidade("Meditação", 2, [0, 80], ["Controle sua mente!", "Recupera sua energia em 80."], False, [CurarEnergia]),
                 Habilidade("Preparação", 3, [30, 30], ["Transforme dor em força!", "Aumenta o seu dano de acordo com o dano recebido."], False, [AbsorverAtaque]),
                 Habilidade("T. Sanduíche", 4, [20, 0], ["Resolve os limites!", "Inverte o dano extra que todos os limites possuem."], False, [Sanduiche]),
                 Habilidade("Série d.Taylor", 5, [30, 0], ["Expanda seu poder!", "Aumenta o seu dano de acordo com o número de derivadas."], False, [Taylor]),
                 Habilidade("T. Rolle", 6, [30, 0], ["Teorema de Rolle!", "Dano em derivadas com o mesmo HP (dano*HP faltando)."], False, [Rolle]),
                 Habilidade("T.F.C", 7, [80, 0], ["Teorema Fundamental do Cálculo!", "Rouba vida em todo ataque por 3 turnos."], False, [TFC]),

]

itemBD = [  Item("Energético", 1, [0, 9999], ["Energético com gosto de manga.", "Recupera toda a energia."], False, [CurarEnergia], 1),
            Item("Analgésico", 2, [0, 100], ["Analgésico genérico.", "Recupera sua vida em 100."], False, [CurarVida], 1),
            Item("Cola", 3, [0, 50], ["Pequena cola num papel.", "Dá 50 de dano em área."], False, [Cola], 1),
]

escolhaBD = [   Escolha('Subir de andar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Voltar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Descer de andar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Aceitar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Recusar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),
                Escolha('Quebrar' , 'Sprites/HUD/escolhaNormal.png', 'Sprites/HUD/escolhaSelecionada.png', []),



]