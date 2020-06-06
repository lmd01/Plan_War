#! usr/bin/python3
# ------------ coding:utf-8------------
# author: John Lee time: 2020/6/5
import pygame
import random
# 屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 屏幕刷新帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 发射子弹定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):  # 重写父类的update方法
        # 在y方向运动
        self.rect.y += self.speed


class Backgroud(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):

        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self, *args):
        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        super().__init__("./images/enemy1.png")

        self.speed = random.randint(1, 3)

        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.bullets = pygame.sprite.Group()

    def update(self, *args):
        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

    def fire(self):
        bullet = EnemyBullet(self.speed + 2)

        bullet.rect.y = self.rect.bottom
        bullet.rect.centerx = self.rect.centerx

        self.bullets.add(bullet)

    # def test(self):
    #     print("111")


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self, speed_x=1, speed_y=0):
        super().__init__("./images/me1.png", 0)
        # 英雄初始位置设置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.speed_x = speed_x
        self.speed_y = speed_y
        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self, *args):
        self.rect.x += self.speed_x
        if self.rect.x < - self.rect.width / 2:
            self.rect.x = - self.rect.width / 2
        elif self.rect.right > SCREEN_RECT.right + self.rect.width / 2:
            self.rect.right = SCREEN_RECT.right + self.rect.width / 2

        self.rect.y += self.speed_y
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        # 创建子弹精灵
        bullet1 = Bullet()
        bullet2 = Bullet()
        bullet3 = Bullet()
        # 设置精灵位置
        bullet1.rect.bottom = self.rect.y - 20
        bullet1.rect.centerx = self.rect.centerx

        bullet2.rect.bottom = self.rect.y - 20
        bullet2.rect.centerx = self.rect.centerx - self.rect.width / 3

        bullet3.rect.bottom = self.rect.y - 20
        bullet3.rect.centerx = self.rect.centerx + self.rect.width / 3
        # 将精灵添加到精灵组
        self.bullets.add(bullet1, bullet2, bullet3)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        super().__init__("./images/bullet2.png", -6)

    def update(self, *args):
        super().update()

        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(GameSprite):
    """敌机子弹精灵"""

    def __init__(self, speed):
        super().__init__("./images/bullet1.png")
        self.speed = speed

    def update(self, *args):
        super().update()

        if self.rect.bottom > SCREEN_RECT.bottom:
            self.kill()
