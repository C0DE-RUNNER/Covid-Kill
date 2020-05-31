import pygame
import random
import math
from pygame import mixer

# initialize thr pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (800, 600))

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon

pygame.display.set_caption("Corona Warrior")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('corona.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 170))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Player
playerImg = pygame.image.load('doctor.png')
playerX = 370
playerY = 520
playerX_change = 0

# Injection
injectionImg = pygame.image.load('injection.png')
injectionX = 0
injectionY = 480
# injectionX_change = 0
injectionY_change = 20
injection_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 800)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = font.render("YOU GOT INFECTED", True, (0, 255, 0))
    screen.blit(over_text, (250, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_injection(x, y):
    global injection_state
    injection_state = "fire"
    screen.blit(injectionImg, (x, y + 5))


def isCollision(coronaX, coronaY, injectionX, injectionY):
    distance = math.sqrt((math.pow(coronaX - injectionX, 2)) + (math.pow(coronaY - injectionY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB values for color
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is presses, check right/left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if injection_state is "ready":
                    injection_sound = mixer.Sound('laser.wav')
                    injection_sound.play()
                    injectionX = playerX
                    fire_injection(injectionX, injectionY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0

    # checking for boundaries of player
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # corona movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], injectionX, injectionY)
        if collision:
            collision_sound = mixer.Sound('hit.wav')
            collision_sound.play()
            injectionY = 480
            injection_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 170)

        enemy(enemyX[i], enemyY[i], i)

    # injection movement
    if injectionY <= 0:
        injectionY = 480
        injection_state = "ready"
    if injection_state is "fire":
        fire_injection(injectionX, injectionY)
        injectionY -= injectionY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
