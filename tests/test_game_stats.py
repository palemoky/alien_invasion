from alien_invasion.game_stats import GameStats


def test_reset_stats_defaults(game):
    stats = GameStats(game)
    assert stats.ships_left == game.settings.ship_limit
    assert stats.score == 0
    assert stats.level == 1


def test_high_score_not_reset(game):
    stats = GameStats(game)
    stats.high_score = 9999
    stats.reset_stats()
    # reset_stats 不应清空最高分
    assert stats.high_score == 9999
