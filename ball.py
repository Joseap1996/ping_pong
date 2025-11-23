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
from game_court import GameCourt
from scoreboard import ScoreBoard

class Ball(CircleShape):
    def __init__(self, x, y, game_court_rect,goal1_rect,goal2_rect, score_board, wav_path):
        super().__init__(x, y, BALL_RADIUS)
        self.velocity = pygame.Vector2(2,1)
        self.starting_speed = self.velocity.length()
        self.max_speed = self.velocity.length() * 10
        self.delay = 0
        self.countdown = 0
        self.countdown_timer = 0
        self.pause = False 
        self.scorer = None
        self.is_caught = False
        self.owner = None
        self.attach_offset = pygame.Vector2(0,0) # attaches to  players hand
        self.game_court = game_court_rect
        self.goal1 = goal1_rect
        self.goal2 = goal2_rect
        self.score_board = score_board
        self.bounce_sound = pygame.mixer.Sound(wav_path)
        
        
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

    def draw_countdown(self, screen, font):
        if self.countdown > 0:
            if self.countdown == 3:
                text = font.render(f"{self.scorer} Scores!", True, "yellow")
            else:
                text = font.render(str(self.countdown), True, "white")

            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect)

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
        r = self.radius
        if dist_sq > r * r:
            return

        if catching:
            self.try_catch(player)
            return
        
        if dist_sq == 0:
            # pick axis by smaller penetration
            dx = min(abs(self.position.x - rect.left), abs(self.position.x - rect.right))
            dy = min(abs(self.position.y - rect.top),  abs(self.position.y - rect.bottom))
            normal = pygame.Vector2(1, 0) if dx < dy else pygame.Vector2(0, 1)
            # orient normal outward from rect center
            rc = pygame.Vector2(rect.center)
            if (self.position - rc).dot(normal) < 0:
                normal *= -1
            pen = r  # fully inside at a corner/edge
        else:
            dist = dist_sq ** 0.5
            normal = to_center / dist
            pen = r - dist  # how much we’re overlapping

        epsilon = 0.5
        self.position += normal * (pen + epsilon)

        v = self.velocity
        self.velocity = v - 2 * v.dot(normal) * normal

        self.position = nearest + normal * (self.radius + 0.1)

        self.delay = 0
    
    def reset(self, scorer):
        self.position = pygame.Vector2(
            self.game_court.centerx,
            self.game_court.centery
        )
        self.velocity = pygame.Vector2(0,0)
        self.countdown = 3
        self.countdown_timer = 0
        self.scorer = scorer
        self.is_caught = False
        self.owner = None   


    def update(self, dt):
        if self.pause:
            return
        
        if self.countdown > 0:
            self.countdown_timer += dt
            if self.countdown_timer >= 1.0:
                self.countdown -= 1
                self.countdown_timer = 0
                print(f"Starting in {self.countdown}")

                if self.countdown == 0:
                    if self.scorer == "Player 1":
                        self.velocity = pygame.Vector2(2, -1) # sends the ball to player 2 for being scored on
                    elif self.scorer == "Player 2":
                        self.velocity = pygame.Vector2(2, 1) # sends the ball to player 1 for being scored on
                    else:
                        self.velocity = pygame.Vector2(1, -1) # place holder ball direction after reset
            return


        if self.is_caught and self.owner is not None:
            # attachs the ball to player
            self.position = self.owner.position + self.attach_offset
            return
        
        self.delay += dt 

        if self.velocity.length() > self.starting_speed and self.delay > 2.0: # start lossing speed after not touching a wall or player after 2 seconds
            self.velocity *= 0.999

        self.position += self.velocity
        #game court walls
        left = self.game_court.left + self.radius
        right = self.game_court.right - self.radius
        top = self.game_court.top + self.radius
        bottom = self.game_court.bottom - self.radius
        #goal walls
        goal1_left = self.goal1.left + self.radius
        goal1_right = self.goal1.right - self.radius
        goal1_top = self.goal1.top + self.radius
        goal1_bottom = self.goal1.bottom - self.radius

        goal2_left = self.goal2.left + self.radius
        goal2_right = self.goal2.right - self.radius
        goal2_top = self.goal2.top + self.radius
        goal2_bottom = self.goal2.bottom - self.radius

        in_goal1_x = goal1_left <= self.position.x <= goal1_right
        in_goal2_x = goal2_left <= self.position.x <= goal2_right

        if self.position.x <= left or self.position.x >= right:
            self.velocity.x *= -1 # this causes the ball to bounce back
            pygame.mixer.Sound.play(self.bounce_sound) # sound effect for ball bouncing off walls
            self.delay = 0 # resets delay timer on bounce
            if self.velocity.length() < self.max_speed:
                self.velocity *= 2 # increases speed on bounce as long is under the speed limit
                if self.velocity.length() > self.max_speed:
                    direction = self.velocity.normalize()
                    self.velocity = direction * self.max_speed #speed cap after boost

            self.position.x = max(left, min(self.position.x, right))

        if self.position.y <= top or self.position.y >= bottom:
            #checking for ball going in the goal
            if (self.position.y >= goal1_top and self.position.y <= top and in_goal1_x and self.velocity.y < 0):
                print("Player 1 scored!")
                scorer = "Player 1"
                self.pause =  True
                self.reset(scorer)
                self.score_board.score_p1()
                pass
            elif (self.position.y >= bottom and self.position.y <= goal2_bottom and in_goal2_x and self.velocity.y > 0):
                print("Player 2 scored!")
                scorer = "Player 2"
                self.pause = True
                self.reset(scorer)
                self.score_board.score_p2()
                pass
            else:
                self.velocity.y *= -1
                pygame.mixer.Sound.play(self.bounce_sound)
                self.delay = 0
                if self.velocity.length() < self.max_speed:
                    self.velocity *= 2
                    if self.velocity.length() > self.max_speed:
                        direction = self.velocity.normalize()
                        self.velocity = direction * self. max_speed
                self.position.y = max(top, min(self.position.y, bottom))
            
        
    
