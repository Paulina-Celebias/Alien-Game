import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # inicjalizacja gry i utworzenie obiektu ekranu
    pygame.init()
    
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien invasion')
    
    # Utworzenie przycisku Gra
    play_button = Button(ai_settings, screen, 'Game')
    
    # Utworzenie egzemplarza przenzaczonego do przechowywania danych
    # statystycznych dotyczących gry oraz utworzenie egzemplarza klasy Scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Utworzenie statku kosmicznego
    ship = Ship(ai_settings, screen)
    
    # Utworzenie grupy przeznaczonej do przechowywania pocisków
    bullets = Group()
    aliens = Group()
    
    
    # Utworzenie floty obcych
    # alien = Alien(ai_settings, screen)
    gf.create_fleet(ai_settings, screen, ship, aliens)
   
    # Rozpoczęcie pętli głównej gry
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
        # print('Score: ', stats.high_score)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
run_game()
                
