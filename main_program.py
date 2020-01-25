import os
import pygame
import random


def load_image(name):
    fullname = os.path.join('pictures', name)
    image = pygame.image.load(fullname)
    return image


class Game:
    def __init__(self):
        self.p = False
        self.s = True
        self.ex = False
        self.sc = int()
        self.en = True

    def start(self):
        self.s = True

    def pause(self):
        if self.p is True:
            self.p = False
        elif self.p is False:
            self.p = True

    def exit(self):
        self.ex = True

    def score(self, scr):
        self.sc += scr

    def get_score(self):
        return self.sc

    def enable(self, condition):
        self.en = condition


class Character(pygame.sprite.Sprite):

    image = load_image("dudle_jump.jpg")

    def __init__(self, group):

        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        self.killed = False
        self.speed = int()
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Character.image
        color_key = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(color_key)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 220
        self.rect.y = 300
        self.sc_speed = int()
        self.touched = False
        self.before_y = 400

    def update(self, g):
        t = False
        for x in range(len(objectGroup['titles'])):
            if pygame.sprite.collide_mask(self, objectGroup['titles'][x]) and g.en is True:
                if self.touched is False:
                    self.sc_speed = self.speed
                self.touched = True
                t = True
                break
            else:
                t = False
        if t is False:
            self.touched = False
        if self.touched is False or (self.touched is True and self.sc_speed < 0):
            self.speed += 0.2
        elif self.touched is True and self.sc_speed > 0:
            self.speed = -9.5
            if self.before_y > self.rect.y:
                self.before_y = self.rect.y
        self.rect = self.rect.move(0, self.speed)
        if self.rect.y >= 1000:
            self.death()
        if self.rect.x >= 400:
            self.rect.x = -50
        if self.rect.x <= -60:
            self.rect.x = 400
        if self.before_y > self.rect.y:
            g.score(abs(self.before_y - self.rect.y) // 3)
            self.before_y = self.rect.y

    def movement(self, x_pos):
        move_x = int()
        if 340 > x_pos > 40 and (x_pos < self.rect.x):
            if x_pos - self.rect.x > -3:
                move_x = -1
            else:
                move_x = -3
        elif 40 < x_pos < 340 and (x_pos > self.rect.x):
            if x_pos - self.rect.x < 3:
                move_x = 1
            else:
                move_x = 3
        elif x_pos > 340:
            move_x = 3
        elif x_pos < 40:
            move_x = -3
        self.rect = self.rect.move(move_x, 0)

    def boost(self):
        self.speed = -11

    def death(self):
        self.rect.x = 260
        self.rect.y = 800
        self.speed = -15
        game.s = False
        game.enable(True)

    def death_from_enemy(self):
        game.enable(False)
        self.speed = 5
        # do thi later

    def shooting(self):
        pass


class StartButton(pygame.sprite.Sprite):

    image = load_image("play.png")

    def __init__(self, group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = StartButton.image
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 10
        self.rect.y = 100


class ExitButton(pygame.sprite.Sprite):

    image = load_image("exit.png")

    def __init__(self, group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = StartButton.image
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 150
        self.rect.y = 350


class PauseSprite(pygame.sprite.Sprite):

    image = load_image("pause.png")

    def __init__(self, group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = PauseSprite.image
        color_key = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(color_key)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 120
        self.rect.y = 175

    def remove(self):
        all_other_sprites.remove(menuBar['pause'][0])
        del menuBar['pause'][0]


class Title(pygame.sprite.Sprite):

    image = load_image("title.jpg")

    def __init__(self, group, x_pos, y_pos):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Title.image
        color_key = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(color_key)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = x_pos
        self.rect.y = y_pos

    def remove(self):
        all_other_sprites.remove(objectGroup['titles'][0])
        del objectGroup['titles'][0]


class Enemy(pygame.sprite.Sprite):

    image = load_image("Enemy.png")

    def __init__(self, group, x_pos, y_pos):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Enemy.image
        color_key = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(color_key)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.die = False

    def update(self, char, g):
        if pygame.sprite.collide_mask(self, char) and char.speed < 0:
            char.death_from_enemy()
            self.die = True
        elif pygame.sprite.collide_mask(self, char) and char.speed > 0 and self.die is False:
            self.enemy_death(g)
            char.boost()

    def enemy_death(self, g):
        all_other_sprites.remove(objectGroup['enemy'][0])
        del objectGroup['enemy'][0]
        g.score(100)

    def destroy(self):
        all_other_sprites.remove(objectGroup['enemy'][0])
        del objectGroup['enemy'][0]


pygame.init()
# размеры окна:
size = width, height = 400, 600

screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))

game = Game()
objectGroup = dict()
menuBar = dict()
objectGroup['titles'] = []
objectGroup['enemy'] = []
menuBar['pause'] = []
menuBar['exit'] = []
menuBar['start'] = []
running = True
MY_EVENT_TYPE = 10
all_other_sprites = pygame.sprite.Group()
character_sprite = pygame.sprite.Group()
character = Character(character_sprite)
pause = PauseSprite(all_other_sprites)
all_other_sprites.remove(pause)
title = Title(all_other_sprites, 200, 350)
objectGroup['titles'].append(title)
title = Title(all_other_sprites, 200, 125)
objectGroup['titles'].append(title)
enemy = Enemy(all_other_sprites, 100, 100)
objectGroup['enemy'].append(enemy)
pygame.time.set_timer(MY_EVENT_TYPE, 10)
mouse_motion_pos_x = int()
font = pygame.font.Font(None, 20)
score = font.render("Score: ", 1, (80, 80, 80))
score_x = 300
score_y = 10
sc_x = 350
sc_y = 10
pause_font = pygame.font.Font(None, 50)
while running:
    for event in pygame.event.get():
        screen.fill((255, 255, 255))
        sc = font.render(f"{game.get_score()}", 1, (80, 80, 80))
        character_sprite.draw(screen)
        all_other_sprites.draw(screen)
        if game.s is True:
            screen.blit(sc, (sc_x, sc_y))
            screen.blit(score, (score_x, score_y))
        if event.type == MY_EVENT_TYPE and game.p is False:
            character.update(game)
        if event.type == pygame.QUIT:
            running = False
        if game.s is True:
            if event.type == pygame.MOUSEMOTION:
                mouse_motion_pos_x, mouse_motion_pos_y = event.pos
        else:
            if len(menuBar['start']) == 0:
                start_button = StartButton(all_other_sprites)
                menuBar['start'].append(start_button)
            else:
                menuBar['start'][0].update()
                mouse_motion_pos_x = character.rect.x
                while len(objectGroup['titles']) != 0:
                    objectGroup['titles'][0].remove()
                if len(objectGroup['enemy']) != 0:
                    objectGroup['enemy'][0].destroy()
                title = Title(all_other_sprites, 250, 450)
                objectGroup['titles'].append(title)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.s is True:
                    game.pause()
        if game.p is False:
            if len(menuBar['pause']) != 0:
                menuBar['pause'][0].remove()
            character.movement(mouse_motion_pos_x)
            if len(objectGroup['enemy']) != 0:
                objectGroup['enemy'][0].update(character, game)
        else:
            if len(menuBar['pause']) == 0:
                pause = PauseSprite(all_other_sprites)
                menuBar['pause'].append(pause)
    pygame.display.flip()