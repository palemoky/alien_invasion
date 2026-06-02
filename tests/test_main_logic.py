import pygame


def _keydown(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def _keyup(key):
    return pygame.event.Event(pygame.KEYUP, key=key)


def test_play_button_click_starts_game(game):
    game.game_active = False
    game._check_play_button(game.play_button.rect.center)
    assert game.game_active is True
    assert game.paused is False
    assert len(game.aliens) > 0


def test_play_button_click_outside_does_nothing(game):
    game.game_active = False
    game._check_play_button((0, 0))
    assert game.game_active is False


def test_keyup_stops_movement(game):
    game.ship.moving_left = True
    game.ship.moving_right = True
    game._check_keyup_events(_keyup(pygame.K_LEFT))
    game._check_keyup_events(_keyup(pygame.K_RIGHT))
    assert game.ship.moving_left is False
    assert game.ship.moving_right is False


def test_keydown_moves_ship(game):
    game._check_keydown_events(_keydown(pygame.K_LEFT))
    assert game.ship.moving_left is True
    game._check_keydown_events(_keydown(pygame.K_RIGHT))
    assert game.ship.moving_right is True


def test_change_fleet_direction_flips_and_drops(game):
    direction = game.settings.fleet_direction
    ys_before = [a.rect.y for a in game.aliens.sprites()]
    game._change_fleet_direction()
    assert game.settings.fleet_direction == -direction
    ys_after = [a.rect.y for a in game.aliens.sprites()]
    assert all(b < a for b, a in zip(ys_before, ys_after, strict=True))


def test_check_fleet_edges_triggers_direction_change(game):
    direction = game.settings.fleet_direction
    alien = game.aliens.sprites()[0]
    alien.rect.right = game.screen.get_rect().right + 1
    game._check_fleet_edges()
    assert game.settings.fleet_direction == -direction


def test_alien_reaching_bottom_costs_a_life(game):
    game.game_active = True
    game.stats.ships_left = 3
    alien = game.aliens.sprites()[0]
    alien.rect.bottom = game.settings.screen_height
    game._check_alien_bottom()
    assert game.stats.ships_left == 2


def test_update_bullets_removes_offscreen(game):
    game._fire_bullet()
    bullet = next(iter(game.bullets))
    # 把子弹移到屏幕上方之外（update() 会用 self.y 重算 rect）
    bullet.y = -100.0
    game._update_bullets()
    assert bullet not in game.bullets


def test_update_screen_runs_in_all_states(game):
    game._update_screen()  # 开始界面
    game.game_active = True
    game._update_screen()  # 进行中
    game.paused = True
    game._update_screen()  # 暂停
