from PPlay.window import *

def CriarJanela():
    janela = Window(1280 ,720 )

    screen = pygame.display.set_mode((1280, 720))
    pygame.draw.line(screen, (0, 100, 0), (0, 500), (600, 500), 3) # linha do horizonte
    janela.set_title("Calcry")
    return janela


