import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf


def run_game():
    # Инициализация игры и создание объекта экрана
    pygame.init()

    # Конфигурация экрана
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Вторжение пришельцев")  # Alien Invasion

    # Создание кноаки Play
    play_button = Button(ai_settings, screen, "Play")

    # Создание корабля
    ship = Ship(ai_settings, screen)
    # Создадим группу для хранения пути снарядов (снарядов)
    bullets = Group()
    # Создание группы пришельцев
    aliens = Group()
    # Создания экземпляра статистики и отображения счёта
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиатуры или мыши
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            # Отслеживание обновления позиции корабля
            ship.update()

            # Отслеживание позиции снаряда
            # Удаление пуль, вышедших за край экрана
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # Отслеживание позиции флота пришельцев
            gf.update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets)

        # При каждом проходе цикла перерисовывается экран
        # Отображение последнего прорисованного экрана
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


if __name__ == '__main__':
    run_game()
