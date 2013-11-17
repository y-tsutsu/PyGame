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

class Ball(pygame.sprite.Sprite):
    """ ボール """

    speed = 5

    def __init__(self, paddle):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image(r"image\ball.png")
        self.dx = self.dy = 0   # ボールの速度
        self.paddle = paddle
        self.update = self.start

    def start(self):
        """ ボールの位置を初期化 """
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        if pygame.mouse.get_pressed()[0] == 1:  # 左クリック
            self.dx = self.speed
            self.dy = -self.speed
            self.update = self.move

    def move(self):
        """ ボールの移動 """
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        # 壁との反射
        if self.rect.left < SCR_RECT.left:
            self.rect.left = SCR_RECT.left
            self.dx = -self.dx
        if SCR_RECT.right < self.rect.right:
            self.rect.right = SCR_RECT.right
            self.dx = -self.dx
        if self.rect.top < SCR_RECT.top:
            self.rect.top = SCR_RECT.top
            self.dy = -self.dy
        # パドルとの反射
        if self.rect.colliderect(self.paddle.rect) and 0 < self.dy:
            self.dy = -self.dy
        # ボールを落とした
        if SCR_RECT.bottom < self.rect.top:
            self.update = self.start

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("ブロックくずし:)")

    all = pygame.sprite.RenderUpdates()
    Paddle.containers = all
    Ball.containers = all

    paddle = Paddle()
    Ball(paddle)

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
