import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


class Main:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # 窗口模式
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # 全屏模式
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 侦听键盘与鼠标事件
            self._check_events()
            # 根据按键做出反应
            self.ship.update()
            # 更新子弹位置并删除子弹
            self._update_bullets()

            # 刷新图像位置
            self._update_screen()
            # 设置游戏帧率为 60fps
            self.clock.tick(60)

    def _check_events(self):
        """响应按钮和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # 左右移动
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        # 退出游戏（按下 Cmd+Q 或 Ctrl+Q）
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and (keys[pygame.KMOD_META] or keys[pygame.KMOD_CTRL]):
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # 更新子弹位置
        self.bullets.update()

        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = Main()
    ai.run_game()
