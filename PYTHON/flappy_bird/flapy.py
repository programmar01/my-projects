import pygame
import random
pygame.init()

clock = pygame.time.Clock()
fps = 150
width = 864
height = 550 + 168
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load("images/bg.png")
ground = pygame.image.load("images/ground.png")

ground_x = 0
ground_scrolling = 3

pipe_gap = 200

pipe_frequency = 1500 #მილიწამი
last_pipe = pygame.time.get_ticks() - pipe_frequency

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1, 4):
            img = pygame.image.load(f"images/bird{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    def update(self):
        #გრავიტაცია
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom <= 550:
                self.rect.bottom += self.vel
        #ახტომა
        if game_over == False:
            if flying == True and self.clicked == False:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.vel = -10
                    self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


        if game_over == False:
            #ანიმაცია
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -5)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.topleft = [x, y + pipe_gap / 2]
        elif position == -1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap / 2]
    def update(self):
        self.rect.x -= ground_scrolling
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, self.rect)
        return action

def game_reset():
    global ground_scrolling, score, game_over
    bird1.rect.center = [100, int(height / 2)]
    pipe_group.empty()
    ground_scrolling = 3
    game_over = False
    score = 0



pipe_group = pygame.sprite.Group()


birds_group = pygame.sprite.Group()
bird1 = Bird(100, int(height / 2))
birds_group.add(bird1)

flying = False
game_over = False

font = pygame.font.Font(None, 40)

def print_score(score, font, x, y):
    text = font.render(str(score), True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = [x, y]
    screen.blit(text, rect)


button = Button("images/restart.png", width // 2, height // 2)
score = 0

passing = False

run = True
while run:
    # clock.tick(fps)
    screen.blit(bg, (0, 0))
    birds_group.draw(screen)
    birds_group.update()
    pipe_group.draw(screen)
    pipe_group.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if flying == False and game_over == False and event.type == pygame.MOUSEBUTTONDOWN:
            flying = True

    if game_over ==  False and flying == True:
        #მილების გენერირება
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(width, int(height / 2 + pipe_height), 1)
            top_pipe = Pipe(width, int(height / 2 + pipe_height), -1)
            pipe_group.add(btm_pipe, top_pipe)
            last_pipe = time_now
        #მიწის მოძრაობა
        ground_x -= ground_scrolling
        if ground_x < -35:
            ground_x = 0

    screen.blit(ground, (ground_x, 550))
    #მილებთან შეჯახება
    if pygame.sprite.groupcollide(birds_group, pipe_group, False, False) or bird1.rect.top < 0:
        game_over = True
        ground_scrolling = 0


    if bird1.rect.bottom >= 550:
        game_over = True
        flying = False
        ground_scrolling = 0
    print_score(score, font, width // 2, 70)
    #ქულის დათვლა
    if len(pipe_group) > 0:
        if birds_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and birds_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and passing == False:
            passing = True
        if passing == True:
            if birds_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                passing = False
                score += 1
    if game_over == True:
        if button.draw() == True:
            game_reset()

    pygame.display.update()
pygame.quit()
