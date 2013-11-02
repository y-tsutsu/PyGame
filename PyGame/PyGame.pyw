# coding: utf-8

import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("PyGame")

while True:
    screen.fill((30, 30, 30))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
