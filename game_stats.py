from scoreboard import Scoreboard

class GameStats():
    '''Monitorowanie danych statystycznych w grze "Inwazja obcych" '''
    
    def __init__(self, ai_settings):
        '''Inicjalizacja danych statystycznych'''
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Uruchomienie gry 'Inwazja obcyh' w stanie nieaktywnym
        self.game_active = False
        
        self.global_high_score = self.get_global_score()
        
        # Najlepszy wynik nigdy nie powinien być wyzerowany
        self.high_score = self.global_high_score
        
    def get_high_score(ai_settings, score):
        self.global_high_score =  prep_high_score(high_score)
        
      
    def get_global_score(self):
        file = open('./Projekty/AlienGame/global_high_score.txt', 'r')
        file_content = file.read()
        global_high_score = int(file_content)
        file.close()
        return global_high_score
    
    def set_global_score(self, score):
        file = open('./Projekty/AlienGame/global_high_score.txt', 'w')
        file.write(str(score))
        file.close()
        self.global_high_score = score
        
    def reset_stats(self):
        '''Inicjalizacja danych statystycznych, które mogą zmieniać się w trakcje gry'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1