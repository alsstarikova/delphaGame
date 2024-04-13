import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Отслеживание событий клавиатуры или мыши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            _check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            _check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                       aliens, bullets, mouse_x, mouse_y)


def _check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                       aliens, bullets, mouse_x, mouse_y):
    """Запускает игру при нажатии на Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек
        ai_settings.init_dynamic_settings()
        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)
        # Сброс игровой статистики
        stats.reset_stats()
        # Статус игры активный
        stats.game_active = True
        # Инициализация счета для новой игры
        sb.prep_score()
        # Инициализация уровня игры
        sb.prep_level()
        # Отображение кол-ва попыток
        sb.prep_ships()

        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создать новый флот и разместить корабль
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def _check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Нажатие клавиш (ВЛЕВО, ВПРАВО)"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        _fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def _fire_bullet(ai_settings, screen, ship, bullets):
    # Создание нового снаряда и вклучение его в группу
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def _check_keyup_events(event, ship):
    """Отпускание клавишь (ВЛЕВО, ВПРАВО)"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран"""
    # При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)

    # Вывод снарядов на экран
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    # Кнопка Play отображается в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позицию снарядов и уничтожает старые снаряды"""
    # Обновление позиций снарядов
    bullets.update()

    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    _check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def _check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Проверка попаданий в пришельцев.
    # При обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            sb.check_high_score()
    # Восстановление флота
    if len(aliens) == 0:
        # Уничтожить существующие пули и создать новый флот
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        # Увеличение уровня
        stats.level += 1
        sb.prep_level()


def create_fleet(ai_settings, screen, ship, aliens):
    """Создание флота пришельцев"""
    # Создание пришельца и вычисление пришельцев в ряду.
    # Определить интервал между пришельцами (одна ширина пришельца)
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    ship_height = ship.rect.height
    alien_height = alien.rect.height
    number_aliens_x = _get_number_aliens_x(ai_settings, alien_width)
    number_rows = _get_number_rows(ai_settings, ship_height, alien_height)

    # Создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Содание пришельца и размещение его в ряду
            _create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number)


def _get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет кол-во пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def _create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number):
    """Создание пришельца и размещение его в ряду"""
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 100
    aliens.add(alien)


def _get_number_rows(ai_settings, ship_height, alien_height):
    """Определение кол-ва рядов пришедьцев на экране"""
    available_space_y = (ai_settings.screen_height
                         - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height)) - 1
    return number_rows


def update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets):
    """Проверяет, достиг ли флот края экрана, после чего обновляет его позицию"""
    _check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка коллизий "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        _ship_hit(ai_settings, stats, screen, ship, sb, aliens, bullets)

    # Проверка пришельцев, добравшихся до нижнего края экрана
    _check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def _check_fleet_edges(ai_settings, aliens):
    """Реакция на достижение края экрана флотом пришельцев"""
    for alien in aliens.sprites():
        if alien.check_edges():
            _change_fleet_direction(ai_settings, aliens)
            break


def _change_fleet_direction(ai_settings, aliens):
    """Опускать флот и менять его направление"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def _ship_hit(ai_settings, stats, screen, ship, sb, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем"""
    if stats.ship_left > 0:
        # Уменьшение ship_left
        stats.ship_left -= 1
        sb.prep_ships()

        # Очистить списки пришельцев и снарядов
        aliens.empty()
        bullets.empty()

        # Создание нового флота пришельцев и разместить наш корабль по центру
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def _check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что и при столкновении с кораблём
            _ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
