import pygame
from fighter import Fighter
from pygame import mixer
clock = pygame.time.Clock()
fps = 60
mixer.init()
pygame.init()

screen_width = 1000
screen_height = 600


#ხმის ეფექტები
sword_sound = pygame.mixer.Sound("images/sword.wav")
sword_sound.set_volume(0.5)
magic_sound = pygame.mixer.Sound("images/magic.wav")
magic_sound.set_volume(1)

background_music = pygame.mixer.music.load("images/music.mp3")
pygame.mixer.music.play(-1, 0.0, 5000)


white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)

warrior_size = 162
warrior_scale = 4
warrior_offset = [72, 56]
warrior_data = [warrior_size, warrior_scale, warrior_offset]
wizard_size = 250
wizard_scale = 3
wizard_offset = [112, 107]
wizard_data = [wizard_size, wizard_scale, wizard_offset]

#game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
round_over_cooldown = 2000


victory_image = pygame.image.load("images/victory.png")

pygame.display.set_caption("Street Fighter")
screen = pygame.display.set_mode((screen_width, screen_height))

background = pygame.image.load("images/background.jpg")

#სფრაითშითის ატვირთვა
warrior_sheet = pygame.image.load("images/warrior.png")
wizard_sheet = pygame.image.load("images/wizard.png")

#animation steps
warrior_animation_steps = [10, 8, 1, 7, 7, 3, 7]
wizard_animation_steps = [8, 8, 2, 8, 8, 3, 7]

count_font = pygame.font.Font("images/turok.ttf", 80)
score_font = pygame.font.Font("images/turok.ttf", 30)

def write_text(text, font, color, x, y):
    number = font.render(text, True, color)
    screen.blit(number, (x, y))

def draw_background():
    scaled_background = pygame.transform.scale(background, (screen_width, screen_height))
    screen.blit(scaled_background, (0, 0))

#სიცოცხლის ჩვენება
def score_bar(score, x, y):
    ratio = score / 100
    pygame.draw.rect(screen, white, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, red, (x, y, 400, 30))
    pygame.draw.rect(screen, yellow, (x, y, 400 * ratio, 30))



fighter1 = Fighter(200, 310, 1,  False, warrior_data, warrior_sheet, warrior_animation_steps, sword_sound)
fighter2 = Fighter(700, 310, 2, True, wizard_data, wizard_sheet, wizard_animation_steps, magic_sound)


run = True
while run:
    clock.tick(fps)
    draw_background()

    score_bar(fighter1.score, 20, 20)
    score_bar(fighter2.score, 580, 20)
    write_text("P1:" + str(score[0]), score_font, red, 20, 60)
    write_text("P2:" + str(score[1]), score_font, red, 580, 60)


    if intro_count <= 0:
        fighter1.move(screen_width, screen_height, screen, fighter2, round_over)
        fighter2.move(screen_width, screen_height, screen, fighter1, round_over)
    else:
        write_text(str(intro_count), count_font, red, screen_width // 2, screen_height // 3)
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    if round_over == False:
        if fighter1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_image, (360, 150))
        if pygame.time.get_ticks() - round_over_time >= round_over_cooldown:
            round_over = False
            intro_count = 3
            fighter1 = Fighter(200, 310, 1, False, warrior_data, warrior_sheet, warrior_animation_steps, sword_sound)
            fighter2 = Fighter(700, 310, 2, True, wizard_data, wizard_sheet, wizard_animation_steps, magic_sound)



    fighter1.update()
    fighter2.update()

    fighter1.draw(screen)
    fighter2.draw(screen)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()