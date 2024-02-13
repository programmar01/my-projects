import pygame

class Fighter():
    def __init__(self, x, y, player, flip, data, sprite_sheet, sprite_animation_steps, sound_effect):
        self.player = player
        self.sound_effect = sound_effect
        self.flip = flip
        self.size = data[0]
        self.scale = data[1]
        self.offset = data[2]
        self.image_list = self.load_image(sprite_sheet, sprite_animation_steps)
        self.action = 0 # 0_ დგომა / 1 _ სირბილი / 2 _ ახტომა / 3 _ პირველი შეტევა / 4 _ მეორე შეტევა / 5 _  დარტყმის მიღება / 6 _ სიკვდილი
        self.frame_index = 0
        self.image = self.image_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.run = False
        self.jump = False
        self.attack = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.alive = True
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.score = 100

    def load_image(self, sprite_sheet, sprite_animation_steps):
        main_list = []
        for y, animation in enumerate(sprite_animation_steps):
            temporary_list = []
            for x in range(animation):
                temp_image = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temporary_list.append(pygame.transform.scale(temp_image, (self.size * self.scale, self.size * self.scale)))
            main_list.append(temporary_list)
        return main_list


     #მოძრაობა
    def move(self, screen_width, screen_height, screen, target, round_over):
        gravity = 2
        speed = 10
        dx = 0
        dy = 0
        self.run = False
        self.attack_type = 0
        key = pygame.key.get_pressed()
        if self.attack == False and self.alive == True and round_over == False:
            if self.player == 1:
                if key[pygame.K_x]:
                    dx = speed
                    self.run = True
                if key[pygame.K_a]:
                    dx = -speed
                    self.run = True
                if key[pygame.K_d]:
                    dx = +speed
                    self.run = True
                if key[pygame.K_w] and self.jump == False:
                    self.jump = True
                    self.vel_y = -30
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.my_attack(target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2
            elif self.player == 2:
                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.run = True
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.run = True
                if key[pygame.K_UP] and self.jump == False:
                    self.jump = True
                    self.vel_y = -30
                if key[pygame.K_k] or key[pygame.K_l]:
                    self.my_attack(target)
                    if key[pygame.K_k]:
                        self.attack_type = 1
                    if key[pygame.K_l]:
                        self.attack_type = 2


        self.vel_y += gravity
        dy += self.vel_y


        #მარცხენა საზღვარი
        if self.rect.x + dx < 0:
            dx = 0 - self.rect.x
        #მარჯვენა საზღვარი
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        #დახტომის კოდი
        if self.rect.bottom + dy > screen_height - 110:
            dy = screen_height - 110 - self.rect.bottom
            self.jump = False

        self.rect.x += dx
        self.rect.y += dy

        #საით იყურება მოთამაშე
        if self.rect.centerx < target.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #cooldown count
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1





    #სპრაიტების ცვლილება
    def update(self):
        # ხომ არ გარდაიცვალა
        if self.score <= 0:
            self.score = 0
            self.alive = False
            self.action_update(6) # death
        elif self.hit == True:
            self.action_update(5) #hit
        elif self.attack == True:
            if self.attack_type == 1:
                self.action_update(3) #first attack
                self.attack_cooldown = 10
            elif self.attack_type == 2:
                self.action_update(4) #second attack
                self.attack_cooldown = 10
        elif self.jump == True:
            self.action_update(2) #jumping
        elif self.run == True:
            self.action_update(1) #runing
        else:
            self.action_update(0) #standing
        time_between = 50
        self.image = self.image_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= time_between:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.image_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.image_list[self.action]) - 1
            else:
                if self.attack == True:
                    self.attack = False
                elif self.hit == True:
                    self.hit = False
                self.frame_index = 0


    #შეტევა
    def my_attack(self, target):
        if self.attack_cooldown == 0:
            self.attack = True
            self.sound_effect.play()
            attacking_rect = pygame.Rect(self.rect.centerx - self.flip * (self.rect.width * 2), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.score -= 5
                target.hit = True


    def action_update(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #დახატვა
    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - (self.scale * self.offset[0]), self.rect.y - (self.scale * self.offset[1])))