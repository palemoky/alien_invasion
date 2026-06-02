import logging
import os


def configure_logging() -> None:
    """配置全局日志。日志级别可通过环境变量 AI_LOG_LEVEL 覆盖（默认 WARNING）。"""
    level_name = os.environ.get("AI_LOG_LEVEL", "WARNING").upper()
    level = getattr(logging, level_name, logging.WARNING)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
