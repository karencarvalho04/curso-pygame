import pygame as pg 
from pygame.locals import *
from sys import exit
from random import randint

pg.init()

pg.mixer.music.load('musica_fundo.mp3')
pg.mixer.music.play(-1)  
pg.mixer.music.set_volume(0.5)  
barulho_colisao = pg.mixer.Sound('smw_coin.wav')

largura = 640
altura = 480
x = largura/2
y = altura/2

x_amarelo = randint(0, largura)
y_amarelo = randint(0, altura)

fonte = pg.font.SysFont("arial", 20, True, True)
pontos = 0

VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("Jogo de Teste")
relogio = pg.time.Clock()


while True:
    relogio.tick(60)  
    tela.fill(PRETO)
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, BRANCO)
    tela.blit(texto_formatado, (10, 10))
    for evento in pg.event.get():
        if evento.type == QUIT:
            exit()
    if pg.key.get_pressed()[K_UP]:
        y -= 20
    if pg.key.get_pressed()[K_DOWN]:
        y += 20
    if pg.key.get_pressed()[K_LEFT]:
        x -= 20
    if pg.key.get_pressed()[K_RIGHT]:
        x += 20
    ret_vermelho = pg.draw.rect(tela, VERMELHO, (x, y, 40, 50))
    ret_amarelo = pg.draw.rect(tela, AMARELO, (x_amarelo, y_amarelo, 40, 50))

    if ret_vermelho.colliderect(ret_amarelo):
        x_amarelo = randint(0, largura - 40)
        y_amarelo = randint(0, altura - 50)
        pontos += 1
        barulho_colisao.play()
    pg.display.update()

