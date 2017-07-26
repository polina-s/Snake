import pygame
from pygame.locals import *

WIDTH = 500
HEIGHT = 500

WHITE = (255, 255, 255)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return


if __name__ == '__main__': main()