from PPlay.window import *




# Loop que apenas checa se tem alguma tecla pressionada no frame atual
def LerInput(teclado, janela):

    if teclado.key_pressed("w"):  # Direcional ^
        return 1
    if teclado.key_pressed("s"):  # Direcional \/
        return 2
    if teclado.key_pressed("d"):  # Direcional ->
        return 3
    if teclado.key_pressed("a"):  # Direcional <-
        return 4
    if teclado.key_pressed("l"):  # teste
        return 9



    if teclado.key_pressed("ESC"):  # Esc, escape..
        janela.close()  # Fecha o programa

    return 0
