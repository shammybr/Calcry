from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import pygame

ultimoLoop = time.time()
deltaTime = 0
isPaused = True
gameOver = False

pontosPlayer = 0
pontosAI = 0
cooldownAI = 0.1
ulimaViradaAI = 0.5

janela = Window(800, 600)
teclado = Window.get_keyboard()

imagem =  pygame.image.load("ball.png") 
bola = Sprite("ball.png")
bola.image = pygame.transform.scale(imagem, (30, 30))
bola.width = 30
bola.height = 30
bola.set_position((janela.width /2 ) - (bola.width / 2), (janela.height / 2) - (bola.height / 2))



velX = 300
velY = 300
sinalX = 1
sinalY = 1

barraE = Sprite("barra.png")
barraD = Sprite("barra.png")
barraE.set_position((janela.width /22 ) - (barraE.width / 2), (janela.height / 2) - (barraE.height / 2))
barraD.set_position((janela.width - (janela.width /22) ) - (barraD.width / 2), (janela.height / 2) - (barraD.height / 2))
velBarra = 750
ultimoMovimentoAI = 0

pontoEsquerdo = bola.x
pontoDireito = bola.x + bola.width
pontoCima = bola.x

def LerInput(teclado, deltaTime):
    if(teclado.key_pressed("w")):
        
        barraE.y = max(0, barraE.y - velBarra * min(deltaTime, 0.5))
    elif(teclado.key_pressed("s")):
        barraE.y = min(janela.height - barraE.height , barraE.y + velBarra * min(deltaTime, 0.5))

def ResetarPosicoes():
    global velX
    global velY
    global sinalX
    global sinalY
    global cooldownAI
        
    barraE.set_position((janela.width /22 ) - (barraE.width / 2), (janela.height / 2) - (barraE.height / 2))
    barraD.set_position((janela.width - (janela.width /22) ) - (barraD.width / 2), (janela.height / 2) - (barraD.height / 2))
    bola.set_position((janela.width /2 ) - (bola.width / 2), (janela.height / 2) - (bola.height / 2))
    velX = 300
    velY = 300
    sinalX = 1
    sinalY = 1
    cooldownAI -= 0.01

def GameOver(ganhador):
    janela.draw_text(str(ganhador) + " ganhou!", janela.width /2 - 150, janela.height / 20, 30, (255, 255, 255))


def CalcularAI(deltaTime):
    global ulimaViradaAI
    global ultimoMovimentoAI
    global gameOver

    if(bola.y + 100 > barraD.y + barraD.height):
        barraD.y = min(janela.height - barraD.height , barraD.y + velBarra * min(deltaTime, 0.5))
        if(ultimoMovimentoAI != 1):
            ulimaViradaAI = 0
        
        ultimoMovimentoAI = 1
    elif(bola.y - 100 < barraD.y):
        barraD.y = max(0, barraD.y - velBarra * min(deltaTime, 0.5))
        if(ultimoMovimentoAI != -1):
            ulimaViradaAI = 0

        ultimoMovimentoAI = -1

        

while(True):
    deltaTime = time.time() - ultimoLoop
    ultimoLoop = time.time()
    
    

    if(not isPaused):
        LerInput(teclado, deltaTime)

        if(ulimaViradaAI > cooldownAI):
            CalcularAI(deltaTime)
        else:
            ulimaViradaAI += min(deltaTime, 0.5)

        bola.x += velX * sinalX * min(deltaTime, 0.5)
        bola.y += velY * sinalY * min(deltaTime, 0.5)

        if(bola.x < 0):
            bola.x = 0
        if(bola.y < 0):
            bola.y = 0

        if(bola.x <= 0):
            pontosAI += 1
            if(pontosAI >= 3):
                gameOver = True
            else:
                ResetarPosicoes()
            isPaused = True
        elif(bola.x + bola.width >= janela.width):
            pontosPlayer += 1
            if(pontosPlayer >= 3):
                gameOver = True
            else:
                ResetarPosicoes()
            isPaused = True


        if(bola.y <= 0):
            bola.y = 0
            sinalY *= -1
            velY += 50
        elif(bola.y + bola.height >= janela.height):
            bola.y = janela.height - bola.height
            sinalY *= -1
            velY += 50

        if(bola.collided(barraE) and sinalX < 0):
            sinalX *= -1
            velX += 50  
            if(teclado.key_pressed("s")):
                sinalY = 1
                velY += 50
            if(teclado.key_pressed("w")):
                sinalY = -1
                velY += 50
        elif(bola.collided(barraD) and sinalX > 0):
            sinalX *= -1
            velX += 50  
            if(ultimoMovimentoAI == -1):
                sinalY = 1
                velY += 50
            if(ultimoMovimentoAI == 1):
                sinalY = -1
                velY += 50

    else:
        if(teclado.key_pressed("SPACE")):
            if(gameOver):
                ResetarPosicoes()
                pontosPlayer = 0
                pontosAI = 0
                gameOver = False

            else:
                isPaused = False

    if(not gameOver):
        janela.set_background_color((0, 0, 0))
        janela.draw_text(str(pontosPlayer) + " / " +  str(pontosAI), janela.width /2 - 30, janela.height / 20, 30, (255, 255, 255))
        bola.draw()
        barraE.draw()
        barraD.draw()
    else:
        janela.set_background_color((0, 0, 0))
        bola.draw()
        barraE.draw()
        barraD.draw()
        if(pontosAI >= 3):
            GameOver("O computador")
        else:
            GameOver("O player")



    janela.update()
