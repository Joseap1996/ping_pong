import sys
import pygame
from constants import *
from player import Player
from ball import Ball

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    ball = Ball(100, 100)
    Player.containers = (updatable, drawable)
    

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
    player.ball = ball

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)
        screen.fill("black")
        ball.update(dt)
        ball.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60)/ 1000

        # logic to keep player from going off bounds
        if player.position.x > SCREEN_WIDTH:
            player.position.x = SCREEN_WIDTH
        elif player.position.x < 0:
            player.position.x = 0

        if player.position.y > SCREEN_HEIGHT:
            player.position.y = SCREEN_HEIGHT
        elif player.position.y < 0:
            player.position.y = 0
        
    

if __name__ == "__main__":
    main()

