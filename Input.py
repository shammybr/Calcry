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
    if teclado.key_pressed("z"):  # confirmar
        return 5
    if teclado.key_pressed("x"):  # voltar
        return 6
    
    if teclado.key_pressed("l"):  # teste
        return 9
    if teclado.key_pressed("k"):  # teste
        return 10
    if teclado.key_pressed("F1"):  # teste
        return 11
    if teclado.key_pressed("F2"):  # teste
        return 12


    if teclado.key_pressed("ESC"):  # Esc, escape..
        janela.close()  # Fecha o programa

    return 0
