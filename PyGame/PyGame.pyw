# coding: utf-8

import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("PyGame:)")

sysfont = pygame.font.SysFont(None, 80)
hello1 = sysfont.render("Hello Python!!", False, (0, 0, 0))
hello2 = sysfont.render("Hello Python!!", True, (255,0,102))
hello3 = sysfont.render("Hello Python!!", True, (30, 30, 30), (128, 128, 128))

while True:
    screen.fill((30, 30, 30))

    screen.blit(hello1, (20, 50))
    screen.blit(hello2, (20, 120))
    screen.blit(hello3, (20, 190))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
