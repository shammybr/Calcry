import pickle
import random
from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
from functools import cmp_to_key

from Janela import CriarJanela

janela = CriarJanela()


import Sprites
import Data
import Input
import Mapa
import math
import HUD
import Luta
import GameInstance
import Sounds

Sprites.CarregarTexturas(janela)
jogo = GameInstance.Jogo(janela)

jogo.Musica.musica_atual.set_repeat(True)
jogo.Musica.musica_atual.play()
botoes_menu=Sprites.get_lista_botoes_menu()
botoes_submenu=Sprites.get_lista_botoes_submenu()
display_volume=Sprites.get_diplay_volume()
lista_efeitos=Sounds.criar_lista_efeitos()

luta = jogo.luta
#jogo.jogador.AprenderHabilidade(Data.habilidadeBD[0])
jogo.jogador.AprenderHabilidade(Data.habilidadeBD[1])
#jogo.jogador.AprenderHabilidade(Data.habilidadeBD[5])
#jogo.jogador.AprenderHabilidade(Data.habilidadeBD[2])


ismousepressed=False




def Update():
    global minimapa

    jogo.deltaTime = time.time() - jogo.tempoUltimoFrame
    jogo.tempoUltimoFrame = time.time()

    jogo.segundo += jogo.deltaTime

    jogo.ultimoDraw += jogo.deltaTime

    jogo.ultimoInput = Input.LerInput(jogo.teclado, janela)
    if(jogo.ultimoInput == 0):
        jogo.botaoSolto = True



    jogo.Musica.atualizar_musica_mais_facil(jogo.estadoJogo) # Passível de Otimização

    if (jogo.ultimoInput == 13):
        jogo.Musica.atualizar_musica(Data.EEstado.MAINMENU)
        ismousepressed = False
        while True:
            jogo.SubMenu.DesenharSubMenu(janela, botoes_submenu)
            if (jogo.mouse.is_button_pressed(1)):
                if (not ismousepressed):
                    ismousepressed=True
                    if (jogo.mouse.is_over_object(botoes_submenu[0])):
                        break
                    elif (jogo.mouse.is_over_object(botoes_submenu[1])):
                        while (True):
                            jogo.SubMenu.Desenharopcoes(janela, botoes_submenu, display_volume, jogo.Musica.musica_atual.volume)

                            if (jogo.mouse.is_button_pressed(1)):
                                if (not ismousepressed):
                                    ismousepressed=True
                                    if (jogo.mouse.is_over_object(botoes_submenu[4])):
                                        mudar_volume(-10)
                                    elif (jogo.mouse.is_over_object(botoes_submenu[5])):
                                        mudar_volume(10)
                                    elif (jogo.mouse.is_over_object(botoes_submenu[6])):
                                        break                                    
                            else:
                                ismousepressed=False
                    elif (jogo.mouse.is_over_object(botoes_submenu[2])):
                        while True:
                            jogo.SubMenu.DesenharControles(janela, botoes_submenu)
                            if (jogo.mouse.is_button_pressed(1)):
                                if (not ismousepressed):
                                    ismousepressed=True
                                    if (jogo.mouse.is_over_object(botoes_submenu[6])):
                                        break                                    
                            else:
                                ismousepressed=False
                    elif (jogo.mouse.is_over_object(botoes_submenu[3])):
                        jogo.SalvarJogo()
                        jogo.estadoJogo=Data.EEstado.MAINMENU
                        break

            else:
                ismousepressed=False



    if(jogo.estadoJogo == Data.EEstado.ANDANDO):

        if(time.time() - jogo.ultimaRotacao > 0.005):
            if(jogo.isRodando):
                
                VirarJogadorLoop(jogo.ultimaDirecaoX, jogo.ultimaDirecaoY)

            else:


                if(jogo.ultimoInput == 3):
                    AtualizarDirecaoJogador(jogo.ultimoInput)
                    jogo.rodandoDirecao = 1
                    jogo.isRodando = True
                    jogo.ultimaDirecaoX = jogo.jogador.dirX
                    jogo.ultimaDirecaoY = jogo.jogador.dirY


                elif(jogo.ultimoInput == 4):
                    AtualizarDirecaoJogador(jogo.ultimoInput)
                    jogo.rodandoDirecao = 2
                    jogo.isRodando = True
                    jogo.ultimaDirecaoX = jogo.jogador.dirX
                    jogo.ultimaDirecaoY = jogo.jogador.dirY

                





        if(time.time() - jogo.ultimoMovimento > 0.1):

            if(jogo.isAndando):
                AndarJogadorLoop(jogo.jogador, jogo.andandoDestino, jogo.inicioJogador, jogo.andarVelocidade)

                if(abs(jogo.andandoDestino[0] - jogo.jogador.x) < 0.05 and abs(jogo.andandoDestino[1] - jogo.jogador.y) < 0.05):
                    jogo.jogador.x = jogo.andandoDestino[0]
                    jogo.jogador.y = jogo.andandoDestino[1]

                    jogo.isAndando = False
                    jogo.ultimoMovimento = time.time()
                    minimapa=GetMinimapa()

            elif(AndarJogador(jogo.ultimoInput)):
                

                jogo.isAndando = True

        




        if((time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto) or jogo.ultimoInput != jogo.ultimoInputAnterior):
            if(jogo.ultimoInput == 5):
                ChecarInteracao()
                jogo.botaoSolto = False
                jogo.ultimoMovimentoBotao = time.time()

        if(jogo.ultimoInput == 9):
            ComecarLuta()

            
        if(jogo.ultimoInput == 10 and jogo.botaoSolto):

            jogo.botaoSolto = False
            jogo.jogador.TomarDano(5)

        if(jogo.ultimoInput == 11 and jogo.botaoSolto):

            jogo.botaoSolto = False
            jogo.SalvarJogo()
        
        if(jogo.ultimoInput == 12 and jogo.botaoSolto):

            jogo.botaoSolto = False
            CarregarJogo()


        RenderizarMapa()

    elif(jogo.estadoJogo == Data.EEstado.ESCOLHA):


        if((time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto) or jogo.ultimoInput != jogo.ultimoInputAnterior):
            if(jogo.ultimoInput == 1):   
                CalcularEscolhaSelecionada(1)
                jogo.botaoSolto = False
                jogo.ultimoMovimentoBotao = time.time()
            elif(jogo.ultimoInput == 2):
                CalcularEscolhaSelecionada(-1)
                jogo.botaoSolto = False
                jogo.ultimoMovimentoBotao = time.time()

            elif(jogo.ultimoInput == 5):
                jogo.dialogoMensagens.clear()

                for func in jogo.escolhas[jogo.escolhaSelecionada].funcoes:
                    func()

                jogo.botaoSolto = False
                jogo.ultimoMovimentoBotao = time.time()



        DesenharEscolhas(jogo.escolhas)

    elif(jogo.estadoJogo == Data.EEstado.DIALOGO):


        if((time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto)):
            if(jogo.ultimoInput == 5):
                if(jogo.ultimoInput == 5):
                    if(len(jogo.dialogoMensagens) <= 6):
                        if(jogo.ultimoEstadoJogo != Data.EEstado.ESCOLHA):
                            jogo.dialogoMensagens.clear()

                        if(jogo.ultimoEstadoJogo != Data.EEstado.DIALOGO):
                            jogo.estadoJogo = jogo.ultimoEstadoJogo
                        else:
                            jogo.estadoJogo = Data.EEstado.ANDANDO
                    else:
                        for i in range(0, 6):
                            jogo.dialogoMensagens.pop(0)


                        jogo.ultimoMovimentoBotao = time.time()
                    jogo.botaoSolto = False


        RenderizarMapa()
        DesenharDialogo()
        EscreverDialogo(jogo.dialogoMensagens)


    elif(jogo.estadoJogo == Data.EEstado.ANIMACAOOVERWORLD):
        if(jogo.animacao == Data.EANIMACAOOVERWORLD.NADA):
            jogo.estadoJogo = Data.EEstado.ANDANDO
        else:
            if(jogo.animacao ==  Data.EANIMACAOOVERWORLD.MUDARANDAR):
                RenderizarMapa()
                velocidadeFade = 1000
                if(jogo.fade.fading):
                    if(jogo.fade.alpha < 255):
                        jogo.fade.FadeIn(velocidadeFade * min(jogo.deltaTime, 0.01))
                    else:
                        if(jogo.fade.tempo < 0.3):
                            jogo.fade.Cooldown(jogo.deltaTime)
                        else:
                            jogo.fade.fading = False

                else:
                    if(jogo.fade.alpha > 0):
                        jogo.fade.FadeOut(velocidadeFade * min(jogo.deltaTime, 0.01))

                    else:
                        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                        jogo.estadoJogo = Data.EEstado.ANDANDO


                janela.get_screen().blit(jogo.fade.surface, (0, 0))

            if(jogo.animacao == Data.EANIMACAOOVERWORLD.CADEIRAS):
                RenderizarMapa()
                velocidadeFade = 1000
                if(jogo.fade.fading):
                    if(jogo.fade.alpha < 255):
                        jogo.fade.FadeIn(velocidadeFade * min(jogo.deltaTime, 0.01))
                    else:
                        if(jogo.fade.tempo < 0.3):
                            jogo.fade.Cooldown(jogo.deltaTime)
                        else:
                            jogo.jogador.quests[1] = 99
                            jogo.jogador.x = 2.5
                            jogo.jogador.y = 11.5
                            jogo.jogador.dirX = -1
                            jogo.jogador.dirY = 0
                            jogo.jogador.planeX = 0
                            jogo.jogador.planeY = 0.66
                            jogo.jogador.direcao = Data.direcao["O"]

                            jogo.mapaAtual = Mapa.GerarMapa(2, jogo)
                            jogo.fade.fading = False

                else:
                    if(jogo.fade.alpha > 0):
                        jogo.fade.FadeOut(velocidadeFade * min(jogo.deltaTime, 0.01))

                    else:
                        jogo.dialogoMensagens.append("Professor Feliz:")
                        jogo.dialogoMensagens.append(" ")
                        jogo.dialogoMensagens.append("Minhas cadeiras! Você achou elas!")
                        jogo.dialogoMensagens.append("Ah, mas que saudade eu estava de olhar")
                        jogo.dialogoMensagens.append("esse azul... azul tão profundo...")
                        jogo.dialogoMensagens.append(" ")
                        jogo.dialogoMensagens.append("Professor Feliz:")
                        jogo.dialogoMensagens.append(" ")
                        jogo.dialogoMensagens.append("Oh! Desculpe, esqueci que estava aí.")
                        jogo.dialogoMensagens.append("Eu achei isso aqui enquanto procurava as")
                        jogo.dialogoMensagens.append("cadeiras, talvez você queira.")
                        jogo.dialogoMensagens.append(" ")
                        jogo.dialogoMensagens.append("Você obteve uma engrenagem!")
                        jogo.dialogoMensagens.append("Você aprendeu: Série de Taylor!")
                        jogo.jogador.engrenagems[1] = True
                        jogo.jogador.AprenderHabilidade(Data.habilidadeBD[4])
                        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                        jogo.estadoJogo = Data.EEstado.DIALOGO
                        jogo.SalvarJogo()

                janela.get_screen().blit(jogo.fade.surface, (0, 0))

    elif(jogo.estadoJogo == Data.EEstado.GAMEOVER):
        

        velocidadeFade = 10

        if(jogo.fade.fading):
            if(jogo.fade.alpha < 255):
                if(jogo.fade.tempo < 0.05):
                    jogo.fade.Cooldown(jogo.deltaTime)
                else:
                    jogo.fade.tempo = 0
                    jogo.fade.FadeIn(5)
                    jogo.fade.surface.fill((255 - jogo.fade.alpha, 0, 0))
            else:
                    jogo.fade.surface.fill((0, 0, 0))

                    jogo.fade.fading = False

            janela.get_screen().blit(jogo.fade.surface, (0, 0))

        else:
                GameOverScreen()
                jogo.fade.FadeBlack()

        

    elif(jogo.estadoJogo == Data.EEstado.LUTA):

        if(luta.estadoLuta == luta.EEstadoLuta.ANIMACAO):
            if(luta.estadoAnimacao <= 1):
                if(luta.EntrarLuta(janela, jogo.deltaTime) == 1):
                    jogo.jogador.danoGuardado = 0
                    jogo.botaoSelecionadoLuta = Data.ELuta.ATACAR
                    luta.ResetarBotoes(jogo.lutaHUD, jogo.botaoSelecionadoLuta, jogo.posicoesBotoesLuta)
                    CalcularBotoesLuta()
                    
                    
                    
                    DesenharLutaHUD()
                    DesenharInimigos()
                    DesenharLutaBotoes()
                    luta.EntrarLuta(janela, 0.001)
                    luta.CriarTurno(jogo.inimigosNaLuta, jogo.jogador)
                
            elif(luta.estadoAnimacao == 2):
                luta.AnimarTrocaBotoesLoop(janela, jogo.deltaTime, jogo.lutaHUD, jogo.botaoSelecionadoLuta, jogo.posicoesBotoesLuta)
                RenderizarLuta()

            elif(luta.estadoAnimacao == 3):
                luta.AnimarDanoLoop(janela, jogo.inimigosNaLuta[jogo.alvoLutaAnimacao], jogo.deltaTime)
                RenderizarLuta()
                DesenharLutaLog()
                EscreverLutaLog(luta.mensagem)

                if(luta.esperandoInput and time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto):
                    if(jogo.ultimoInput == 5):
                        luta.esperandoInput = False
                        jogo.botaoSolto = False
                        jogo.ultimoMovimentoBotao = time.time()
                        luta.estadoLuta = luta.EEstadoLuta.PROCESSANDOTURNO


            elif(luta.estadoAnimacao == 4):
                luta.AnimarDanoPlayerLoop(janela, jogo)
                DesenharInimigos()
                DesenharLutaBotoes()
                DesenharLutaLog()
                EscreverLutaLog(luta.mensagem)

                if(luta.esperandoInput and time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto):
                    if(jogo.ultimoInput == 5):
                        luta.esperandoInput = False
                        jogo.botaoSolto = False
                        jogo.ultimoMovimentoBotao = time.time()
                        luta.estadoLuta = luta.EEstadoLuta.PROCESSANDOTURNO


            elif(luta.estadoAnimacao <= 100):
                if(luta.SairLutaLoop(janela, jogo.deltaTime) == 1):
                    AtualizarHUD()
                    RenderizarMapa()
                    luta.SairLutaLoop(janela, 0.001)
                    
            elif(luta.estadoAnimacao == 999):
                Fim()

        elif(luta.estadoLuta == luta.EEstadoLuta.LUTANDO):
            

            if((time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto) or jogo.ultimoInput != jogo.ultimoInputAnterior):
                if(jogo.ultimoInput == 2):
                    jogo.botaoAntigo = jogo.botaoSelecionadoLuta

                    if(jogo.botaoSelecionadoLuta == Data.ELuta.ATACAR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.HABILIDADE


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.HABILIDADE):
                        jogo.botaoSelecionadoLuta = Data.ELuta.FUGIR


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.FUGIR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ITEM


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.ITEM):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ATACAR

                    luta.AnimarTrocaBotoes(jogo.lutaHUD, jogo.botaoAntigo, jogo.botaoSelecionadoLuta)

                    jogo.ultimoMovimentoBotao = time.time()
                    jogo.botaoSolto = False

                elif(jogo.ultimoInput == 1):
                    jogo.botaoAntigo = jogo.botaoSelecionadoLuta

                    if(jogo.botaoSelecionadoLuta == Data.ELuta.ATACAR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ITEM


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.ITEM):
                        jogo.botaoSelecionadoLuta = Data.ELuta.FUGIR


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.FUGIR):
                        jogo.botaoSelecionadoLuta = Data.ELuta.HABILIDADE


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.HABILIDADE):
                        jogo.botaoSelecionadoLuta = Data.ELuta.ATACAR

                    luta.AnimarTrocaBotoes(jogo.lutaHUD, jogo.botaoAntigo, jogo.botaoSelecionadoLuta)

                    jogo.ultimoMovimentoBotao = time.time()
                    jogo.botaoSolto = False

                elif(jogo.ultimoInput == 5):

                    if(jogo.botaoSelecionadoLuta == Data.ELuta.ATACAR):
                        jogo.alvoLuta = 0
                        jogo.lutaHUD.setaSelecionarAlvo.Transformar(janela.width * 0.05, janela.height* 0.05)
                        alvoTransformado = CalcularSelecionarAlvo(0)
                        luta.mensagem.clear()
                        luta.mensagem.append(jogo.inimigosNaLuta[alvoTransformado].nome)
                        luta.estadoLuta = luta.EEstadoLuta.ESCOLHENDOALVO


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.ITEM):
                        luta.itemSelecionado = 0
                        luta.mensagem.clear()
                        if(len(jogo.jogador.items)):
                            luta.mensagem = jogo.jogador.items[0].desc.copy()

                        CalcularLutaItemSelecionado(0)
                        luta.estadoLuta = luta.EEstadoLuta.ESCOLHENDOITEM


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.FUGIR):
                        jogo.botaoSolto = False
                        jogo.ultimoMovimentoBotao = time.time()
                        if(luta.TentarFugir(jogo.inimigosNaLuta)):
                            luta.mensagem.clear()
                            luta.mensagem.append("O jogador fugiu da luta!")
                            luta.estadoLuta = luta.EEstadoLuta.RESULTADO
                        else:
                            luta.mensagem.clear()
                            luta.mensagem.append("O jogador não conseguiu")
                            luta.mensagem.append("fugir da luta!")
                            luta.estadoLuta = luta.EEstadoLuta.PROCESSANDOTURNO
                            luta.esperandoInput = True
                            luta.ultimoTurno = time.time()
                        


                    elif(jogo.botaoSelecionadoLuta == Data.ELuta.HABILIDADE):
                        luta.habilidadeSelecionada = 0
                        luta.mensagem.clear()
                        luta.mensagem = jogo.jogador.habilidades[0].desc.copy()
                        CalcularLutaHabilidadeSelecionada(0)
                        luta.estadoLuta = luta.EEstadoLuta.ESCOLHENDOHABILIDADE

                    jogo.ultimoMovimentoBotao = time.time()
                    jogo.botaoSolto = False

            RenderizarLuta()

        elif(luta.estadoLuta == luta.EEstadoLuta.ESCOLHENDOALVO):

            if((time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto) or jogo.ultimoInput != jogo.ultimoInputAnterior):
                if(jogo.ultimoInput == 3):

                    alvoTransformado = CalcularSelecionarAlvo(1)
                    jogo.botaoSolto = False
                    jogo.ultimoMovimentoBotao = time.time()
                    luta.mensagem.clear()
                    luta.mensagem.append(jogo.inimigosNaLuta[alvoTransformado].nome)

                elif(jogo.ultimoInput == 4):
                    
                    alvoTransformado = CalcularSelecionarAlvo(-1)
                    jogo.botaoSolto = False
                    jogo.ultimoMovimentoBotao = time.time()
                    luta.mensagem.clear()
                    luta.mensagem.append(jogo.inimigosNaLuta[alvoTransformado].nome)

                elif(jogo.ultimoInput == 5):
                    inimigosVivos = []
                    for i, inimigo in enumerate(jogo.inimigosNaLuta):
                        if(inimigo.vida > 0):
                            inimigosVivos.append(i)

                    inimigosVivos.sort(key=cmp_to_key(ComparaInimigos))

                    #alvoTransformado = int(((jogo.alvoLuta - 1)**2 + (jogo.alvoLuta - 1)) / 2 + abs((jogo.alvoLuta - 1)) - (jogo.alvoLuta - 1))
                    alvoTransformado = inimigosVivos[min(len(inimigosVivos) - 1, jogo.alvoLuta)]
                    
                    if(alvoTransformado < len(jogo.inimigosNaLuta)):
                        luta.mensagem.clear()

                        modAtaque = 0
                        modDefesa = 0
                        for buff in jogo.jogador.buffs:
                            for i in range(0, len(buff.atributos)):
                                if(buff.atributos[i] == Data.Datributo["Defesa"]):
                                    modDefesa += buff.valores[i]
                                elif(buff.atributos[i] == Data.Datributo["Ataque"]):
                                    modAtaque += buff.valores[i]


                        if(jogo.jogador.danoGuardado > 0):
                            luta.mensagem.append("UOOOOOOOOOOOOOOOOO!!!!")
                            luta.mensagem.append("")
                            jogo.jogador.danoGuardado *= -1
                            luta.esperandoInput = True

                        else:
                            if(jogo.jogador.danoGuardado < 0):
                                modAtaque += (jogo.jogador.danoGuardado * -1)
                                jogo.jogador.danoGuardado = 0
                                
                            danoCausado = luta.Atacar(jogo.inimigosNaLuta[alvoTransformado], jogo.jogador.dano + modAtaque)
                            luta.AnimarDano(jogo.inimigosNaLuta[alvoTransformado].sprite.x, jogo.inimigosNaLuta[alvoTransformado].sprite.y)
                            jogo.alvoLutaAnimacao = alvoTransformado
                            
                            luta.mensagem.append("Jogador atacou " + jogo.inimigosNaLuta[alvoTransformado].nome + "!")
                            luta.mensagem.append("Causou " + str(danoCausado) + " de dano!")
                        #if(jogo.inimigosNaLuta[alvoTransformado].vida == 0):
                        #    CalcularSelecionarAlvo(0)

                    jogo.botaoSolto = False
                    jogo.ultimoMovimentoBotao = time.time()

                elif(jogo.ultimoInput == 6):
                    jogo.botaoSolto = False
                    jogo.ultimoMovimentoBotao = time.time()
                    luta.estadoLuta = luta.EEstadoLuta.LUTANDO


            if(luta.esperandoInput and time.time() - jogo.ultimoMovimentoBotao > 0.2 and jogo.botaoSolto):
                if(jogo.ultimoInput == 5):
                    luta.esperandoInput = False
                    jogo.botaoSolto = False
                    jogo.ultimoMovimentoBotao = time.time()


            RenderizarLuta()
            DesenharAlvoHUD()
            DesenharLutaLog()
            EscreverLutaLog(luta.mensagem)

        elif(luta.estadoLuta == luta.EEstadoLuta.ESCOLHENDOHABILIDADE):

            if((time.time() - jogo.ultimoMovimentoBotao > 0.05 and jogo.botaoSolto) or jogo.ultimoInput != jogo.ultimoInputAnterior):
                if(jogo.botaoSolto):
                    
                        if(jogo.ultimoInput == 1):

                            CalcularLutaHabilidadeSelecionada(1)
                            luta.mensagem.clear()
                            luta.mensagem = jogo.jogador.habilidades[luta.habilidadeSelecionada].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()


                        elif(jogo.ultimoInput == 2):
                            
                            CalcularLutaHabilidadeSelecionada(-1)
                            luta.mensagem.clear()
                            luta.mensagem = jogo.jogador.habilidades[luta.habilidadeSelecionada].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()

                        elif(jogo.ultimoInput == 5):
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()
                            luta.mensagem.clear()

                            if(jogo.jogador.energia >= jogo.jogador.habilidades[luta.habilidadeSelecionada].valores[0]):
                                i = 1
                                for funcao in jogo.jogador.habilidades[luta.habilidadeSelecionada].funcs:
                                    if(jogo.jogador.habilidades[luta.habilidadeSelecionada].temAlvo):
                                        pass
                                    else:
                                        if(funcao == Data.Sanduiche):
                                            limites = []

                                            for inimigo in jogo.inimigosNaLuta:
                                                if(inimigo.vida > 0):
                                                    if inimigo.tipo == Data.tipoEntidade["Limite"]:
                                                        limites.append(inimigo)
                                                

                                            for mensagem in funcao(limites, jogo.jogador.habilidades[luta.habilidadeSelecionada].valores[i]):
                                                luta.mensagem.append(mensagem)
                                        elif(funcao == Data.Rolle):
                                            derivadas = []

                                            for inimigo in jogo.inimigosNaLuta:
                                                if(inimigo.vida > 0):
                                                    if inimigo.tipo == Data.tipoEntidade["Derivada"]:
                                                        derivadas.append(inimigo)
                                            
                                            hpIgual = []
                                            for i in range(0, len(derivadas)):
                                                for k in range(0, len(derivadas)):
                                                    if(i != k):
                                                        if(derivadas[i].vida == derivadas[k].vida):
                                                            hpIgual.append(derivadas[i])
                                                            break

                                            danoExtra = []

                                            if(len(hpIgual) > 0):
                                                for inimigo in hpIgual:
                                                    danoExtra.append( int((inimigo.vidaMaxima - inimigo.vida)))


                                            for mensagem in funcao(hpIgual, danoExtra * int((jogo.jogador.danoGuardado + jogo.jogador.dano) / 10 )):
                                                luta.mensagem.append(mensagem)

                                        elif(funcao == Data.Taylor):
                                            derivadas = 0

                                            for inimigo in jogo.inimigosNaLuta:
                                                if(inimigo.vida > 0):
                                                    if inimigo.tipo == Data.tipoEntidade["Derivada"]:
                                                        derivadas += 1

                                            for mensagem in funcao([jogo.jogador], derivadas):
                                                luta.mensagem.append(mensagem)    
                                                                       
                                        else:
                                            for mensagem in funcao([jogo.jogador], jogo.jogador.habilidades[luta.habilidadeSelecionada].valores[i]):
                                                luta.mensagem.append(mensagem)

                                        i += 1

                                jogo.jogador.energia -= jogo.jogador.habilidades[luta.habilidadeSelecionada].valores[0]
                                luta.estadoLuta = luta.EEstadoLuta.PROCESSANDOTURNO
                                luta.esperandoInput = True

                        elif(jogo.ultimoInput == 6):
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()
                            luta.estadoLuta = luta.EEstadoLuta.LUTANDO
                else:
                    if(time.time() - jogo.ultimoMovimentoBotao > 0.3):
                        if(jogo.ultimoInput == 1):
                            CalcularLutaHabilidadeSelecionada(1)
                            luta.mensagem.clear()
                            luta.mensagem = jogo.jogador.habilidades[luta.habilidadeSelecionada].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time() - 0.25

                        elif(jogo.ultimoInput == 2): 
                            CalcularLutaHabilidadeSelecionada(-1)
                            luta.mensagem.clear()
                            luta.mensagem = jogo.jogador.habilidades[luta.habilidadeSelecionada].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time() - 0.25
                    
            RenderizarLuta()
            DesenharLutaJanelaHabilidades() 
            DesenharLutaHabilidadeSelecionada()
            DesenharHabilidades()
            DesenharLutaLog()
            EscreverLutaLog(luta.mensagem)

        elif(luta.estadoLuta == luta.EEstadoLuta.ESCOLHENDOITEM):

            if((time.time() - jogo.ultimoMovimentoBotao > 0.05 and jogo.botaoSolto) or jogo.ultimoInput != jogo.ultimoInputAnterior):
                if(jogo.botaoSolto):
                    
                        if(jogo.ultimoInput == 1):

                            CalcularLutaItemSelecionado(1)
                            luta.mensagem.clear()
                            if(len(jogo.jogador.items)):
                                luta.mensagem = jogo.jogador.items[luta.itemSelecionado].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()


                        elif(jogo.ultimoInput == 2):
                            
                            CalcularLutaItemSelecionado(-1)
                            luta.mensagem.clear()
                            if(len(jogo.jogador.items)):
                                luta.mensagem = jogo.jogador.items[luta.itemSelecionado].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()

                        elif(jogo.ultimoInput == 5):
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()
                            luta.mensagem.clear()


                            i = 1
                            for funcao in jogo.jogador.items[luta.itemSelecionado].funcs:
                                if(jogo.jogador.items[luta.itemSelecionado].temAlvo):
                                    pass
                                else:
                                    for mensagem in funcao([jogo.jogador], jogo.jogador.items[luta.itemSelecionado].valores[i]):
                                        luta.mensagem.append(mensagem)

                                    i += 1

                            jogo.jogador.items[luta.itemSelecionado].quantidade -= 1
                            if(jogo.jogador.items[luta.itemSelecionado].quantidade <= 0):
                                jogo.jogador.items.pop(luta.itemSelecionado)

                            luta.estadoLuta = luta.EEstadoLuta.PROCESSANDOTURNO
                            luta.esperandoInput = True

                        elif(jogo.ultimoInput == 6):
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time()
                            luta.estadoLuta = luta.EEstadoLuta.LUTANDO
                else:
                    if(time.time() - jogo.ultimoMovimentoBotao > 0.3):
                        if(jogo.ultimoInput == 1):
                            CalcularLutaItemSelecionado(1)
                            luta.mensagem.clear()
                            if(len(jogo.jogador.items)):
                                luta.mensagem = jogo.jogador.habilidades[luta.habilidadeSelecionada].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time() - 0.25

                        elif(jogo.ultimoInput == 2): 
                            CalcularLutaItemSelecionado(-1)
                            luta.mensagem.clear()
                            if(len(jogo.jogador.items)):
                                luta.mensagem = jogo.jogador.habilidades[luta.habilidadeSelecionada].desc.copy()
                            jogo.botaoSolto = False
                            jogo.ultimoMovimentoBotao = time.time() - 0.25
                    

            RenderizarLuta()
            DesenharLutaJanelaHabilidades() 
            DesenharLutaHabilidadeSelecionada()
            DesenharItems()
            DesenharLutaLog()
            EscreverLutaLog(luta.mensagem)



        elif(luta.estadoLuta == luta.EEstadoLuta.PROCESSANDOTURNO):

            if(time.time() - luta.ultimoTurno > 1 and not luta.esperandoInput):
                luta.mensagem.clear()
                end = True
                for inimigo in jogo.inimigosNaLuta:
                    if(inimigo.vida > 0):
                        end = False

                if(not end):
                    luta.PassoTurno()
                    luta.ProcessarTurno(jogo.jogador)
                    luta.ultimoTurno = time.time()
                    if(jogo.jogador.vida <= 0):
                        GameOver()
                else:
                    luta.mensagem.clear()
                    jogo.botaoSolto = False
                    jogo.ultimoMovimentoBotao = time.time()
                    luta.mensagem.append("Vitória!")
                    xp = 0
                    for inimigo in jogo.inimigosNaLuta:
                        xp += inimigo.xpDado

                    luta.mensagem.append("Ganhou " + str(xp) + " de XP!")
                    if(jogo.jogador.GanharXP(xp)):
                        luta.mensagem.append("Subiu para o level " + str(jogo.jogador.level) + "!")
                    
                    luta.estadoLuta = luta.EEstadoLuta.RESULTADO
                    

            RenderizarLuta()
            DesenharLutaLog()
            EscreverLutaLog(luta.mensagem)

            if(luta.esperandoInput and time.time() - jogo.ultimoMovimentoBotao > 0.2 and jogo.botaoSolto):
                if(jogo.ultimoInput == 5):

                    if(len(luta.mensagem) <= 2):
                        luta.esperandoInput = False
                        jogo.botaoSolto = False
                        jogo.ultimoMovimentoBotao = time.time()
                        luta.ultimoTurno = 0
                    else:
                        luta.mensagem.pop(0)
                        luta.mensagem.pop(0)
                        jogo.ultimoMovimentoBotao = time.time()
                        jogo.botaoSolto = False


        elif(luta.estadoLuta == luta.EEstadoLuta.RESULTADO):
            if(jogo.ultimaLuta):
                luta.estadoLuta = luta.EEstadoLuta.ANIMACAO
                luta.estadoAnimacao = 999
            else:
                if(time.time() - jogo.ultimoMovimentoBotao > 0.1 and jogo.botaoSolto):
                    if(jogo.ultimoInput == 5):
                        if(len(luta.mensagem) <= 2):
                            luta.AcabarLuta()
                        else:
                            luta.mensagem.pop(0)
                            luta.mensagem.pop(0)
                            jogo.ultimoMovimentoBotao = time.time()
                            jogo.botaoSolto = False
        

                RenderizarLuta()
                DesenharLutaLog()
                EscreverLutaLog(luta.mensagem)

        elif(luta.estadoLuta == luta.EEstadoLuta.FIM):
            jogo.SalvarJogo()
            jogo.estadoJogo = jogo.ultimoEstadoJogo



    jogo.numeroFrames += 1
    
    janela.update()

    jogo.ultimoInputAnterior = jogo.ultimoInput

    if(jogo.segundo > 1):

        print(jogo.numeroFrames)
        print(jogo.jogador.quests[2])
      # print(f"Direção: {jogo.jogador.direcao}")
        jogo.numeroFrames = 0
        jogo.segundo -= 1



