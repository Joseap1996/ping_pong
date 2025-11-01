import pygame
from constants import *

class GameCourt(pygame.sprite.Sprite):
          
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        court_width = SCREEN_WIDTH - 560
        court_height = SCREEN_HEIGHT - 100
        goal_width = court_width / 4
        goal_height = court_height / 16

        court_top_left_x = (SCREEN_WIDTH / 2 ) - (court_width / 2)
        court_top_left_y = (SCREEN_HEIGHT / 2) - (court_height / 2)
        self.game_court = pygame.Rect(court_top_left_x, court_top_left_y, court_width, court_height)

        goal_x = self.game_court.centerx - (goal_width / 2)
        self.goal1 = pygame.Rect(goal_x, self.game_court.top - goal_height, goal_width, goal_height)
        self.goal2 = pygame.Rect(goal_x, self.game_court.bottom, goal_width, goal_height) 
        
    def draw(self, screen):
        pygame.draw.rect(screen, "blue", self.goal1, 2)
        pygame.draw.rect(screen, "blue", self.goal2, 2)
        pygame.draw.rect(screen, "white", self.game_court, 2)
        

        pygame.draw.line(screen, "white", (self.game_court.left, self.game_court.centery),(self.game_court.right, self.game_court.centery) , 2)
        pygame.draw.circle(screen, "white", self.game_court.center, 20, 2)