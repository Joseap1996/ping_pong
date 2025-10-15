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
        self.velocity = pygame.Vector2(2,1)
        self.starting_speed = self.velocity.length()
        self.max_speed = self.velocity.length() * 4

    def draw(self, screen):
        current_speed = self.velocity.length()
        if current_speed >= self.max_speed:
            color = "orange"
        elif current_speed > self.starting_speed:
            color = "red"
        else:
            color = "white"
        pygame.draw.circle(screen, color, self.position, self.radius)   

    def update(self, dt):
        if self.velocity.length() > self.starting_speed:
            self.velocity *= 0.999

        self.position += self.velocity
            
        if self.position.x <= self.radius or self.position.x >= SCREEN_WIDTH - self.radius:
            self.velocity.x *= -1 # this causes the ball to bounce back
            if self.velocity.length() < self.max_speed:
                self.velocity *= 2 # increases speed on bounce as long is under the speed limit
                if self.velocity.length() > self.max_speed:
                    direction = self.velocity.normalize()
                    self.velocity = direction * self.max_speed #speed cap after boost

        if self.position.y <= self.radius or self.position.y >= SCREEN_HEIGHT - self.radius:
            self.velocity.y *= -1
            if self.velocity.length() < self.max_speed:
                self.velocity *= 2
                if self.velocity.length() > self.max_speed:
                    direction = self.velocity.normalize()
                    self.velocity = direction * self. max_speed
            
                