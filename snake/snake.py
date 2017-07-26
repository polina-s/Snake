import os, random
import pygame
from pygame.locals import *
from collections import deque

WIDTH = 500
HEIGHT = 500
STEP = 20

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

dir_map = {'UP': (0, -STEP), 'DOWN': (0, STEP), 'RIGHT': (STEP, 0), 'LEFT': (-STEP, 0)}

def load_png(png):
    fullname = os.path.join(png)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as err:
        print("Can't load image.")
        raise SystemExit(err.args[0])
    image = image.convert_alpha()
    return image, image.get_rect()\

def write(text, size, pos, color):
    font = pygame.font.Font(None, size)
    tx = font.render(text, True, color)
    tx_rect = tx.get_rect()
    tx_rect.center = pos
    return tx, tx_rect


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
        self.dir = 'RIGHT'

    def head_coord(self):
        return self.segments[len(self.segments)-1].coord()

    def newpos(self):
        return [self.head_coord()[0] + dir_map[self.dir][0], self.head_coord()[1] + dir_map[self.dir][1]]

    def ok_turn(self, side):
        if (self.dir == 'RIGHT' and side == 'LEFT') or \
                (self.dir == 'LEFT' and side == 'RIGHT') or \
                (self.dir == 'UP' and side == 'DOWN') or \
                (self.dir == 'DOWN' and side == 'UP'):
            return False
        else:
            return True

    def move(self):
        self.segments[0].change_pos(self.newpos())
        self.segments.append(self.segments.popleft())

    def grow(self):
        new_segm = Segment(self.newpos())
        self.segments.append(new_segm)
        return new_segm

    def self_crash(self):
        n = len(self.segments)
        for i in range(1, n):
            for j in range(i+1, n):
                if self.segments[i].rect.colliderect(self.segments[j].rect):
                    return True
        return False


class Apple(pygame.sprite.Sprite):
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('apple.png')
        self.rect.topleft = xy

    def coord(self):
        return self.rect.topleft

    def update(self):
        self.rect.topleft = (random.randrange(0, WIDTH, STEP), random.randrange(0, WIDTH, STEP))


def game(screen, clock):
    screen_area = screen.get_rect()

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    snake = Snake()
    apple = Apple([100, 100])
    snake_group = pygame.sprite.RenderUpdates(snake.segments)
    apple_group = pygame.sprite.RenderUpdates(apple)

    screen.blit(background, (0, 0))
    apple_group.draw(screen)
    snake_group.draw(screen)
    pygame.display.flip()

    speed = 5

    while 1:
        clock.tick(speed)

        new_dir = snake.dir
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    new_dir = 'UP'
                elif event.key == K_DOWN:
                    new_dir = 'DOWN'
                elif event.key == K_RIGHT:
                    new_dir = 'RIGHT'
                elif event.key == K_LEFT:
                    new_dir = 'LEFT'

        if snake.ok_turn(new_dir):
            snake.dir = new_dir

        if snake.head_coord() == apple.coord():
            snake_group.add(snake.grow())
            while pygame.sprite.spritecollideany(apple, snake_group):
                apple_group.update()
            if len(snake.segments) % 5 == 0:
                speed = speed + 1
        else:
            snake.move()

        if snake.self_crash() or not screen_area.collidepoint(snake.head_coord()):
            return

        screen.blit(background, (0, 0))
        apple_group.draw(screen)
        snake_group.draw(screen)
        pygame.display.flip()


def play_again(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)
    text1, text1r = write("Game over", 80, (250, 200), RED)
    text3, text3r = write("Play again", 55, (250, 350), BLUE)
    screen.blit(background, (0, 0))
    screen.blit(text1, text1r)
    screen.blit(text3, text3r)
    pygame.display.flip()
    while 1:
        event = pygame.event.wait()
        if event.type == QUIT:
            return False
        elif event.type == MOUSEBUTTONDOWN:
            return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    while 1:
        game(screen, clock)
        if not play_again(screen):
            return

if __name__ == '__main__': main()