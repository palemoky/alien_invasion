class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    # 难度预设：影响生命数、子弹上限、初始外星人速度与加速倍率
    DIFFICULTIES = {
        "easy": {
            "ship_limit": 5,
            "bullets_allowed": 5,
            "alien_speed_start": 0.7,
            "speedup_scale": 1.05,
        },
        "normal": {
            "ship_limit": 3,
            "bullets_allowed": 3,
            "alien_speed_start": 1.0,
            "speedup_scale": 1.1,
        },
        "hard": {
            "ship_limit": 2,
            "bullets_allowed": 3,
            "alien_speed_start": 1.4,
            "speedup_scale": 1.2,
        },
    }

    def __init__(self):
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.fps = 60  # 游戏帧率

        # 星舰移速设置
        self.fleet_drop_speed = 10

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # 加快游戏节奏
        self.score_scale = 1.5

        # 应用默认难度（会设置 ship_limit/bullets_allowed/speedup_scale 等）
        self.set_difficulty("normal")

    def set_difficulty(self, name: str) -> None:
        """切换难度。未知难度名将抛出 ValueError。"""
        if name not in self.DIFFICULTIES:
            raise ValueError(f"未知难度：{name}")
        preset = self.DIFFICULTIES[name]
        self.difficulty = name
        self.ship_limit = preset["ship_limit"]
        self.bullets_allowed = preset["bullets_allowed"]
        self.speedup_scale = preset["speedup_scale"]
        self._alien_speed_start = preset["alien_speed_start"]
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 3.75
        self.bullet_speed = 8.5
        self.alien_speed = self._alien_speed_start

        # fleet_direction 为 1 表示向右，为 -1 表示向左
        self.fleet_direction = 1

        # 记分设置
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置的值和外星人分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
