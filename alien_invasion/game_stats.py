import json
import logging
from pathlib import Path

from .paths import high_score_path

logger = logging.getLogger(__name__)


class GameStats:
    def __init__(self, game, high_score_file: Path | None = None):
        """跟踪游戏统计信息。high_score_file 可注入，便于测试。"""
        self.settings = game.settings
        self._high_score_file = high_score_file or high_score_path()
        self.reset_stats()
        # 最高分从存档加载，任何情况下都不应在游戏内被重置
        self.high_score = self._load_high_score()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _load_high_score(self) -> int:
        """从存档读取最高分，文件缺失或损坏时回退为 0。"""
        try:
            data = json.loads(self._high_score_file.read_text(encoding="utf-8"))
            return int(data["high_score"])
        except FileNotFoundError:
            return 0
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            logger.warning("最高分存档损坏，已忽略：%s", self._high_score_file)
            return 0

    def save_high_score(self) -> None:
        """将最高分写入存档，失败不影响游戏运行。"""
        try:
            self._high_score_file.parent.mkdir(parents=True, exist_ok=True)
            self._high_score_file.write_text(
                json.dumps({"high_score": self.high_score}), encoding="utf-8"
            )
        except OSError:
            logger.exception("无法写入最高分存档：%s", self._high_score_file)
