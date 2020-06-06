#! usr/bin/python3
# ------------ coding:utf-8------------
# author: John Lee time: 2020/6/5
import pygame
from plane_sprites import *


class PlaneGame(object):
    """Plane War v1.0"""

    def __init__(self):
        print("Initializing...")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        # 设置定时器事件
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Backgroud()
        bg2 = Backgroud(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        self.enemy_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("start game")

        while True:
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()

    # 捕获事件
    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()

            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
                for enemy in self.enemy_group.sprites():
                    enemy.fire()

            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 方向控制
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed_x = 5
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed_x = -5
        elif key_pressed[pygame.K_UP]:
            self.hero.speed_y = -5
        elif key_pressed[pygame.K_DOWN]:
            self.hero.speed_y = 5
        else:
            self.hero.speed_x = 0
            self.hero.speed_y = 0

    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        for enemy in self.enemy_group.sprites():
            bullets = pygame.sprite.groupcollide(self.hero_group, enemy.bullets, True, True)
            if len(bullets) > 0:
                self.hero.kill()
                PlaneGame.__game_over()
        enemies = pygame.sprite.groupcollide(self.hero_group, self.enemy_group, True, True)

        if len(enemies) > 0:
            self.hero.kill()
            PlaneGame.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        for enemy in self.enemy_group.sprites():
            enemy.bullets.update()
            enemy.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("game over!!!")

        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    # 启动游戏
    game.start_game()
