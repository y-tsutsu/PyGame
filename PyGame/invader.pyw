# coding: utf-8

import sys
import math
import pygame
from pygame.locals import *
from py_game import load_image

SCR_RECT = Rect(0, 0, 640, 480)

class Player(pygame.sprite.Sprite):
    """ 自機 """

    __speed = 5
    __reload_time = 15

    def __init__(self):
        super(Player, self).__init__(self.containers)
        self.image, self.rect = load_image(r"image\player.png")
        self.rect.bottom = SCR_RECT.bottom
        self.__reload_timer = 0

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.__speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.__speed, 0)
        self.rect.clamp_ip(SCR_RECT)

        if pressed_keys[K_SPACE]:
            if self.__reload_timer > 0:
                self.__reload_timer -= 1
            else:
                Player.shot_sount.play()
                Shot(self.rect.center)
                self.__reload_timer = self.__reload_time

class Shot(pygame.sprite.Sprite):
    """ プレイヤーのミサイル """

    __speed = 9

    def __init__(self, pos):
        super(Shot, self).__init__(self.containers)
        self.image, self.rect = load_image(r"image\shot.png")
        self.rect.center = pos

    def update(self):
        self.rect.move_ip(0, -self.__speed)
        if self.rect.top < 0:
            self.kill()

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("インベーダー:)")

    all = pygame.sprite.RenderUpdates()
    Player.containers = all
    Shot.containers = all
    Player.shot_sount = pygame.mixer.Sound(r"sound\shot.wav")
    Player()

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((30, 30, 30))
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
