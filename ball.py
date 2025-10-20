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
        self.delay = 0
        self.is_caught = False
        self.owner = None
        self.attach_offset = pygame.Vector2(0,0) # attaches to  players hand

    def try_catch(self, player, catch_radius=30):
        if self.is_caught:
            return False
        
        if self.position.distance_to(player.position) <= catch_radius:
            self.is_caught = True
            self.owner = player
            self.velocity.update(0,0)
            self.attach_offset = getattr(player, "hand_offset", pygame.Vector2(0, -20))
            self.delay = 0.0
            return True
        return False
    
    def release(self, throw_dir: pygame.Vector2, throw_speed:float):
        if not self.is_caught:
            return
        if throw_dir.length_squared() == 0:
            throw_dir = pygame.Vector2(1,0)
        self.velocity = throw_dir.normalize() * min(throw_speed, self.max_speed)
        self.starting_speed = max(self.starting_speed, self.velocity.length())
        self.is_caught = False
        self.owner = None
        self.delay = 0.0

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
        if self.is_caught and self.owner is not None:
            # attachs the ball to player
            self.position = self.owner.position + self.attach_offset
            return
        
        self.delay += dt 

        if self.velocity.length() > self.starting_speed and self.delay > 2.0: # start lossing speed after not touching a wall or player after 2 seconds
            self.velocity *= 0.999

        self.position += self.velocity
            
        if self.position.x <= self.radius or self.position.x >= SCREEN_WIDTH - self.radius:
            self.velocity.x *= -1 # this causes the ball to bounce back
            self.delay = 0 # resets delay timer on bounce
            if self.velocity.length() < self.max_speed:
                self.velocity *= 2 # increases speed on bounce as long is under the speed limit
                if self.velocity.length() > self.max_speed:
                    direction = self.velocity.normalize()
                    self.velocity = direction * self.max_speed #speed cap after boost

        if self.position.y <= self.radius or self.position.y >= SCREEN_HEIGHT - self.radius:
            self.velocity.y *= -1
            self.delay = 0
            if self.velocity.length() < self.max_speed:
                self.velocity *= 2
                if self.velocity.length() > self.max_speed:
                    direction = self.velocity.normalize()
                    self.velocity = direction * self. max_speed
            
                