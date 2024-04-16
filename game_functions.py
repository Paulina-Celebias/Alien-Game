import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard
from game_stats import GameStats

def get_number_aliens_x(ai_settings, alien_width):
    '''Ustalenie liczby obcych, którzy zmieszczą się w rzędzie'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''Ustalenie, ile rzędów obcych zmieści się na ekranie'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    '''Utworzenie obcego i umieszczenie go w rzędzie'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    '''Utworzenie pełnej floty obcych'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
   
    # Utworzenie floty obcych
    for row_number in range(number_rows):
        for alien_number in range (number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            
def check_fleet_edges(ai_settings, aliens):
    '''Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    '''Przesunięcie całej floty w dół i zmiana kierunku, w którym się ona porusza'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Reakcja na uderzenie obcego w statek'''
    # Zmniejszenie wartości przechowywanej w ships_left
    print('ship hit')
    if stats.ships_left > 1:
        stats.ships_left -= 1
        print('lifes left: ', stats.ships_left)
        
        # Uaktualnienie tablicy wyników
        sb.prep_ships()
    
        # Usunięcie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()
        
        # Utworzenie nowej floty i wysrodkowanie statku
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # Pauza
        sleep(0.5)
    else:
        print('game over')
        stats.game_active = False
        pygame.mouse.set_visible(True)
        if (stats.score > stats.global_high_score):
            stats.set_global_score(stats.score)
            
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Sprawdzenie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Tak samo jak w przypadku zderzenia statku z obcym
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
        
def update_aliens(ai_settings, screen, stats, sb,  ship, aliens, bullets):
    '''Sprawdzenie, czy flota znajduje się przy krawędzi ekranu,
    a następnie uaktualnienie połozenia wszystkich obcych we flocie'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Wykrywanie kolizji międzyobcym i statkiem
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    # Wyszukiwanie obcych docierających do dolnej krawędzi ekranu
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
# reakcja na naciśnięcie klawisza lub przycisku myszy
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):        
       
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Rozpoczęcie nowej gry po kliknięciu przycisku Game przez użytkownika'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        
        # Wyzerowanie ustawień dotyczacych gry
        ai_settings.initialize_dynamic_settings()
        
        # Ukrycie kursora myszy
        pygame.mouse.set_visible(False)
        
        # Wyzerowanie danych statystycznych gry
        stats.reset_stats()
        stats.game_active = True
        
        # Wyzerowanie obrazów tablicy wyników
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Usunięcie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()
        
        # Utworzenie nowej floty i wyśrodkowanie statku
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown_events (event, ai_settings, screen, ship, bullets):
    '''Reakcja na naciśnięcie klawisza'''
    if event.key == pygame.K_RIGHT:
        # Przesunięcie statku w prawą stronę
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        # Utworzenie nowego pocisku i dodanie go do grupy pocisków
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
            
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' Uaktualnienie położenia pocisków i usunięcie tych niewidocznych na ekranie'''
     # Usunięcie pocisków, które są poza ekranem
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Reakcja na kolizję między pociskiem a obcym'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points + len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # Jeżeli cała flota została usunięta, gracz przechodzi na kolejny poziom
        bullets.empty()
        ai_settings.increase_speed()
        
        # Inkrementacja poziomu
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
        
def check_keyup_events (event, ship):
    '''Reakcja na zwolnienie klaiwsza'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_high_score(stats, sb):
    '''Sprawdzenie, czy mamy nowy najlepszy wynik'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
            
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # '''Uaktualnienie obrazów na ekranie i przejście do nowego ekranu'''
    # Odświeżenie ekranu w trakcie każdej iteracji pętli
    screen.fill(ai_settings.bg_color)
    
    # Ponowne wyświetlenie wszytskich pocisków pod warstwami statku kosmicznego i obcych
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    
    # WYświetlenie informacji o punktacji
    sb.show_score()
    
    # Wyświetlenie przycisku tylko wtedy, gdy gra jest nieaktywna
    if not stats.game_active:
        play_button.draw_button()
  
    # Wyświetlenie ostatnio zmodyfikowanego ekranu 
    pygame.display.flip()