def ComecarLuta():
        PrepararLuta()
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.LUTA
        luta.estadoLuta = luta.EEstadoLuta.ANIMACAO
        luta.estadoAnimacao = 0

def RenderizarLuta():

    
    DesenharLutaHUD()
    DesenharInimigos()
    DesenharLutaBotoes()
    
def DesenharLutaJanelaHabilidades():
    jogo.lutaHUD.habilidadeMenuBackground.draw()

def DesenharLutaHabilidadeSelecionada():
    if(jogo.lutaHUD.itemSelecionadoAparecendo):
        if(jogo.lutaHUD.itemSelecionado.image.get_alpha() >= 240):
            jogo.lutaHUD.itemSelecionadoAparecendo = False

        jogo.lutaHUD.itemSelecionado.image.set_alpha(jogo.lutaHUD.itemSelecionado.image.get_alpha() + 500 * jogo.deltaTime)
    else:
        if(jogo.lutaHUD.itemSelecionado.image.get_alpha() <= 30):
            jogo.lutaHUD.itemSelecionadoAparecendo = True

        jogo.lutaHUD.itemSelecionado.image.set_alpha(jogo.lutaHUD.itemSelecionado.image.get_alpha() - 500 * jogo.deltaTime)

    jogo.lutaHUD.itemSelecionado.draw()


    
