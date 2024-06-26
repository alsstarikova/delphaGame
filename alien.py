import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс для одного пришельца"""
    def __init__(self, ai_settings, screen):
        """Инициализация пришельца и определеине его начальной позиции"""
        super(Alien, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Загрузка изображения и назначение атрибута rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # Каждый пришелец появляется в левом верхнеи углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Перемещение флота пришельцев вправо или влево"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        """Вывод пришельца в текущем положении"""
        self.screen.blit(self.image, self.rect)


