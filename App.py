import pygame
import sys
import random

# Inicialização do pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Atirando Fiona")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Carregar imagens
jogador_imagem = pygame.image.load("assets/img/jogador.png")
inimigo_imagem = pygame.image.load("assets/img/inimigo.png")
menu_imagem = pygame.image.load("assets/img/menu.png")

# Carregar sons
som_tiro = pygame.mixer.Sound("assets/sons/tiro.wav")
pygame.mixer.music.load("assets/sons/musica_menu.mp3")
pygame.mixer.music.play(-1)

# Configurações do jogador
jogador_largura = jogador_imagem.get_width()
jogador_altura = jogador_imagem.get_height()
jogador_x = LARGURA // 2
jogador_y = ALTURA - jogador_altura - 10
jogador_velocidade = 5

# Configurações dos tiros
tiros = []
tiro_largura = 5
tiro_altura = 10
tiro_velocidade = -7

# Configurações dos inimigos
inimigos = []
inimigo_largura = inimigo_imagem.get_width()
inimigo_altura = inimigo_imagem.get_height()
velocidade_inimigo = 2

# Score
score = 0

# Fonte
fonte = pygame.font.SysFont(None, 36)

# Relógio para controlar FPS
relogio = pygame.time.Clock()

# Função para criar inimigos
def criar_inimigo():
    x = random.randint(0, LARGURA - inimigo_largura)
    y = random.randint(-150, -50)
    inimigos.append(pygame.Rect(x, y, inimigo_largura, inimigo_altura))

# Menu principal
def menu():
    while True:
        TELA.fill(PRETO)
        TELA.blit(menu_imagem, (0, 0))
        iniciar = fonte.render("Pressione ENTER para iniciar", True, VERMELHO)

        TELA.blit(iniciar, (LARGURA // 2 - iniciar.get_width() // 2, ALTURA - 300))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                return

# Tela de game over
def game_over():
    while True:
        TELA.fill(PRETO)
        mensagem = fonte.render("Game Over", True, VERMELHO)
        reiniciar = fonte.render("Pressione R para reiniciar ou Q para sair", True, VERMELHO)

        TELA.blit(mensagem, (LARGURA // 2 - mensagem.get_width() // 2, ALTURA // 3))
        TELA.blit(reiniciar, (LARGURA // 2 - reiniciar.get_width() // 2, ALTURA // 2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

menu()

# Criar inimigos iniciais
for _ in range(5):
    criar_inimigo()

# Loop principal do jogo
while True:
    TELA.fill(PRETO)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimentação do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jogador_x -= jogador_velocidade
    if teclas[pygame.K_RIGHT]:
        jogador_x += jogador_velocidade
    if teclas[pygame.K_SPACE]:
        tiros.append(pygame.Rect(jogador_x + jogador_largura // 2, jogador_y, tiro_largura, tiro_altura))
        som_tiro.play()

    # Limitar o jogador à tela
    if jogador_x < 0:
        jogador_x = 0
    if jogador_x > LARGURA - jogador_largura:
        jogador_x = LARGURA - jogador_largura

    # Atualizar tiros
    for tiro in list(tiros):
        tiro.y += tiro_velocidade
        if tiro.y < 0:
            tiros.remove(tiro)

    # Atualizar inimigos
    for inimigo in list(inimigos):
        inimigo.y += velocidade_inimigo
        if inimigo.y > ALTURA:
            inimigos.clear()
            game_over()
            for _ in range(5):
                criar_inimigo()
            jogador_x = LARGURA // 2
            jogador_y = ALTURA - jogador_altura - 10
            score = 0

        # Verificar colisão com tiros
        for tiro in list(tiros):
            if tiro.colliderect(inimigo):
                if inimigo in inimigos:
                    inimigos.remove(inimigo)
                if tiro in tiros:
                    tiros.remove(tiro)
                criar_inimigo()
                score += 1

    # Desenhar jogador
    TELA.blit(jogador_imagem, (jogador_x, jogador_y))

    # Desenhar tiros
    for tiro in tiros:
        pygame.draw.rect(TELA, VERMELHO, tiro)

    # Desenhar inimigos
    for inimigo in inimigos:
        TELA.blit(inimigo_imagem, (inimigo.x, inimigo.y))

    # Mostrar score
    texto_score = fonte.render(f"Score: {score}", True, BRANCO)
    TELA.blit(texto_score, (10, 10))

    # Atualizar a tela
    pygame.display.flip()

    # Controlar FPS
    relogio.tick(60)
