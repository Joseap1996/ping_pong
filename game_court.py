import pygame
from constants import *

class GameCourt(pygame.sprite.Sprite):
          
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        court_width = SCREEN_WIDTH - 560
        court_height = SCREEN_HEIGHT - 100

        court_top_left_x = (SCREEN_WIDTH /2 ) - (court_width / 2)
        court_top_left_y = (SCREEN_HEIGHT / 2) - (court_height / 2)
        self.game_court = pygame.Rect(court_top_left_x, court_top_left_y, court_width, court_height) 
        
    def draw(self, screen):
        # This now draws the instance-specific game_court
        pygame.draw.rect(screen, "white", self.game_court, 2)