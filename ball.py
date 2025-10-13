# to do: ball will have a default starting speed,
# at game start it will go to one of the players, this will chosen ramdomly.
# ball will lose momentum if not affected by the player or wall,
# but will not ever stop moving. 
# ball will bounce of the walls of the game court, not outbounds or pacman balling. 
# ball speed and angle will change depending on the player action 
# ball will be either be caught or struck back by player to be determined later...
# ball will be a circle from CircleShap and be blue

import pygame
from circle_shape import CircleShape
from constants import *
class Ball(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_RADIUS)
        