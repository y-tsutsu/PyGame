# coding: utf-8

import pygame
from pygame.locals import *
import sys

SCR_WIDTH, SCR_HEIGHT = 640, 480

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
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("PyGame:)")

    sysfont = pygame.font.SysFont(None, 80)
    hello1 = sysfont.render("Hello Python!!", False, (102,0,255))
    hello2 = sysfont.render("Hello Python!!", True, (200, 200, 200))
    hello3 = sysfont.render("Hello Python!!", True, (30, 30, 30), (128, 128, 128))

    gloomy_image, gloomy_rect = load_image("image\\gloomy.png")
    gloomy_rect.topleft = (50, 230)
    gloomy_vx_pixel = gloomy_vy_pixel = 240

    cat_image, cat_rect = load_image("image\\catpink.png")
    cat_rect.topleft = (0, 0)
    cat_vx_pixel = cat_vy_pixel = 120

    while True:
        time_seconds = pygame.time.Clock().tick(60) / 1000.0  # 60fpsで前回からの経過時間

        # 背景
        screen.fill((30, 30, 30)) 

        # 図形
        pygame.draw.line(screen, (64, 64, 64), (0, 0), (640, 480), 6)
        pygame.draw.ellipse(screen, (255, 64, 255), (400, 300, 200, 100), 4)
        pygame.draw.rect(screen, (255, 255, 128), Rect(10, 10, 300, 200), 2)
        pygame.draw.circle(screen, (32, 64, 128), (320, 240), 100)

        # テキスト
        screen.blit(hello1, (20, 50))
        screen.blit(hello2, (20, 120))
        screen.blit(hello3, (20, 190))

        # マウス
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            x, y = pygame.mouse.get_pos()
            gloomy_rect.center = (x, y)

        # キー
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_LEFT]:
            gloomy_rect.move_ip(-gloomy_vx_pixel * time_seconds, 0)
        if key_pressed[K_RIGHT]:
            gloomy_rect.move_ip(gloomy_vx_pixel * time_seconds, 0)
        if key_pressed[K_UP]:
            gloomy_rect.move_ip(0, -gloomy_vy_pixel * time_seconds)
        if key_pressed[K_DOWN]:
            gloomy_rect.move_ip(0, gloomy_vy_pixel * time_seconds)

        # グルーミー移動
        screen.blit(gloomy_image, gloomy_rect)

        # ネコ移動
        cat_rect.move_ip(cat_vx_pixel * time_seconds, cat_vy_pixel * time_seconds)
        if cat_rect.left < 0 or SCR_WIDTH < cat_rect.right:
            cat_vx_pixel = -cat_vx_pixel
        if cat_rect.top < 0 or SCR_HEIGHT < cat_rect.bottom:
            cat_vy_pixel = -cat_vy_pixel
        screen.blit(cat_image, cat_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