def CalcularLutaHabilidadeSelecionada(passo):
    if(passo == -1):
        luta.habilidadeSelecionada = min(luta.habilidadeSelecionada + 1, len(jogo.jogador.habilidades) - 1)
    elif(passo == 1):
        luta.habilidadeSelecionada = max(luta.habilidadeSelecionada - 1, 0)

    jogo.lutaHUD.itemSelecionado.set_position(janela.width * 0.81, janela.height * 0.54 + (luta.habilidadeSelecionada * janela.height * 0.05))

def CalcularLutaItemSelecionado(passo):
    if(passo == -1):
        luta.itemSelecionado = min(luta.itemSelecionado + 1, len(jogo.jogador.items) - 1)
    elif(passo == 1):
        luta.itemSelecionado = max(luta.itemSelecionado - 1, 0)

    jogo.lutaHUD.itemSelecionado.set_position(janela.width * 0.81, janela.height * 0.54 + (luta.itemSelecionado * janela.height * 0.05))


def DesenharHabilidades():


    for i in range(0, 10):

    
            if i < len(jogo.jogador.habilidades):


            
                janela.draw_text(jogo.jogador.habilidades[i].nome, janela.width * 0.82, janela.height * 0.55 + (i * janela.height * 0.05), "Sprites/HUD/PressStart2P-Regular.ttf", 13 * int((1280/janela.width)), (255,255,255), )
                janela.draw_text(str(jogo.jogador.habilidades[i].valores[0]), janela.width * 0.96, janela.height * 0.55 + (i * janela.height * 0.05), "Sprites/HUD/PressStart2P-Regular.ttf", 13 * int((1280/janela.width)), (255,255,255), )
           
            else:
                janela.draw_text("--------------" , janela.width * 0.82, janela.height * 0.55 + (i * janela.height * 0.05), "Sprites/HUD/PressStart2P-Regular.ttf", 13 * int((1280/janela.width)), (255,255,255), )


