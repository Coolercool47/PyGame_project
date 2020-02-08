import os
import pygame
import random
import sqlite3


def load_image(name):
    fullname = os.path.join('pictures', name)
    image = pygame.image.load(fullname)
    return image


class Game:
    def __init__(self):
        self.p = False
        self.s = False
        self.ex = False
        self.sc = int()
        self.en = True
        self.music = True
        self.sfx = True

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

    def update(self, g, state):

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
            if state is True:
                self.speed += 0.3
            else:
                self.speed += 0.2
        elif self.touched is True and self.sc_speed > 0:
            self.speed = -10
            if game.sfx:
                jump_sound.play()
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
        con = sqlite3.connect("scores.db")
        cur = con.cursor()
        list_scores = list(cur.execute('''SELECT * FROM Scores'''))
        con.commit()
        for k in list_scores:
            if k[1] > game.sc:
                continue
            con = sqlite3.connect("scores.db")
            cur = con.cursor()
            cur.execute(f'''UPDATE Scores
                SET score = {game.sc}
                where id == {k[0]}''')
            con.commit()
            list_scores = list_scores[k[0] - 1:9]
            break
        for s in list_scores:
            if s[1] > game.sc:
                continue
            con = sqlite3.connect("scores.db")
            cur = con.cursor()
            cur.execute(f'''UPDATE Scores
                            SET score = {s[1]}
                            where id == {s[0] + 1}''')
            con.commit()

    def death_from_enemy(self):
        game.enable(False)
        self.speed = 5
        # do thi later

    def shooting(self):
        pass


