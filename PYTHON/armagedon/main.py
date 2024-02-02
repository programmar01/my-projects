import pygame, sys, random
from pygame import mixer
pygame.init()
clock = pygame.time.Clock()
width = 1242 / 3.5
height = 2208 / 3.5

screen = pygame.display.set_mode((width, height))

icon = pygame.image.load("images/asteroid2.png")
pygame.display.set_caption("Armagedon...")
pygame.display.set_icon(icon)

backround = pygame.image.load("images/back.jpg")
backround = pygame.transform.scale(backround, (width, height))

player_image = pygame.image.load("images/earth.png")
player_image = pygame.transform.scale(player_image, (50, 50))


words = ["cosmos", "asteroid", "planet", "sun", "galaxy", "solar system", "jupiter"]


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = width / 2
        self.y = height * 90/100
        self.rect = self.image.get_rect(center=[self.x, self.y])
        self.player_speed = 0
        self.word = ""

    def update(self):
        text = font0.render(f"{self.word}", False, (255, 250, 100), (0, 0, 0))
        text_rect = text.get_rect(center=[self.x, self.y - 35])
        screen.blit(text, text_rect)

        self.x += self.player_speed
        self.rect.center = [self.x, self.y]
        if self.x < 25:
            self.x = 25
        if self.x > width - 25:
            self.x = width - 25

player_group = pygame.sprite.Group()

earth = Player(player_image)
player_group.add(earth)


#მეტეორები
asteroid0 = pygame.image.load("images/asteroid0.png")
asteroid1 = pygame.image.load("images/asteroid1.png")
asteroid2 = pygame.image.load("images/asteroid2.png")
asteroid3 = pygame.image.load("images/asteroid3.png")
asteroid4 = pygame.image.load("images/asteroid4.png")
asteroid5 = pygame.image.load("images/asteroid5.png")

asteroids = [asteroid0, asteroid1, asteroid2, asteroid3, asteroid4, asteroid5]

for i in range(len(asteroids)):
    asteroids[i] = pygame.transform.scale(asteroids[i], (30, 30))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, images_list, words_list, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(images_list)
        self.x = random.randint(15, int(width - 15))
        self.y = random.randint(-500, -50)
        self.rect = self.image.get_rect(center=[self.x, self.y])
        self.mass = random.randint(3, 7)
        self.word = random.choice(words_list)
        ind = words.index(self.word)
        # words.pop(ind)



    def update(self):
        global score
        self.text = font0.render(f"{self.word}", False, (255, 250, 100), (0, 0, 0))
        self.word_rect = self.text.get_rect(center=[self.x, self.y + 30])
        self.y += gravity * self.mass
        self.rect.center = [self.x, self.y]
        self.word_rect.center = [self.x, self.y + 30]
        screen.blit(self.text, self.word_rect)

        if self.y > height:
            self.kill()

        if earth.rect.collidepoint((self.x, self.y + 10)):
            self.kill()
            score -= 1


        if self.word != "" and self.word == earth.word:
            score += 1
            self.word = ""
            self.mass = 10*self.mass
            earth.word = ""


font0 = pygame.font.Font(None, 20)
font = pygame.font.Font(None, 60)
def show_score(font):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect(center=[width/2, 50])
    screen.blit(text, text_rect)


asteroids_group = pygame.sprite.Group()
score = 0
counter = 0
gravity = 0.2
run = True
while run:
    clock.tick(60)
    screen.blit(backround, (0, 0))
    player_group.draw(screen)
    player_group.update()

    asteroids_group.draw(screen)
    asteroids_group.update()
    show_score(font)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                earth.player_speed = 2
            if event.key == pygame.K_LEFT:
                earth.player_speed = -2
            if event.key not in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DELETE, pygame.K_BACKSPACE]:
                earth.word += event.unicode
            if event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                earth.word = ""
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                earth.player_speed = 0


    counter += 1
    if counter > 240:
        counter = 0
    if counter == 240 and len(words) > 0:
        new_asteroid0 = Asteroid(asteroids, words, font0)
        new_asteroid1 = Asteroid(asteroids, words, font0)
        asteroids_group.add(new_asteroid0, new_asteroid1)

    if score < 0:
        run = False
    pygame.display.update()


pygame.quit()
sys.exit()