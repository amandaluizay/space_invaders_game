import math
import random

import pygame
from pygame import mixer

# iniciando pygame
pygame.init()

# criando a tela e atribuindo suas proporções
screen = pygame.display.set_mode((800, 600))

# fundo
bg = pygame.image.load('fundopx.png')

# musica de fundo
mixer.music.load('background.wav')
mixer.music.play(-1)

# Titulo e icone
pygame.display.set_caption("Guardians of the Galaxy")
icon = pygame.image.load('thanos.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('navepx.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemys = 6

# Movimento enemy
for i in range(numEnemys):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3.5)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 12
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
txtX = 10
txtY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 350))


# Def score
def print_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# função que atribui cordenadas a nave
def player(x, y):
    screen.blit(playerImg, (x, y))


# função que atribui cordenadas ao inimigo
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# mostrar bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 36, y + 30))


# detecta colisão
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Loop para rodar a tela
running = True
while running:
    # muda cor da tela
    screen.fill((205, 180, 219))
    screen.blit(bg, (0, 0))
    # botão de fechar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # verifica teclas pressionadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # se nenhuma tecla pressionada
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # delimitar tela para nave
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # multiplos inimigos
    for i in range(numEnemys):
        # Game Over
        if enemyY[i] > 440:
            for j in range(numEnemys):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3.5
            enemyY[i] += enemyY_change[i]
        # colisão
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            pointSound = mixer.Sound("explosion.wav")
            pointSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY < 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    print_score(txtX, txtY)
    # atualiza modificações na tela
    pygame.display.update()
