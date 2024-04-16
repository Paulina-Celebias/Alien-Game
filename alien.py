import pygame 
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Klasa przedstawiającego pojedynczgo obcego we flocie'''
    
    def __init__(self, ai_settings, screen):
        '''Inicjalizacja obcego i zdefiniowanie jego położenia początkowego'''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Wczytanie obrazu obcego i zdefiniowanie jego atrybutu rect
        self.image  = pygame.image.load('C:/Projects/python-courses/PythonBook/pcc_3e-main/chapter_12//adding_ship_image/images/alien1.bmp')
        self.rect = self.image.get_rect()
        
        # Umieszczanie nowego obcego w pobliżu lewego górnego rogu ekranu
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Przechowywanie dokładnego położenia obcego
        self.x = float(self.rect.x)
    
    def check_edges(self):
        '''Zwraca wartośc True, jeśli obcy znajdzie się przy krawędzi ekranu'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        '''Przesunięcie obcego w prawo lub w lewo'''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    def blitme(self):
        """Wyświetlanie obcego w jego aktualnym położeniu"""
        self.screen.blit(self.image, self.rect)
        