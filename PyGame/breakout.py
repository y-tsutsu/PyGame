# coding: utf-8

import sys
import pygame
from pygame.locals import *
from py_game import load_image

SCR_RECT = Rect(0, 0, 372, 384)

class Paddle(pygame.sprite.Sprite):
    """ ボールを打つパドル """

    def __init__(self):
        # containersはmain()でセットされる
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image(r"image\paddle.png")
        self.rect.bottom = SCR_RECT.bottom

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.clamp_ip(SCR_RECT)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("ブロックくずし:)")

    all = pygame.sprite.RenderUpdates()
    Paddle.containers = all

    paddle = Paddle()

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))
        all.update()
        all.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