def DesenharItems():
    for i in range(0, 10):
            if i < len(jogo.jogador.items):
                janela.draw_text(jogo.jogador.items[i].nome, janela.width * 0.82, janela.height * 0.55 + (i * janela.height * 0.05), "Sprites/HUD/PressStart2P-Regular.ttf", 13 * int((1280/janela.width)), (255,255,255), )
                janela.draw_text(str(jogo.jogador.items[i].quantidade), janela.width * 0.96, janela.height * 0.55 + (i * janela.height * 0.05), "Sprites/HUD/PressStart2P-Regular.ttf", 13 * int((1280/janela.width)), (255,255,255), )
           
            else:
                janela.draw_text("--------------" , janela.width * 0.82, janela.height * 0.55 + (i * janela.height * 0.05), "Sprites/HUD/PressStart2P-Regular.ttf", 13 * int((1280/janela.width)), (255,255,255), )



def RenderizarMapa():

        #dar update em 60 frames
    if(jogo.ultimoDraw > 0.016):

        janela.get_screen().fill((100, 100, 100)) # cinza
        pygame.draw.rect(janela.get_screen(), (214, 211, 209), (0, 0, janela.width, janela.height/2)) #teto
        pygame.draw.rect(janela.get_screen(), (130, 120, 109), (0, janela.height, janela.width, janela.height)) #chão



        Mapa.RenderizarMapa3DLowPoly2(jogo.janelaMenor, jogo.GAME_HEIGHT, jogo.GAME_WIDTH, jogo.jogador)
        scaled_surface = pygame.transform.scale(jogo.janelaMenor, (janela.width , janela.height))
    

        janela.get_screen().blit(scaled_surface, (0, 0))


        Mapa.RenderizarMapa3D(janela, jogo.jogador)


        DesenharHUD()
        DesenharMinimapa()

        



        jogo.ultimoDraw = 0



def ChecarColisao(novaPosicaoX, novaPosicaoY):

    if(ChecarEvento(novaPosicaoX, novaPosicaoY)):
        return True

    if(novaPosicaoX - jogo.jogador.x > 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].oeste):
            return True
        
    elif(novaPosicaoX - jogo.jogador.x < 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].leste):
            return True
        
    elif(novaPosicaoY - jogo.jogador.y < 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].norte):
            return True
        
    elif(novaPosicaoY - jogo.jogador.y > 0):
        if(Mapa.GetMapaAtual()[int(novaPosicaoY)][int(novaPosicaoX)].sul):
            return True


    return False

def Fim():
    janela.get_screen().fill((0, 0, 0)) 
    janela.draw_text("Fim", janela.width * 0.5, janela.height * 0.5, "Sprites/HUD/PressStart2P-Regular.ttf", 50 * int((1280/janela.width)), (255,255,255), )

def ProfessorPirataDialogo():
    if(jogo.jogador.habilidades.count(Data.habilidadeBD[2]) == 0):
        jogo.dialogoMensagens.append("Professor Pirata:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Yarr! Escondi um tesouro neste andar!")
        jogo.dialogoMensagens.append("3 S 4 O 4 N 2 O")
        jogo.dialogoMensagens.append("É de quem primeiro achar!")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
    else:
        jogo.dialogoMensagens.append("Professor Pirata:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Yarr! Parabéns! Você é o rei dos limites!")
        jogo.dialogoMensagens.append("Não esqueça de revisar a matéria nas salas")
        jogo.dialogoMensagens.append("vazias.")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
    return True

def ProfessorProvaAndar1():
    jogo.dialogoMensagens.append("Professor Substituto:")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Eu não sei se consigo fazer exercícios")
    jogo.dialogoMensagens.append("muito legais...")
    jogo.dialogoMensagens.append("Poderia me ajudar a testar essa lista?")
    jogo.dialogoMensagens.append("Em troca, te ensino uma coisa nova.")
    jogo.escolhas.clear()
    jogo.escolhaSelecionada = 0



    jogo.escolhas.append(Data.escolhaBD[3])
    jogo.escolhas[0].imagem.Transformar(janela.width * 0.3, janela.height* 0.09)
    jogo.escolhas[0].imagem.set_position(janela.width * 0.5 - ( jogo.escolhas[0].imagem.largura / 2), janela.height * 0.35 - ( jogo.escolhas[0].imagem.altura / 2))




    jogo.escolhas.append(Data.escolhaBD[4])
    jogo.escolhas[1].imagem.Transformar(janela.width * 0.3, janela.height* 0.09)
    jogo.escolhas[1].imagem.set_position(janela.width * 0.5 - ( jogo.escolhas[1].imagem.largura / 2), janela.height * 0.5 - ( jogo.escolhas[1].imagem.altura / 2))
    
    CalcularEscolhaSelecionada(0)

    jogo.ultimoEstadoJogo = Data.EEstado.ESCOLHA
    jogo.estadoJogo = Data.EEstado.DIALOGO
    return True

def ProfessorCadeiras():
    if(jogo.jogador.quests[1] < 1):
        jogo.dialogoMensagens.append("Professor Triste:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Cade minhas cadeiras?! Como eu vou dar")
        jogo.dialogoMensagens.append("aula sem cadeiras?")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Professor Triste: ")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Por favor, me ajude a encontrar minhas")
        jogo.dialogoMensagens.append("preciosas cadeiras...")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        return True
    
    elif(jogo.jogador.quests[1] < 3):
        jogo.dialogoMensagens.append("Professor Triste:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Uma cadeira no banheiro?!")
        jogo.dialogoMensagens.append("Será que alguém escondeu elas no banheiro")
        jogo.dialogoMensagens.append("feminino? Mas eu não posso entrar lá...")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        return True
    
    elif(jogo.jogador.quests[1] == 3):
        jogo.dialogoMensagens.append("Professor Triste:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("AHH!! FOGOOOOOOO!!!")
        jogo.dialogoMensagens.append("SALVEM AS CADEIRAS!!!!")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        return True


    elif(jogo.jogador.quests[1] == 99):
        jogo.dialogoMensagens.append("Professor Feliz:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Muito obrigado!")
        jogo.dialogoMensagens.append("Ah, que cadeiras lindas...")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        return True

def EntrarBanheiroMeninas():
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Não parece ser uma boa ideia entrar aí...")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        return True

def EntrarBanheiroMeninasCadeiras():
    if(jogo.jogador.andar != 2 or jogo.jogador.quests[1] == 0 or jogo.jogador.quests[1] == 2):
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Não parece ser uma boa ideia entrar aí...")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        return True
    elif(jogo.jogador.quests[1] == 1):
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Dá pra ouvir o som de pessoas usando o")
        jogo.dialogoMensagens.append("banheiro. Melhor esperar estar vazio.")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        jogo.jogador.quests[1] = 2
        jogo.SalvarJogo()
        return True

def PegarCadeiras():
    lista_efeitos[3].play()
    jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
    jogo.fade.fading = True
    jogo.fade.alpha = 0
    jogo.fade.surface.set_alpha(0)
    jogo.estadoJogo = Data.EEstado.ANIMACAOOVERWORLD
    jogo.animacao = Data.EANIMACAOOVERWORLD.CADEIRAS

    return True

def UltimaLuta():
    jogo.dialogoMensagens.append("Professor de Cálculo:")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Hmm, já está na hora de aplicar a prova.")
    jogo.dialogoMensagens.append("Sugiro que nem façam, melhor ir pra casa,")
    jogo.dialogoMensagens.append("vocês não tem chance de passar.")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Professor de Cálculo:")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Hã? Estudou? Sabe a matéria?")
    jogo.dialogoMensagens.append("HAHAHAHAHAHAHAHAHAHA!")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Professor de Cálculo:")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Isso não tem absolutamente nada a ver")
    jogo.dialogoMensagens.append("com sua nota. Agora sente-se e se afogue")
    jogo.dialogoMensagens.append("no seu próprio desespero! Hahahahahaha!")
    jogo.dialogoMensagens.append(" ")


    jogo.inimigosNaLuta.clear()


    inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)



    inimigo = Data.IBOSS("Bixo de 7 Cabeças")




    inimigo.sprite.Transformar(int(317 * (janela.width/1920)), int(497 * (janela.height/1080)))
    largura = (inimigo.sprite.largura / 2)
    altura = (inimigo.sprite.altura / 2)


    inimigo.sprite.set_position( int( (0.5 * janela.width)  - largura), int( 0.65 * janela.height - altura )    )


    luta.estadoLuta = luta.EEstadoLuta.ANIMACAO
    luta.estadoAnimacao = 0
    jogo.ultimoEstadoJogo = Data.EEstado.LUTA
    jogo.estadoJogo = Data.EEstado.DIALOGO
    jogo.ultimaLuta = True

def ChecarEvento(novaPosicaoX, novaPosicaoY):
    evento = Mapa.GetMapaEventos()[int(novaPosicaoY)][int(novaPosicaoX)]

    if(evento != 0):
        if(evento == 1):
            if(jogo.jogador.andar < 4):
                jogo.escolhas.clear()
                jogo.escolhaSelecionada = 0


                
                jogo.escolhas.append(Data.escolhaBD[0])
                jogo.escolhas[0].imagem.Transformar(janela.width * 0.3, janela.height* 0.09)
                jogo.escolhas[0].imagem.set_position(janela.width * 0.5 - ( jogo.escolhas[0].imagem.largura / 2), janela.height * 0.35 - ( jogo.escolhas[0].imagem.altura / 2))




                jogo.escolhas.append(Data.escolhaBD[1])
                jogo.escolhas[1].imagem.Transformar(janela.width * 0.3, janela.height* 0.09)
                jogo.escolhas[1].imagem.set_position(janela.width * 0.5 - ( jogo.escolhas[1].imagem.largura / 2), janela.height * 0.5 - ( jogo.escolhas[1].imagem.altura / 2))

                if(jogo.jogador.andar > 1):

                    jogo.escolhas.append(Data.escolhaBD[2])
                    jogo.escolhas[2].imagem.Transformar(janela.width * 0.3, janela.height* 0.09)
                    jogo.escolhas[2].imagem.set_position(janela.width * 0.5 - (jogo.escolhas[2].imagem.largura / 2), janela.height * 0.65 - (jogo.escolhas[2].imagem.altura / 2))

                jogo.estadoJogo = Data.EEstado.ESCOLHA

            else:
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Sem tempo pra voltar agora.")
                jogo.dialogoMensagens.append(" ")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
            return True 
        

        elif(evento == 2):
            return ProfessorPirataDialogo()
        
        elif(evento == 4):
            return ProfessorProvaAndar1()
        
        elif(evento == 6):
            return ProfessorCadeiras()
        elif(evento == 7):
            if(jogo.jogador.quests[1] == 0):
                jogo.jogador.quests[1] = 1
                jogo.SalvarJogo()

        elif(evento == 8):
            return EntrarBanheiroMeninasCadeiras()
        
        elif(evento == 9):
            return PegarCadeiras()
        

        elif(evento == 10):
            ChecarElevador()
        elif(evento == 12):
            return ProfessorListaPerdida()
        elif(evento == 13):
            if(not jogo.jogador.provas[1]):
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Hmm? Parece que tem uma folha debaixo da")
                jogo.dialogoMensagens.append("porta.")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você obteve uma folha da prova!")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
                EncontrarProva(1)
                return True
            
        elif(evento == 14):
            if((jogo.jogador.provas[0] or jogo.jogador.provas[1]) and jogo.jogador.quests[2] == 1):
                jogo.dialogoMensagens.append("Voz Do Almoxarifado: ")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append("Olá?! Tem alguém aí?")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Voz Do Almoxarifado: ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("De algum jeito eu me tranquei aqui e")
                jogo.dialogoMensagens.append("estou sem a chave! Poderia ir no primeiro")
                jogo.dialogoMensagens.append("andar pegar a chave extra?")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
                jogo.jogador.quests[2] = 2

        elif(evento == 15):
            if(jogo.jogador.quests[2] == 2):
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append("Você pegou um chaveiro cheio de chaves.")
                lista_efeitos[4].play()
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
                jogo.jogador.quests[2] = 3
            
            return True
        
        elif(evento == 16):
            if(jogo.jogador.quests[2] == 3):
                jogo.dialogoMensagens.append("Voz Do Almoxarifado: ")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append("Muito obrigado! Eu achei esse papel")
                jogo.dialogoMensagens.append("enquanto limpava, talvez você queira.")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você obteve uma folha da prova!")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
                jogo.jogador.quests[2] = 4
                EncontrarProva(2)
            
            return True
        elif(evento == 98):
            
            UltimaLuta()
            
            return True
        
        elif(evento == 99):
            
            jogo.dialogoMensagens.append("")
            jogo.dialogoMensagens.append("A prova é na última sala do corredor")
            jogo.dialogoMensagens.append("esquerdo...")
            jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
            jogo.estadoJogo = Data.EEstado.DIALOGO
            
            return True

        elif(evento == -1):
            return True
