import logging
import os

import pygame.font

logger = logging.getLogger(__name__)

# 各平台「字形较完整」的中文字体文件，按优先级排列（越靠前越完整/美观）。
# 直接按路径加载，避免 pygame 的 SysFont 漏掉 .ttc 字体或选到字形残缺的字体。
_CJK_FONT_PATHS = (
    # macOS
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    # Windows
    "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
    "C:/Windows/Fonts/msyh.ttf",
    "C:/Windows/Fonts/simhei.ttf",  # 黑体
    "C:/Windows/Fonts/simsun.ttc",  # 宋体
    # Linux（Noto Sans CJK / 思源 / 文泉驿）
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc",
)

# 按系统字体名匹配的兜底候选（覆盖安装在非标准路径、但已注册到系统的字体）
_CJK_FONT_NAMES = (
    "pingfangsc,microsoftyahei,simhei,notosanscjksc,notosanscjk,"
    "wenquanyimicrohei,arialunicodems,hiraginosansgb,stheiti,songti"
)


def get_cjk_font(size: int) -> pygame.font.Font:
    """返回一个支持中文的字体。

    优先加载各平台字形较完整的字体文件（PingFang / Arial Unicode MS /
    微软雅黑 / Noto Sans CJK 等）；找不到时退回系统字体名匹配，最后退回默认字体。
    """
    for path in _CJK_FONT_PATHS:
        if os.path.exists(path):
            return pygame.font.Font(path, size)

    matched = pygame.font.match_font(_CJK_FONT_NAMES)
    if matched:
        return pygame.font.Font(matched, size)

    logger.warning("未找到支持中文的系统字体，中文可能显示为方块")
    return pygame.font.SysFont(None, size)
