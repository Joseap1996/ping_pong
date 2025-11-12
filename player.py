import pygame
from constants import *
from circle_shape import CircleShape
from ball import Ball


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.timer = 0

    def square(self):

        half_size = self.radius # this half the width/lenght of the square
        #this gets the corners of the square
        top_left = (self.position.x - half_size, self.position.y - half_size)
        top_right = (self.position.x + half_size, self.position.y - half_size)
        bottom_right = (self.position.x + half_size, self.position.y + half_size)
        bottom_left = (self.position.x - half_size, self.position.y + half_size)
        
        
        return [top_left, top_right, bottom_right, bottom_left]
    
    def draw(self, screen):
        pygame.draw.polygon(screen,"black", self.square())
        pygame.draw.polygon(screen, "red", self.square(), 2)
    
    def move_up(self, dt):
        self.position.y -= PLAYER_SPEED * dt 
    
    def move_down(self, dt):
        self.position.y += PLAYER_SPEED * dt
    
    def move_right(self, dt):
        self.position.x += PLAYER_SPEED * dt
    
    def move_left(self, dt):
        self.position.x -= PLAYER_SPEED * dt
    
    def update(self, dt):
        self.timer -= dt

       