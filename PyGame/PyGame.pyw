# coding: utf-8

import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

def load_image(filename, colorkey = None):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)

    image = image.convert_alpha()

    if colorkey != None:
        if colorkey == -1:
            dolorkye = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("PyGame:)")

    sysfont = pygame.font.SysFont(None, 80)
    hello1 = sysfont.render("Hello Python!!", False, (255,0,102))
    hello2 = sysfont.render("Hello Python!!", True, (200, 200, 200))
    hello3 = sysfont.render("Hello Python!!", True, (30, 30, 30), (128, 128, 128))

    image, rect = load_image("image\\gloomy.png")

    while True:
        # 背景
        screen.fill((30, 30, 30)) 

        # 図形
        pygame.draw.rect(screen, (255, 255, 0), Rect(10, 10, 300, 200), 2)
        pygame.draw.circle(screen, (255, 0, 0), (320, 240), 100)
        pygame.draw.ellipse(screen, (255, 0, 255), (400, 300, 200, 100), 4)
        pygame.draw.line(screen, (255, 255, 255), (0, 0), (640, 480), 6)

        # テキスト
        screen.blit(hello1, (20, 50))
        screen.blit(hello2, (20, 120))
        screen.blit(hello3, (20, 190))

        # 画像
        screen.blit(image, (50, 230))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
