class GameStats:
    """Отслеживание статистики игры"""
    def __init__(self, ai_settings):
        """Инициализируем статистику"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии
        self.game_active = False
        # Рекорд должен сбрасываться
        self.high_score = 0

    def reset_stats(self):
        """Инициализация статистики"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        # Уровень игры
        self.level = 1
