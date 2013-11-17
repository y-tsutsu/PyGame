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

class Brick(pygame.sprite.Sprite):
    """ レンガ """
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image(r"image\brick.png")
        self.rect.left = SCR_RECT.left + x * self.rect.width
        self.rect.top = SCR_RECT.left + y * self.rect.height

class Ball(pygame.sprite.Sprite):
    """ ボール """

    speed = 5

    def __init__(self, paddle, bricks):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image(r"image\ball.png")
        self.dx = self.dy = 0   # ボールの速度
        self.paddle = paddle
        self.bricks = bricks
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
        # ブロックを壊す
        bricks_collided = pygame.sprite.spritecollide(self, self.bricks, True)
        if bricks_collided:
            oldrect = self.rect
            for brick in bricks_collided:
                if oldrect.left < brick.rect.left < oldrect.right < brick.rect.right:
                    self.rect.right = brick.rect.left
                    self.dx = -self.dx
                if brick.rect.left < oldrect.left < brick.rect.right < oldrect.right:
                    self.rect.left = brick.rect.right
                    self.dx = -self.dx
                if oldrect.top < brick.rect.top < oldrect.bottom < brick.rect.bottom:
                    self.rect.bottom = brick.rect.top
                    self.dy = -self.dy
                if brick.rect.top < oldrect.top < brick.rect.bottom < oldrect.bottom:
                    self.rect.top = brick.rect.bottom
                    self.dy = -self.dy

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("ブロックくずし:)")

    all = pygame.sprite.RenderUpdates()
    bricks = pygame.sprite.Group()
    Paddle.containers = all
    Ball.containers = all
    Brick.containers = (all, bricks)

    paddle = Paddle()
    Ball(paddle, bricks)
    for x in range(1, 11):
        for y in range(1, 6):
            Brick(x, y)

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
