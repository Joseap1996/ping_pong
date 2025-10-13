import pygame
from constants import *

class GameCourt(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1,0),
            lambda y: pygame.Vector2()
        ]
    ]