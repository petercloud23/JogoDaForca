import pygame as pg
import random

# --- CORES ---
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (200, 0, 0)
verde = (0, 150, 0)

# --- SETUP DA JANELA ---
pg.init()
window = pg.display.set_mode((1000, 600))
pg.display.set_caption("Jogo da Forca")

# --- FONTES ---
font = pg.font.SysFont('courier new', 50)
font_rb = pg.font.SysFont('courier new', 30)
font_small = pg.font.SysFont('courier new', 24)

# --- PALAVRAS ---
palavras = ['paralelepipedo', 'ornintorinco', 'apartamento', 'xicara de cha']

# --- VARIÁVEIS DE ESTADO ---
tentativas_de_letras = []
palavra_escolhida = ''
palavra_camuflada = ''
chance = 0
game_over = False
mensagem_final = ""
entrada_usuario = ""
input_active = False

# posição da caixa de input
INPUT_X, INPUT_Y, INPUT_W, INPUT_H = 700, 400, 250, 40


def resetar_jogo():
    """Reseta o estado do jogo."""
    global tentativas_de_letras, palavra_escolhida, palavra_camuflada
    global chance, game_over, mensagem_final, entrada_usuario, input_active

    tentativas_de_letras = []
    palavra_escolhida = random.choice(palavras).upper()  # sorteia palavra
    palavra_camuflada = camuflar(palavra_escolhida, tentativas_de_letras)
    chance = 0
    game_over = False
    mensagem_final = ""
    entrada_usuario = ""
    input_active = False


def desenhar_forca(chance):
    """Desenha a forca e partes do boneco."""
    pg.draw.rect(window, branco, (0, 0, 1000, 600))
    pg.draw.line(window, preto, (100, 500), (100, 100), 10)
    pg.draw.line(window, preto, (50, 500), (150, 500), 10)
    pg.draw.line(window, preto, (100, 100), (300, 100), 10)
    pg.draw.line(window, preto, (300, 100), (300, 150), 10)

    if chance >= 1:
        pg.draw.circle(window, preto, (300, 200), 50, 10)
    if chance >= 2:
        pg.draw.line(window, preto, (300, 250), (300, 350), 10)
    if chance >= 3:
        pg.draw.line(window, preto, (300, 260), (225, 350), 10)
    if chance >= 4:
        pg.draw.line(window, preto, (300, 260), (375, 350), 10)
    if chance >= 5:
        pg.draw.line(window, preto, (300, 350), (375, 450), 10)
    if chance >= 6:
        pg.draw.line(window, preto, (300, 350), (225, 450), 10)


def desenhar_restart():
    """Desenha botão de restart."""
    pg.draw.rect(window, preto, (700, 100, 200, 65))
    texto = font_rb.render("Restart(1)", True, branco)
    window.blit(texto, (710, 120))


def camuflar(palavra, tentativas):
    """Retorna palavra mascarada com #"""
    return "".join([letra if letra in tentativas or letra in [' ', '-'] else "#" for letra in palavra])


def mostrar_palavra(palavra_camuflada):
    texto = font.render(palavra_camuflada, True, preto)
    window.blit(texto, (200, 500))


def mostrar_mensagem(msg, cor):
    texto = font.render(msg, True, cor)
    rect = texto.get_rect(center=(500, 300))
    window.blit(texto, rect)


def mostrar_tentativas():
    certas = [l for l in tentativas_de_letras if l in palavra_escolhida]
    erradas = [l for l in tentativas_de_letras if l not in palavra_escolhida]

    titulo = font_rb.render("Tentativas:", True, preto)
    window.blit(titulo, (700, 200))

    certas_txt = font_small.render("Certas: " + " ".join(certas), True, verde)
    window.blit(certas_txt, (700, 240))

    erradas_txt = font_small.render("Erradas: " + " ".join(erradas), True, vermelho)
    window.blit(erradas_txt, (700, 270))

    chances_restantes = 6 - chance
    cor = verde if chances_restantes > 2 else vermelho
    chances_txt = font_small.render(f"Chances: {chances_restantes}/6", True, cor)
    window.blit(chances_txt, (700, 310))


def mostrar_input():
    titulo = font_rb.render("Digite a palavra (ENTER):", True, preto)
    window.blit(titulo, (700, 360))
    pg.draw.rect(window, preto, (INPUT_X, INPUT_Y, INPUT_W, INPUT_H), 2)

    mostrar = entrada_usuario[-20:]
    caixa = font_small.render(mostrar, True, preto)
    window.blit(caixa, (INPUT_X + 10, INPUT_Y + 6))


# --- INÍCIO ---
resetar_jogo()

# --- LOOP PRINCIPAL ---
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 700 <= x <= 900 and 100 <= y <= 165:
                resetar_jogo()
            elif INPUT_X <= x <= INPUT_X + INPUT_W and INPUT_Y <= y <= INPUT_Y + INPUT_H:
                input_active = True
                entrada_usuario = ""
            else:
                input_active = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                resetar_jogo()

            if not game_over:
                if not input_active:  # tentando letra
                    if event.unicode.isalpha():
                        letra = event.unicode.upper()
                        if letra not in tentativas_de_letras:
                            tentativas_de_letras.append(letra)
                            if letra not in palavra_escolhida:
                                chance += 1
                else:  # digitando palavra inteira
                    if event.key == pg.K_RETURN:
                        if entrada_usuario.upper() == palavra_escolhida:
                            mensagem_final = "Parabéns, você venceu!"
                        else:
                            mensagem_final = f'Você perdeu! A palavra era:\n {palavra_escolhida}'
                            chance = 6
                        game_over = True
                    elif event.key == pg.K_BACKSPACE:
                        entrada_usuario = entrada_usuario[:-1]
                    else:
                        entrada_usuario += event.unicode.upper()

    # --- DESENHO ---
    desenhar_forca(chance)
    desenhar_restart()
    palavra_camuflada = camuflar(palavra_escolhida, tentativas_de_letras)
    mostrar_palavra(palavra_camuflada)
    mostrar_tentativas()
    mostrar_input()

    if not game_over:
        if chance >= 6:
            mensagem_final = f"Você perdeu! A palavra era: {palavra_escolhida}"
            game_over = True
        elif palavra_camuflada == palavra_escolhida:
            mensagem_final = "Parabéns, você venceu!"
            game_over = True

    if game_over and mensagem_final:
        cor = verde if "venceu" in mensagem_final else vermelho
        mostrar_mensagem(mensagem_final, cor)

    pg.display.update()
