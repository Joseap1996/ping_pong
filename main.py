import os, sys
if "microsoft" in sys.platform or os.environ.get("WSL_DISTRO_NAME"): # this for testing my logic in wsl because sound does not work in it
    os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from constants import *
from player import Player
from ball import Ball
from game_court import GameCourt
from scoreboard import ScoreBoard



def main():
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 128)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    gray = (102, 102, 102) #screen color
    game_state = "start"
    base = os.path.dirname(__file__)
    wav_path = os.path.join(base,"assets","bounce_sound.wav")
    

    font = pygame.font.Font(None, 74) 
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    GameCourt.containers = (drawable,)
    ScoreBoard.containers = (drawable,)
    Ball.containers = (updatable, drawable)

    my_game_court = GameCourt()
    score_board = ScoreBoard(game_court_rect=my_game_court.game_court)

    my_ball = Ball(
        x=my_game_court.game_court.centerx,
        y=my_game_court.game_court.centery,
        game_court_rect=my_game_court.game_court,
        goal1_rect=my_game_court.goal1,
        goal2_rect=my_game_court.goal2,
        score_board=score_board,
        wav_path=wav_path
    )

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
    player2 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 1200)
    player.ball = my_ball

    dt = 0
    border_w = 2

    while True:
        catching = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_state == "start":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_state = "playing"
                        
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return
            elif game_state == "playing":
                if event.type == pygame.KEYDOWN and my_ball.pause:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        my_ball.pause = False
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return
            elif game_state == "end":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_state = "playing"
                        score_board.reset()
                        my_ball.reset(None)
                        my_ball.pause = False
                    
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return
        #UPDATE
        if game_state == "playing" and not my_ball.pause:
            updatable.update(dt)
        else:
            pass


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
        
        if my_ball.position.x < player2.position.x: # if the ball is left of the cpu, cpu moves left
            player2.move_left(dt)
        if my_ball.position.x > player2.position.x: # if the ball is to the right, cpu moves right
            player2.move_right(dt)
        
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

        if score_board.p1_score >= 6 or score_board.p2_score >= 6:
            game_state = "end"
            my_ball.pause = True

        #DRAW
        screen.fill(gray)
        my_game_court.draw(screen)
       
        
        for obj in drawable:
            obj.draw(screen)

        score_board.draw(screen)
        my_ball.draw_countdown(screen, font)

        
        if game_state == "start":
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,200))
            screen.blit(overlay,(0,0))
            title = font.render("GAME START", True, (255,255,255))
            prompt = font.render("Press SPACE to start", True, (255,255,255))
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
            screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2 + 20)))
        
        elif game_state == "end":
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,200))
            screen.blit(overlay,(0,0))
            msg = font.render("Max score reached, GAME OVER", True, (255,255,255))
            msg2 = font.render("Press SPACE to play again or q/Esc to quit", True, (255,255,255))
            screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
            screen.blit(msg2, msg2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

        elif my_ball.pause:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,160))
            screen.blit(overlay, (0,0))
            msg = font.render("Goal! Press SPACE to continue or Q/Esc to quit", True, (255,255,255))
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(msg, msg_rect)

        pygame.display.flip()
        dt = clock.tick(60)/ 1000

if __name__ == "__main__":
    main()