def ChecarElevador():
    if(jogo.jogador.andar < 4):
        engrenagens = 0

        if(jogo.jogador.engrenagems[0]):
            engrenagens += 1
        
        if(jogo.jogador.engrenagems[1]):
            engrenagens += 1
        if(jogo.jogador.engrenagems[2]):
            engrenagens += 1

        if(engrenagens < 3):
            jogo.dialogoMensagens.clear()
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("O elevador parece quebrado...")
            jogo.dialogoMensagens.append(" ")




        
            if(engrenagens == 1):
                jogo.dialogoMensagens.append("Tem mais duas engrenagens faltando...")
            elif(engrenagens == 2):
                jogo.dialogoMensagens.append("Tem mais uma engrenagem faltando...")

            jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
            jogo.estadoJogo = Data.EEstado.DIALOGO

        else:
            lista_efeitos[1].play()
            jogo.jogador.andar = 4
            jogo.animacao = Data.EANIMACAOOVERWORLD.MUDARANDAR
            jogo.fade.fading = True
            jogo.fade.alpha = 0
            jogo.fade.surface.set_alpha(0)
            jogo.mapaAtual = Mapa.GerarMapa(jogo.jogador.andar, jogo)
            jogo.estadoJogo = Data.EEstado.ANIMACAOOVERWORLD

    else:
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Sem tempo pra voltar agora.")
            jogo.dialogoMensagens.append(" ")
            jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
            jogo.estadoJogo = Data.EEstado.DIALOGO

def CalcularEscolhaSelecionada(passo):
    if(passo == -1):
        jogo.escolhaSelecionada = min(jogo.escolhaSelecionada + 1, len(jogo.escolhas) - 1)
    elif(passo == 1):
        jogo.escolhaSelecionada = max(jogo.escolhaSelecionada - 1, 0)

    for i, escolha in enumerate(jogo.escolhas):
        if(i == jogo.escolhaSelecionada):
            escolha.Selecionar(True)
        else:
            escolha.Selecionar(False)




def DesenharEscolhas(escolhas):
    tamanhoFonte = 20 * int((1280/janela.width))
    
    for escolha in escolhas:
       
        escolha.imagem.draw()
        janela.draw_text( escolha.desc , escolha.imagem.coordenadas[0] + (escolha.imagem.largura / 2) - (tamanhoFonte * len(escolha.desc) / 2), escolha.imagem.coordenadas[1] + (escolha.imagem.altura / 2) - (tamanhoFonte / 2) , "Sprites/HUD/PressStart2P-Regular.ttf", tamanhoFonte, (212,219,170), )


def AndarJogadorLoop(jogador, andandoDestino, inicioJogador, velocidade):
    
    if(andandoDestino[1] == jogador.y):
        jogador.x += (andandoDestino[0] - inicioJogador.x) * velocidade * min(0.1, jogo.deltaTime)
    elif(andandoDestino[0] == jogador.x):
        jogador.y += (andandoDestino[1] - inicioJogador.y) * velocidade * min(0.1, jogo.deltaTime)

def AndarJogador(ultimoInput):

    passo = 0

    if(ultimoInput == 1):
        passo = 1

        
    elif(ultimoInput == 2):
        passo = -1


    if(passo != 0):
        #norte
        if(jogo.jogador.dirX == 0 and jogo.jogador.dirY == 1):
            if(not ChecarColisao(jogo.jogador.x, (jogo.jogador.y + passo))):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x
                jogo.andandoDestino[1] = jogo.jogador.y + passo
                return True
        #sul
        elif(jogo.jogador.dirX == 0 and jogo.jogador.dirY == -1 ):
            if(not ChecarColisao(jogo.jogador.x, (jogo.jogador.y - passo))):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x
                jogo.andandoDestino[1] = jogo.jogador.y - passo
                return True
        #leste
        if(jogo.jogador.dirX == 1 and jogo.jogador.dirY == 0):
            if(not ChecarColisao(jogo.jogador.x + passo, jogo.jogador.y)):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x + passo
                jogo.andandoDestino[1] = jogo.jogador.y
                return True
        #oeste
        elif(jogo.jogador.dirX == -1 and jogo.jogador.dirY == 0 ):
            if(not ChecarColisao(jogo.jogador.x - passo, jogo.jogador.y)):
                jogo.inicioJogador = jogo.jogador

                jogo.andandoDestino[0] = jogo.jogador.x - passo
                jogo.andandoDestino[1] = jogo.jogador.y
                return True


def AtualizarDirecaoJogador(input):

    if(input == 3):
        if(jogo.jogador.direcao == Data.direcao["O"]):
            jogo.jogador.direcao = Data.direcao["N"]
        else:
            jogo.jogador.direcao += 1
    elif(input == 4):
        if(jogo.jogador.direcao == Data.direcao["N"]):
            jogo.jogador.direcao = Data.direcao["O"]
        else:
            jogo.jogador.direcao -= 1

#virar aos poucos pra ficar bonitinho
def VirarJogadorLoop(ultimaDirecaoX, ultimaDirecaoY):

    # print("Ultima direção X:  " + str(ultimaDirecaoX))
    # print("jogador.dirX:  " + str(jogador.dirX))

    VirarJogador(jogo.rodandoDirecao, ultimaDirecaoX, ultimaDirecaoY)

    jogo.ultimaRotacao = time.time()
    




    




def VirarJogador(direcao, ultimaDirecaoX, ultimaDirecaoY):
    #direita

    
    if(direcao == 1):
       
        oldDirX = jogo.jogador.dirX


        jogo.jogador.dirX = jogo.jogador.dirX * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.dirY * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.dirY = oldDirX * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.dirY * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime))

        oldPlaneX = jogo.jogador.planeX
        jogo.jogador.planeX = jogo.jogador.planeX * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.planeY * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.planeY = oldPlaneX * math.sin(-jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.planeY * math.cos(-jogo.velRotacao * min(0.1, jogo.deltaTime))







    elif(direcao == 2):


        oldDirX = jogo.jogador.dirX
        jogo.jogador.dirX = jogo.jogador.dirX * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.dirY * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.dirY = oldDirX * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.dirY * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime))

        oldPlaneX = jogo.jogador.planeX
        jogo.jogador.planeX = jogo.jogador.planeX * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime)) - jogo.jogador.planeY * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime))
        jogo.jogador.planeY = oldPlaneX * math.sin(jogo.velRotacao * min(0.1, jogo.deltaTime)) + jogo.jogador.planeY * math.cos(jogo.velRotacao * min(0.1, jogo.deltaTime))

    
    if(abs(ultimaDirecaoX - jogo.jogador.dirX) >= 1):
        jogo.jogador.dirX = 0
        
        #norte
        if(jogo.jogador.dirY > 0):
            jogo.jogador.dirY = 1
            jogo.jogador.planeX = 0.66
            jogo.jogador.planeY = 0.0

        #sul
        else:
            jogo.jogador.dirY = -1
            jogo.jogador.planeX = -0.66
            jogo.jogador.planeY = 0.0

        jogo.isRodando = False
        jogo.ultimaRotacao = time.time() + jogo.cooldownRodar

    elif(abs(ultimaDirecaoY - jogo.jogador.dirY) >= 1):
        jogo.jogador.dirY = 0
        
        #leste
        if(jogo.jogador.dirX > 0):
            jogo.jogador.dirX = 1
            jogo.jogador.planeX = 0
            jogo.jogador.planeY = -0.66

        #oeste
        else:
            jogo.jogador.dirX = -1
            jogo.jogador.planeX = 0.0
            jogo.jogador.planeY = 0.66

        jogo.isRodando = False
        jogo.ultimaRotacao = time.time() + jogo.cooldownRodar



def DesenharHUD():

    jogo.jogadorHUD.background.draw()
    jogo.jogadorHUD.barraHPBackground.draw()
    jogo.jogadorHUD.barraHP.Transformar((janela.width * 0.2) * min(1, (jogo.jogador.vida / jogo.jogador.vidaMaxima)), janela.height* 0.03)
    jogo.jogadorHUD.barraHP.draw()

    jogo.jogadorHUD.barraEnergiaBackground.draw()
    jogo.jogadorHUD.barraEnergia.Transformar((janela.width * 0.2) * min(1, (jogo.jogador.energia / jogo.jogador.energiaMaxima)), janela.height* 0.03)
    jogo.jogadorHUD.barraEnergia.draw()

    jogo.jogadorHUD.jogadorSprite.draw()
 

    janela.draw_text("Vida:    " + str(jogo.jogador.vida) + " / " + str(jogo.jogador.vidaMaxima), janela.width * 0.18, janela.height * 0.89, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )
    janela.draw_text("Energia: " + str(jogo.jogador.energia)+ " / " + str(jogo.jogador.energiaMaxima), janela.width * 0.42, janela.height * 0.89, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )

    janela.draw_text("Level: " + str(jogo.jogador.level), janela.width * 0.72, janela.height * 0.9, "Sprites/HUD/PressStart2P-Regular.ttf", 14 * int((1280/janela.width)), (63,78,182), )
    janela.draw_text("XP: " + str(jogo.jogador.xp)+ " / " + str(Data.xpProximoLevel[jogo.jogador.level]), janela.width * 0.72, janela.height * 0.95, "Sprites/HUD/PressStart2P-Regular.ttf", 10 * int((1280/janela.width)), (255,255,255), )
    
    janela.draw_text(str(jogo.jogador.andar), janela.width * 0.83, janela.height * 0.93, "Sprites/HUD/PressStart2P-Regular.ttf", 16 * int((1280/janela.width)), (255,255,255), )


def DesenharDialogo():

    jogo.jogadorHUD.logBG.draw()

def AtualizarHUD():
    jogo.jogadorHUD.background.Transformar(janela.width, janela.height* 0.3)
    jogo.jogadorHUD.background.set_position(0, janela.height - (janela.height* 0.3))

    jogo.jogadorHUD.barraHPBackground.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogo.jogadorHUD.barraHPBackground.set_position(janela.width * 0.18, janela.height * 0.925)

    jogo.jogadorHUD.barraHP.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogo.jogadorHUD.barraHP.set_position(janela.width * 0.18, janela.height * 0.925)


    jogo.jogadorHUD.barraEnergiaBackground.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogo.jogadorHUD.barraEnergiaBackground.set_position(janela.width * 0.42, janela.height * 0.925)

    jogo.jogadorHUD.barraEnergia.Transformar(janela.width * 0.2, janela.height* 0.03)
    jogo.jogadorHUD.barraEnergia.set_position(janela.width * 0.42, janela.height * 0.925)



