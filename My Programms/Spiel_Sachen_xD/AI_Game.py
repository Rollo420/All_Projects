import pygame
import random

# Initialisiere Pygame und setze Bildschirmgröße
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Setze Farben
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255,255,255)

# Setze Größen
coin_size = 20
obstacle_size = 30
player_size = 50

# Setze Anfangspositionen
coin_x = random.randint(0, screen_width - coin_size)
coin_y = random.randint(0, screen_height - coin_size)
obstacle_x = random.randint(0, screen_width - obstacle_size)
obstacle_y = random.randint(0, screen_height - obstacle_size)
player_x = random.randint(0, screen_width - player_size)
player_y = random.randint(0, screen_height - player_size)

# Setze Geschwindigkeiten
coin_speed = 10
obstacle_speed = 50
player_speed = 8

# Setze Anfangsvariablen
game_over = False
coins_collected = 0

clock = pygame.time.Clock()

while not game_over:
    # Verarbeite Eingabe
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
    
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_w]:
        player_y -= player_speed
    if keys_pressed[pygame.K_s]:
        player_y += player_speed
    if keys_pressed[pygame.K_a]:
        player_x -= player_speed
    if keys_pressed[pygame.K_d]:
        player_x += player_speed

    # Bewege Münze und Hindernis
    coin_x += coin_speed
    obstacle_x += obstacle_speed

    # Prüfe, ob Münze oder Hindernis außerhalb des Bildschirms sind, und passe ihre Position entsprechend an
    if coin_x < 0 or coin_x + coin_size > screen_width:
        coin_speed = -coin_speed
    if obstacle_x < 0 or obstacle_x + obstacle_size > screen_width:
        obstacle_speed = random.randint(-5, 5)
        obstacle_y = random.randint(0, screen_height - obstacle_size)

    # Prüfe Kollisionen
    if player_x < coin_x + coin_size and player_x + player_size > coin_x and player_y < coin_y + coin_size > coin_y:
        coins_collected += 1
        coin_x = random.randint(0, screen_width - coin_size)
        coin_y = random.randint(0, screen_height - coin_size)
    if player_x < obstacle_x + obstacle_size and player_x + player_size > obstacle_x and player_y < obstacle_y + obstacle_size and player_y + player_size > obstacle_y:
        game_over = True

    # Lösche Bildschirm
    screen.fill(BLACK)

    # Zeichne Münze, Hindernis und Spieler
    pygame.draw.rect(screen, YELLOW, (coin_x, coin_y, coin_size, coin_size))
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_size, obstacle_size))
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_size, obstacle_size))
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_size, obstacle_size))
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_size, obstacle_size))
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    # Aktualisiere Bildschirm
    pygame.display.flip()

    # Setze Framerate
    clock.tick(60)

# Zeige Game Over-Bildschirm
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over", True, WHITE, BLACK)
game_over_rect = game_over_text.get_rect()
game_over_rect.centerx = screen.get_rect().centerx
game_over_rect.centery = screen.get_rect().centery
screen.blit(game_over_text, game_over_rect)
pygame.display.flip()

# Warte auf Eingabe
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            waiting = False

# Beende Pygame
pygame.quit()

