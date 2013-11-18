# coding: utf-8

import sys
import math
import pygame
from pygame.locals import *
from py_game import load_image

SCR_RECT = Rect(0, 0, 372, 384)

class Paddle(pygame.sprite.Sprite):
    """ ボールを打つパドル """

    def __init__(self):
        # containersはmain()でセットされる
        super(Paddle, self).__init__(self.containers)
        self.image, self.rect = load_image(r"image\paddle.png")
        self.rect.bottom = SCR_RECT.bottom

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.clamp_ip(SCR_RECT)

class Brick(pygame.sprite.Sprite):
    """ レンガ """
    
    def __init__(self, x, y):
        super(Brick, self).__init__(self.containers)
        self.image, self.rect = load_image(r"image\brick.png")
        self.rect.left = SCR_RECT.left + x * self.rect.width
        self.rect.top = SCR_RECT.left + y * self.rect.height

class Ball(pygame.sprite.Sprite):
    """ ボール """

    __speed = 5
    __angle_left = 135
    __angle_right = 45

    def __init__(self, paddle, bricks):
        super(Ball, self).__init__(self.containers)
        self.image, self.rect = load_image(r"image\ball.png")
        self.dx = self.dy = 0   # ボールの速度
        self.__paddle = paddle
        self.__bricks = bricks
        self.update = self.start

    def start(self):
        """ ボールの位置を初期化 """
        self.rect.centerx = self.__paddle.rect.centerx
        self.rect.bottom = self.__paddle.rect.top
        if pygame.mouse.get_pressed()[0] == 1:  # 左クリック
            self.dx = 0
            self.dy = -self.__speed
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
        if self.rect.colliderect(self.__paddle.rect) and 0 < self.dy:
            # パドルの左端に当たったときは135度，右端は45度とし，その間は線形補間で反射角度を算出
            x1 = self.__paddle.rect.left - self.rect.width
            y1 = self.__angle_left
            x2 = self.__paddle.rect.right
            y2 = self.__angle_right
            a = (y2 - y1) / (x2 - x1)
            x = self.rect.left
            y = a * (x - x1) + y1
            angle = math.radians(y)
            self.dx = self.__speed * math.cos(angle)
            self.dy = -self.__speed * math.sin(angle)
            self.paddle_sound.play()
        # ボールを落とした
        if SCR_RECT.bottom < self.rect.top:
            self.update = self.start
            self.fall_sound.play()
        # ブロックを壊す
        bricks_collided = pygame.sprite.spritecollide(self, self.__bricks, True)
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
                self.brick_sound.play()

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("ブロックくずし:)")

    Ball.paddle_sound = pygame.mixer.Sound(r"sound\paddle.wav")
    Ball.brick_sound = pygame.mixer.Sound(r"sound\brick.wav")
    Ball.fall_sound = pygame.mixer.Sound(r"sound\fall.wav")

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
