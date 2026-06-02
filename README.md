# 外星人入侵
《Python编程：从入门到实践》（第三版）飞船入侵练习项目

## 运行

依赖使用 [uv](https://docs.astral.sh/uv/) 管理（基于 `pygame-ce`，兼容 Python 3.14）：

```bash
uv run python -m alien_invasion
```

`uv` 会自动创建虚拟环境并按 `uv.lock` 安装依赖，无需手动操作。

## 测试

```bash
uv run pytest
```

测试以无头模式运行（`SDL_VIDEODRIVER=dummy`），无需显示器；CI 见 `.github/workflows/ci.yml`。

## 开发

代码风格由 [ruff](https://docs.astral.sh/ruff/) 统一（lint + format），类型由 [mypy](https://mypy-lang.org/) 静态检查，并通过 [pre-commit](https://pre-commit.com/) 在提交前自动运行：

```bash
uv run pre-commit install          # 首次：安装 git 钩子
uv run ruff check . && uv run ruff format .   # lint + 格式化
uv run mypy                        # 类型检查
uv run pytest                      # 测试 + 覆盖率门禁（≥80%）
```

PyGame 入门：
1. 极简入门：http://c.biancheng.net/pygame/
2. 官方文档：https://www.pygame.org/docs/

引申练习：
1. 绘制星空
2. 绘制绵绵细雨
3. 贪吃蛇
4. Flappy Bird

## 操作

- ← / →：移动飞船
- 空格：发射子弹
- `1` / `2` / `3`：在开始界面选择难度（简单 / 普通 / 困难）
- `P`：暂停 / 继续
- Cmd/Ctrl + Q：退出

TODO
- [x] 增加难度等级（简单、普通、困难）
- [x] P 键暂停 / 继续
- [x] 将最高分写入文件，避免重启丢失
