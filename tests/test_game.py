def test_create_fleet_makes_aliens(game):
    # 初始化时已创建一支舰队
    assert len(game.aliens) > 0


def test_ship_hit_decrements_lives(game):
    """回归测试：曾经误写成 ships_left = -1。"""
    game.stats.ships_left = 3
    game.game_active = True

    game._ship_hit()

    assert game.stats.ships_left == 2
    assert game.game_active is True


def test_ship_hit_resets_fleet_and_bullets(game):
    game.stats.ships_left = 3
    game._fire_bullet()
    assert len(game.bullets) > 0

    game._ship_hit()

    # 被撞后子弹清空、舰队重建
    assert len(game.bullets) == 0
    assert len(game.aliens) > 0


def test_ship_hit_ends_game_when_no_lives(game):
    game.stats.ships_left = 0
    game.game_active = True

    game._ship_hit()

    assert game.game_active is False


def test_bullet_alien_collision_scores_and_levels_up(game):
    """击落整支舰队后应清空子弹、提升等级、加速。"""
    game.stats.score = 0
    start_level = game.stats.level
    start_alien_speed = game.settings.alien_speed

    # 清掉所有外星人，模拟全部被击落
    game.aliens.empty()
    game._check_bullet_alien_collisions()

    assert game.stats.level == start_level + 1
    assert game.settings.alien_speed > start_alien_speed
    assert len(game.aliens) > 0  # 生成了新舰队


def test_fire_bullet_respects_limit(game):
    game.bullets.empty()
    for _ in range(game.settings.bullets_allowed + 5):
        game._fire_bullet()
    assert len(game.bullets) == game.settings.bullets_allowed
