import pygame, sys
from random import randint
from  pygame import mixer
pygame.init()

width = 900
height = 700

screen = pygame.display.set_mode((width, height))

mixer.music.load("images/Space Invaders - Space Invaders.mp3")
mixer.music.play(-1)
#ფოტოს შემოტანა
background = pygame.image.load("images/background1.png")

background = pygame.transform.scale(background, (width, height))

#სათაურის და სათურის ფოტოს შეცვლა
icon = pygame.image.load("images/player.png")
pygame.display.set_caption("space fighters")
pygame.display.set_icon(icon)
#მოთამაშის ფიგურის შემოტანა
player = pygame.image.load("images/player.png")

player = pygame.transform.scale(player, (100, 100))
#მოტამაშის კვადრატში ჩასმა
player_rect = player.get_rect()
#მოთამაშს კოორდინატები
player_x = 450
player_y = 650

#მოთამაშის მოძრაობის სიჩქარე
player_speed = 0

#უცხოპლანეტელის სურათის შემოტანა
enemy = pygame.image.load("images/enemy1.png")
enemy = pygame.transform.scale(enemy, (80, 80))
enemy_x = randint(50, 850)
enemy_y = 50
enemy_rect = enemy.get_rect()

enemy_speed_x = 15
enemy_speed_y = 50
#ტყვიის შემოტანა
bullet = pygame.image.load("images/bullet (1).png")
bullet = pygame.transform.scale(bullet, (40, 50))
bullet_x = player_x
bullet_y = player_y
bullet_rect = bullet.get_rect()
bullet_speed = 20
game_over_font = pygame.font.Font("freesansbold.ttf", 100)
#გასროლილია თუ არა ტყვია
fired = False
score = 0
#score
font = pygame.font.Font(None, 60)
def show_score(font):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect(center=[width / 2, 50])
    screen.blit(text, text_rect)
def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (140, 300))


while True:
    # მართკუთხედის ცენტრი
    player_rect.center = [player_x, player_y]
    enemy_rect.center = [enemy_x, enemy_y]

    screen.blit(background, (0, 0))
    show_score(font)
    screen.blit(player, player_rect)
    screen.blit(enemy, enemy_rect)

    #მოთამაშის იქსკოორდიატების ცვლილება
    player_x += player_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_speed = 10
            if event.key == pygame.K_LEFT:
                player_speed = -10
            if event.key == pygame.K_SPACE and fired == False:
                fired = True
                bullet_x = player_x
                bullet_y = player_y - 50
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_speed = 0
    #ეკრანის ზღვრის დაწესება მოთამაშისთვის
    if player_x < 50:
        player_x = 50
    if player_x > 850:
        player_x = 850
    #მოწინააღმდეგის მოძრაობა
    enemy_x += enemy_speed_x
    if enemy_x > 850:
        enemy_speed_x *= -1
        enemy_y += enemy_speed_y
    if enemy_x < 50:
        enemy_speed_x *= -1
        enemy_y += enemy_speed_y
    if enemy_y >= 650:
        enemy_y = 50
        enemy_x = randint(50, 850)
    #ტყვიის გასროლა
    if fired == True:
        bullet_y -= bullet_speed
        bullet_rect.center = [bullet_x, bullet_y]
        screen.blit(bullet, bullet_rect)
    if bullet_y < 0:
        fired = False

    #ტყვიის მოხვედრის ფუნქციონალი
    if fired == True and bullet_rect.colliderect(enemy_rect):
        fired = False
        score += 1
        if score > 3:

            game_over()
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
    #ერთმანეთთან შეჯახების ფუნქციონალი
        if enemy_rect.collidepoint(player_rect.center):
            game_over()
            pygame.display.update()
            pygame.time.wait(2000)
            sys.exit()
            pygame.quit()

    pygame.display.update()