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


def test_high_score_persists_across_instances(game, tmp_path):
    f = tmp_path / "hs.json"
    stats = GameStats(game, high_score_file=f)
    stats.high_score = 4200
    stats.save_high_score()

    # 新实例应从存档读回最高分
    reloaded = GameStats(game, high_score_file=f)
    assert reloaded.high_score == 4200


def test_missing_file_defaults_to_zero(game, tmp_path):
    stats = GameStats(game, high_score_file=tmp_path / "nope.json")
    assert stats.high_score == 0


def test_corrupted_file_defaults_to_zero(game, tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("not json at all", encoding="utf-8")
    stats = GameStats(game, high_score_file=f)
    assert stats.high_score == 0


def test_save_creates_parent_dirs(game, tmp_path):
    f = tmp_path / "nested" / "dir" / "hs.json"
    stats = GameStats(game, high_score_file=f)
    stats.high_score = 10
    stats.save_high_score()
    assert f.exists()
