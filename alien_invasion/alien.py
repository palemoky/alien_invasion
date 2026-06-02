import pygame
from pygame.sprite import Sprite

from .paths import IMAGES_DIR


class Alien(Sprite):
    """表示单个外星人的类"""

    # 图像在所有外星人实例间共享，只加载一次，避免每次创建都读盘
    _image = None

    def __init__(self, game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # 加载外星人图像并设置其rect属性；convert() 让 blit 更快
        if Alien._image is None:
            Alien._image = pygame.image.load(IMAGES_DIR / "alien.bmp").convert()
        self.image = Alien._image
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def update(self):
        """向左或向右移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edge(self):
        """如果外星人位于屏幕边缘，返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

