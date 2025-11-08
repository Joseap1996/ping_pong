import sys
import pygame
from constants import *
from player import Player
from ball import Ball
from game_court import GameCourt



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()


    font = pygame.font.Font(None, 74) 
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    GameCourt.containers = (drawable,)
    Ball.containers = (updatable, drawable)

    my_game_court = GameCourt()

    my_ball = Ball(
        x=my_game_court.game_court.centerx,
        y=my_game_court.game_court.centery,
        game_court_rect=my_game_court.game_court,
        goal1_rect=my_game_court.goal1,
        goal2_rect=my_game_court.goal2
    )

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
    player2 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 1000)
    player.ball = my_ball

    dt = 0
    border_w = 2

    while True:
        catching = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #UPDATE
        updatable.update(dt)
        
        my_ball.handle_collision(player, catching)
        my_ball.handle_collision(player2, catching)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.move_left(dt)
        if keys[pygame.K_d]:
            player.move_right(dt)
        if keys[pygame.K_w]:
            player.move_up(dt)
        if keys[pygame.K_s]:
            player.move_down(dt)
        
        if keys[pygame.K_KP4]:
            player2.move_left(dt)
        if keys[pygame.K_KP6]:
            player2.move_right(dt)
        if keys[pygame.K_KP8]:
            player2.move_up(dt)
        if keys[pygame.K_KP5]:
            player2.move_down(dt)

        #CLAMP PLAYER BEFORE DRAW
        left = my_game_court.game_court.left + player.radius + border_w
        right = my_game_court.game_court.right - player.radius - border_w
        top = my_game_court.game_court.top + player.radius + border_w
        bottom = my_game_court.game_court.bottom - player.radius - border_w

        # logic to keep player from going off bounds
        player.position.x = max(left, min(player.position.x, right))
        player.position.y = max(top, min(player.position.y, bottom))
        player2.position.x = max(left, min(player2.position.x, right))
        player2.position.y = max(top, min(player2.position.y, bottom))

        

        #DRAW
        screen.fill("black")
        my_game_court.draw(screen)
        
        for obj in drawable:
            obj.draw(screen)
        
        my_ball.draw_countdown(screen, font)

        pygame.display.flip()
        dt = clock.tick(60)/ 1000

if __name__ == "__main__":
    main()

