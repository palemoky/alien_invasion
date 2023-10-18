import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class Main:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # 窗口模式
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height),
                                              pygame.RESIZABLE)

        # 全屏模式
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 创建一个用于存储游戏统计信息的实例，并创建记分牌
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 游戏启动后处于活动状态
        self.game_active = False

        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 侦听键盘与鼠标事件
            self._check_events()

            if self.game_active:
                # 根据按键做出反应
                self.ship.update()
                # 更新子弹位置并删除子弹
                self._update_bullets()
                # 更新飞碟位置
                self._update_aliens()

            # 刷新图像位置
            self._update_screen()
            # # 显示指针坐标，便于调试
            # self._show_mouse_coordinates()
            # 设置游戏帧率
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """响应按钮和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            if self.play_button.rect.collidepoint(mouse_pos):
                # 还原游戏设置
                self.settings.initialize_dynamic_settings()

                # 隐藏光标
                pygame.mouse.set_visible(False)

                # 重置游戏信息
                self.stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
                self.game_active = True

                # 清空外星人列表与子弹列表
                self.bullets.empty()
                self.aliens.empty()

                # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
                self._create_fleet()
                self.ship.center_ship()

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

        self._check_bullet_alien_collisions()

    def _create_fleet(self):
        """创建一个外星舰队"""
        alien = Alien(self)
        # 外星人的间距和高度为外星人的宽度和高度
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 添加一行外星人后，重置 x 值并递增 y 值
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _check_alien_bottom(self):
        """检查是否有外星人到达屏幕下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行中"""
        # print(f"飞碟坐标为：({x_position},{y_position})")
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕的下边缘
        self._check_alien_bottom()

    def _show_mouse_coordinates(self):
        screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        font = pygame.font.Font(None, 16)

        # 获取鼠标当前位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 清空屏幕
        self.screen.fill((255, 255, 255), (10, 10, self.settings.screen_width, self.settings.screen_height))
        # 绘制坐标信息
        text = font.render(f"Mouse Coordinates: ({mouse_x}, {mouse_y})", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        # 局部刷新
        pygame.display.update((10, 10, text.get_width(), text.get_height()))

    # def _update_coordinates(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.MOUSEMOTION:
    #             self._show_mouse_coordinates()

    def _show_coordinates(self):
        font = pygame.font.Font(None, 16)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = font.render(f"Mouse Coordinates: ({mouse_x}, {mouse_y})", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        pygame.display.update((10, 10, text.get_width(), text.get_height()))

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将 ships_left 减 1 并更新记分牌
            self.stats.ships_left = -1
            self.sb.prep_ships()

            # 清空子弹与飞碟
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星舰队，并将飞船放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_bullet_alien_collisions(self):
        # 检查子弹是否击中飞碟，击中则删除对应子弹与飞碟
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的所有子弹，并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()

        # 更新屏幕
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = Main()
    ai.run_game()
