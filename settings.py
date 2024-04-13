import colors


class Settings:
    """Класс для хранения всех настроект игры 'Вторжение пришельцев'"""

    def __init__(self):
        """Инициализация настройки игры"""

        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Параметры корабля
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = colors.silver
        self.bullets_allowed = 3

        # Настройки пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Инициализирует настройки настройки, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        # Увеличение стоимости пришельцев
        self.alien_points = int(self.alien_points * self.score_scale)
