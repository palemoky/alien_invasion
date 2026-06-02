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

PyGame 入门：
1. 极简入门：http://c.biancheng.net/pygame/
2. 官方文档：https://www.pygame.org/docs/

引申练习：
1. 绘制星空
2. 绘制绵绵细雨
3. 贪吃蛇
4. Flappy Bird

TODO 
- [ ] 增加难度等级（入门、中等、挑战）
- [ ] 空格键开始与暂停操作
- [ ] 将最高分写入文件，避免重启丢失
