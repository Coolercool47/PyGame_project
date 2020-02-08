import pygame
import random
import os

running = True
pygame.init()
time = 1500
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.flip()
num = 0


def load_image(name):
    fullname = os.path.join('data', name)
    image0 = pygame.image.load(fullname)
    return image0


image = load_image("play.png")
image = pygame.transform.scale(image, (50, 10))

all_sprites = pygame.sprite.Group()
jump_sound = pygame.mixer.Sound(os.path.join('data', 'jump.wav'))
main_theme = pygame.mixer.Sound(os.path.join('data', 'main_theme.wav'))
start = True


class TestObject(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        global start
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 50)
        if start:
            self.rect.y = random.randrange(height)
        else:
            self.rect.y = random.randrange(-20, -10)

    def update(self, button):
        global num
        if button == 5:
            self.rect = self.rect.move(0, 10)
        elif button == 4:
            self.rect = self.rect.move(0, -10)
        if self.rect.y > 500:
            self.remove(all_sprites)
            num -= 1


for _ in range(10):
    num = 10
    TestObject(all_sprites)

# ожидание закрытия окна:
clock = pygame.time.Clock()
while running:
    start = False
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    if num != 10:
        for i in range(10 - num):
            TestObject(all_sprites)
        num = 10
    if time == 1500:
        time = 0
        main_theme.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event.button)
            # jump_sound.play()
    pygame.display.flip()
    time += 10
    clock.tick(100)
pygame.quit()