class HighScoresButtons(pygame.sprite.Sprite):
    image = load_image("highscores.png")
    # color 2e3174

    def __init__(self, group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = StartButton.image
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 15
        self.rect.y = 200

    def clicked(self, pos, index):
        if self.rect.collidepoint(pos):
            global scores_on
            scores_on = True
            e = menuBar.keys()
            for s in e:
                if menuBar[s]:
                    all_other_sprites.remove(menuBar[s][0])
                    menuBar[s] = []


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

    def clicked(self, pos, index):
        global just_started
        if self.rect.collidepoint(pos):
            game.s = True
            e = menuBar.keys()
            for j in e:
                if menuBar[j]:
                    all_other_sprites.remove(menuBar[j][0])
                    menuBar[j] = []
            just_started = True


class BackButton(pygame.sprite.Sprite):

    image = load_image("back.jpg")

    def __init__(self, group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = StartButton.image
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 10
        self.rect.y = 10

    def clicked(self, pos, index):
        global settings_on, scores_on
        if self.rect.collidepoint(pos):
            if settings_on:
                settings_on = False
                e = settingsBar.keys()
                for p in e:
                    if settingsBar[p]:
                        all_other_sprites.remove(settingsBar[p][0])
                        settingsBar[p] = []
            if scores_on:
                scores_on = False
                e = settingsBar.keys()
                for p in e:
                    if settingsBar[p]:
                        all_other_sprites.remove(settingsBar[p][0])
                        settingsBar[p] = []


class ExitButton(pygame.sprite.Sprite):

    image = load_image("exit.png")

    def __init__(self, group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = StartButton.image
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 10
        self.rect.y = 350

    def clicked(self, pos, index):
        global br
        if self.rect.collidepoint(pos):
            br = True


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


class SettingsButton(pygame.sprite.Sprite):

    image = load_image('SettingsButton.png')

    def __init__(self, group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = PauseSprite.image
        color_key = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(color_key)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 365
        self.rect.y = 0

    def remove(self):
        all_other_sprites.remove(menuBar['pause'][0])
        del menuBar['pause'][0]

    def clicked(self, pos, index):
        global settings_on
        if self.rect.collidepoint(pos):
            settings_on = True
            e = menuBar.keys()
            for j in e:
                if menuBar[j]:
                    all_other_sprites.remove(menuBar[j][0])
                    menuBar[j] = []


class MusicButton(pygame.sprite.Sprite):

    def __init__(self, group):
        if game.music:
            self.image = load_image('on.png')
        else:
            self.image = load_image('off.png')
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 10
        self.rect.y = 350

    def clicked(self, pos, index):
        if self.rect.collidepoint(pos):
            global time
            game.music = not game.music
            if game.music:
                self.image = load_image('on.png')
                time = 0
            else:
                self.image = load_image('off.png')
            self.sprite.image = self.image
            self.rect = self.sprite.image.get_rect()
            self.mask = pygame.mask.from_surface(self.sprite.image)
            self.rect.x = 10
            self.rect.y = 350


class SFXButton(pygame.sprite.Sprite):

    def __init__(self, group):
        if game.music:
            self.image = load_image('on.png')
        else:
            self.image = load_image('off.png')
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = 10
        self.rect.y = 150

    def clicked(self, pos, index):
        if self.rect.collidepoint(pos):
            global time
            game.sfx = not game.sfx
            if game.sfx:
                self.image = load_image('on.png')
                time = 0
            else:
                self.image = load_image('off.png')
            self.sprite.image = self.image
            self.rect = self.sprite.image.get_rect()
            self.mask = pygame.mask.from_surface(self.sprite.image)
            self.rect.x = 10
            self.rect.y = 150


class Tile(pygame.sprite.Sprite):

    image = load_image("сова.png")

    def __init__(self, group, x_pos, y_pos):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Tile.image
        color_key = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(color_key)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = x_pos
        self.rect.y = y_pos

    def movement(self):
        global running
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 50)
        if running:
            self.rect.y = random.randrange(height)
        else:
            self.rect.y = random.randrange(-20, -10)

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
br = False
settings_on = False
time = 1500.0
main_theme = pygame.mixer.Sound(os.path.join('sounds', 'main_theme.wav'))
jump_sound = pygame.mixer.Sound(os.path.join('sounds', 'jump.wav'))
game = Game()
objectGroup = dict()
menuBar = dict()
objectGroup['titles'] = []
objectGroup['enemy'] = []
menuBar['pause'] = []
menuBar['exit'] = []
menuBar['start'] = []
menuBar['high_scores'] = []
menuBar['settings'] = []
settingsBar = dict()
settingsBar['music'] = []
settingsBar['sfx'] = []
settingsBar['back'] = []
running = True
MY_EVENT_TYPE = 10
all_other_sprites = pygame.sprite.Group()
character_sprite = pygame.sprite.Group()
character = Character(character_sprite)
pause = PauseSprite(all_other_sprites)
all_other_sprites.remove(pause)
title = Tile(all_other_sprites, 200, 350)
objectGroup['titles'].append(title)
title = Tile(all_other_sprites, 200, 125)
objectGroup['titles'].append(title)
enemy = Enemy(all_other_sprites, 100, 100)
objectGroup['enemy'].append(enemy)
SettingButton = SettingsButton(all_other_sprites)
menuBar['settings'].append(SettingButton)
ScoreBoard = HighScoresButtons(all_other_sprites)
menuBar['high_scores'].append(ScoreBoard)
pygame.time.set_timer(MY_EVENT_TYPE, 10)
mouse_motion_pos_x = int()
font = pygame.font.Font(None, 20)
score = font.render("Score: ", 1, (80, 80, 80))
just_started = False
scores_on = False
score_x = 300
score_y = 10
sc_x = 350
sc_y = 10
a = 0
font2 = pygame.font.Font(None, 50)
clock = pygame.time.Clock()
pause_font = pygame.font.Font(None, 50)
b = False
while running:
    if game.music:
        if time == 1550:
            time = 0
            main_theme.play()
    for event in pygame.event.get():
        screen.fill((255, 255, 255))
        sc = font.render(f"{game.get_score()}", 1, (80, 80, 80))
        character_sprite.draw(screen)
        all_other_sprites.draw(screen)
        if event.type == MY_EVENT_TYPE and game.p is False:
            character.update(game, b)
        if event.type == pygame.QUIT:
            running = False
        if game.s and not settings_on and not scores_on:
            for i in objectGroup['enemy']:
                if i.rect.y > 1000:
                    objectGroup['enemy'] = []
            if event.type == pygame.MOUSEMOTION:
                mouse_motion_pos_x, mouse_motion_pos_y = event.pos
            screen.blit(sc, (sc_x, sc_y))
            screen.blit(score, (score_x, score_y))
            for i in range(len(objectGroup['titles'])):
                if objectGroup['titles'][i].rect.y > 600:
                    del objectGroup['titles'][i]
                    break
            if len(objectGroup['titles']) < 7 and just_started:
                list_cords = []
                yy = []
                for i in objectGroup['titles']:
                    list_cords.append((i.rect.x, i.rect.y))
                    yy.append(i.rect.y)
                for i in range(7 - len(objectGroup['titles'])):
                    x = random.randrange(0, 350)
                    y = random.randrange(0, max(yy) - 70)
                    for j in list_cords:
                        while (x + 74 < j[0] or x > j[0] + 74) and (y + 20 < j[1] or x > j[1] + 20):
                            x = random.randrange(0, 350)
                            y = random.randrange(0, max(yy) - 40)
                    tile = Tile(all_other_sprites, x, y)
                    objectGroup['titles'].append(tile)
                just_started = False
            elif len(objectGroup['titles']) < 7 and not just_started:
                list_cords = []
                yy = []
                g = random.randrange(10)
                for i in objectGroup['titles']:
                    list_cords.append((i.rect.x, i.rect.y))
                    yy.append(i.rect.y)
                for i in range(7 - len(objectGroup['titles'])):
                    x = random.randrange(0, 350)
                    y = random.randrange(-10, 10)
                    for j in list_cords:
                        while (x + 74 < j[0] or x > j[0] + 74) and (y + 20 < j[1] or x > j[1] + 20):
                            x = random.randrange(0, 350)
                            y = random.randrange(-10, 10)
                    tile = Tile(all_other_sprites, x, y)
                    objectGroup['titles'].append(tile)
                if not objectGroup['enemy']:
                    x = random.randrange(0, 350)
                    y = random.randrange(-200, -100)
                    enemy = Enemy(all_other_sprites, x, y)
                    objectGroup['enemy'].append(enemy)
            if character.rect.y < 200 and not game.p:
                b = True
                a = 1

            if character.rect.y > 250 and not game.p:
                b = False
                if character.rect.y < 400:
                    a = 2

            if character.rect.y < 10 and not game.p:
                for i in objectGroup['titles']:
                    i.rect = i.rect.move(0, 9)
                for i in objectGroup['enemy']:
                    i.rect = i.rect.move(0, 9)

            elif b is True and game.p is False:
                for i in objectGroup['titles']:
                    i.rect = i.rect.move(0, 4)
                for i in objectGroup['enemy']:
                    i.rect = i.rect.move(0, 4)

        elif settings_on:
            text = font2.render("Music", 10, (0, 0, 0))
            text_x = 25
            text_y = 300
            screen.blit(text, (text_x, text_y))
            text1 = font2.render("SFX", 10, (0, 0, 0))
            text1_x = 35
            text1_y = 100
            screen.blit(text1, (text1_x, text1_y))
            if len(settingsBar['music']) == 0:
                msc = MusicButton(all_other_sprites)
                settingsBar['music'].append(msc)
            if len(settingsBar['sfx']) == 0:
                msc = SFXButton(all_other_sprites)
                settingsBar['sfx'].append(msc)
            if len(settingsBar['back']) == 0:
                back = BackButton(all_other_sprites)
                settingsBar['back'].append(back)
        elif scores_on:
            if len(settingsBar['back']) == 0:
                back = BackButton(all_other_sprites)
                settingsBar['back'].append(back)
            text = font2.render("HIGH SCORES", 1, (0, 0, 100))
            text_x = 10
            text_y = 50
            screen.blit(text, (text_x, text_y))
            con = sqlite3.connect("scores.db")
            cur = con.cursor()
            list_scores = list(cur.execute('''SELECT * FROM Scores'''))
            con.commit()
            a = 40
            for i in range(len(list_scores)):
                text = font2.render(f'{i + 1}: {list_scores[i][1]}', 1, (0, 0, 100))
                text_x = 10
                text_y = a * (i + 1) + 50
                screen.blit(text, (text_x, text_y))

        else:
            game.sc = 0
            if len(menuBar['start']) == 0:
                start_button = StartButton(all_other_sprites)
                menuBar['start'].append(start_button)
            elif len(menuBar['exit']) == 0:
                start_button = ExitButton(all_other_sprites)
                menuBar['exit'].append(start_button)
            elif len(menuBar['settings']) == 0:
                settings_button = SettingsButton(all_other_sprites)
                menuBar['settings'].append(settings_button)
            elif len(menuBar['high_scores']) == 0:
                ScoreBoard = HighScoresButtons(all_other_sprites)
                menuBar['high_scores'].append(ScoreBoard)
            else:
                menuBar['start'][0].update()
                mouse_motion_pos_x = character.rect.x
                while len(objectGroup['titles']) != 0:
                    objectGroup['titles'][0].remove()
                if len(objectGroup['enemy']) != 0:
                    objectGroup['enemy'][0].destroy()
                title = Tile(all_other_sprites, 225, 400)
                objectGroup['titles'].append(title)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.s is True:
                    game.pause()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                a = menuBar.keys()
                for i in a:
                    if menuBar[i]:
                        menuBar[i][0].clicked(event.pos, i)
                for i in settingsBar.keys():
                    if settingsBar[i]:
                        settingsBar[i][0].clicked(event.pos, i)
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
    if game.music:
        time += 2.5
    else:
        time = 1550
    if a == 2:
        game.sc += 2
        a = 0
    elif a == 1:
        game.sc += 1
        a = 0
    clock.tick(100)
    pygame.display.flip()
    if br:
        break
