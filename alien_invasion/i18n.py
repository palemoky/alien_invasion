"""极简国际化：根据系统语言在中英文之间切换。

默认英文；仅当系统语言为中文（zh*）时显示中文。
"""

from __future__ import annotations

import locale
import os
import re
import subprocess
import sys

# 各语言的界面文案。键保持稳定，新增文案时两种语言都要补全。
_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "title": "Select Difficulty",
        "easy": "Easy",
        "normal": "Normal",
        "hard": "Hard",
        "menu_hint": "Up / Down: Select     Enter: Start",
        "paused": "Paused (press P to resume)",
    },
    "zh": {
        "title": "选择难度",
        "easy": "简单",
        "normal": "普通",
        "hard": "困难",
        "menu_hint": "上 / 下 选择      回车 开始",
        "paused": "已暂停（按 P 继续）",
    },
}

_DEFAULT_LANG = "en"


def _macos_preferred_language() -> str | None:
    """读取 macOS 偏好语言列表的首项（即系统显示语言）。"""
    try:
        out = subprocess.run(
            ["defaults", "read", "-g", "AppleLanguages"],
            capture_output=True,
            text=True,
            timeout=2,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    match = re.search(r'"([^"]+)"', out)  # 形如 (\n  "zh-Hans-US",\n  "en-US"\n)
    return match.group(1) if match else None


def _windows_ui_language() -> str | None:
    """读取 Windows 用户界面语言（如 zh_CN）。"""
    try:
        import ctypes

        lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()  # type: ignore[attr-defined]
    except (OSError, AttributeError):
        return None
    return locale.windows_locale.get(lcid)


def detect_language() -> str:
    """检测系统语言，返回 'zh' 或 'en'（默认 'en'）。"""
    signals: list[str] = []

    if sys.platform == "darwin":
        mac_lang = _macos_preferred_language()
        if mac_lang:
            signals.append(mac_lang)
    elif sys.platform.startswith("win"):
        win_lang = _windows_ui_language()
        if win_lang:
            signals.append(win_lang)

    # 通用：环境变量（Linux 主要依赖这些）
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(var)
        if value:
            signals.append(value)

    for signal in signals:
        if signal.lower().startswith("zh"):
            return "zh"
    return _DEFAULT_LANG


class Translator:
    """按检测到的语言提供界面文案。"""

    def __init__(self, lang: str | None = None) -> None:
        self.lang = lang if lang in _TRANSLATIONS else detect_language()
        self._table = _TRANSLATIONS[self.lang]

    def __call__(self, key: str) -> str:
        """返回 key 对应的文案；缺失时回退到英文。"""
        return self._table.get(key) or _TRANSLATIONS[_DEFAULT_LANG][key]
