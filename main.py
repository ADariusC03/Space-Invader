import pygame
import math
import random

from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the Game Screen
screen = pygame.display.set_mode((800, 600))  # 600=height , 800=width

# Background
bckgd = pygame.image.load("background.png")

# Background Music
mixer.music.load("Andromeda Journey.wav")
mixer.music.play(-1)

# Title and Icons
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('001-spacecraft.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("space-invaders.png")
playerX = 370  # X-coordinates ref to the width. starts Left to Right margins from small(0) to large(800)
playerY = 480  # Y-coordinates ref to the height. up to down from top(0) to bottom(600)
playerX_change = 0

# Bullet
bullImg = pygame.image.load("missile.png")
bullX = 0
bullY = 480
bullX_change = 0
bullY_change = 1.5
bull_state = "ready"  # Ready - You can't see bullet on the screen

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("006-antenna-1.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)

# Score on screen
score_value = 0
font = pygame.font.Font("esp.ttf", 32)

textX = 10  # x,y value coordinates to position the score title
textY = 10

# Game Over Text
game_overf = pygame.font.Font("esp.ttf", 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 190, 0))
    screen.blit(score, (x, y))


def game_over_text():
    game_overt = game_overf.render("GAME OVER", True, (136, 0, 0))
    screen.blit(game_overt, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # Blit means to draw; function to glue img on screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bull(x, y):
    global bull_state
    bull_state = "fire"
    screen.blit(bullImg, (x + 16, y + 1.5))  # missile same place = x, y= above spaceship


def isCollision(enemyX, enemyY, bullX, bullY):
    distance = math.sqrt((math.pow(enemyX - bullX, 2)) + (math.pow(enemyY - bullY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))  # RGB Color
    screen.blit(bckgd, (0, 0))  # Background Image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Keystroke is pressed check whether left or rights
        if event.type == pygame.KEYDOWN:  # Indicates Pressing the key
            if event.key == pygame.K_LEFT:
                playerX_change = -1  # speed to move left
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                bull_Sound = mixer.Sound("Bottle Rocket-SoundBible.com-332895117.wav")
                bull_Sound.play()
                if bull_state == "ready":  # Get the current x coordinate of the spaceship
                    bullX = playerX
                    fire_bull(bullX, bullY)

        if event.type == pygame.KEYUP:  # indicates the key has been released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # when not pressing a key the img stay constant

    # Checking Boundaries For spaceship
    playerX += playerX_change

    if playerX <= 0:  # adding boundary
        playerX = 0
    elif playerX >= 736:  # 736 + 64(img bit) = 800(x-cor boundary),
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]  # When the enemy hit the boundary the enemy drops
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bullX, bullY)
        if collision:
            explosion_Sound = mixer.Sound("Bomb Explosion 1-SoundBible.com-980698079.wav")
            explosion_Sound.play()
            bullY = 480
            bull_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bullY <= 0:
        bullY = 480
        bull_state = "ready"  # Firing bullet many times

    if bull_state == "fire":  # Making of bullet to fire
        fire_bull(bullX, bullY)
        bullY -= bullY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