def DesenharLutaHUD():
    jogo.lutaHUD.background.draw()


    for inimigo in jogo.inimigosNaLuta:
        if(inimigo.vida > 0):
            inimigo.barraHPBackground.Transformar(janela.width * 0.1, janela.height* 0.02)
            inimigo.barraHPBackground.set_position(inimigo.sprite.x + (inimigo.barraHPBackground.largura / 2), inimigo.sprite.y - inimigo.barraHPBackground.altura)
            inimigo.barraHPBackground.draw()

            inimigo.barraHP.Transformar((janela.width * 0.1) * min(1, (inimigo.vida / inimigo.vidaMaxima)), janela.height* 0.02)
            inimigo.barraHP.set_position(inimigo.sprite.x + (inimigo.barraHPBackground.largura / 2), inimigo.sprite.y - inimigo.barraHP.altura)
            inimigo.barraHP.draw()


    jogo.jogadorHUD.barraHPBackground.Transformar(janela.width * 0.1, janela.height* 0.02)
    jogo.jogadorHUD.barraHPBackground.set_position(janela.width * 0.3, janela.height * 0.95)

    jogo.jogadorHUD.barraHP.Transformar((janela.width * 0.1) * min(1, (jogo.jogador.vida / jogo.jogador.vidaMaxima)), janela.height* 0.02)
    jogo.jogadorHUD.barraHP.set_position(janela.width * 0.3, janela.height * 0.95)


    jogo.jogadorHUD.barraEnergiaBackground.Transformar(janela.width * 0.1, janela.height* 0.02)
    jogo.jogadorHUD.barraEnergiaBackground.set_position(janela.width * 0.6, janela.height * 0.95)

    jogo.jogadorHUD.barraEnergia.Transformar((janela.width * 0.1) * min(1, (jogo.jogador.energia / jogo.jogador.energiaMaxima)), janela.height* 0.02)
    jogo.jogadorHUD.barraEnergia.set_position(janela.width * 0.6, janela.height * 0.95)

    jogo.jogadorHUD.barraHPBackground.draw()
    jogo.jogadorHUD.barraHP.draw()
    jogo.jogadorHUD.barraEnergiaBackground.draw()
    jogo.jogadorHUD.barraEnergia.draw()

    janela.draw_text("Vida: " + str(jogo.jogador.vida) + " / " + str(jogo.jogador.vidaMaxima), janela.width * 0.3, janela.height * 0.94, "Sprites/HUD/PressStart2P-Regular.ttf", 8 * int((1280/janela.width)), (255,255,255), )
    janela.draw_text("Energia: " + str(jogo.jogador.energia)+ " / " + str(jogo.jogador.energiaMaxima), janela.width * 0.6, janela.height * 0.94, "Sprites/HUD/PressStart2P-Regular.ttf", 8 * int((1280/janela.width)), (255,255,255), )

def ComparaInimigos(a, b):
    if(a == 2):
        return -1
    elif(a == 0 and b != 2):
        return -1
    elif(a == 1 and b != 0 and b != 2):
        return -1
    elif(a == 3):
        return 1

    return 1

def CalcularSelecionarAlvo(passo):
    inimigosVivos = []
    for i, inimigo in enumerate(jogo.inimigosNaLuta):
        if(inimigo.vida > 0):
            inimigosVivos.append(i)

    inimigosVivos.sort(key=cmp_to_key(ComparaInimigos))

    alvoLuta = jogo.alvoLuta
    
    if(passo != 0):
        if(passo > 0):
            alvoLuta = min(len(inimigosVivos) - 1, jogo.alvoLuta + 1)
        else:
            alvoLuta = max(0, jogo.alvoLuta - 1)
    else:
        alvoLuta = min(len(inimigosVivos) - 1, 0)

    alvoTransformado = inimigosVivos[min(len(inimigosVivos) - 1, alvoLuta)]

    if(alvoTransformado < len(jogo.inimigosNaLuta)):
        if(jogo.inimigosNaLuta[alvoTransformado].vida > 0):
            jogo.alvoLuta = alvoLuta

            jogo.lutaHUD.setaSelecionarAlvo.set_position(jogo.inimigosNaLuta[alvoTransformado].barraHPBackground.x + (jogo.inimigosNaLuta[alvoTransformado].barraHPBackground.largura / 2) - (jogo.lutaHUD.setaSelecionarAlvo.largura / 2), jogo.inimigosNaLuta[alvoTransformado].sprite.y - jogo.lutaHUD.setaSelecionarAlvo.altura * 2)

    return alvoTransformado


def DesenharAlvoHUD():
    jogo.lutaHUD.setaSelecionarAlvo.draw()


def DesenharLutaLog():
    jogo.lutaHUD.logBG.draw()

def EscreverLutaLog(mensagens):
    tamanho = 20

    for i, mensagem in enumerate(mensagens[:2]):
        if(len(mensagem) > 40):
            tamanho = 10
        elif(len(mensagem) > 35):
            tamanho = 14
        elif(len(mensagem) > 30):
            tamanho = 15
        else:
            tamanho = 18
            
        janela.draw_text(mensagem,  jogo.lutaHUD.logBG.x + (jogo.lutaHUD.logBG.width * 0.01),  jogo.lutaHUD.logBG.y + (janela.height * 0.03 + (i * janela.height * 0.035)), "Sprites/HUD/PressStart2P-Regular.ttf", tamanho * int((1280/janela.width)), (255,255,255), )

def EscreverDialogo(mensagens):
    tamanho = 20

    for i, mensagem in enumerate(mensagens[:6]):
            
        janela.draw_text(mensagem,  jogo.jogadorHUD.logBG.x + (jogo.jogadorHUD.logBG.width * 0.01),  jogo.jogadorHUD.logBG.y + (janela.height * 0.03 + (i * janela.height * 0.035)), "Sprites/HUD/PressStart2P-Regular.ttf", tamanho * int((1280/janela.width)), (255,255,255), )


def DesenharLutaBotoes():


    #não olhe...
    ultimoDraw = 0
    if jogo.botaoSelecionadoLuta.value == 1 and jogo.botaoAntigo.value == 4:
        ultimoDraw = 2
    elif jogo.botaoSelecionadoLuta.value == 1 and jogo.botaoAntigo.value == 2:
        ultimoDraw = 3
    elif jogo.botaoSelecionadoLuta.value == 2 and jogo.botaoAntigo.value == 1:
        ultimoDraw = 3
    elif jogo.botaoSelecionadoLuta.value == 2 and jogo.botaoAntigo.value == 3:
        ultimoDraw = 0
    elif jogo.botaoSelecionadoLuta.value == 3 and jogo.botaoAntigo.value == 2:
        ultimoDraw = 0
    elif jogo.botaoSelecionadoLuta.value == 3 and jogo.botaoAntigo.value == 4:
        ultimoDraw = 1
    elif jogo.botaoSelecionadoLuta.value == 4 and jogo.botaoAntigo.value == 3:
        ultimoDraw = 1
    elif jogo.botaoSelecionadoLuta.value == 4 and jogo.botaoAntigo.value == 1:
        ultimoDraw = 2


    jogo.botoesLuta[ultimoDraw].draw()

    for i, button in enumerate(jogo.botoesLuta):


        if i != ultimoDraw:
            button.draw()


    


def CalcularBotoesLuta():

    jogo.lutaHUD.bItem.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 3) % 4][0], jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 3) % 4][1])
    jogo.lutaHUD.bAtacar.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 2) % 4][0], jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 2) % 4][1])
    jogo.lutaHUD.bHabilidade.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 1) % 4][0],jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value + 1) % 4][1] )
    jogo.lutaHUD.bFugir.set_position(jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value) % 4][0], jogo.posicoesBotoesLuta[(jogo.botaoSelecionadoLuta.value) % 4][1] )
   
   




def DesenharInimigos():
   


    ordemDesenhar = []
    for inimigo in jogo.inimigosNaLuta:
        if(inimigo.vida > 0):
            if(inimigo.tipo == Data.tipoEntidade["Limite"] or inimigo.tipo == Data.tipoEntidade["Derivada"] or Data.tipoEntidade["Integral"]):

                    ordemDesenhar.insert(0, inimigo)


    for inimigo in ordemDesenhar:
        inimigo.sprite.draw()


def PrepararLuta():


    jogo.inimigosNaLuta.clear()
    jogo.inimigosNaLuta = luta.CalcularInimigos(Data.EANDAR.EANDAR1)

    i = 0

    for inimigo in jogo.inimigosNaLuta:
        if(inimigo.vida > 0):
            if(inimigo.tipo == Data.tipoEntidade["Limite"]):
                    inimigo.sprite.Transformar(int(317 * (janela.width/1920)), int(497 * (janela.height/1080)))
                    largura = (inimigo.sprite.largura / 2)
                    altura = (inimigo.sprite.altura / 2)

                    if(i == 0):
                        inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.65 * janela.height - altura )    )
                    
                    elif(i == 1):
                        inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.65 * janela.height  - altura)    )

                    elif(i == 2):
                        inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.55 * janela.height - altura )    )
                    
                    elif(i == 3):
                        inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.55 * janela.height - altura )    )


            elif(inimigo.tipo == Data.tipoEntidade["Derivada"]):
                    inimigo.sprite.Transformar(int(415 * (janela.width/1920)), int(547 * (janela.height/1080)))
                    largura = (inimigo.sprite.largura / 2)
                    altura = (inimigo.sprite.altura / 2)

                    if(i == 0):
                        inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.65 * janela.height - altura )    )
                    
                    elif(i == 1):
                        inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.65 * janela.height  - altura)    )

                    elif(i == 2):
                        inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.55 * janela.height - altura )    )
                    
                    elif(i == 3):
                        inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.55 * janela.height - altura )    )

            elif(inimigo.tipo == Data.tipoEntidade["Integral"]):
                    inimigo.sprite.Transformar(int(451 * (janela.width/1920)), int(187 * (janela.height/1080)))
                    largura = (inimigo.sprite.largura / 2)
                    altura = (inimigo.sprite.altura / 2)

                    if(i == 0):
                        inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.80 * janela.height - altura )    )
                    
                    elif(i == 1):
                        inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.80 * janela.height  - altura)    )

                    elif(i == 2):
                        inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.70 * janela.height - altura )    )
                    
                    elif(i == 3):
                        inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.70 * janela.height - altura )    )

                        
        i += 1

def BebedouroCurar():
    lista_efeitos[0].play()
    jogo.jogador.Curar(jogo.jogador.vidaMaxima, jogo.jogador.energiaMaxima)

def ChecarInteracao():
    interacao = Mapa.GetMapaInteracoes()[int(jogo.jogador.y)][int(jogo.jogador.x)]
    #norte
    if(jogo.jogador.dirX == 0 and jogo.jogador.dirY == 1):
        if(interacao.norte):
            CalcularInteracao(interacao)
    #sul
    elif(jogo.jogador.dirX == 0 and jogo.jogador.dirY == -1 ):
        if(interacao.sul):
            CalcularInteracao(interacao)


    #leste
    if(jogo.jogador.dirX == 1 and jogo.jogador.dirY == 0):
        if(interacao.leste):
            CalcularInteracao(interacao)


    #oeste

    elif(jogo.jogador.dirX == -1 and jogo.jogador.dirY == 0 ):
        if(interacao.oeste):
            CalcularInteracao(interacao)


def PegarTesouro():
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Tem uma pequena caixa debaixo da")
    jogo.dialogoMensagens.append("carteira... ")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append(" ")
    jogo.dialogoMensagens.append("Jogador aprendeu: Preparação!")
    jogo.jogador.AprenderHabilidade(Data.habilidadeBD[2])
    jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
    jogo.estadoJogo = Data.EEstado.DIALOGO
    jogo.SalvarJogo()

def PegarEngrenagem(andar):

    jogo.jogador.engrenagems[andar - 1] = True

def AlarmeIncendio():
    if(jogo.jogador.andar != 2 or jogo.jogador.quests[1] < 2):
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Quebrar isso causaria uma confusão.")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO

    elif(jogo.jogador.andar == 2 and jogo.jogador.quests[1] == 2):
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Quebrar isso causaria uma confusão.")

        jogo.escolhas.clear()
        jogo.escolhaSelecionada = 0



        jogo.escolhas.append(Data.escolhaBD[5])
        jogo.escolhas[0].imagem.Transformar(janela.width * 0.3, janela.height* 0.09)
        jogo.escolhas[0].imagem.set_position(janela.width * 0.5 - ( jogo.escolhas[0].imagem.largura / 2), janela.height * 0.35 - ( jogo.escolhas[0].imagem.altura / 2))




        jogo.escolhas.append(Data.escolhaBD[1])
        jogo.escolhas[1].imagem.Transformar(janela.width * 0.3, janela.height* 0.09)
        jogo.escolhas[1].imagem.set_position(janela.width * 0.5 - ( jogo.escolhas[1].imagem.largura / 2), janela.height * 0.5 - ( jogo.escolhas[1].imagem.altura / 2))
        
        CalcularEscolhaSelecionada(0)

        jogo.ultimoEstadoJogo = Data.EEstado.ESCOLHA
        jogo.estadoJogo = Data.EEstado.DIALOGO
        return True

