import pygame

# Inicializa o Pygame
pygame.init()

# Define o tamanho da janela
tela = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Objetos e Classes em Pygame")

# Define a classe Personagem
class Personagem:
    def __init__(self, nome, cor, x, y):
        self.nome = nome
        self.cor = cor
        self.x = x
        self.y = y

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (self.x, self.y), 30)

# Instancia dois personagens diferentes
personagem1 = Personagem("Herói", (255, 255, 0), 100, 150)  # Amarelo
personagem2 = Personagem("Vilão", (255, 0, 0), 300, 150)    # Vermelho

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualiza a tela
    tela.fill((0, 0, 0))  # Cor de fundo: preto
    personagem1.desenhar(tela)
    personagem2.desenhar(tela)
    pygame.display.update()

# Encerra o Pygame
pygame.quit()
