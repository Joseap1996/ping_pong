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
        incoming = self.velocity
        if incoming.length_squared() == 0:
            incoming = pygame.Vector2(0, -1)
        throw_dir = incoming.normalize() # for now this sets the direction for the ball back after being released

        keys = pygame.key.get_pressed()
        self.timer -= dt

        if keys[pygame.K_a]:
            self.move_left(dt)
        if keys[pygame.K_d]:
            self.move_right(dt)
        if keys[pygame.K_w]:
            self.move_up(dt)
        if keys[pygame.K_s]:
            self.move_down(dt)
        if keys[pygame.K_SPACE]:
            self.ball.try_catch(self)
        if keys[pygame.K_j]:
            self.ball.release(throw_dir, throw_speed = 100)