def ProfessorListaPerdida():
    if(jogo.jogador.quests[2] <= 1):
        jogo.dialogoMensagens.append("Professor Desajeitado:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Ah meu deus, eu não consigo achar as")
        jogo.dialogoMensagens.append("provas que darei hoje!")
        jogo.dialogoMensagens.append("Eu tenho certeza que estavam comigo...")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Professor Desajeitado:")
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("E agora, o que é que eu faço?")
        jogo.jogador.quests[2] = 1
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO
        jogo.SalvarJogo()
    else:
        if(jogo.jogador.quests[2] < 99):
            paginas = 0
            if(jogo.jogador.provas[0]):
                    paginas +=1

            if(jogo.jogador.provas[1]):
                    paginas +=1

            if(jogo.jogador.provas[2]):     
                    paginas +=1   
            
            if(paginas == 0):
                jogo.dialogoMensagens.append("Professor Desajeitado:")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Ah meu deus, eu não consigo achar as")
                jogo.dialogoMensagens.append("provas que darei hoje!")
                jogo.dialogoMensagens.append("Eu tenho certeza que estavam comigo...")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Professor Desajeitado:")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("E agora, o que é que eu faço?")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO

            elif(paginas == 1):
                jogo.dialogoMensagens.append("Professor Desajeitado:")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você achou uma página? Eu ainda tenho")
                jogo.dialogoMensagens.append("esperanças! Por favor, encontre o resto!")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO

            elif(paginas == 2):
                jogo.dialogoMensagens.append("Professor Desajeitado:")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você achou duas páginas? Meu herói!")
                jogo.dialogoMensagens.append("Só falta uma!")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO        

            elif(paginas == 3):
                jogo.dialogoMensagens.append("Professor Desajeitado:")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você achou todas as páginas!")
                jogo.dialogoMensagens.append("Muito obrigado! Você merece um")
                jogo.dialogoMensagens.append("prêmio!")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Professor Desajeitado:")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Onde foi que eu botei mesmo...?")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append("Ué...")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Professor Desajeitado:")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Ah, que tal essa engrenagem que")
                jogo.dialogoMensagens.append("acabei de achar?")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você encontrou uma engrenagem!")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
                jogo.jogador.quests[2] = 99
                PegarEngrenagem(2)
                jogo.SalvarJogo()
        else:
            jogo.dialogoMensagens.append("Professor Desajeitado:")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Já já tenho que aplicar essa prova.")
            jogo.dialogoMensagens.append("Deixa eu ver que horas são...")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Ué, cadê meu celular?")
            jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
            jogo.estadoJogo = Data.EEstado.DIALOGO        

    return True

def EncontrarProva(num):
    jogo.jogador.provas[num] = True
    jogo.SalvarJogo()

def CriarAula(andar, aula):
    if(andar == 1):
            jogo.inimigosNaLuta.clear()

            for i in range(0, aula + 1):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Limite"]):
                        nlimite += 1

                inimigo = Data.ILimite("Limite " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)



            jogo.estadoJogo = Data.EEstado.LUTA
            luta.estadoLuta = luta.EEstadoLuta.ANIMACAO
            luta.estadoAnimacao = 0
            jogo.dialogoMensagens.append("Conteúdo revisado!")
            jogo.ultimoEstadoJogo = Data.EEstado.DIALOGO

    elif(andar == 2):
        
        jogo.inimigosNaLuta.clear()

        if(aula == 0):

            for i in range(0, aula + 1):
                inimigo = Data.ILimite("Limite")
                jogo.inimigosNaLuta.append(inimigo)


                inimigo = Data.IDerivada("Derivada")

                jogo.inimigosNaLuta.append(inimigo)

        elif(aula == 1):

            for i in range(0, aula + 1):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Derivada"]):
                        nlimite += 1

                inimigo = Data.IDerivada("Derivada " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)

        elif(aula == 2):

            for i in range(0, aula):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Derivada"]):
                        nlimite += 1

                inimigo = Data.IDerivada("Derivada " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)

            inimigo = Data.ILimite("Limite")
            jogo.inimigosNaLuta.append(inimigo)

        elif(aula == 3 or aula == 4):

            for i in range(0, aula):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Derivada"]):
                        nlimite += 1

                inimigo = Data.IDerivada("Derivada " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)

        elif(aula == 5):
            for i in range(0, 3):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Derivada"]):
                        nlimite += 1

                inimigo = Data.IDerivada("Derivada " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)

            inimigo = Data.ILimite("Limite ")
            jogo.inimigosNaLuta.append(inimigo)



        jogo.estadoJogo = Data.EEstado.LUTA
        luta.estadoLuta = luta.EEstadoLuta.ANIMACAO
        luta.estadoAnimacao = 0
        jogo.dialogoMensagens.append("Conteúdo revisado!")
        jogo.ultimoEstadoJogo = Data.EEstado.DIALOGO


    elif(andar == 3):
        
        jogo.inimigosNaLuta.clear()

        if(aula == 0):

            for i in range(0, aula + 1):
                inimigo = Data.IIntegral("Integral")
                jogo.inimigosNaLuta.append(inimigo)


                inimigo = Data.IDerivada("Derivada")

                jogo.inimigosNaLuta.append(inimigo)

        elif(aula == 1):

            for i in range(0, aula + 1):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Integral"]):
                        nlimite += 1

                inimigo = Data.IIntegral("Integral " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)
            
            inimigo = Data.IDerivada("Derivada" + "A")

            jogo.inimigosNaLuta.append(inimigo)
            inimigo = Data.IDerivada("Derivada" + "B")

            jogo.inimigosNaLuta.append(inimigo)

        elif(aula == 2):

            for i in range(0, aula):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Limite"]):
                        nlimite += 1

                inimigo = Data.ILimite("Limite " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)

            inimigo = Data.IIntegral("Integral" + "A")
            jogo.inimigosNaLuta.append(inimigo)
            inimigo = Data.IIntegral("Integral" + "B")
            jogo.inimigosNaLuta.append(inimigo)

        elif(aula == 3 or aula == 4):

            for i in range(0, aula):
                inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

                nlimite = 0
                for i in range(0, len( jogo.inimigosNaLuta)):
                    if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Integral"]):
                        nlimite += 1

                inimigo = Data.IIntegral("Integral " + chr(65 + nlimite))
                jogo.inimigosNaLuta.append(inimigo)


        if(aula == 5):
            inimigo = Data.IIntegral("Integral" + "A")
            jogo.inimigosNaLuta.append(inimigo)
            inimigo = Data.IIntegral("Integral" + "B")
            jogo.inimigosNaLuta.append(inimigo)
            inimigo = Data.ILimite("Limite ")
            jogo.inimigosNaLuta.append(inimigo)
            inimigo = Data.IDerivada("Derivada")

            jogo.inimigosNaLuta.append(inimigo)



        jogo.estadoJogo = Data.EEstado.LUTA
        luta.estadoLuta = luta.EEstadoLuta.ANIMACAO
        luta.estadoAnimacao = 0
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("Conteúdo revisado!")
        jogo.ultimoEstadoJogo = Data.EEstado.DIALOGO
    
    
    i = 0

    for inimigo in jogo.inimigosNaLuta:
        if(inimigo.vida > 0):
            if(inimigo.tipo == Data.tipoEntidade["Limite"]):
                    inimigo.sprite.Transformar(int(317 * (janela.width/1920)), int(497 * (janela.height/1080)))
                    largura = (inimigo.sprite.largura / 2)
                    altura = (inimigo.sprite.altura / 2)

                    if(i == 0):
                        inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.65 * janela.height - altura )    )
                    
                    elif(i == 1):
                        inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.65 * janela.height  - altura)    )

                    elif(i == 2):
                        inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.55 * janela.height - altura )    )
                    
                    elif(i == 3):
                        inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.55 * janela.height - altura )    )


            elif(inimigo.tipo == Data.tipoEntidade["Derivada"]):
                    inimigo.sprite.Transformar(int(415 * (janela.width/1920)), int(547 * (janela.height/1080)))
                    largura = (inimigo.sprite.largura / 2)
                    altura = (inimigo.sprite.altura / 2)

                    if(i == 0):
                        inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.65 * janela.height - altura )    )
                    
                    elif(i == 1):
                        inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.65 * janela.height  - altura)    )

                    elif(i == 2):
                        inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.55 * janela.height - altura )    )
                    
                    elif(i == 3):
                        inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.55 * janela.height - altura )    )

            elif(inimigo.tipo == Data.tipoEntidade["Integral"]):
                    inimigo.sprite.Transformar(int(451 * (janela.width/1920)), int(187 * (janela.height/1080)))
                    largura = (inimigo.sprite.largura / 2)
                    altura = (inimigo.sprite.altura / 2)

                    if(i == 0):
                        inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.80 * janela.height - altura )    )
                    
                    elif(i == 1):
                        inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.80 * janela.height  - altura)    )

                    elif(i == 2):
                        inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.70 * janela.height - altura )    )
                    
                    elif(i == 3):
                        inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.70 * janela.height - altura )    )


        i += 1

    jogo.jogador.aulas[andar - 1][aula] = True

    todas = True
    for aula in jogo.jogador.aulas[andar - 1]:
        if(aula == False):
            todas = False
    
    if(todas):
        if(andar == 1):
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("As revisões deram fruto...")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Você aprendeu: Concentração!")
            jogo.jogador.AprenderHabilidade(Data.habilidadeBD[0])
            jogo.ultimoEstadoJogo = Data.EEstado.DIALOGO


        elif(andar == 2):
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("As revisões deram fruto...")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Você aprendeu: Teorema de Rolle!")
            jogo.jogador.AprenderHabilidade(Data.habilidadeBD[5])
            jogo.ultimoEstadoJogo = Data.EEstado.DIALOGO


        elif(andar == 3):
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("As revisões deram fruto...")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Você aprendeu: Teorema Fundamental do Cálculo!")
            jogo.jogador.AprenderHabilidade(Data.habilidadeBD[6])
            jogo.ultimoEstadoJogo = Data.EEstado.DIALOGO


def CalcularInteracao(interacao):
    if(interacao.interacao == 1):
        if(interacao.id == 1):
            BebedouroCurar()
            jogo.SalvarJogo()

    elif(interacao.interacao == 2):
        ProfessorPirataDialogo()
    elif(interacao.interacao == 3):
        if(jogo.jogador.habilidades.count(Data.habilidadeBD[2]) == 0):
            PegarTesouro()

    elif(interacao.interacao == 4):
            ProfessorProvaAndar1()
    elif(interacao.interacao == 5):
            if(not jogo.jogador.engrenagems[0]):
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você encontrou uma engrenagem!")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
                PegarEngrenagem(1)
                jogo.SalvarJogo()

    elif(interacao.interacao == 6):
        ProfessorCadeiras()


    elif(interacao.interacao == 8):
        EntrarBanheiroMeninasCadeiras()

    elif(interacao.interacao == 9):
        AlarmeIncendio()
    elif(interacao.interacao == 10):
        ChecarElevador()
    elif(interacao.interacao == 11):
        EntrarBanheiroMeninas()
    elif(interacao.interacao == 12):
        ProfessorListaPerdida()
    elif(interacao.interacao == 13):
        if(jogo.jogador.provas[0]):
            BebedouroCurar()
            jogo.SalvarJogo()
        else:
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Hmm? Parece que tem uma folha atrás do")
            jogo.dialogoMensagens.append("bebedouro.")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append(" ")
            jogo.dialogoMensagens.append("Você obteve uma folha da prova!")
            jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
            jogo.estadoJogo = Data.EEstado.DIALOGO
            EncontrarProva(0)
            jogo.SalvarJogo()

    elif(interacao.interacao == 15):
        if(jogo.jogador.quests[2] == 2):
            jogo.dialogoMensagens.append("")
            jogo.dialogoMensagens.append("Você pegou um chaveiro cheio de chaves.")
            jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
            jogo.estadoJogo = Data.EEstado.DIALOGO
            jogo.jogador.quests[2] = 3
            jogo.SalvarJogo()
    elif(interacao.interacao == 16):
            if(jogo.jogador.quests[2] == 3):
                jogo.dialogoMensagens.append("Voz Do Almoxarifado: ")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append("Muito obrigado! Eu achei esse papel")
                jogo.dialogoMensagens.append("enquanto limpava, talvez você queira.")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append("")
                jogo.dialogoMensagens.append(" ")
                jogo.dialogoMensagens.append("Você obteve uma folha da prova!")
                jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
                jogo.estadoJogo = Data.EEstado.DIALOGO
                jogo.jogador.quests[2] = 4
                EncontrarProva(2)
                jogo.SalvarJogo()

            return True
    
    elif(interacao.interacao == 20):
        if(not jogo.jogador.aulas[0][interacao.id]):
            CriarAula(1, interacao.id)
    elif(interacao.interacao == 21):
        if(not jogo.jogador.aulas[1][interacao.id]):
            CriarAula(2, interacao.id)
    elif(interacao.interacao == 22):
        if(not jogo.jogador.aulas[2][interacao.id]):
            CriarAula(3, interacao.id)

    elif(interacao.interacao == 98):
        UltimaLuta()

