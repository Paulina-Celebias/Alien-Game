import pygame

class Settings():
    '''Klasa przeznaczona do przechowywania wszystkich ustawień gry'''
    
    def __init__(self):
        '''Inicjalizacja danych statystycznych gry'''
        # Ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (25, 25, 112)
        
        #  Ustawienia dotyczące statku
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        
        # Ustawienia dotyczące pocisku
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 140, 0
        self.bullets_allowed = 3
        
        # Ustawienia dotyczące obcego
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # Wartość fllet_direction wynosząca 1 oznacza prawo, natomiast -1 oznacza lewo
        self.fleet_direction = 1
        
        # Łatwa zmiana szybkości
        self.speedup_scale = 1.1
        # Łatwa zmiana liczby punktów przyznawanych za zestrzelenie obcego
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        '''Inicjalizacja ustawień, które ulegają zmianie w trakcie gry'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        
        # Wartość fleet_direction wynosząca 1 oznacza w prawo, natomias -1 w lewo
        self.fleet_direction = 1
        
        # Punktacja
        self.alien_points = 50
        
    def increase_speed(self):
        '''Zmiana ustawień dotyczących szybkości gry i liczby przyznawanych punktów'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)