import pygame
from constants import *

from game_court import GameCourt

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, game_court_rect):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.game_court = game_court_rect
        width = 300
        height = 250
        self.p1_score = 0
        self.p2_score = 0
        self.font = pygame.font.SysFont(None, 64)

        score_board_top_left_x = self.game_court.left - 300 - 20
        score_board_top_left_y = self.game_court.top
        self.score_board = pygame.Rect(score_board_top_left_x, score_board_top_left_y, width, height)

    def score_p1(self,amount=1):
            self.p1_score += amount
    def score_p2(self, amount=1):
            self.p2_score += amount
    def reset(self):
          self.p1_score = 0
          self.p2_score = 0
          
    def draw(self,screen):
        pygame.draw.rect(screen, "teal", self.score_board)
        pygame.draw.rect(screen, "white", self.score_board, 2)

        p1_text = self.font.render(str(self.p1_score), True, (255, 255, 255))
        p2_text = self.font.render(str(self.p2_score), True, (255, 255, 255))

        p1_pos = p1_text.get_rect(center=(self.score_board.centerx - 60, self.score_board.centery))
        p2_pos = p2_text.get_rect(center=(self.score_board.centerx + 60, self.score_board.centery))
        screen.blit(p1_text, p1_pos)
        screen.blit(p2_text, p2_pos)    
   

        