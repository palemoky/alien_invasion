import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘飞船都在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 将飞船的 x 坐标转换为浮点数，便于后续移动时的坐标计算
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_left = False
        self.moving_right = False

    def update(self):
        if self.moving_left and self.rect.left > 0:
            """ 
            注意此处不可直接计算更新 self.rect.x！
            因为 pygame 中该坐标以整数表示，而移速是浮点数，计算更新会导致精度丢失，左右移速不一致的问题。
            先将浮点数计算结果暂存在 self.x 中再赋值给 self.rect.x，则可避免浮点数精度丢失的问题。
            """
            self.x -= self.settings.ship_speed
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
