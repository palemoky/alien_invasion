from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from .paths import IMAGES_DIR

if TYPE_CHECKING:
    from .main import Main


class Ship(Sprite):
    """管理飞船的类"""

    # 图像在所有飞船实例（含记分牌的生命图标）间共享，只加载一次
    _image: pygame.Surface | None = None

    # 收窄基类 Sprite 中 Optional 的类型声明（子类必定赋值）
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, game: Main) -> None:
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形；convert() 让 blit 更快
        if Ship._image is None:
            Ship._image = pygame.image.load(IMAGES_DIR / "ship.bmp").convert()
        self.image = Ship._image
        self.rect = self.image.get_rect()

        # 每艘飞船都在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 将飞船的 x 坐标转换为浮点数，便于后续移动时的坐标计算
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_left = False
        self.moving_right = False

    def update(self, *args: object, **kwargs: object) -> None:
        if self.moving_left and self.rect.left > 0:
            # 注意此处不可直接计算更新 self.rect.x！
            # 因为 pygame 中该坐标以整数表示，而移速是浮点数，直接计算会导致精度丢失、
            # 左右移速不一致。先把浮点结果暂存到 self.x，再赋值给 self.rect.x 即可避免。
            self.x -= self.settings.ship_speed
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        self.rect.x = int(self.x)

    def blitme(self) -> None:
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self) -> None:
        """将飞船放在屏幕底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
