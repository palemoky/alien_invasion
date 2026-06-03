import logging
import sys
from time import sleep

import pygame

from .alien import Alien
from .bullet import Bullet
from .fonts import get_cjk_font
from .game_stats import GameStats
from .i18n import Translator
from .logging_config import configure_logging
from .scoreboard import ScoreBoard
from .settings import Settings
from .ship import Ship

logger = logging.getLogger(__name__)


class Main:
    """管理游戏资源和行为的类"""

    def __init__(self) -> None:
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # 窗口模式
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE
        )

        # 全屏模式
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 创建一个用于存储游戏统计信息的实例，并创建记分牌
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets: pygame.sprite.Group = pygame.sprite.Group()
        self.aliens: pygame.sprite.Group = pygame.sprite.Group()
        self._create_fleet()

        # 游戏启动后处于活动状态
        self.game_active = False
        self.paused = False

        # 根据系统语言选择界面语言（默认英文，系统为中文时显示中文）
        self.t = Translator()
        logger.info("界面语言：%s", self.t.lang)

        # 难度菜单（超级玛丽式竖向选择），文案随语言切换
        self._difficulties: list[str] = ["easy", "normal", "hard"]
        # 默认高亮当前难度
        self._menu_index = next(
            (i for i, key in enumerate(self._difficulties) if key == self.settings.difficulty),
            1,
        )

        # 文字字体（需支持中文）
        self.menu_title_font = get_cjk_font(56)
        self.msg_font = get_cjk_font(40)
        self.hint_font = get_cjk_font(28)

    def run_game(self) -> None:
        """开始游戏的主循环"""
        while True:
            # 侦听键盘与鼠标事件
            self._check_events()

            if self.game_active and not self.paused:
                # 根据按键做出反应
                self.ship.update()
                # 更新子弹位置并删除子弹
                self._update_bullets()
                # 更新飞碟位置
                self._update_aliens()

            # 刷新图像位置
            self._update_screen()
            # 设置游戏帧率
            self.clock.tick(self.settings.fps)

    def _check_events(self) -> None:
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

    def _check_play_button(self, mouse_pos: tuple[int, int]) -> None:
        """在开始界面点击某个难度项即可开始游戏。"""
        if self.game_active:
            return
        for index, _key, _image, rect in self._menu_layout():
            if rect.collidepoint(mouse_pos):
                self._menu_index = index
                self._start_game()
                return

    def _start_game(self) -> None:
        """以当前选中的难度开始新游戏。"""
        if self.game_active:
            return

        # 应用选中的难度（内部会重置动态设置）
        self.settings.set_difficulty(self._difficulties[self._menu_index])

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏信息
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True
        self.paused = False

        # 清空外星人列表与子弹列表
        self.bullets.empty()
        self.aliens.empty()

        # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
        self._create_fleet()
        self.ship.center_ship()
        logger.info("开始新游戏（难度：%s）", self.settings.difficulty)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        # 左右移动
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and self.game_active:
            # 暂停 / 继续
            self.paused = not self.paused
            pygame.mouse.set_visible(self.paused)
            logger.info("游戏%s", "暂停" if self.paused else "继续")
        elif event.key == pygame.K_UP and not self.game_active:
            # 在开始界面向上移动难度光标
            self._menu_index = (self._menu_index - 1) % len(self._difficulties)
        elif event.key == pygame.K_DOWN and not self.game_active:
            # 在开始界面向下移动难度光标
            self._menu_index = (self._menu_index + 1) % len(self._difficulties)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and not self.game_active:
            # 回车确认所选难度并开始游戏
            self._start_game()
        elif event.key == pygame.K_q:
            # 退出游戏（按下 Cmd+Q 或 Ctrl+Q）
            mods = pygame.key.get_mods()
            if mods & (pygame.KMOD_META | pygame.KMOD_CTRL):
                sys.exit()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self) -> None:
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self) -> None:
        # 更新子弹位置
        self.bullets.update()

        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _create_fleet(self) -> None:
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

    def _check_fleet_edges(self) -> None:
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _check_alien_bottom(self) -> None:
        """检查是否有外星人到达屏幕下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break

    def _change_fleet_direction(self) -> None:
        """将整个外星舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position: int, y_position: int) -> None:
        """创建一个外星人并将其放在当前行中"""
        logger.debug("创建外星人 @ (%s, %s)", x_position, y_position)
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self) -> None:
        """更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕的下边缘
        self._check_alien_bottom()

    def _ship_hit(self) -> None:
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将 ships_left 减 1 并更新记分牌
            self.stats.ships_left -= 1
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
            logger.info("游戏结束，最终得分 %s", self.stats.score)

    def _check_bullet_alien_collisions(self) -> None:
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
            logger.info("进入第 %s 关", self.stats.level)

    def _update_screen(self) -> None:
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        if not self.game_active:
            self._draw_start_menu()
        elif self.paused:
            self._draw_center_text(self.t("paused"))

        # 更新屏幕
        pygame.display.flip()

    def _draw_center_text(self, msg: str, dy: int = 0) -> None:
        """在屏幕中央绘制一行提示文字。"""
        image = self.msg_font.render(msg, True, (30, 30, 30))
        rect = image.get_rect()
        rect.center = self.screen.get_rect().center
        rect.y += dy
        self.screen.blit(image, rect)

    def _menu_layout(self) -> list[tuple[int, str, pygame.Surface, pygame.Rect]]:
        """计算难度菜单各项（图像与位置），供绘制与鼠标点击共用。"""
        center = self.screen.get_rect().center
        layout: list[tuple[int, str, pygame.Surface, pygame.Rect]] = []
        for index, key in enumerate(self._difficulties):
            selected = index == self._menu_index
            color = (255, 255, 255) if selected else (90, 90, 90)
            image = self.msg_font.render(self.t(key), True, color)
            rect = image.get_rect()
            rect.centerx = center[0]
            rect.centery = center[1] - 20 + index * 60
            layout.append((index, key, image, rect))
        return layout

    def _draw_start_menu(self) -> None:
        """绘制超级玛丽式的竖向难度菜单。"""
        screen_rect = self.screen.get_rect()

        title = self.menu_title_font.render(self.t("title"), True, (30, 30, 30))
        title_rect = title.get_rect(centerx=screen_rect.centerx, centery=screen_rect.centery - 150)
        self.screen.blit(title, title_rect)

        for index, _key, image, rect in self._menu_layout():
            if index == self._menu_index:
                # 选中项绘制一个高亮底框（超级玛丽式光标）
                highlight = rect.inflate(220 - rect.width, 18)
                highlight.centerx = rect.centerx
                pygame.draw.rect(self.screen, (0, 135, 0), highlight, border_radius=8)
            self.screen.blit(image, rect)

        hint = self.hint_font.render(self.t("menu_hint"), True, (120, 120, 120))
        hint_rect = hint.get_rect(centerx=screen_rect.centerx, centery=screen_rect.centery + 170)
        self.screen.blit(hint, hint_rect)


def run() -> None:
    """创建游戏实例并运行游戏"""
    configure_logging()
    logger.info("启动 Alien Invasion")
    ai = Main()
    ai.run_game()


if __name__ == "__main__":
    run()
