# coding: utf-8

import sys
import math
import random
import pygame
from pygame.locals import *
from py_game import load_image
from py_game import split_image

START, PLAY, GAMEOVER = 0, 1, 2
SCR_RECT = Rect(0, 0, 640, 480)

class Invader:
    """ インベーダーゲーム """

    def __init__(self):
        """ コンストラクタ """
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("インベーダー:)")

        self.load_images()
        self.load_sounds()

        self.init_game()

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self):
        """ ゲームオブジェクトを初期化 """
        self.__game_state = START

        self.__all = pygame.sprite.RenderUpdates()
        self.__shots = pygame.sprite.Group()
        self.__aliens = pygame.sprite.Group()
        self.__beams = pygame.sprite.Group()

        Player.containers = self.__all
        Shot.containers = self.__all, self.__shots
        Alien.containers = self.__all, self.__aliens
        Beam.containers = self.__all, self.__beams
        Explosion.containers = self.__all

        self.__player = Player()
        for x, y in [(20 + (i % 10) * 40, 20 + int(i / 10) * 40) for i in range(0, 50)]: Alien((x, y))

    def update(self):
        """ ゲーム状態の更新 """
        if self.__game_state == PLAY:
            self.__all.update()
            self.collision_detection()
            if len(self.__aliens.sprites()) == 0:
                self.__game_state = GAMEOVER

    def draw(self, screen):
        """ 描画 """
        screen.fill((0, 0, 0))
        if self.__game_state == START:
            title_font = pygame.font.SysFont(None, 80)
            title = title_font.render("INVADER GAME", True, (255, 0, 0))
            screen.blit(title, (int((SCR_RECT.width - title.get_width()) / 2), 100))

            alien_image = Alien.get_image()
            screen.blit(alien_image, (int((SCR_RECT.width - alien_image.get_width()) / 2), 200))

            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", True, (255, 255, 255))
            screen.blit(push_space, (int((SCR_RECT.width - push_space.get_width()) / 2), 300))

            credit_font = pygame.font.SysFont(None, 20)
            credit = credit_font.render("http://www.pygame.org", True, (255, 255, 255))
            screen.blit(credit, (int((SCR_RECT.width - credit.get_width()) / 2), 380))
        elif self.__game_state == PLAY:
            self.__all.draw(screen)
        elif self.__game_state == GAMEOVER:
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(gameover, (int((SCR_RECT.width - gameover.get_width()) / 2), 100))

            alien_iamge = Alien.get_image()
            screen.blit(alien_iamge, (int((SCR_RECT.width - alien_iamge.get_width()) / 2), 200))

            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", True, (255, 255, 255))
            screen.blit(push_space, (int((SCR_RECT.width - push_space.get_width()) / 2), 300))

    def key_handler(self):
        """ キーハンドラ """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.__game_state == START:
                    self.__game_state = PLAY
                elif self.__game_state == GAMEOVER:
                    self.init_game()
                    self.__game_state = PLAY

    def collision_detection(self):
        """ 衝突判定 """
        aliens_collided = pygame.sprite.groupcollide(self.__aliens, self.__shots, True, True)
        for alien in aliens_collided.keys():
            Alien.kill_sound.play()
            Explosion(alien.rect.center)

        beam_collided = pygame.sprite.spritecollide(self.__player, self.__beams, True)
        if beam_collided:
            Player.bomb_sound.play()
            self.__game_state = GAMEOVER
    
    def load_images(self):
        """ イメージのロード """
        Player.load_image()
        Alien.load_image()

    def load_sounds(self):
        """ サウンドのロード """
        Player.load_sound()
        Alien.load_sound()

class Player(pygame.sprite.Sprite):
    """ 自機 """

    __SPEED = 5
    __reload_time = 15

    def __init__(self):
        super(Player, self).__init__(self.containers)
        self.image, self.rect = Player.__image, Player.__rect
        self.rect.bottom = SCR_RECT.bottom
        self.__reload_timer = 0

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.__SPEED, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.__SPEED, 0)
        self.rect.clamp_ip(SCR_RECT)

        if pressed_keys[K_SPACE]:
            if self.__reload_timer > 0:
                self.__reload_timer -= 1
            else:
                Player.shot_sound.play()
                Shot(self.rect.center)
                self.__reload_timer = self.__reload_time

    @staticmethod
    def load_image():
        Player.__image, Player.__rect = load_image(r"image\player.png")

    @staticmethod
    def load_sound():
        Player.shot_sound = pygame.mixer.Sound(r"sound\shot.wav")
        Player.bomb_sound = pygame.mixer.Sound(r"sound\bomb.wav")

class Shot(pygame.sprite.Sprite):
    """ プレイヤーのミサイル """

    __SPEED = 9

    def __init__(self, pos):
        super(Shot, self).__init__(self.containers)
        self.image, self.rect = load_image(r"image\shot.png")
        self.rect.center = pos

    def update(self):
        self.rect.move_ip(0, -self.__SPEED)
        if self.rect.top < 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    """ エイリアン """

    __SPEED = 2
    __frame = 0
    __ANIMCYCLE = 18
    __MOVE_WIDTH = 230
    __PROB_BEAM = 0.005

    def __init__(self, pos):
        super(Alien, self).__init__(self.containers)
        self.image = Alien.__images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.left = pos[0]
        self.right = self.left + self.__MOVE_WIDTH

    def update(self):
        self.rect.move_ip(self.__SPEED, 0)
        if self.rect.center[0] < self.left or self.right < self.rect.center[0]:
            self.__SPEED = -self.__SPEED
        if random.random() < self.__PROB_BEAM:
            Beam(self.rect.center)
        self.__frame += 1
        self.image = Alien.__images[int(self.__frame / self.__ANIMCYCLE) % 2]

    @staticmethod
    def load_image():
        img, rect = load_image(r"image\alien.png")
        Alien.__images = split_image(img, 2)

    @staticmethod
    def load_sound():
        Alien.kill_sound = pygame.mixer.Sound(r"sound\kill.wav")

    @staticmethod
    def get_image():
        return Alien.__images[0]

class Beam(pygame.sprite.Sprite):
    """ エイリアンが発射するビーム """

    __SPEED = 5

    def __init__(self, pos):
        super(Beam, self).__init__(self.containers)
        self.image, self.rect = load_image(r"image\beam.png")
        self.rect.center = pos

    def update(self):
        self.rect.move_ip(0, self.__SPEED)
        if SCR_RECT.height < self.rect.bottom:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    """ 爆破エフェクト """

    __frame = 0
    __ANIMCYCLE = 2

    def __init__(self, pos):
        super(Explosion, self).__init__(self.containers)
        img, rect = load_image(r"image\explosion.png")
        self.__images = split_image(img, 16)
        self.image = self.__images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.__MAX_FRAME = len(self.__images) * self.__ANIMCYCLE

    def update(self):
        self.image = self.__images[int(self.__frame / self.__ANIMCYCLE)]
        self.__frame += 1
        if self.__frame == self.__MAX_FRAME:
            self.kill()

def main():
    Invader()

if __name__ == "__main__":
    main()
