import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Инициализация корабля и определение его начальной позиции"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения корабля и получение прямоугольника
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Корабль должен появляться у нижнего края экрана по центру
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False

        # Сохранение вещественной координаты центра корабля
        self.center = float(self.rect.centerx)

    def update(self):
        """Обновляет позицию корабля с учётом флага"""
        # Теперь обновляем center, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """Рисует корабль в текщей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Разместить корабль снизу в центре"""
        self.center = self.screen_rect.centerx
