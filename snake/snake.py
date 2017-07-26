import os
import pygame
from pygame.locals import *

WIDTH = 500
HEIGHT = 500

WHITE = (255, 255, 255)

def load_png(png):
    fullname = os.path.join(png)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as err:
        print("Can't load image.")
        raise SystemExit(err.args[0])
    image = image.convert_alpha()
    return image, image.get_rect()


class Segment(pygame.sprite.Sprite):
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('segment.png')
        self.rect.topleft = xy


class Apple(pygame.sprite.Sprite):
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('apple.png')
        self.rect.topleft = xy


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    segm = Segment([20, 20])
    apple = Apple([100, 100])

    sprites = pygame.sprite.Group(segm, apple)

    screen.blit(background, (0, 0))
    sprites.draw(screen)
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return


if __name__ == '__main__': main()