import pygame
from os import listdir
from os.path import join, isfile
pygame.init()
fps = 60
player_vel = 5
Width, Height = 800, 600
screen = pygame.display.set_mode((Width, Height))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    block_path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(block_path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.fall_count = 0
        self.animation_count = 0
        self.mask = None
        self.jump_count = 0

    red_color = (255, 0, 0)
    gravity = 1
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    animation_delay = 3

    def jump(self):
        self.y_vel = -self.gravity * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0


    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.gravity)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.sprite_update()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    def hit_head(self):
        self.count = 0
        self.y_vel *= - 1

    def sprite_update(self):
        sprite_sheet = "idle"
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        if self.y_vel > self.gravity * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.animation_delay) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    #6
    def draw(self, window, offset_x):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    #5
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)




def background_info(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(Width // width + 1):
        for j in range(Height // height + 1):
            pos = [i * width, j * height]
            tiles.append(pos)
    return tiles, image


#4
def draw(window, tiles, image, player, object, offset_x):
    for pos in tiles:
        window.blit(image, tuple(pos))
    for obj in object:
        obj.draw(screen, offset_x)
    player.draw(screen, offset_x)
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def movement_controlls(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(player_vel)
    if keys[pygame.K_RIGHT]:
        player.move_right(player_vel)

    handle_vertical_collision(player, objects, player.y_vel)



def main(screen):
    clock = pygame.time.Clock()
    tiles_location, background_image = background_info("Green.png")
    block_size = 96
    player = Player(100, 100, 50, 50)
    floor = [Block(i * block_size, Height - block_size, block_size) for i in range(0, Width // block_size + 1)]

    #1
    offset_x = 0
    scroll_area_width = 100

    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        player.loop(fps)
        movement_controlls(player, floor) #ადგილი არ შეუცვალო
        #3
        draw(screen, tiles_location, background_image, player, floor, offset_x)

        #2
        if (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0) or (player.rect.right - offset_x >= Width - scroll_area_width and player.x_vel > 0):
            offset_x += player.x_vel


    pygame.quit()

if __name__ == "__main__":
    main(screen)