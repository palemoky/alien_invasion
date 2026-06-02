def test_dynamic_settings_initialized(settings):
    assert settings.fleet_direction == 1
    assert settings.alien_points == 50


def test_increase_speed_scales_values(settings):
    ship0 = settings.ship_speed
    bullet0 = settings.bullet_speed
    alien0 = settings.alien_speed

    settings.increase_speed()

    assert settings.ship_speed == ship0 * settings.speedup_scale
    assert settings.bullet_speed == bullet0 * settings.speedup_scale
    assert settings.alien_speed == alien0 * settings.speedup_scale


def test_increase_speed_scales_points(settings):
    points0 = settings.alien_points
    settings.increase_speed()
    assert settings.alien_points == int(points0 * settings.score_scale)
    assert isinstance(settings.alien_points, int)


def test_initialize_dynamic_settings_resets_after_increase(settings):
    settings.increase_speed()
    settings.initialize_dynamic_settings()
    assert settings.alien_points == 50
    assert settings.fleet_direction == 1
