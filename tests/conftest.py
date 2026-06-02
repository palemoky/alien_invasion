import os

# 必须在导入 pygame 之前设置，确保测试在无显示器/无声卡环境（如 CI）下也能运行
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

from alien_invasion.main import Main
from alien_invasion.settings import Settings
from alien_invasion.game_stats import GameStats


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """避免 _ship_hit 中的 sleep 拖慢测试。"""
    monkeypatch.setattr("alien_invasion.main.sleep", lambda *a, **k: None)


@pytest.fixture
def game():
    """一个完整初始化的游戏实例（无头模式）。"""
    return Main()


@pytest.fixture
def settings():
    return Settings()
