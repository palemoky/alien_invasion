from pathlib import Path

from platformdirs import user_data_path

# 图片资源目录，基于本文件位置解析，与运行时的当前工作目录无关
IMAGES_DIR = Path(__file__).parent / "images"


def high_score_path() -> Path:
    """最高分存档路径，位于跨平台的用户数据目录下。"""
    return user_data_path("alien_invasion") / "high_score.json"
