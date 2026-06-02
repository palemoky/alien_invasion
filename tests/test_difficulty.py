import pytest

from alien_invasion.settings import Settings


def test_default_difficulty_is_normal():
    s = Settings()
    assert s.difficulty == "normal"
    assert s.ship_limit == 3
    assert s.alien_speed == 1.0


@pytest.mark.parametrize(
    ("name", "ship_limit"),
    [("easy", 5), ("normal", 3), ("hard", 2)],
)
def test_set_difficulty_applies_preset(name, ship_limit):
    s = Settings()
    s.set_difficulty(name)
    assert s.difficulty == name
    assert s.ship_limit == ship_limit
    assert s.alien_speed == Settings.DIFFICULTIES[name]["alien_speed_start"]


def test_unknown_difficulty_raises():
    s = Settings()
    with pytest.raises(ValueError):
        s.set_difficulty("nightmare")


def test_initialize_dynamic_settings_keeps_difficulty_speed():
    s = Settings()
    s.set_difficulty("hard")
    s.increase_speed()
    s.initialize_dynamic_settings()
    # 重置动态设置后，初始速度应回到困难难度的起始值
    assert s.alien_speed == Settings.DIFFICULTIES["hard"]["alien_speed_start"]
