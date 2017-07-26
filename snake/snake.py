import os
import pygame
from pygame.locals import *
from collections import deque

WIDTH = 500
HEIGHT = 500
STEP = 20

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

    def coord(self):
        return self.rect.topleft

    def change_pos(self, xy):
        self.rect.topleft = xy


class Snake(object):
    def __init__(self):
        self.segments = deque()
        self.segments.append(Segment([STEP,STEP]))
        self.segments.append(Segment([2*STEP,STEP]))
        self.segments.append(Segment([3*STEP,STEP]))
        self.segments.append(Segment([4*STEP,STEP]))

    def head_coord(self):
        return self.segments[len(self.segments)-1].coord()

    def newpos(self):
        return [self.head_coord()[0] + STEP, self.head_coord()[1]]

    def move(self):
        self.segments[0].change_pos(self.newpos())
        self.segments.append(self.segments.popleft())


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

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple([100, 100])

    sprites = pygame.sprite.Group(snake.segments, apple)

    screen.blit(background, (0, 0))
    sprites.draw(screen)
    pygame.display.flip()

    while 1:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        snake.move()
        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()