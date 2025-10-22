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

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    ball = Ball(100, 100)
    Player.containers = (updatable, drawable)
    GameCourt.containers = (drawable)
    game_court = GameCourt()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
    player.ball = ball

    dt = 0
    

    while True:
        catching = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)
        screen.fill("black")
        game_court.draw(screen)
        ball.update(dt)
        ball.handle_collision(player, catching)

        ball.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60)/ 1000

        # logic to keep player from going off bounds
        if player.position.x + player.radius > SCREEN_WIDTH:
            player.position.x = SCREEN_WIDTH - player.radius
        elif player.position.x - player.radius < 0:
            player.position.x = player.radius
        
        if player.position.y + player.radius > SCREEN_HEIGHT:
            player.position.y = SCREEN_HEIGHT - player.radius
        elif player.position.y - player.radius < 0:
            player.position.y = player.radius
        

if __name__ == "__main__":
    main()

