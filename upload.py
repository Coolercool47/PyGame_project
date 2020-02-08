import os
import pygame
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    image = pygame.image.load(fullname)
    return image


class GameOver(pygame.sprite.Sprite):

    image = load_image("exit.png")

    def __init__(self, group):

        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = GameOver.image
        colorKey = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(colorKey)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        while True:
            c = bool(True)
            self.rect.x = random.randint(0, 400)
            self.rect.y = random.randint(0, 400)
            for i in range(len(x_yGroup)):
                if pygame.sprite.collide_mask(self, x_yGroup[i]):
                    c = bool(False)
                    break
            if c == bool(True):
                break

    def clicked(self, pos, index, group):
        if self.rect.collidepoint(pos):
            group.remove(group.sprites()[index])
            Boom(group, self.rect.x, self.rect.y)


class Boom(pygame.sprite.Sprite):

    image = load_image("pause.png")

    def __init__(self, group, x, y):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Boom.image
        colorKey = self.sprite.image.get_at((0, 0))
        self.sprite.image.set_colorkey(colorKey)
        self.rect = self.sprite.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite.image)
        self.rect.x = x
        self.rect.y = y

    def clicked(self, *args):
        pass


pygame.init()
# размеры окна:
size = width, height = 500, 500

screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))

x = int()
y = int()
x_yGroup = list()
running = True
all_sprites = pygame.sprite.Group()
for i in range(10):
    gO = GameOver(all_sprites)
    x_yGroup.append(gO)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                a = len(all_sprites.sprites())
                for i in range(a):
                    all_sprites.sprites()[i].clicked(event.pos, i, all_sprites)
                    if a > len(all_sprites.sprites()):
                        break
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()