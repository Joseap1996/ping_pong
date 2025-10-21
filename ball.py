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
    
    def player_rect(self, player):
        half = player.radius
        return pygame.Rect(
            int(player.position.x - half),
            int(player.position.y - half),
            int(2 * half),
            int(2 * half),
        )
    
    def handle_collision(self, player, catching:bool):
        rect = self.player_rect(player)

        nx = max(rect.left, min(self.position.x, rect.right))
        ny = max(rect.top,  min(self.position.y, rect.bottom))
        nearest = pygame.Vector2(nx, ny)

        to_center = self.position - nearest
        dist_sq = to_center.length_squared()
        if dist_sq > self.radius * self.radius:
            return  # no collision

        if catching:
            self.try_catch(player)
            return
        if dist_sq == 0:
        # center is exactly on an edge/corner: choose axis by smallest penetration
            dx_left = abs(self.position.x - rect.left)
            dx_right = abs(self.position.x - rect.right)
            dy_top = abs(self.position.y - rect.top)
            dy_bottom = abs(self.position.y - rect.bottom)
            if min(dx_left, dx_right) < min(dy_top, dy_bottom):
                normal = pygame.Vector2(1 if dx_left < dx_right else -1, 0)
            else:
                normal = pygame.Vector2(0, 1 if dy_top < dy_bottom else -1)
        else:
            normal = to_center.normalize()
        v = self.velocity
        self.velocity = v - 2 * v.dot(normal) * normal

        self.position = nearest + normal * (self.radius + 0.1)

        self.delay = 0.0

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
            
                