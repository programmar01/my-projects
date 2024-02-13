from pygame import *
import random
init()
clock = time.Clock()
fps = 40
device_info = display.Info()
width = device_info.current_w
height = device_info.current_h
screen = display.set_mode((width, height))
display.set_caption("alien eat alien")

font_score = font.Font("images/spanjbob.ttf", 30)
logo = image.load("images/logo.png")
display.set_icon(logo)

mouse.set_visible(0)

class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 60
        self.width = self.score
        self.height = self.score
        self.rect = Rect(width/2, height/2, self.width, self.height)
        self.speed = 20 * 60 / self.score
        self.velocity_x = 0
        self.velocity_y = 0
        self.rendered_score = font_score.render(f"{self.score}", True, (0, 0, 0))
        self.score_rect = self.rendered_score.get_rect(centerx=self.rect.centerx, centery=self.rect.centery - self.score*50/100 / 2 - 20)
        self.image = image.load("images/player.png")
        self.current_image = transform.scale(self.image, (self.score, self.score))

    def draw(self):
        self.width = self.score
        self.height = self.score
        self.rect = Rect(self.rect.x, self.rect.y, self.width, self.height)
        # draw.rect(screen, (200, 100, 100), self.rect)
        self.right_image = transform.scale(self.image, (self.width, self.height))
        self.left_image = transform.flip(self.right_image, True, False)


        screen.blit(self.current_image, self.rect)

        # self.score_rect.centerx = self.rect.centerx
        # self.score_rect.centery = self.rect.centery - self.score*50/100 / 2 - 40
        # self.rendered_score = font_score.render(f"{self.score}", True, (255, 255, 155))
        # screen.blit(self.rendered_score, self.score_rect)

    def player_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        keys = key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            self.velocity_y = -self.speed
        if keys[K_s] or keys[K_DOWN]:
            self.velocity_y = self.speed
        if keys[K_d] or keys[K_RIGHT]:
            self.current_image = self.right_image
            self.velocity_x = self.speed
        if keys[K_a] or keys[K_LEFT]:
            self.current_image = self.left_image
            self.velocity_x = -self.speed

    def move(self):
        self.rect.centerx += self.velocity_x
        self.rect.centery += self.velocity_y
        #საზღვრების დაწესება
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width
        if self.rect.bottom >= height:
            self.rect.bottom = height
        if self.rect.top <= 0:
            self.rect.top = 0

        self.speed = 20 * 60 / self.score

    def update(self):
        self.draw()
        self.player_input()
        self.move()


enemy1_image = image.load("images/fish1.png")
enemy2_image = image.load("images/fish2.png")

enemy_list = [enemy1_image, enemy2_image]


class Enemy(sprite.Sprite):
    def __init__(self, images_list):
        super().__init__()
        self.image = random.choice(images_list)
        x_range1 = random.randint(-200, int(width/20))
        x_range2 = random.randint(int(width + width/20), width + 200)
        y_range = random.randint(50, int(height - 50))
        self.size_w = random.randint(20, 300)
        self.score = self.size_w
        self.size_h = int(self.size_w)
        self.image = transform.scale(self.image, (self.size_w, self.size_h))
        self.rect = Rect(random.choice([x_range1, x_range2]), y_range, self.size_w, self.size_h)
        if self.rect.centerx < width/2:
            self.speed = 4 * 60 / self.size_w

        else:
            self.speed = -4 * 60 / self.size_w
            self.image = transform.flip(self.image, True, False)

        #ქულის დარენდერება
        self.rendered_score = font_score.render(f"{self.size_w}", True, (255, 255, 255))
        self.score_rect = self.rendered_score.get_rect(centerx=self.rect.centerx, centery=self.rect.centery - self.size_h/2 - 20)


    def draw(self):
        # draw.rect(screen, (100, 200, 100), self.rect)
        screen.blit(self.image, self.rect)

        self.score_rect.centerx = self.rect.centerx

        screen.blit(self.rendered_score, self.score_rect)
    def move(self):
        self.rect.centerx += self.speed
    def update(self):
        self.draw()
        self.move()
        # ეკრანის გაცდენისას მოწინააღმდეგის სპრაიტის განადგურება
        if self.speed > 0:
            if self.rect.left > width:
                self.kill()
        elif self.speed < 0:
            if self.rect.right < 0:
                self.kill()

background = transform.scale(image.load("images/background.png"), (width, height + 100))
player = Player()
enemy_group = sprite.Group()
player_group = sprite.Group()
player_group.add(player)
enemies_list = []
counter = 0

player_font = font.Font("images/spanjbob.ttf", 60)
def write_score():
    rendered_score = player_font.render(f"Score: {player.score}", True, (255, 255, 255))
    screen.blit(rendered_score, (20, 20))

over_font = font.Font("images/spanjbob.ttf", 120)
def game_over():
    rendered_score = over_font.render("Game Over!", True, (255, 255, 255))
    rendered_rect = rendered_score.get_rect(centerx=width/2, centery=height/2)
    screen.blit(rendered_score, rendered_rect)

run = True
while run:
    counter += 1
    if counter >= 120:
        counter = 0
        enemy = Enemy(enemy_list)
        enemies_list.append(enemy)
        enemy_group.add(enemy)

    clock.tick(fps)
    screen.blit(background, (0, 0))

    player_group.update()
    enemy_group.update()
    for ev in event.get():
        if ev.type == QUIT:
            run = False
        elif ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:
                run = False

    #დაჯახებისას რა ხდება
    for en in enemies_list:
        if en.rect.colliderect(player.rect):
            if player.score > en.score:
                player.score += int(en.score/4)
                enemies_list.remove(en)
                en.kill()



            elif player.score < en.score:
                player.kill()
                run = False
            else:
                pass
    write_score()
    display.update()

game_over()
display.update()
time.wait(3000)

quit()