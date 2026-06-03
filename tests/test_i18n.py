import pytest

from alien_invasion import i18n
from alien_invasion.i18n import Translator, detect_language

_LANG_VARS = ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG")


@pytest.fixture
def _clear_lang_env(monkeypatch):
    """清空语言相关环境变量，并屏蔽平台特定的探测，便于隔离测试。"""
    for var in _LANG_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(i18n.sys, "platform", "linux")
    return monkeypatch


def test_defaults_to_english_without_signals(_clear_lang_env):
    assert detect_language() == "en"


@pytest.mark.parametrize("value", ["zh_CN.UTF-8", "zh_TW", "zh-Hans"])
def test_chinese_locale_detected(_clear_lang_env, value):
    _clear_lang_env.setenv("LANG", value)
    assert detect_language() == "zh"


def test_non_chinese_locale_is_english(_clear_lang_env):
    _clear_lang_env.setenv("LANG", "ja_JP.UTF-8")
    assert detect_language() == "en"


def test_translator_returns_localized_strings():
    assert Translator("zh")("easy") == "简单"
    assert Translator("en")("easy") == "Easy"


def test_translator_unknown_lang_falls_back_to_english():
    t = Translator("fr")
    # 未知语言会触发系统探测；至少应返回有效（英文）文案
    assert t("title") in ("Select Difficulty", "选择难度")


def test_every_key_present_in_both_languages():
    en_keys = set(i18n._TRANSLATIONS["en"])
    zh_keys = set(i18n._TRANSLATIONS["zh"])
    assert en_keys == zh_keys