# Inicio Parte minimapa

minimapa_completo=Mapa.GetMinimapaComp(jogo.jogador)

def GetMinimapa():
    
    #criando o minimapa
    
    minimapa=[]
    for jota in range(5):
        minimapa.append([0]*5)
    
    #definindo os limites máximos do minimapa

    xo_no_completo=int(jogo.jogador.x)-2
    yo_no_completo=int(jogo.jogador.y)-2
    xo_minimapa=0
    yo_minimapa=0
    xf_no_completo=int(jogo.jogador.x)+2
    yf_no_completo=int(jogo.jogador.y)+2
    xf_minimapa=4
    yf_minimapa=4

    #Atualizando os limites para o máximo real (Caso em bordas do mapa)

    while xo_no_completo<0:
        xo_no_completo+=1
        xo_minimapa+=1
    
    while yo_no_completo<0:
        yo_no_completo+=1
        yo_minimapa+=1
    
    while xf_no_completo>len(minimapa_completo[0])-1:
        xf_no_completo-=1
        xf_minimapa-=1
    
    while yf_no_completo>len(minimapa_completo)-1:
        yf_no_completo-=1
        yf_minimapa-=1
    soma=0
    
    # Colocando os sprites nos locais corretos do minimapa

    while xo_minimapa<=xf_minimapa:
        aux1=yo_minimapa
        aux2=yo_no_completo
        while aux1<=yf_minimapa:
            if (minimapa_completo[aux2][xo_no_completo]==1):
                soma+=1
                Sprite_auxiliar=Sprite("Sprites/minimapa/quadrado_branco.png")
                Sprite_auxiliar.set_position(1241-34*xo_minimapa, 545+34*aux1)
                minimapa[aux1][xo_minimapa]=Sprite_auxiliar
            aux1+=1
            aux2+=1
        xo_minimapa+=1
        xo_no_completo+=1
    
    for j1 in range(2):
        for j2 in range(5):
            auxiliar=minimapa[j2][j1]
            minimapa[j2][j1]=minimapa[j2][4-j1]
            minimapa[j2][4-j1]=auxiliar

    return minimapa

minimapa=GetMinimapa()

def DesenharMinimapa():
    global minimapa

    for i1 in range(5):
        for i2 in range(5):
            if minimapa[i1][i2]!=0:
                minimapa[i1][i2].draw()
    sprite_central=Sprite(f"Sprites/minimapa/Seta{jogo.jogador.direcao}.png")
    sprite_central.set_position(1173, 613)
    sprite_central.draw()
    


# Fim Parte minimapa


def CancelarOpcoes():
    jogo.estadoJogo = Data.EEstado.ANDANDO

Data.escolhaBD[1].AdicionarFunc(CancelarOpcoes)

def SubirAndar():
    if(jogo.jogador.andar < 3):
        jogo.jogador.andar += 1
        jogo.animacao = Data.EANIMACAOOVERWORLD.MUDARANDAR
        lista_efeitos[2].play()
        jogo.fade.fading = True
        jogo.fade.alpha = 0
        jogo.fade.surface.set_alpha(0)
        jogo.mapaAtual = Mapa.GerarMapa(jogo.jogador.andar, jogo)
        jogo.estadoJogo = Data.EEstado.ANIMACAOOVERWORLD
        jogo.SalvarJogo()

    else:
        jogo.dialogoMensagens.append(" ")
        jogo.dialogoMensagens.append("A escada para o próximo andar está")
        jogo.dialogoMensagens.append("interditada. ")
        jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
        jogo.estadoJogo = Data.EEstado.DIALOGO

Data.escolhaBD[0].AdicionarFunc(SubirAndar)


def DescerAndar():
    jogo.jogador.andar -= 1
    jogo.animacao = Data.EANIMACAOOVERWORLD.MUDARANDAR
    lista_efeitos[2].play()
    jogo.fade.fading = True
    jogo.fade.alpha = 0
    jogo.fade.surface.set_alpha(0)
    jogo.mapaAtual = Mapa.GerarMapa(jogo.jogador.andar, jogo)
    jogo.estadoJogo = Data.EEstado.ANIMACAOOVERWORLD
    jogo.SalvarJogo()

Data.escolhaBD[2].AdicionarFunc(DescerAndar)

def FazerListaLimites():
    jogo.inimigosNaLuta.clear()

    for i in range(0, 4):
        inimigo = Data.Inimigo("",0, 0, 0, 0, 0, HUD.GameImageMelhor('Sprites/Inimigos/Erro.png', 0, 0), 0 ,0, 0, 0)

        nlimite = 0
        for i in range(0, len( jogo.inimigosNaLuta)):
            if(jogo.inimigosNaLuta[i].tipo == Data.tipoEntidade["Limite"]):
                nlimite += 1

        inimigo = Data.ILimite("Limite " + chr(65 + nlimite))
        jogo.inimigosNaLuta.append(inimigo)

    i = 0

    for inimigo in jogo.inimigosNaLuta:
        if(inimigo.vida > 0):
            if(inimigo.tipo == Data.tipoEntidade["Limite"]):
                    inimigo.sprite.Transformar(int(317 * (janela.width/1920)), int(497 * (janela.height/1080)))
                    largura = (inimigo.sprite.largura / 2)
                    altura = (inimigo.sprite.altura / 2)

                    if(i == 0):
                        inimigo.sprite.set_position( int( (0.40 * janela.width)  - largura), int( 0.65 * janela.height - altura )    )
                    
                    elif(i == 1):
                        inimigo.sprite.set_position( int( (0.60 * janela.width) - largura), int( 0.65 * janela.height  - altura)    )

                    elif(i == 2):
                        inimigo.sprite.set_position( int( (0.25 * janela.width) - largura), int( 0.55 * janela.height - altura )    )
                    
                    elif(i == 3):
                        inimigo.sprite.set_position( int( (0.75 * janela.width) - largura), int( 0.55 * janela.height - altura )    )

        i += 1

    jogo.estadoJogo = Data.EEstado.LUTA
    luta.estadoLuta = luta.EEstadoLuta.ANIMACAO
    luta.podeFugir = False
    luta.estadoAnimacao = 0
    jogo.dialogoMensagens.append("Professor Substituto:")
    jogo.dialogoMensagens.append("")
    jogo.dialogoMensagens.append("Muito obrigado! Acho que sei como")
    jogo.dialogoMensagens.append("melhorar essa lista.")
    jogo.dialogoMensagens.append("")
    jogo.dialogoMensagens.append("")
    jogo.dialogoMensagens.append("")
    jogo.dialogoMensagens.append("Jogador aprendeu: Teorema do Sanduíche!")
    jogo.jogador.AprenderHabilidade(Data.habilidadeBD[3])
    jogo.ultimoEstadoJogo = Data.EEstado.DIALOGO

Data.escolhaBD[3].AdicionarFunc(FazerListaLimites)

def RecusarProfessor():
    jogo.dialogoMensagens.append("Professor Substituto:")
    jogo.dialogoMensagens.append("")
    jogo.dialogoMensagens.append("Poxa... ")
    jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
    jogo.estadoJogo = Data.EEstado.DIALOGO


Data.escolhaBD[4].AdicionarFunc(RecusarProfessor)

def AcionarAlarme():
    jogo.jogador.quests[1] = 3
    jogo.ultimoEstadoJogo = Data.EEstado.ANDANDO
    jogo.estadoJogo = Data.EEstado.ANDANDO
    jogo.SalvarJogo()

Data.escolhaBD[5].AdicionarFunc(AcionarAlarme)

#não usado
def UpdateTest():
    janela.get_screen().fill((100, 100, 100)) # Gray floor
    paredes = []
    paredes.append(Data.Parede(1,0, Data.direcao["L"]))
    paredes.append(Data.Parede(1,1, Data.direcao["L"]))
    paredes.append(Data.Parede(1,0, Data.direcao["O"]))
    paredes.append(Data.Parede(1,2, Data.direcao["S"]))
    paredes.append(Data.Parede(2,2, Data.direcao["S"]))
    paredes.append(Data.Parede(0,0, Data.direcao["N"]))
    Sprites.DrawLines(jogo.jogador, janela, paredes)
    


    janela.update()

def GameOverScreen():
    janela.get_screen().blit(jogo.fade.surface, (0, 0))
    janela.draw_text("Sua jornada termina aqui..." , janela.width * 0.5  - int((26/2) * 30 * int((1280/janela.width))), janela.height * 0.3, "Sprites/HUD/PressStart2P-Regular.ttf", 30 * int((1280/janela.width)), (255,255,255), )

def GameOver():

    jogo.fade.FadeRed()
    jogo.fade.fading = True
    jogo.fade.alpha = 0
    jogo.fade.surface.set_alpha(1)
    jogo.estadoJogo = Data.EEstado.GAMEOVER


def CriarJogo():
    jogo.jogador=Data.Jogador(23.5 , 8.5, 0, Data.direcao["L"], 110)
    jogo.jogador.AprenderHabilidade(Data.habilidadeBD[0])
    jogo.jogador.AprenderHabilidade(Data.habilidadeBD[1])
    jogo.estadoJogo = Data.EEstado.ANDANDO

def CarregarJogo():
    try:
        with open("save.pkl", "rb") as f:
            save = pickle.load(f)
            jogo.estadoJogo = Data.EEstado.ANDANDO
            jogo.CarregarJogo(save)
            jogo.mapaAtual = Mapa.GerarMapa(jogo.jogador.andar, jogo)
    except FileNotFoundError:
        print("No save file found.")
        
    except (pickle.UnpicklingError, EOFError):
        print("Save file is corrupted!")

def mudar_volume(valor):
    aux=jogo.Musica.musica_atual.volume
    print("volume:", aux)
    if valor<0:
        if aux>=0:
            jogo.Musica.musica_atual.increase_volume(valor)
            aux=jogo.Musica.musica_atual.volume
            if aux!=0:
                for i in range(len(lista_efeitos)):
                    lista_efeitos[i].volume=aux+10
    else:
        if aux<=100:
            jogo.Musica.musica_atual.increase_volume(valor)
            aux=jogo.Musica.musica_atual.volume
            if aux!=0:
                for i in range(len(lista_efeitos)):
                    lista_efeitos[i].volume=aux+10


while(True):
    if(jogo.estadoJogo == Data.EEstado.MAINMENU):
        jogo.MainMenu.DesenharMainMenu(janela, botoes_menu)
        if (jogo.mouse.is_button_pressed(1)):
            if (not ismousepressed):
                ismousepressed=True
                if (jogo.mouse.is_over_object(botoes_menu[0])):
                    CriarJogo()
                elif (jogo.mouse.is_over_object(botoes_menu[1])):
                    CarregarJogo()
                elif (jogo.mouse.is_over_object(botoes_menu[2])):

                    while (True):
                        jogo.MainMenu.Desenharopcoes(janela, botoes_menu, display_volume, jogo.Musica.musica_atual.volume)

                        if (jogo.mouse.is_button_pressed(1)):
                            if (not ismousepressed):
                                ismousepressed=True
                                if (jogo.mouse.is_over_object(botoes_menu[4])):
                                    mudar_volume(-10)
                                elif (jogo.mouse.is_over_object(botoes_menu[5])):
                                    mudar_volume(10)
                                elif (jogo.mouse.is_over_object(botoes_menu[6])):
                                    break                                    
                        else:
                            ismousepressed=False

                elif (jogo.mouse.is_over_object(botoes_menu[3])):
                    break
        else:
            ismousepressed=False
    else:
        Update()

jogo.Musica.musica_atual.stop()